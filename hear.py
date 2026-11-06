from faster_whisper import WhisperModel

model = WhisperModel("base.en", device="cpu", compute_type="int8")

segments, info = model.transcribe("t01_noisy.wav")

text = ""
for segment in segments:
    text = text + segment.text

print("Whisper heard:", text)
