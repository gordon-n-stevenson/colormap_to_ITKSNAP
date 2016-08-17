import matplotlib.cm as cmap
import numpy as np
import ColorMapWriter

mpl_map = cmap.viridis(np.arange(256))
c = ColorMapWriter.ColorMapWriter(mpl_map, 'viridis.xml', 5)
c.createLookupTable()
