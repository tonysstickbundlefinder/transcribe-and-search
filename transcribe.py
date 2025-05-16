import os
import tempfile

import ffmpeg
import torch
try:
    import whisper
except ImportError:
    raise ImportError("Please install the whisper library: pip install -U openai-whisper")
from pprint import pprint

# Device setup (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Whisper model using the whisper library
print("Loading model (downloading if running for first time)...")
model_id = "large-v3-turbo"
model = whisper.load_model(
    model_id,
)
model.to(device)
print("Model loaded")

# Transcription options
transcribe_kwargs = {
    "language": "english",
    "word_timestamps": True,
}

def transcribe_video(video_path: str):
    """
    Extracts audio from the given video and transcribes it with word-level timestamps.

    Args:
        video_path: Path to the input video file.

    Returns:
        List of segments, each a dict with keys:
          - 'start': float, start time in seconds
          - 'end': float, end time in seconds
          - 'text': str, the recognized word
    """
    # Prepare temporary audio file
    base = os.path.splitext(os.path.basename(video_path))[0]
    tmp_dir = tempfile.gettempdir()
    audio_path = os.path.join(tmp_dir, f"{base}_audio.wav")

    # Extract mono 16kHz WAV audio
    ffmpeg.input(video_path).output(
        audio_path,
        ac=1,
        ar=16000,
        format='wav'
    ).overwrite_output().run(quiet=True)

    # Transcribe audio with Whisper
    result = model.transcribe(audio_path, **transcribe_kwargs)

    # Clean up temporary file
    try:
        os.remove(audio_path)
    except OSError:
        pass


    print("result")
    pprint(result)

    # Extract word-level segments
    segments = []
    for seg in result.get("segments", []):
        if "words" in seg:
            for w in seg["words"]:
                segments.append({
                    "start": float(w["start"]),
                    "end": float(w["end"]),
                    "text": w["word"]
                })
        else:
            segments.append({
                "start": float(seg["start"]),
                "end": float(seg["end"]),
                "text": seg["text"].strip()
            })
    return segments