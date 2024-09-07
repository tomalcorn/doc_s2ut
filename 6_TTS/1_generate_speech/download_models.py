import speechbrain as sb
from speechbrain.inference.TTS import Tacotron2
from speechbrain.inference.vocoders import HIFIGAN
import os

# os.environ['HF_HOME'] = '/work/tc062/tc062/s2517781/.cache'
os.makedirs('/Users/tomalcorn/Documents/University/pg/diss/6_TTS/TTS/1_generate_speech', exist_ok=True)

# Download Tacotron2
tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="/Users/tomalcorn/Documents/University/pg/diss/6_TTS/TTS/1_generate_speech/models/local_tacotron2")

# Download HIFIGAN
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="/Users/tomalcorn/Documents/University/pg/diss/6_TTS/TTS/1_generate_speech/models/local_hifigan")

print("Models downloaded successfully.")