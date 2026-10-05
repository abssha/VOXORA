import pyttsx3
from pydub import AudioSegment

# Generate speech
engine = pyttsx3.init()

engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

engine.save_to_file(
    "Hello, you are connected to Voxora. How can I help you today?",
    "temp.wav"
)

engine.runAndWait()

print("✅ TTS generated")

# Convert to Exotel format
audio = AudioSegment.from_wav("temp.wav")

audio = (
    audio
    .set_frame_rate(8000)
    .set_channels(1)
    .set_sample_width(2)
)

# Export RAW PCM
with open("greeting.pcm", "wb") as f:
    f.write(audio.raw_data)

print("✅ greeting.pcm generated")
print("Sample rate:", audio.frame_rate)
print("Channels:", audio.channels)
print("Sample width:", audio.sample_width)
print("Bytes:", len(audio.raw_data))