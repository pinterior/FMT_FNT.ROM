FMT_FNT.ROM
===

Scripts to generate font rom for FM-TOWNS emulator from BDF.

Prerequisite
---

 - numpy
 - [bdflib](https://pypi.org/project/bdflib/)
 - BDF font
   - ex. [xfonts-shinonome](https://salsa.debian.org/fonts-team/xfonts-shinonome), [towns-font](https://github.com/pinterior/towns-font)

Usage
---

### Create FMT_FNT.ROM

```
python 16dot.py \
   --graphics  ./towns-font/towns16g.bdf \
   --jisx0201  ./xfonts-shinonome/bdf/shnm8x16r.bdf \
   --jisx0208  ./xfonts-shinonome/bdf/shnmk16min.bdf \
   --char8     ./towns-font/ank8.bdf \
   --graphics8 ./towns-font/ank8g.bdf \
   --out FMT_FNT.ROM
```

### Create part of FMT_SYS.ROM

```
python 12dot.py \
   --graphics ./towns-font/towns12g.bdf \
   --jisx0201 ./xfonts-shinonome/bdf/shnm6x12r.bdf \
   --jisx0208 ./xfonts-shinonome/bdf/shnmk12.bdf \
   --out FMT_SYS0.F12
```
