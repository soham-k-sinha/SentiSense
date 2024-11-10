import os
import subprocess
import ffmpeg
import whisper

def convert_mp4_to_mp3(mp4File, mp3File):
    try:
        # Check if the input file exists
        if not os.path.exists(mp4File):
            raise FileNotFoundError(f"Input file {mp4File} not found.")
        
        # Convert MP4 to MP3 with the -y flag to overwrite the output file without asking
        ffmpeg.input(mp4File).output(mp3File, acodec='libmp3lame').overwrite_output().run()
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e.stderr.decode()}")
        raise RuntimeError(f"Failed to convert {mp4File} to {mp3File}") from e

# Load the Whisper model
model = whisper.load_model("base")

def transcribe_audio(audioFilePath, transcriptFilePath):
    try:
        # Check if the audio file contains valid data
        if os.path.getsize(audioFilePath) == 0:
            raise RuntimeError(f"Audio file {audioFilePath} is empty.")
        
        result = model.transcribe(audioFilePath)
        with open(transcriptFilePath, 'w') as f:
            f.write(result['text'])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

def run(mp4_file_path):
    mp3_file_path = 'output_audio.mp3'
    
    # Convert MP4 to MP3
    convert_mp4_to_mp3(mp4_file_path, mp3_file_path)
    
    # Ensure the audio file is created correctly
    if not os.path.exists(mp3_file_path):
        raise FileNotFoundError(f"Audio file {mp3_file_path} not found.")
    
    # Transcribe the audio file
    transcribe_audio(mp3_file_path, "transcript.txt")