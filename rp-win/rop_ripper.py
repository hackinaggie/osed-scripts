#!/usr/bin/env python3
##################################
# Original Author: John Hammond
# Edited by: hackinaggie
##################################

from re import search
from struct import pack
import argparse

parser = argparse.ArgumentParser(
    description='rop_ripper: A simple rp++ output file parser.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-f', '--file', help='rp++ output file to parse', required=True)
parser.add_argument('-b', '--bad-bytes', help=r'Bad bytes, if any, separated by space (00 0a)', nargs='+')
parser.add_argument('-u', '--unique', help='Show only one instance of a gadget', action='store_true', default=False)
args = parser.parse_args()

worthy_regexes = [
    r"xchg (...), (...)",
    r"inc ...",
    r"dec ...",
    r"mov ..., ...",
    r"push ... ; pop ...",
    r"xor ..., ...",
    r"neg ...",
    r"mov ..., dword \[...\]",
    r"mov dword \[...\], ...",
    r"add ..., ...",
    r"sub ..., ...",
    r"pop ...",
    # r"add ..., 0x[a-f0-9]{1,8}",  # This tends to find a lot...
    r"push ...",
    r"pushad ..."
]

for index, regex in enumerate(worthy_regexes):
    # gadget if it starts with anywhere from 6-8 hex chars
    worthy_regexes[index] = r"^0x[a-f0-9A-F]{6,8}: " + regex + r" ; (ret\s+|retn 0x00\d+\s+|);"

if args.bad_bytes:
    for bad_b in args.bad_bytes:
        try:
            int(bad_b, 16)
        except ValueError:
            parser.error(f'Invalid bad byte: {bad_b}')

found = []
output = []
with open(args.file, 'r') as f:
    for line in f:
        for regex in worthy_regexes:
            if search(regex, line):
                idx = line.find(':')
                address = line[:idx].removeprefix('0x').strip()
                # split addr into byte chunks
                address_list = [address[i:i+2] for i in range(0, len(address), 2)]

                # if none of the addr bytes are in the bad_chars list
                if not args.bad_bytes or not any(hex_addr_byte in args.bad_bytes for hex_addr_byte in address_list):
                    instructions = line[idx+2:].strip()
                    idx = instructions.rfind(' ;')
                    if idx > 0:
                        instructions = instructions[:idx]
                    
                    # If we have something with a retn but already have a clean one
                    # don't use the retn
                    if "_and_retn_" in instructions:
                        instructions_base = instructions[
                            : instructions.index("_and_retn")
                        ]
                    else:
                        instructions_base = instructions
                    
                    if not args.unique or instructions_base not in found:
                        output.append(f"{instructions} = {hex(int(address,16))}")
                        found.append(instructions)
output.sort()
for out in output:
    var, val = out.split("=")
    print(f"{var:50} = {val}")