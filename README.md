# colormap_to_ITKSNAP
A simple script to convert MPL cmaps to an XML format readable by ITK-SNAP

Simply use the ColorMapWriter to take any available color map in ITK-SNAP or a [256,4] RGBA array in numpy and this script will write out a valid XML which can be used in ITK-SNAP

Example code

import ColorMapWriter
import matplotlib.cm as cmap
mpl_map = cmap.viridis(np.arange(256))
ColorMapWriter.ColorMapWriter(mpl_map, 'viridis.xml')

As shown in ITK-SNAP
![alt tag](https://raw.github.com/gordon-n-stevenson/colormap_to_ITKSNAP/itksnap_3dview.png)

![alt tag](https://raw.github.com/gordon-n-stevenson/colormap_to_ITKSNAP/itksnap_cmap.png)
