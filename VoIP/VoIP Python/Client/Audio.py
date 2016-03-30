import pyaudio
import wave
import winsound


class Audio:


    #object to keep the audio settings, record and play.
    def __init__(self, CHANNELS, FORMAT, RATE, CHUNK, NOFFRAMES):
        self.audio = audio = pyaudio.PyAudio()
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.RATE = RATE
        self.CHUNK = CHUNK
        self.NOFFRAMES = NOFFRAMES
        self.RECORD_SECONDS = 1


    #record from mic based on the object audio settings and convert to string.
    def record_to_string(self):
        frames = []
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
	    				rate=self.RATE, input=True,
	    				frames_per_buffer=self.CHUNK)
        for i in range(0, int(self.RATE / self.CHUNK * self.NOFFRAMES)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        return b''.join(frames)
        stream.stop_stream()
        stream.close()


    #play audio based on the object audio settings from string.
    def string_to_wave(self, file_name, data):
        waveFile = wave.open(file_name, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(data)
        waveFile.close()
        winsound.PlaySound(file_name, winsound.SND_ASYNC)
