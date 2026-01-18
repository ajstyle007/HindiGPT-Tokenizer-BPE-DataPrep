# oscar2109_full_clean
import gzip
import re, os

output = "oscar2109_hindi_full.txt"

print("OSCAR-2109 Hindi full clean shuru — 5 parts → ~7.8 GB final")

with open(output, 'w', encoding='utf-8') as out:
    total_lines = 0
    for i in range(1, 6):
        file = f"hi_part_{i}.txt.gz"
        print(f"\nProcessing {file}...")
        with gzip.open(file, 'rt', encoding='utf-8', errors='ignore') as f:
            part_lines = 0
            for line in f:
                cleaned = re.sub(r'[^\u0900-\u097F\s\.,!?\-\u2018\u2019\'\"]', '', line)
                cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                if cleaned and len(cleaned) > 50:
                    out.write(cleaned + '\n')
                    part_lines += 1
                    total_lines += 1
                    if total_lines % 100000 == 0:
                        print(f"Saved {total_lines:,} lines so far...")
            print(f"{file} done → {part_lines:,} clean lines")

print(f"\nDone! OSCAR-2109 Hindi full clean ready")
print(f"File: {output}")
print(f"Size: {os.path.getsize(output)/1e9:.2f} GB")
print(f"Total clean lines: {total_lines:,}")