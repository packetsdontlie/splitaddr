#!/usr/bin/env python3
# -----------------------------------------------
# beastmaster: bek
# purpose: take in address, standardize it using
# t5 BERT model, then pass to another module for
# normalization, then tries to normalize capital
# letters.  attempts to cache model, in the real
# world, this would need a global cache for the
# model
# -----------------------------------------------

#!/usr/bin/env python3

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import argparse
import usaddress
import re

# Cache model and tokenizer globally
MODEL_NAME = "Hnabil/t5-address-standardizer"
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def standardize_address(raw_address: str) -> str:
    inputs = tokenizer(raw_address, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)
    result = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return result[0]

def smart_title_case(text: str) -> str:
    return re.sub(r'\b[a-z]+\b', lambda m: m.group().title(), text)

def parse_components(standardized: str) -> dict:
    try:
        parsed, _ = usaddress.tag(standardized)
        return {k: smart_title_case(v) for k, v in parsed.items()}
    except usaddress.RepeatedLabelError as e:
        print("Parsing error:", e)
        return {}

def main():
    parser = argparse.ArgumentParser(description="Standardize a postal address using T5 model.")
    parser.add_argument("address", type=str, help="Raw address to standardize")
    args = parser.parse_args()

    standardized = standardize_address(args.address)
    standardized = smart_title_case(standardized)
    # print("Standardized:", standardized)
    # if you don't love FUniCodeK, are you even human
    print(f"\n🔤 Given:", args.address)
    print(f"📍 Standardized:", standardized)

    components = parse_components(standardized)
    if components:
        print("-----------------------------------------")
        print("✂️  Parsed Components:")
        print("-----------------------------------------")
        for key, value in components.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
