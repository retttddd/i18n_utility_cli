import json
import os

from transformers import pipeline
from pathlib import Path

from cli_src.langmap import LANG_MAP

# ---------------- INITIALIZE MODEL ----------------
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")

def translate(text, srcLang, tgtLang):
    result = translator(text, src_lang=srcLang, tgt_lang=tgtLang)
    return result[0]['translation_text']


def fill_missing_values(obj, tgtSrc):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if value is None or value == "":
                obj[key] = translate(key, srcLang='eng_Latn', tgtLang=tgtSrc)
            else:
                obj[key] = fill_missing_values(value, tgtSrc)

    elif isinstance(obj, list):
        return [fill_missing_values(item, tgtSrc) for item in obj]

    return obj

def crawlDirectory(path):
    mapped_files = []
    files = os.listdir(path)
    for file in files:
        if file  in  LANG_MAP:
            mapped_files.append({
                "tgtSrc": LANG_MAP[file]["tgtSrc"],
                "pathToFile": path + "/" + file,
            })

    return mapped_files



def process_json_file(file_path: Path, tgtSrc):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    translated_data = fill_missing_values(data, tgtSrc)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, indent=2, ensure_ascii=False)

def runTranslations(path):
    print(f"Starting Translation in {path}")
    files_to_tranlsate = crawlDirectory(path)
    if files_to_tranlsate:
        for item in files_to_tranlsate:
            JSON_FILE = Path(item.get("pathToFile"))
            if JSON_FILE.exists():
                process_json_file(JSON_FILE, item.get("tgtSrc"))
                print(f">>>Translation completed: {JSON_FILE.name}")
            else:
                print(f"Translation failed: {JSON_FILE.name}")