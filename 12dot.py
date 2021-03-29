#!/usr/bin/python3

import argparse
import itertools
import numpy as np

from bdflib import reader

import common

def singlebyte(rom, bdf, *iters):
   with open(bdf, 'rb') as fp:
      font = reader.read_bdf(fp)
      cp = font.codepoints()
      for c in itertools.chain(*iters):
         if c in cp:
            b = common.to_data(font[c], 8, 12)
            o = c * 12
            rom[o:(o + len(b))] = b

def graphics(rom, bdf):
   singlebyte(rom, bdf, range(0x00, 0x20), range(0x7f, 0xa0), range(0xe0, 0x100))

def jisx0201(rom, bdf):
   singlebyte(rom, bdf, range(0x20, 0x7f), range(0xa0, 0xe0))

def krom_index(c1, c2):
   if c1 in range(0x21, 0x50) and c2 in range(0x21, 0x7f):
      return (c1 - 0x21) * 94 + (c2 - 0x21)
   else:
      return None

def jisx0208(rom, bdf):
   with open(bdf, 'rb') as fp:
      font = reader.read_bdf(fp)
      cp = font.codepoints()
      for c1 in range(0x21, 0x50):
         for c2 in range(0x21, 0x7f):
            c = c1 * 256 + c2
            i = krom_index(c1, c2)
            if c in cp and i is not None:
               b = common.to_data(font[c], 16, 12)
               o = 3072 + i * 24
               rom[o:(o + len(b))] = b

parser = argparse.ArgumentParser()
parser.add_argument('--graphics', type=str)
parser.add_argument('--jisx0201', type=str)
parser.add_argument('--jisx0208', type=str)
parser.add_argument('--out', type=str)

rom = np.zeros([128 * 1024], dtype=np.int8)
args = parser.parse_args()
if (args.graphics is not None):
   graphics(rom, args.graphics)
if (args.jisx0201 is not None):
   jisx0201(rom, args.jisx0201)
if (args.jisx0208 is not None):
   jisx0208(rom, args.jisx0208)

rom.tofile(args.out)
