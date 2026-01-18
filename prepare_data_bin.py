import sentencepiece as spm
import numpy as np
from tqdm import tqdm
import os

sp = spm.SentencePieceProcessor(model_file="hindi_tokenizer_new.model")

input_file = "data/hindi_no_exact_dup.txt"
output_prefix = "train"
chunk_size = 25_000_000

print("Pure Hindi data → binary conversion start...")

tokens_buffer = []
file_idx = 0
total_tokens = 0

with open(input_file, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(tqdm(f, total=17_693_221, unit="line", desc="Tokenizing")):
        line = line.strip()
        if not line:
            continue
        
        
        token_ids = sp.encode(line, out_type=int)
        token_ids.append(3)               # EOS token
        tokens_buffer.extend(token_ids)
        total_tokens += len(token_ids)
        

        # when the buffer will full then we will write into the file
        if len(tokens_buffer) >= chunk_size:
            arr = np.array(tokens_buffer, dtype=np.uint16)
            arr.tofile(f"{output_prefix}_{file_idx}.bin")
            print(f"\nSaved {output_prefix}_{file_idx}.bin -> {arr.nbytes//(1024**3):.2f} GB")
            tokens_buffer = []
            file_idx += 1

# saving the left part
if tokens_buffer:
    arr = np.array(tokens_buffer, dtype=np.uint16)
    arr.tofile(f"{output_prefix}_{file_idx}.bin")
    print(f"\nSaved {output_prefix}_{file_idx}.bin -> {arr.nbytes//(1024**3):.2f} GB")


print(f"\nALL DONE!")
print(f"Total tokens: {total_tokens:,}")
print(f"Total files : train_0.bin, train_1.bin, ... train_{file_idx}.bin")
print("Lets start the training!")
