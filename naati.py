from google.cloud import texttospeech
from pydub import AudioSegment
import os

# Optional: Set service account credentials if needed
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/path/to/your/service-account.json"

# Step 1: Initialize the TTS client
client = texttospeech.TextToSpeechClient()

# Step 2: Prepare empty AudioSegment to store final output
final_audio = AudioSegment.empty()

# Step 3: Read the input file line by line and process each line
with open("input.txt", "r", encoding="utf-8") as file:
    line_counter = 0  # Initialize line counter

    for line in file:
        # Remove leading/trailing whitespace
        line = line.strip()

        # If the line is not empty, generate TTS + silence + bell
        if line:
            # For the first line, use en-US-Standard-A
            if line_counter == 0:
                language_code = "en-US"
                voice_name = "en-US-Standard-A"
            else:
                # Alternating language and voice selection for subsequent lines
                if line_counter % 2 == 1:  # Even line: Use Australian English
                    language_code = "en-AU"
                    voice_name = "en-AU-Standard-D"
                else:  # Odd line: Use Filipino
                    language_code = "fil-PH"
                    voice_name = "fil-PH-Standard-B"

            # Synthesize TTS
            synthesis_input = texttospeech.SynthesisInput(text=line)

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Step 4: Save the TTS audio to a file
            with open("output.mp3", "wb") as out:
                out.write(response.audio_content)

            # Step 5: Load TTS audio, create silence and load the bell sound
            tts_audio = AudioSegment.from_file("output.mp3", format="mp3")
            silence_after_tts = AudioSegment.silent(duration=2000)  # 2 seconds of silence after TTS
            bell = AudioSegment.from_file("bell.mp3", format="mp3")
            silence_after_bell = AudioSegment.silent(duration=2000)  # 2 seconds of silence after bell

            # Step 6: Combine TTS, silence, and bell
            final_audio += tts_audio + silence_after_tts + bell + silence_after_bell

            line_counter += 1  # Increment line counter for alternating languages

# Step 7: Export the final compiled audio
final_audio.export("final_output.mp3", format="mp3")

if os.path.exists("output.mp3"):
    os.remove("output.mp3")
    print(f"Deleted: output.mp3")
else:
    print(f"output.mp3 does not exist.")
print("✅ Final output compiled and saved as 'final_output.mp3'")
os._exit(0)