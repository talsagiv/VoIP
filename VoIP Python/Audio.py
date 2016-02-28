import pyaudio
import wave
import winsound


class Audio:

    def __init__(self, CHANNELS, RATE, CHUNK, NOFFRAMES):
        self.audio = audio = pyaudio.PyAudio()
        self.FORMAT = self.FORMAT
        self.CHANNELS = CHANNELS
        self.RATE = RATE
        self.CHUNK = CHUNK
        self.NOFFRAMES = NOFFRAMES

    def record_to_string(self):
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
	    				rate=self.RATE, input=True,
	    				frames_per_buffer=self.CHUNK)
        data = stream.read(self.NOFFRAMES*self.CHUNK)
        return data


    def string_to_wave(self, file_name, data):
        waveFile = wave.open(file_name, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(data)
        waveFile.close()
        winsound.PlaySound('chimes.wav', winsound.SND_ASYNC)
