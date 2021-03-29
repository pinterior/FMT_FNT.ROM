import numpy as np

def to_data(g, x, y):
   p = np.stack([np.fromiter(e, np.int8) for e in g.iter_pixels()])
   b = np.zeros([ y, x ], np.int8)

   s = np.shape(p)
   ix = min(s[1], x)
   iy = min(s[0], y)
   b[:iy, :ix] = p[:iy, :ix]

   r = b.reshape([ x * y // 8, 8 ])
   return np.packbits(r)
