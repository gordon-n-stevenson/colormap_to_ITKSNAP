__author__ = 'gordonnstevenson'
__project__ = 'ColorMapToITKSNAP'

import xml.etree.ElementTree as xml
import numpy as np

class ColorMapWriter(object):

    ctrl_pt_number = None
    lookuptable = None
    filename = None

    def __init__(self, lookuptable, filename, ctrl_pt_num = 10):
    
        if not isinstance(lookuptable, np.ndarray) or lookuptable.shape[1] != 4:
            print ("Invalid Lookup Table Format!")
            return

        self.ctrl_pt_number = ctrl_pt_num
        self.lookuptable = lookuptable
        self.filename = filename

    def createLookupTable(self):
        if not isinstance(self.lookuptable, np.ndarray) or self.lookuptable.shape[1] != 4:
            print ("Invalid Lookup Table Format!")
            return
        
        self.root = xml.Element("registry")
        num_tbl_pts = int(self.lookuptable.shape[0])

        range_nudge = 1
        clr_range = range(0, num_tbl_pts, range_nudge)
        clr_range.append(num_tbl_pts-1)


        rgba = [0, 0, 0, 0]
        rgba_vals = list()

        clr_range = range(0, num_tbl_pts, range_nudge)
        clr_range.append(num_tbl_pts-1)

        for x in clr_range:
            rgba = self.lookuptable[x,:]
            rgba_vals.extend([[int(rgba[0]*255.0),int(rgba[1]*255.0),int(rgba[2]*255.0), int(rgba[3]*255.0)]])

        st_ind, end_ind = clr_range[0], clr_range[::-1][0]

        #num_ctrl_pts = len(range(0, num_tbl_pts, range_nudge))
        num_ctrl_pts = np.arange(0,self.lookuptable.shape[0]+1, (self.lookuptable.shape[0]-1)/(self.ctrl_pt_number)).astype(np.int)
        
        st_ind, end_ind = num_ctrl_pts[0], num_ctrl_pts[::-1][0]

        self.writeHeader()

        
        for ct,i in enumerate(num_ctrl_pts):
            if ct == st_ind or ct == end_ind:
                ctrl_pt = self.create_control_point(ct, rgba_vals[i], self.ctrl_pt_number, True)
            else:
                ctrl_pt = self.create_control_point(ct, rgba_vals[i], self.ctrl_pt_number, False)
            self.root.append(ctrl_pt)

        self.indent(self.root)
        tree = xml.ElementTree(self.root)

        with open(self.filename, 'w') as f:
            declaration = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE registry [\n<!ELEMENT registry (entry*,folder*)>\n<!ELEMENT folder (entry*,folder*)>\n<!ELEMENT entry EMPTY>\n<!ATTLIST folder key CDATA #REQUIRED>\n<!ATTLIST entry key CDATA #REQUIRED>\n<!ATTLIST entry value CDATA #REQUIRED>\n]>\n'
            f.write(declaration)
            tree.write(f, 'utf-8')

    def writeHeader(self):
        num_ctrlpts_ele = xml.Element("entry")
        num_ctrlpts_ele.set('key','NumberOfControlPoints')
        num_ctrlpts_ele.set('value', '{:d}'.format(self.ctrl_pt_number+1))
        preset_ele = xml.Element("entry")
        preset_ele.set('key', 'Preset')
        preset_ele.set('value', 'Custom')
        self.root.append(num_ctrlpts_ele)
        self.root.append(preset_ele)
            
    def create_control_point(self, pos, rgba_vals, numcols, type_val = True):
        ctrl_pt_ele = xml.Element('folder')
        ctrl_pt_ele.set('key', 'ControlPoint[{}]'.format(str(pos).zfill(4)))

        ind_entry =  xml.Element('entry')
        ind_entry.set('key','Index')

        ind_entry.set('value', '{0:.2f}'.format(float(pos/float(numcols))))
        type_entry =  xml.Element('entry')
        type_entry.set('key','Type')
        if type_val:
            type_entry.set('value', 'Discontinuous')
        else:
            type_entry.set('value', 'Continuous')
        ctrl_pt_ele.append(ind_entry)
        ctrl_pt_ele.append(type_entry)

        ctrl_pt_ele.append(self.create_rbga_folder('Left',rgba_vals,pos))
        ctrl_pt_ele.append(self.create_rbga_folder('Right',rgba_vals,pos))
        return ctrl_pt_ele

    def create_rbga_entry(self, component, value):
        rgba_entry = xml.Element('entry')
        rgba_entry.set('key',component)
        rgba_entry.set('value', value)
        return rgba_entry

    def create_rbga_folder(self, lft_right,rgba_vals,pos):
        rbga_ele = xml.Element('folder')
        rbga_ele.set('key', lft_right)
        rbga_ele.append(self.create_rbga_entry('A','{:d}'.format(rgba_vals[3])))
        rbga_ele.append(self.create_rbga_entry('B','{:d}'.format(rgba_vals[2])))
        rbga_ele.append(self.create_rbga_entry('G','{:d}'.format(rgba_vals[1])))
        rbga_ele.append(self.create_rbga_entry('R','{:d}'.format(rgba_vals[0])))
        return rbga_ele

    def indent(self, elem, level=0):
      i = "\n" + level*"  "
      if len(elem):
        if not elem.text or not elem.text.strip():
          elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
          elem.tail = i
        for elem in elem:
          self.indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
          elem.tail = i
      else:
        if level and (not elem.tail or not elem.tail.strip()):
          elem.tail = i


import matplotlib.cm as cmap

mpl_map = cmap.viridis(np.arange(256))
ColorMapWriter(mpl_map, 'viridis.xml')