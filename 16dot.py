#!/usr/bin/python3

import argparse
import itertools
import numpy as np

from bdflib import reader


def to_data(g, x, y):
   p = np.stack([np.fromiter(e, np.int8) for e in g.iter_pixels()])
   b = np.zeros([ y, x ], np.int8)

   s = np.shape(p)
   ix = min(s[1], x)
   iy = min(s[0], y)
   b[:iy, :ix] = p[:iy, :ix]
   b = b.reshape([ x * y // 8, 8 ])

   return np.packbits(b)

def jisx0201(rom, bdf):
   with open(bdf, 'rb') as fp:
      font = reader.read_bdf(fp)
      cp = font.codepoints()
      for c in itertools.chain(range(0x20, 0x7f), range(0xa1, 0xe0)):
         if c in cp:
            b = to_data(font[c], 8, 16)
            o = 251904 + c * 16
            rom[o:(o + len(b))] = b

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
               b = to_data(font[c], 16, 16)
               o = i * 32
               rom[o:(o + len(b))] = b

parser = argparse.ArgumentParser()
parser.add_argument('--jisx0201', type=str)
parser.add_argument('--jisx0208', type=str)
parser.add_argument('--out', type=str)

rom = np.zeros([256 * 1024], dtype=np.int8)
args = parser.parse_args()
if (args.jisx0201 is not None):
   jisx0201(rom, args.jisx0201)
if (args.jisx0208 is not None):
   jisx0208(rom, args.jisx0208)

rom.tofile(args.out)
