import re
import json
from pydub import AudioSegment
import os


# 🔍 Extracts the first JSON block from a string (e.g. GPT output)
def extract_json_block(text):
    
    # Look for a block starting and ending with curly braces
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())    # Attempt to parse the matched block as JSON
        except json.JSONDecodeError as e:
            print("❌ JSON decoding failed:", e)
            print("OpenAI response:", text)
            raise
    
    else:
        print("❌ No JSON found in OpenAI response.")
        print("Raw output:", text)
        raise ValueError("Response did not contain valid JSON.")


# 🎧 Splits an audio file into multiple smaller chunks based on Whisper API's max file size
def split_audio_file(audio_path, max_size_bytes=25 * 1024 * 1024):
    print("🔍 Determining optimal chunk size for Whisper API...")

    # Load full audio file using pydub
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)
    base_name = os.path.splitext(audio_path)[0]
    
    # 🎯 Try different durations to find the largest that fits under the size limit
    test_durations = [15 * 60 * 1000, 10 * 60 * 1000, 5 * 60 * 1000]    # in milliseconds

    for test_duration in test_durations:
        test_chunk = audio[:test_duration]
        test_path = f"{base_name}_test_chunk.m4a"
        test_chunk.export(test_path, format="mp4")
        size = os.path.getsize(test_path)
        os.remove(test_path)
        
        if size <= max_size_bytes:
            chunk_length_ms = test_duration
            break
    
    # 🕐 If none of the test durations work, fall back to 1-minute chunks and shrink until valid
    else:
        chunk_length_ms = 60 * 1000
        while True:
            test_chunk = audio[:chunk_length_ms]
            test_path = f"{base_name}_test_chunk.m4a"
            test_chunk.export(test_path, format="mp4")
            
            if os.path.getsize(test_path) > max_size_bytes:
                chunk_length_ms -= 10 * 1000
                os.remove(test_path)
            
            else:
                os.remove(test_path)
                break

    # 🔪 Split full audio file into final chunks
    chunks = []
    for i in range(0, duration_ms, chunk_length_ms):
        chunk = audio[i : i + chunk_length_ms]
        chunk_path = f"{base_name}_part{i // chunk_length_ms}.m4a"
        chunk.export(chunk_path, format="mp4")
        chunks.append(chunk_path)

    print(f"🧩 Final chunk size: {chunk_length_ms // 1000} seconds")
    print(f"📂 Total chunks: {len(chunks)}")
    return chunks