# colormap_to_ITKSNAP
A simple script to convert matplotlib colormaps to an XML format readable by ITK-SNAP. Allows beautiful colormaps of your choice to be put into ITK-SNAP!

Simply use the ColorMapWriter to take any available color map in ITK-SNAP or a [256,4] RGBA array in numpy and this script will write out a valid XML which can be used in ITK-SNAP.
<<<<<<< HEAD

Simply pass a 4xN colormap, the path to the XML file and the number of control points you would like into the ColorMapWriter and then run the 'createLookupTable' method.
=======
>>>>>>> e3e9d015e9688c92f48f6a7a00bc513f962d4513

Example code that creates an ITK compatible color map

```python
import ColorMapWriter
import matplotlib.cm as cmap
mpl_map = cmap.viridis(np.arange(256))
<<<<<<< HEAD
c = ColorMapWriter.ColorMapWriter(mpl_map, 'viridis.xml', 5)
c.createLookupTable()
=======
ColorMapWriter.ColorMapWriter(mpl_map, 'viridis.xml')
```
>>>>>>> e3e9d015e9688c92f48f6a7a00bc513f962d4513

The file then needs placed in the %APPDATA%\itksnap.org\ITK-SNAP\ColorMaps folder if using Windows for example.


As shown in ITK-SNAP as the following

![alt tag](https://raw.githubusercontent.com/gordon-n-stevenson/colormap_to_ITKSNAP/master/itksnap_3dview.PNG) ![alt tag](https://raw.githubusercontent.com/gordon-n-stevenson/colormap_to_ITKSNAP/master/itksnap_cmap.PNG)
