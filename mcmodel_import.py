import json,math,os,regex
import Part,Draft
from PySide import QtCore
from PySide import QtGui
def makeBox(pos1,pos2):
	size=[]
	for i in range(len(pos1)):
		size.append(pos2[i]-pos1[i])
	#print(pos1.__str__(),size.__str__())
	box = doc.addObject("Part::Box", modelName)
	box.Length=max(size[0],0.01)
	box.Width=max(size[1],0.01)
	box.Height=max(size[2],0.01)
	# box.Placement.Base=FreeCAD.Vector(pos1[0],pos1[1],pos1[2])
	box.Placement.move(FreeCAD.Vector(pos1[0],pos1[1],pos1[2]))
	return box

dict_axis={
"x":FreeCAD.Vector(1.0,0.0,0.0),
"y":FreeCAD.Vector(0.0,1.0,0.0),
"z":FreeCAD.Vector(0.0,0.0,1.0),}
def rotate(body,rotation):
	origin=rotation["origin"]
	axis=dict_axis[rotation["axis"]]
	angle=rotation["angle"]
	body.Placement.rotate(origin,axis,angle)
	#body.Placement.Rotation.Angle=angle
	#body.Placement.Rotation.Axis=axis

def importModel(model):
	if "elements" in model:
		elements=model["elements"]
		for element in elements:
			if "from" in element and "to" in element:
				pos1=element["from"]
				pos2=element["to"]
				box=makeBox(pos1,pos2)
				if "rotation" in element:
					rotate(box,element["rotation"])
	elif "parent" in model and findParent:
		parent=os.path.join(rootdir,splitNamespace(model["parent"]))
		print(parent)
		model2=json.JSONDecoder().decode(open(parent,"r").read())
		importModel(model2)

def splitNamespace(name:str):
	split=name.split(":",1)
	id=split[-1]
	namespace=split[-2] if split.__len__()>1 else "minecraft"
	return os.path.join(namespace,"models",id+".json")

findParent=True
file=QtGui.QFileDialog.getOpenFileName(None,"Open Model", "", "Minecraft Model (*.json)")
doc = FreeCAD.activeDocument()
if file[1]=="Minecraft Model (*.json)":
	modelName=os.path.basename(file[0])
	match=regex.match("(.*/assets/)\w*/models",file[0])
	try:
		rootdir=match.group(1)
		print(rootdir)
	except:
		findParent=False
	model=json.JSONDecoder().decode(open(file[0],"r").read())
	importModel(model)