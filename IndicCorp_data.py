import re
import os

def clean_line(line):
    # Sirf Devanagari Hindi + basic punctuation
    cleaned = re.sub(r'[^\u0900-\u097F\s\.\,\!\?\;\:\-\u2018\u2019\u201c\u201d\'\"]', '', line)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned if len(cleaned) > 50 else None

input_file  = "hindi_data/hi-1.txt"
output_file = "hindi_data/hindi_final_5.5GB.txt"

print("Cleaning hi-1.txt → ~5.5 GB clean Hindi text bana raha hun...")

target_size_gb = 5.5
bytes_target = target_size_gb * 1024 * 1024 * 1024  # 5.5 GB in bytes
bytes_written = 0
lines_saved = 0

with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:

    for line in infile:
        cleaned = clean_line(line)
        if cleaned:
            outfile.write(cleaned + "\n")
            bytes_written += len((cleaned + "\n").encode('utf-8'))
            lines_saved += 1
            
            if lines_saved % 100000 == 0:
                print(f"Saved {lines_saved:,} lines | {bytes_written/1e9:.2f} GB written...")

        # Stop jab 5.5 GB ho jaye
        if bytes_written >= bytes_target:
            print(f"\nTarget size reached! Stopped at {bytes_written/1e9:.2f} GB")
            break

print(f"\nDone! Final dataset ready:")
print(f"   File → {output_file}")
print(f"   Size → {os.path.getsize(output_file)/1e9:.2f} GB")
print(f"   Lines → {lines_saved:,}")