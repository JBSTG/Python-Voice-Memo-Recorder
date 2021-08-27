import pyaudio
import wave
import threading
import os
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QLineEdit, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton,QFileDialog
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtGui import QFont

print(os.getcwd())


class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))    
        self.setWindowTitle("Hello world - pythonprogramminglanguage.com") 

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)  

        # Record Button.
        self.recordButton = QPushButton('Record', self)
        self.recordButton.clicked.connect(self.on_record)
        gridLayout.addWidget(self.recordButton,3,0)


        #play button
        self.playButton = QPushButton('Play',self)
        self.playButton.setEnabled(False)
        self.recordButton.clicked.connect(self.on_play)
        gridLayout.addWidget(self.playButton,2,0)

        #Save Button.
        self.saveButton = QPushButton('Save Memo', self)
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.on_save)
        gridLayout.addWidget(self.saveButton,1,0)


        #Attributes for binding
        self.isRecording = False
        self.temporaryRecordingExists = False


    def closeEvent(self,e):
        print("Closing Window.")
        self.isRecording = False
        self.temporaryRecordingExists = True
        if os.path.isfile("output.wav"):
            print("Deleting Temporary File.")
            os.remove("output.wav")
        else:
            print("No temp file")
        return super().closeEvent(e)

    @property
    def isRecording(self):
        return self._isRecording

    @isRecording.setter
    def isRecording(self,value):
        self._isRecording = value

    @property
    def temporaryRecordingExists(self):
        """This method runs whenever you try to access self.x"""
        print("Getting self.x")
        return self._temporaryRecordingExists

    @temporaryRecordingExists.setter
    def temporaryRecordingExists(self, value):
        """This method runs whenever you try to set self.temporaryRecordingExists"""
        print("Setting self.x to %s"%(value,))
        self._temporaryRecordingExists = value
        #Enable save button since we have a recording now.
        self.saveButton.setEnabled(self._temporaryRecordingExists)
        self.playButton.setEnabled(self._temporaryRecordingExists)


    @pyqtSlot()
    def on_record(self):
        self.record_wrapper()
        self.sender().setText(str(self.isRecording))
    @pyqtSlot()
    def on_play(self):
        pass
    @pyqtSlot()
    def on_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        print(name)
        if(name[0]):
            file = open(name[0],'wb')
            tempFile = open("output.wav",'rb')
            data = tempFile.read()
            file.write(data)
            file.close()


    def record(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("* recording")

        frames = []

        #record until user stops recording
        while self.isRecording:
            data = stream.read(CHUNK)
            frames.append(data)
        #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #    data = stream.read(CHUNK)
        #    frames.append(data)


        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    def on_window_close(self):
        self.recording = False
        if os.path.isfile("output.wav"):
            os.remove("output.wav")
        else:
            print("No temp file")
        self.target().close()

    def play_wrapper(self):
        if not self.play_enabled or self.recording:
            return
        self.audio_playing = not self.audio_playing
        if self.audio_playing:
            pass
            #self.play_button["image"] = self.pause_button_image
        else:
            pass
            #self.play_button["image"] = self.play_button_image
        print(self.audio_playing)

    def record_wrapper(self):
        t = threading.Thread(target=self.handle_record)
        t.setDaemon(True)
        t.start()
    def handle_record(self):
        if not self.isRecording:
            #self.set_recording_icon_active()
            self.isRecording = True
            self.record()
            #self.set_recording_icon_inactive()
        elif self.isRecording:
            self.isRecording = False
            self.temporaryRecordingExists = True
            #self.set_recording_icon_inactive()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit( app.exec_() )