from tkinter import *
import pyaudio
from PIL import Image, ImageTk
import wave
import threading
import tkinter as tk
import os

recording = False


class Application(tk.Frame):
    def __init__(self, master=None):
        self.recording = False
        super().__init__(master)
        self.master = master
        self.master.geometry("300x300")
        self.master.configure(background="white")
        self.master.protocol("WM_DELETE_WINDOW",self.on_window_close)
        self.pack()
        
        #load image
        load_inactive_mic_image = Image.open("C:/Users/Joel//Desktop/Python-Voice-Memo-Recorder/mic-inactive.png")
        #resize image
        load_inactive_mic_image.thumbnail((75,75),Image.ANTIALIAS)
        
        load_active_mic_image = Image.open("C:/Users/Joel//Desktop/Python-Voice-Memo-Recorder/mic-active.png")
        load_active_mic_image.thumbnail((75,75),Image.ANTIALIAS)

        self.inactive_mic_image = ImageTk.PhotoImage(load_inactive_mic_image)
        self.active_mic_image = ImageTk.PhotoImage(load_active_mic_image)
        self.create_widgets()

    def create_widgets(self):
        self.record_button = tk.Button(self)
        self.record_button["image"] = self.inactive_mic_image
        self.record_button["background"] = "white"
        self.record_button["activebackground"] = "white"
        self.record_button["borderwidth"] = 0
        self.record_button["command"] = self.record_wrapper
        self.record_button.pack(side="right")
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

    def record_wrapper(self):
        t = threading.Thread(target=self.handle_record)
        t.setDaemon(True)
        t.start()
    def handle_record(self):
        if not self.recording:
            self.set_recording_icon_active()
            self.recording = True
            self.record()
            self.set_recording_icon_inactive()
        elif self.recording:
            self.recording = False
            self.set_recording_icon_inactive()
    def set_recording_icon_active(self):
        self.record_button["image"] = self.active_mic_image
    def set_recording_icon_inactive(self):
        self.record_button["image"] = self.inactive_mic_image
root = tk.Tk()
app = Application(master=root)
app.mainloop()

