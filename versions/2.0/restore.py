#===================================================================
# Module with functions to save & restore qt widget values
# Written by: Alan Lilly 
# Website: http://panofish.net
#===================================================================

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import inspect

#===================================================================
# save "ui" controls and values to registry "setting"
# currently only handles comboboxes editlines & checkboxes
# ui = qmainwindow object
# settings = qsettings object
#===================================================================

def guisave(ui, settings):

    #for child in ui.children():  # works like getmembers, but because it traverses the hierarachy, you would have to call guisave recursively to traverse down the tree


    for name, obj in inspect.getmembers(ui):

        #if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
        if isinstance(obj, QComboBox):
            name   = obj.objectName()      # get combobox name
            index  = obj.currentIndex()    # get current index from combobox
            text   = obj.itemText(index)   # get the text for current index
            settings.setValue(name, text)   # save combobox selection to registry

        if isinstance(obj, QLineEdit):
            name = obj.objectName()
            value = obj.text()
            settings.setValue(name, value)    # save ui values, so they can be restored next time

        if isinstance(obj, QCheckBox):
            name = obj.objectName()
            state = obj.isChecked()
            settings.setValue(name, state)

        if isinstance(obj, QDoubleSpinBox):
            name = obj.objectName()
            value = obj.value()
            settings.setValue(name, value)

        if isinstance(obj, QSpinBox):
            name = obj.objectName()
            value = obj.value()
            settings.setValue(name, value)

#===================================================================
# restore "ui" controls with values stored in registry "settings"
# currently only handles comboboxes, editlines &checkboxes
# ui = QMainWindow object
# settings = QSettings object
#===================================================================

def guirestore(ui, settings):

    for name, obj in inspect.getmembers(ui):
        
        if isinstance(obj, QComboBox):
            index  = obj.currentIndex()    # get current region from combobox
            #text   = obj.itemText(index)   # get the text for new selected index
            name   = obj.objectName()

            value = unicode(settings.value(name).toString())  

            if value == "":
                continue

            index = obj.findText(value)   # get the corresponding index for specified string in combobox

            if index == -1:  # add to list if not found
                obj.setCurrentIndex(0)
            else:
                obj.setCurrentIndex(index)   # preselect a combobox value by index    

        if isinstance(obj, QLineEdit):
            name = obj.objectName()
            value = unicode(settings.value(name).toString())  # get stored value from registry
            obj.setText(value)  # restore lineEditFile

        if isinstance(obj, QCheckBox):
            name = obj.objectName()
            value = settings.value(name).toBool()   # get stored value from registry
            if value != None:
                obj.setChecked(value)   # restore checkbox

        if isinstance(obj, QDoubleSpinBox):
            name = obj.objectName()
            value = settings.value(name).toFloat()
            obj.setValue(value[0])

        if isinstance(obj, QSpinBox):
            name = obj.objectName()
            value = settings.value(name).toInt()
            obj.setValue(value[0])

        #if isinstance(obj, QRadioButton):                

################################################################

if __name__ == "__main__":

    # execute when run directly, but not when called as a module.
    # therefore this section allows for testing this module!

    #print "running directly, not as a module!"

    sys.exit()
