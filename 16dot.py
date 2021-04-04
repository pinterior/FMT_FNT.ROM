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
            b = common.to_data(font[c], 8, 16)
            o = 251904 + c * 16
            rom[o:(o + len(b))] = b

def graphics(rom, bdf):
   singlebyte(rom, bdf, range(0x00, 0x20), range(0x7f, 0xa0), range(0xe0, 0x100))

def jisx0201(rom, bdf):
   singlebyte(rom, bdf, range(0x20, 0x7f), range(0xa0, 0xe0))

def krom_index(c1, c2):
   if c1 in range(0x21, 0x29) and c2 in range(0x21, 0x7f):
      r1 = 0 if c1 == 0x28 else c1 - 0x20
      r2 = 0 if c2 < 0x40 else 8 if 0x60 <= c2 else 16
      return (r1 + r2) * 32 + (c2 & 0x1f)
   elif (c1 in range(0x70, 0x74) and c2 in range(0x21, 0x7f)) or (c1 == 0x74 and c2 in range(0x21, 0x27)):
      r1 = c1 - 0x70
      r2 = 0 if c2 < 0x40 else 8 if 0x60 <= c2 else 16
      return (224 + r1 + r2) * 32 + (c2 & 0x1f)
   elif (c1 in range(0x30, 0x70) and c2 in range(0x21, 0x7f)):
      r1 = (c1 - 0x30) // 16 * 48 + c1 % 16
      r2 = (c2 - 0x20) // 32 * 16
      return (32 + r1 + r2) * 32 + (c2 & 0x1f)
   else:
      return None

def jisx0208(rom, bdf):
   with open(bdf, 'rb') as fp:
      font = reader.read_bdf(fp)
      cp = font.codepoints()
      for c1 in range(0x21, 0x7f):
         for c2 in range(0x21, 0x7f):
            c = c1 * 256 + c2
            i = krom_index(c1, c2)
            if c in cp and i is not None:
               b = common.to_data(font[c], 16, 16)
               o = i * 32
               rom[o:(o + len(b))] = b

def c8x8(rom, bdf, *iters):
   with open(bdf, 'rb') as fp:
      font = reader.read_bdf(fp)
      cp = font.codepoints()
      for c in itertools.chain(*iters):
         if c in cp:
            b = common.to_data(font[c], 8, 8)
            o = 249856 + c * 8
            rom[o:(o + len(b))] = b

def graphics8(rom, bdf):
   c8x8(rom, bdf, range(0x00, 0x20), range(0x7f, 0xa0), range(0xe0, 0x100))

def char8(rom, bdf):
   c8x8(rom, bdf, range(0x20, 0x7f), range(0xa0, 0xe0))

parser = argparse.ArgumentParser()
parser.add_argument('--graphics', type=str)
parser.add_argument('--jisx0201', type=str)
parser.add_argument('--jisx0208', type=str)
parser.add_argument('--char8', type=str)
parser.add_argument('--graphics8', type=str)
parser.add_argument('--out', type=str)

rom = np.zeros([256 * 1024], dtype=np.int8)
args = parser.parse_args()
if (args.graphics is not None):
   graphics(rom, args.graphics)
if (args.jisx0201 is not None):
   jisx0201(rom, args.jisx0201)
if (args.jisx0208 is not None):
   jisx0208(rom, args.jisx0208)
if (args.char8 is not None):
   char8(rom, args.char8)
if (args.graphics8 is not None):
   graphics8(rom, args.graphics8)

rom.tofile(args.out)
