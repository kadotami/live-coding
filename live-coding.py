import pyaudio
import numpy as np
import wave
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16

CHANNELS = 1 #モノラル（2にするとステレオ）
RATE = 44100 #サンプルレート（録音の音質）
RECORD_SECONDS = 3 #録音時間
BPM = 60
SECONDS_OF_BEAT = 60/BPM
Hz_ARRAY = [41.2, 43.65, 46.25, 49, 51.91, 55, 58.27, 61.74, 65.41, 69.3, 73.42, 77.78]
SCALE_ALLAY = ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#']

def getNearestValue(target_list, num):
    """
    概要: リストからある値に最も近い値のindexを返却する関数
    @param target_list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(target_list) - num).argmin()
    return idx

def check_scale(fft_data, freq_list):
    """
    概要: 最も大きい音のドレミを返す
    @param fft_data: fft配列
    @param freq_list: 週は数配列
    @return ドレミ
    """
    max_freq = freq_list[np.argmax(fft_data)]
    if(max_freq < 0): max_freq = max_freq * -1
    print(max_freq)
    while(max_freq > 82.4):
       max_freq = max_freq / 2
    return SCALE_ALLAY[getNearestValue(Hz_ARRAY, max_freq)]

if __name__ == "__main__":
    audio = pyaudio.PyAudio()

    stream = audio.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    print("Now Recording...")
    # for i in range(int(RATE / CHUNK * 1)):
    #     data = []
    #     d = np.frombuffer(stream.read(CHUNK), dtype='int16')
    #     data.append(d)
    # data = np.asarray(data).flatten()
    # fft_data = np.abs(np.fft.fft(data))    #FFTした信号の強度
    # freq_list = np.fft.fftfreq(data.shape[0], d=1.0/RATE)    #周波数（グラフの横軸）の取得
    # plt.plot(freq_list, fft_data)
    # scale = check_scale(fft_data, freq_list)
    # print(scale)
    # # plt.xlim(0, 5000)    #0～5000Hzまでとりあえず表示する
    # plt.show()


    try:
        while stream.is_active():
            data = []
            for i in range(0, int(RATE / CHUNK * SECONDS_OF_BEAT)):
                  d = np.frombuffer(stream.read(CHUNK), dtype='int16')
                  data.append(d)
            data = np.asarray(data).flatten()
            fft_data = np.abs(np.fft.fft(data))    #FFTした信号の強度
            freq_list = np.fft.fftfreq(data.shape[0], d=1.0/RATE)    #周波数（グラフの横軸）の取得
            scale = check_scale(fft_data, freq_list)
            print(scale)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        audio.terminate()
    print("Finished Recording.")