# colormap_to_ITKSNAP
A simple script to convert matplotlib colormaps to an XML format readable by ITK-SNAP. Allows beautiful colormaps of your choice to be put into ITK-SNAP!

Simply use the ColorMapWriter to take any available color map in ITK-SNAP or a [256,4] RGBA array in numpy and this script will write out a valid XML which can be used in ITK-SNAP.

Example code that creates an ITK compatible color map

```python
import ColorMapWriter
import matplotlib.cm as cmap
mpl_map = cmap.viridis(np.arange(256))
ColorMapWriter.ColorMapWriter(mpl_map, 'viridis.xml')
```


As shown in ITK-SNAP as the following

![alt tag](https://raw.githubusercontent.com/gordon-n-stevenson/colormap_to_ITKSNAP/master/itksnap_3dview.PNG) ![alt tag](https://raw.githubusercontent.com/gordon-n-stevenson/colormap_to_ITKSNAP/master/itksnap_cmap.PNG)
