# colormap_to_ITKSNAP
A simple script to convert MPL cmaps to an XML format readable by ITK-SNAP

Simply use the ColorMapWriter to take any available color map in ITK-SNAP or a [256,4] RGBA array in numpy and this script will write out a valid XML which can be used in ITK-SNAP.

Simply pass a 4xN colormap, the path to the XML file and the number of control points you would like into the ColorMapWriter and then run the 'createLookupTable' method.

Example code

import ColorMapWriter
import matplotlib.cm as cmap
mpl_map = cmap.viridis(np.arange(256))
c = ColorMapWriter.ColorMapWriter(mpl_map, 'viridis.xml', 5)
c.createLookupTable()

As shown in ITK-SNAP
![alt tag](https://raw.github.com/gordon-n-stevenson/colormap_to_ITKSNAP/itksnap_3dview.png)

![alt tag](https://raw.github.com/gordon-n-stevenson/colormap_to_ITKSNAP/itksnap_cmap.png)
