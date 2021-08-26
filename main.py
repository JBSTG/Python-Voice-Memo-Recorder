import pyaudio
import wave
import threading
import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    

class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))    
        self.setWindowTitle("Hello world - pythonprogramminglanguage.com") 

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   

        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)  

        title = QLabel("Hello World from PyQt", self) 
        title.setAlignment(QtCore.Qt.AlignCenter) 
        gridLayout.addWidget(title, 0, 0)

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
        while self.recording:
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
        self.master.destroy()

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
        if not self.recording:
            #self.set_recording_icon_active()
            self.recording = True
            self.record()
            #self.set_recording_icon_inactive()
        elif self.recording:
            self.recording = False
            #self.set_recording_icon_inactive()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit( app.exec_() )
'''
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
    while self.recording:
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
    self.master.destroy()

def play_wrapper(self):
    if not self.play_enabled or self.recording:
        return
    self.audio_playing = not self.audio_playing
    if self.audio_playing:
        #self.play_button["image"] = self.pause_button_image
    else:
        #self.play_button["image"] = self.play_button_image
    print(self.audio_playing)

def record_wrapper(self):
    t = threading.Thread(target=self.handle_record)
    t.setDaemon(True)
    t.start()
def handle_record(self):
    if not self.recording:
        #self.set_recording_icon_active()
        self.recording = True
        self.record()
        #self.set_recording_icon_inactive()
    elif self.recording:
        self.recording = False
        #self.set_recording_icon_inactive()
'''