import whisper
import ffmpeg

def convert_mp4_to_mp3(mp4File,mp3File):
    try:
        ffmpeg.input(mp4File).output(mp3File, acodec='libmp3lame').run()
        print(f"Conversion successful: {mp4File} -> {mp3File}")
    except ffmpeg.Error as e:
            print("Error during conversion:", e)       

model = whisper.load_model("base")

def transcribe_audio(audioFilePath,outputFilePath):
    result = model.transcribe(audioFilePath)
    with open(outputFilePath, "w") as output_file:
        output_file.write(result["text"])

convert_mp4_to_mp3('Sintel.mp4', 'output_audio.mp3')
transcribe_audio("output_audio.mp3", "transcribed_text.txt")
