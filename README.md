FMT_FNT.ROM
===

Scripts to generate font rom for FM-TOWNS emulator from BDF.


Prerequisite
---

 - numpy
 - [bdflib](https://pypi.org/project/bdflib/)
 - BDF font
   - ex. [xfonts-shinonome](https://salsa.debian.org/fonts-team/xfonts-shinonome)

Usage
---

### Create FMT_FNT.ROM from xfonts-shinonome

```
python 16dot.py \
   --jisx0201 shnm8x16r.bdf \
   --jisx0208 shnmk16min.bdf \
   --out FMT_FNT.ROM
```

### Create part of FMT_SYS.ROM from xfonts-shinonome

```
python 12dot.py \
   --jisx0201 shnm6x12r.bdf \
   --jisx0208 shnmk12.bdf \
   --out FMT_SYS0.F12
```
