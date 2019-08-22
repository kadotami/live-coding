import pyaudio
import numpy
import matplotlib.pyplot as plt

chunk = 1024
FORMAT = pyaudio.paInt16

CHANNELS = 1 #モノラル（2にするとステレオ）
RATE = 44100 #サンプルレート（録音の音質）
RECORD_SECONDS = 3 #録音時間

audio = pyaudio.PyAudio()

stream = audio.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

#レコード開始
print("Now Recording...")
all = []
for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
  data = stream.read(chunk)
  all.append(data)



print("Finished Recording.")

stream.close()
audio.terminate()

data = b"".join(all) #Python3用

#録音したデータを配列に変換
result = numpy.frombuffer(data,dtype="int16") / float(2**15)

print(len(result))

# plt.plot(result)
# plt.show()
