import matplotlib.cm as cmap
import ColorMapWriter
mpl_map = cmap.viridis(np.arange(256))
ColorMapWriter.ColorMapWriter(mpl_map, 'viridis.xml')
