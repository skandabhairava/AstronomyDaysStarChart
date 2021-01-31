# -*- coding: utf-8 -*-
"""StarChart.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Uwpaw-ByjWyl8-TE6EUjG7g9koCqQ5kA
"""

!pip install skyfield

from skyfield.api import Star, load
from skyfield.data import hipparcos
from matplotlib import pyplot as plt
plt.style.use(['dark_background'])

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)

ts = load.timescale()
t = ts.now()

eph = load('de421.bsp')
earth = eph['earth']

print(f'There are {len(df)} stars in the Hipparcos catalog ({hipparcos.URL}).')
limiting_magnitude = 5.0
df_lim = df[df['magnitude'] <= limiting_magnitude]
print(f'After filtering out stars dimmer than mag {limiting_magnitude}, there are {len(df_lim)}')
bright_stars = Star.from_dataframe(df_lim)
df_lim['magnitude'].min()

fig, ax = plt.subplots(5, figsize=(10,48))
for mag in range(1,6):
  df_lim = df[df['magnitude'] <= mag]
  bright_stars = Star.from_dataframe(df_lim)
  astrometric = earth.at(t).observe(bright_stars)
  ra, dec, distance = astrometric.radec()
  ax[mag-1].scatter(ra.hours, dec.degrees, 2*(5-df_lim['magnitude']), 'w')
  ax[mag-1].set_xlim(7.0, 4.0)
  ax[mag-1].set_ylim(-20, 20)
  ax[mag-1].grid(color='gray', linestyle='-', linewidth=.5, alpha=.5)
  ax[mag-1].set(title=f'Stars in Orion brighter than magnitude {mag}')
  ax[mag-1].set_xlabel('right ascension')
  ax[mag-1].set_ylabel('declination')
plt.tight_layout()

fig.savefig(f'bright_stars_.png')