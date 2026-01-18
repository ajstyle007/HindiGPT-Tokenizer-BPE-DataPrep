# from gensim.corpora import WikiCorpus

# input_file = "hiwiki-latest-pages-articles.xml.bz2"
# output_file = "hiwiki_clean_full.txt"

# def extract_wiki():
#     wiki = WikiCorpus(input_file, dictionary={}, processes=1)  # set processes=1 to avoid spawn errors

#     with open(output_file, "w", encoding="utf-8") as out:
#         for i, text in enumerate(wiki.get_texts()):
#             out.write(" ".join(text) + "\n")

#     print("Extraction completed successfully!")

# if __name__ == "__main__":   # <---- REQUIRED on Windows
#     extract_wiki()

# =====================================

# import xml.etree.ElementTree as ET

# file = "hiwiki-latest-pages-articles.xml"

# for event, elem in ET.iterparse(file, events=("start",)):
#     print("Detected Namespace ->", elem.tag.split("}")[0].strip("{"))
#     break


# import xml.etree.ElementTree as ET

# file = "hiwiki-latest-pages-articles.xml"
# limit = 10

# NS = "{http://www.mediawiki.org/xml/export-0.11/}"
# count = 0

# for event, elem in ET.iterparse(file, events=("end",)):

#     if elem.tag.endswith("page"):
#         title = elem.find(f"{NS}title")
#         text = elem.find(f".//{NS}text")

#         if title is not None and text is not None and text.text:
#             count += 1
#             print(f"\n📌 Article {count} → {title.text}")
#             print("="*60)
#             print(text.text[:800])     # Preview only first 800 chars
#             print("\n" + "-"*60)

#         elem.clear()

#         if count >= limit:
#             break


import re
import xml.etree.ElementTree as ET

DUMP_FILE = "hiwiki-latest-pages-articles.xml"
OUTPUT_FILE = "hindi_wiki_corpus.txt"   # <-- yahi file create/save hogi

cleaner = re.compile(r"\{\{.*?\}\}|\[\[.*?\]\]|<.*?>|==.*?==", flags=re.DOTALL)  # compile with flags

def clean(text):
    text = cleaner.sub("", text)  # use compiled pattern's sub method, no flags needed here
    text = re.sub(r"\s+", " ", text)
    return text.strip()


count = 0
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:   # file open for writing
    for event, elem in ET.iterparse(DUMP_FILE, events=("end",)):
        if elem.tag.endswith("page"):
            title = elem.find(".//{http://www.mediawiki.org/xml/export-0.11/}title").text
            revision = elem.find(".//{http://www.mediawiki.org/xml/export-0.11/}revision")
            text = revision.find(".//{http://www.mediawiki.org/xml/export-0.11/}text").text
            
            if text and not title.startswith(("Wikipedia", "विकिपीडिया")):
                cleaned = clean(text)

                if len(cleaned) > 200:
                    f.write(cleaned + "\n\n")     # <-- yahaan save ho raha hai
                    print("✔ Saved →", title)

                    count += 1
                    if count == 500: break       # change limit for full dataset
            
            elem.clear()
