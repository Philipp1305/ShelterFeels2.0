from pathlib import Path
import sounddevice as sd
from torch import cuda

records_folder = Path(__file__).parent / "recordings"
records_folder.mkdir(exist_ok=True, parents=True)

device = 'cuda' if cuda.is_available() else 'cpu'
print("Device", device)

server_port = 8000

url= "http://172.26.172.250:8000/extract_key_words"

#url = "http://10.147.19.101:8000/extract_key_words"
#SF Network Evelina: 48d6023c46603058

whisper_model_name = "base"
whisper_model_language = "en"
number_of_audio_channels_in = 1
sd.default.device = [2, 2]