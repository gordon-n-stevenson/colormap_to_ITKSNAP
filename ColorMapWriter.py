__author__ = 'gordonnstevenson'
__project__ = 'ColorMapToITKSNAP'

import xml.etree.ElementTree as xml
import numpy as np

class ColorMapWriter(object):
    def __init__(self, lookuptable, filename):

        if not isinstance(lookuptable, np.ndarray) or lookuptable.shape[1] != 4:
            print ("Invalid Lookup Table Format!")
            return

        root = xml.Element("registry")
        num_tbl_pts = int(lookuptable.shape[0])

        range_nudge = 1
        clr_range = range(0, num_tbl_pts, range_nudge)
        clr_range.append(num_tbl_pts-1)

        num_ctrlpts_ele = xml.Element("entry")
        num_ctrlpts_ele.set('key','NumberOfControlPoints')
        num_ctrlpts_ele.set('value', '{:d}'.format(len(clr_range)))
        preset_ele = xml.Element("entry")
        preset_ele.set('key', 'Preset')
        preset_ele.set('value', 'Custom')

        root.append(num_ctrlpts_ele)
        root.append(preset_ele)

        rgba = [0, 0, 0, 0]
        rgba_vals = list()

        clr_range = range(0, num_tbl_pts, range_nudge)
        clr_range.append(num_tbl_pts-1)

        for x in clr_range:
            rgba = lookuptable[x,:]
            rgba_vals.extend([[int(rgba[0]*255.0),int(rgba[1]*255.0),int(rgba[2]*255.0), int(rgba[3]*255.0)]])

        st_ind, end_ind = clr_range[0], clr_range[::-1][0]

        num_ctrl_pts = len(range(0, num_tbl_pts, range_nudge))

        for i,ct in enumerate(clr_range):
            if ct == st_ind or ct == end_ind:
                ctrl_pt = self.create_control_point(i, rgba_vals[i], num_ctrl_pts, True)
            else:
                ctrl_pt = self.create_control_point(i, rgba_vals[i], num_ctrl_pts, False)
            root.append(ctrl_pt)

        self.indent(root)
        tree = xml.ElementTree(root)

        with open(filename, 'w') as f:
            declaration = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE registry [\n<!ELEMENT registry (entry*,folder*)>\n<!ELEMENT folder (entry*,folder*)>\n<!ELEMENT entry EMPTY>\n<!ATTLIST folder key CDATA #REQUIRED>\n<!ATTLIST entry key CDATA #REQUIRED>\n<!ATTLIST entry value CDATA #REQUIRED>\n]>\n'
            f.write(declaration)
            tree.write(f, 'utf-8')

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
