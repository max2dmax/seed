import subprocess
import os
from audiocraft.models import MusicGen
import torchaudio
import torchaudio.transforms as T
from time import sleep
import sys
import time

# Load the MusicGen model (using 'melody' here for speed)
model = MusicGen.get_pretrained('facebook/musicgen-large')
model.set_generation_params(duration=10)

def print_progress_bar(iteration, total, length=30):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f"\r⏳ Generating... |{bar}| {percent}% Complete", end='\r')

total_steps = 10
for i in range(total_steps + 1):
    print_progress_bar(i, total_steps)
    time.sleep(1)
print()  # Move to the next line after progress bar

model = MusicGen.get_pretrained('facebook/musicgen-large')
model.set_generation_params(duration=10)

generated = model.generate(descriptions=["a chill indie pop song with acoustic guitar and dreamy synths"])
print("\n✅ Generation complete!")

# Save output
torchaudio.save("output.wav", generated[0].cpu(), 32000)
print("✅ Audio saved as output.wav")