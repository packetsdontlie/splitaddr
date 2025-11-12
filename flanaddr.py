#!/usr/bin/env python3
# -----------------------------------------------
# beastmaster: bek
# purpose: take in address, standardize it using
# t5 BERT model, then pass to another module for
# normalization, then tries to normalize capital
# letters.
# 
# the major change is to switch to flan-t5-small
# which has tested well and is slightly faster
# models are from huggingface as is transformers,
# the library they supply to interact with the
# models
# -----------------------------------------------

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import argparse
import usaddress
import re

# other models could be used here, just track down 
# their namespace from huggingface.co
# formerly "Hnabil/t5-address-standardizer"
MODEL_NAME = "google/flan-t5-small" 
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def standardize_address(raw_address: str) -> str:
    inputs = tokenizer(raw_address, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)
    result = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return result[0]

def smart_title_case(text: str) -> str:
    """
    depending on the model, results can be a mixture of 
    lower and upper case, this is a helper function
    """
    return re.sub(r'\b[a-z]+\b', lambda m: m.group().title(), text)

def parse_components(standardized: str) -> dict:
    try:
        parsed, _ = usaddress.tag(standardized)
        return {k: smart_title_case(v) for k, v in parsed.items()}
    except usaddress.RepeatedLabelError as e:
        print("Parsing error:", e)
        return {}

def main():
    """
    given an address as a long string, standardize it, the componentize it
    example: 1 Infinite Loop, Ste 3900, Cupertino 51025
    """
    parser = argparse.ArgumentParser(description="Standardize a postal address using flan T5 model.")
    parser.add_argument("address", type=str, help="Raw address to standardize")
    args = parser.parse_args()

    standardized = standardize_address(args.address)
    standardized = smart_title_case(standardized)
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
