# Level 2: speak the command, add cabin noise, let Whisper listen.
import subprocess

from faster_whisper import WhisperModel

model = WhisperModel("base.en", device="cpu", compute_type="int8")


def run(command):
    subprocess.run(command, check=True)


def through_the_cabin(text, color="white", amplitude=0.6):
    run(["say", "-v", "Samantha", "-o", "clean.aiff", text])
    run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi",
         "-i", f"anoisesrc=color={color}:amplitude={amplitude}:duration=8",
         "noise.wav"])
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", "clean.aiff", "-i", "noise.wav",
         "-filter_complex", "amix=inputs=2:duration=first", "noisy.wav"])

    segments, info = model.transcribe("noisy.wav")
    heard = ""
    for segment in segments:
        heard = heard + segment.text
    return heard.strip()


