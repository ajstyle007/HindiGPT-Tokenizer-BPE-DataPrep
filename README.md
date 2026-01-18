## HindiGPT Tokenizer (BPE) & Data Preparation Pipeline

A complete from-scratch Hindi tokenizer and large-scale data preparation pipeline built for training HindiGPT, a custom decoder-only Transformer language model.

This repository covers the entire journey from raw noisy Hindi corpora to LLM-ready binary token streams, optimized for efficient large-scale training.

✨ Key Highlights

- 🔤 Pure Hindi SentencePiece BPE Tokenizer (32K vocab)
- 🧹 Multi-stage data cleaning & normalization pipeline
- 🚫 NSFW & noise filtering
- 📦 Efficient binary token storage (.bin)
- ⚡ Designed for billion-token scale training
- 🧠 Used directly in HindiGPT pretraining

🔤 Tokenizer Details
Feature	Value
Tokenizer Type	SentencePiece
Model	BPE (Byte Pair Encoding)
Vocabulary Size	32,768
Language	Hindi (Devanagari only)
Unicode Normalization	NFKC
BOS / EOS / PAD / UNK	Enabled
Byte Fallback	❌ Disabled

### Tokenizer Training Code
```
spm.SentencePieceTrainer.train(
    input="data/hindi_no_exact_dup.txt",
    model_prefix="hindi_tokenizer_new",
    vocab_size=32768,
    model_type="bpe",
    character_coverage=1.0,
    normalization_rule_name="nfkc",
    input_sentence_size=12_000_000,
    shuffle_input_sentence=True,
    pad_id=0, unk_id=1, bos_id=2, eos_id=3
)
```
✔ Trained on ~1.7 crore Hindi sentences
✔ Random sampling ensures full corpus coverage

### Tokenizer Validation
Binary tokens are decoded back to text to ensure correctness:
```
arr = np.fromfile("train_3.bin", dtype=np.uint16)
text = sp.decode(arr[:200].tolist())
```
```
Decoded sample: अद ipu एक धर आस यत पर करत एक अद और वह एक रण सक उपय और अन शयव रस यद समक करण सक उल कभ कभ टर एक अद पश वस अद रण
 ipu उपय यह तर अल यत मनम उद हरण अद ईश वरव कथन ईश वर शब जगह पन और अद यत रस पर अनन आईप अस करन असमर थत लकर उन पर करत आस एक आस
वत षत रखत अद अब अन तर नक इथ शहर अद अब अन तर नक यह नक अद अब शहर नगर दक एव उत तर इसक अन तर नक और यह वजव इथ यन एयरल रम हब यह तव
सह अफ अन शहर एव एश एव उत तर अमर रद करत अन तर नक कई अफ रव शद गय अत यह एस मह अन इथ यन एयरल अफ टवर महत वप नक यह कई टर उड हब उद
हल करत यह अफ मह नच लक रश षण एक अन तर नक अफ यस ततम नक एक जह इस बढ समय नक रफ अन अफ बड नक अन तक यह अफ सर बड नक जह टन
```


### Devanagari-Only Filtering
```
[^\u0900-\u097F\s\.\,\!\?\-]
```
✔ Removes English, symbols, emojis, scripts
✔ Keeps pure Hindi


### Wikipedia XML Cleaning
- Removes templates, tags, metadata
- Drops short & boilerplate pages

### Length & Quality Filters
- Minimum length: 40–200 chars
- Removes junk, lists, headings

### NSFW / Adult Content Filtering
✔ Ensures safe & clean pretraining corpus

### Data Shuffling (Linux)

Final corpus is shuffled at OS level for randomness:
```
shuf hindi_final_15GB.txt > hindi_final_15GB_shuffled.txt
```
✔ Prevents topic clustering
✔ Improves training stability


### Binary Token Generation

Text → tokens → .bin files for fast training IO
```
token_ids = sp.encode(line, out_type=int)
token_ids.append(EOS)
np.array(tokens, dtype=np.uint16).tofile("train_0.bin")
```
