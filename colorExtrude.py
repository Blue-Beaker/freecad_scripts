import math
from PySide import QtGui

def getThickness(color):
    R=color[0]
    G=color[1]
    B=color[2]
    V=max(R,G,B)
    if V == 0:
        S = 0
    else:
        S = (V- min(R,G,B)) / V

    return eval(length_func) if length_func else ((0.30*R)+(0.59*G)+(0.11*B))*10

def extrude(part,name,length):
    part.Document.addObject('Part::Extrusion',name)
    f = part.Document.getObject(name)
    f.Base = part
    f.DirMode = "Custom"
    f.Dir = App.Vector(0.000000000000000, 0.000000000000000, 1.000000000000000)
    f.DirLink = None
    f.LengthFwd = length
    f.LengthRev = 0.000000000000000
    f.Solid = False
    f.Reversed = False
    f.Symmetric = False
    f.TaperAngle = 0.000000000000000
    f.TaperAngleRev = 0.000000000000000
    f.ViewObject.ShapeColor=part.ViewObject.ShapeColor
    part.ViewObject.Visibility=False

def Name(obj):
	return obj.Name


reply=QtGui.QInputDialog.getText(None, "Color Extrude","Enter the expression for extrusion length:\nR,G,B,V and math functions can be used.")
if reply[1]:
	# user clicked OK
	length_func = reply[0]
else:
	# user clicked Cancel
	length_func =  "((0.30*R)+(0.59*G)+(0.11*B))*10"# which will be "" if they clicked Cancel

selection=Gui.Selection.getSelection()
selection.sort(key=Name)
for obj in selection:
	print(obj.__class__)
	if hasattr(obj,'ViewObject'):
		viewobj=obj.ViewObject
		if hasattr(viewobj,'ShapeColor'):
			extrude(obj,"extrusion_"+obj.Name,getThickness(viewobj.ShapeColor))
			#print(getThickness(viewobj.ShapeColor))