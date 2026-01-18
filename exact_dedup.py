import re
import os

INPUT_FILE  = "hindi_final_15GB_shuffled.txt"
OUTPUT_FILE = "hindi_llm_ready.txt"

# -----------------------------
# ❌ NSFW / Adult Word Filter
# -----------------------------
nsfw_words = [
    "चुदाई", "चूत", "लंड", "गांड", "सेक्स", "स्तन", "भाभी", "xxx",
    "नंगी", "चोदी", "झड़", "फक", "lund", "chod", "randi"
]

nsfw_pattern = re.compile("|".join(nsfw_words))

# -----------------------------
# ✅ Extra punctuation cleanup
# -----------------------------
punct_pattern = re.compile(r"\.{2,}|\,{2,}|\!{2,}|\?{2,}")

# -----------------------------
# ✅ Hindi Digit Normalization
# -----------------------------
digit_map = str.maketrans("०१२३४५६७८९", "0123456789")

def clean_line(line):
    line = line.strip()

    # ❌ NSFW remove
    if nsfw_pattern.search(line):
        return None    

    # ✅ Garbage punctuation normalize
    line = punct_pattern.sub(".", line)

    # ✅ Hindi → English digits
    line = line.translate(digit_map)

    # ✅ Extra spaces normalize
    line = re.sub(r"\s+", " ", line)

    if len(line) < 40:
        return None

    return line


# -----------------------------
# 🚀 Streaming Clean Start
# -----------------------------
print("\n🔥 FINAL CLEANING STARTED (15GB SAFE MODE)\n")

saved = 0
removed = 0
bytes_written = 0

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:

    for i, line in enumerate(infile, 1):
        cleaned = clean_line(line)
        if cleaned:
            outfile.write(cleaned + "\n")
            saved += 1
            bytes_written += len(cleaned.encode("utf-8"))
        else:
            removed += 1

        if i % 200000 == 0:
            print(f"Lines Read: {i:,} | Saved: {saved:,} | Removed: {removed:,} | Output: {bytes_written/1e9:.2f} GB")


print("\n✅ FINAL CLEAN COMPLETE!")
print(f"✅ Saved Lines   : {saved:,}")
print(f"❌ Removed Lines : {removed:,}")
print(f"📁 Output File   : {OUTPUT_FILE}")
print(f"💾 Final Size    : {os.path.getsize(OUTPUT_FILE)/1e9:.2f} GB")
