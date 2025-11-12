#!/usr/bin/env python3
# -----------------------------------------------
# beastmaster: bek
# purpose: egads, libPostal seems to be under
# going a takeover.  the command line tools are
# gone, the public repo for pylibpostal is gone
# now, this is an attempt to try and wrap the
# C library (assuming it is installed)
# -----------------------------------------------
# also quite ugly and not super portable...
# the default model vs the much hyped Senzing
# model.  this works for Apple Silicon using
# homebrew, otherwise, these /paths/to/stuff
# have to be changed
# -----------------------------------------------
# switching between models
# default: installed by homebrew
# LIBPOSTAL_DATA_DIR=/opt/homebrew/share/libpostal
# senzing: installed by bek
# https://github.com/Senzing/libpostal-data#version-110
# LIBPOSTAL_DATA_DIR=/Volumes/brace/projects/appfluid/senzing.model
# one can simply use `export`
# as in
# > export LIBPOSTAL_DATA_DIR=/Volumes/brace/projects/appfluid/senzing.model
# and voila, you will be using the senzing.model
# -----------------------------------------------

#!/usr/bin/env python3

import ctypes
import argparse

# Load libpostal shared library
# assuming you are on Apple silicon and using homebrew
# regular X86 unix points to the .so file, probably this one
# libpostal = ctypes.cdll.LoadLibrary("libpostal.so")
libpostal = ctypes.cdll.LoadLibrary("/opt/homebrew/lib/libpostal.dylib")

# Initialize libpostal
libpostal.libpostal_setup()
libpostal.libpostal_setup_parser()

# Define libpostal_address_parser_response struct
class LibpostalAddressParserResponse(ctypes.Structure):
    _fields_ = [
        ("num_components", ctypes.c_size_t),
        ("components", ctypes.POINTER(ctypes.c_char_p)),
        ("labels", ctypes.POINTER(ctypes.c_char_p)),
    ]

# Define function signatures
libpostal.libpostal_parse_address.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
libpostal.libpostal_parse_address.restype = ctypes.POINTER(LibpostalAddressParserResponse)

libpostal.libpostal_address_parser_response_destroy.argtypes = [ctypes.POINTER(LibpostalAddressParserResponse)]

def parse_address(address: str) -> dict:
    encoded = address.encode("utf-8")
    response = libpostal.libpostal_parse_address(encoded, len(encoded)).contents

    result = {}
    for i in range(response.num_components):
        label = response.labels[i].decode("utf-8")
        value = response.components[i].decode("utf-8")
        result[label] = value

    libpostal.libpostal_address_parser_response_destroy(ctypes.pointer(response))
    return result

def main():
    parser = argparse.ArgumentParser(description="Parse an address using libPostal.")
    parser.add_argument("address", type=str, help="Raw address to parse")
    args = parser.parse_args()

    parsed = parse_address(args.address)
    print("Parsed Components:")
    for key, value in parsed.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
