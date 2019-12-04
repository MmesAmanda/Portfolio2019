import maya.cmds as cmds
import random as rnd


if 'myWin' in globals():
   if cmds.window(myWin, exists=True):
      cmds.deleteUI(myWin, window=True)
      
if 'nextBlockId' not in globals():
    nextBlockId = 1000
    
if 'nextWheelId' not in globals():
    nextWheelId = 1000

      
myWin = cmds.window(title="Lego Blocks - Amanda McLeod", menuBar=True)
cmds.menu(label="Basic Options")
cmds.menuItem(label="New Scene", command=('cmds.file(new=True, force=True)'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))

#GUI FOR NORMAL BLOCK
cmds.frameLayout(collapsable=True, label="Standard Block", width=475, height=140)
cmds.intSliderGrp('blockHeight',l="Height", f=True, min=1, max=20, value=3)
cmds.intSliderGrp('blockWidth', l="Width (Bumps)", f=True, min=1, max=20, value=2) 
cmds.intSliderGrp('blockDepth', l="Depth (Bumps)", f=True, min=1, max=20, value=8)
cmds.colorSliderGrp('blockColour', label="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Basic Block", command=('basicBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )

#GUI FOR SLOPED BLOCK
cmds.frameLayout(collapsable=True, label="Sloped Block", width=475, height=140)
cmds.intSliderGrp('slopedWidth', l="Width (Bumps)", f=True, min=1, max=20, value=2) 
cmds.intSliderGrp('slopedDepth', l="Depth (Bumps)", f=True, min=2, max=4, value=2)
cmds.colorSliderGrp('slopedColour', label="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Sloped Block", command=('slopedBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )

#GUI FOR HOLE BLOCK
cmds.frameLayout(collapsable=True, label="Hole Block", width=475, height=140)

#Changed min value on width to 2 since there is no width 1
cmds.intSliderGrp('HoleWidth', l="Width (Bumps)", f=True, min=2, max=20, value=2)
cmds.colorSliderGrp('HoleColour', label="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Hole Block", command=('HoleBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )


#GUI FOR BEAM
cmds.frameLayout(collapsable=True, l="Beam", width=475, height=140)
cmds.intSliderGrp('BeamWidth', l="Length", f=True, min=3, max=20, value=1)
cmds.colorSliderGrp('BeamColour', label="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Beam Block", command=('BeamBlock()')) 
cmds.setParent( '..' )
cmds.setParent( '..' )

#GUI FOR WHEEL
cmds.frameLayout(collapsable=True, label="Wheel Block", width=475, height=140)
cmds.intSliderGrp('WheelSize', l="Wheel (Size)", f=True, min=1, max=20, value=2)
cmds.intSliderGrp('WheelThickness',l="Wheel (Thickness)", f=True, min=1, max=20, value=2)
cmds.colorSliderGrp('WheelColour', label="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Wheel", command=('Wheel()')) 
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.showWindow( myWin )

###########################NORMAL BLOCK FUNCTION###############################

def basicBlock():                                                               
   blockHeight = cmds.intSliderGrp('blockHeight', q=True, v=True)                
   blockWidth = cmds.intSliderGrp('blockWidth', q=True, v=True)
   blockDepth = cmds.intSliderGrp('blockDepth', q=True, v=True)
   
   rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)
   global nextBlockId
   nsTmp = "Block" + str(nextBlockId)
   nextBlockId = nextBlockId + 1
   
   
   cmds.select(clear=True)
   cmds.namespace(set=":")
   cmds.namespace(add=nsTmp)
   cmds.namespace(set=nsTmp)
   
   cubeSizeX = blockWidth * 0.8
   cubeSizeZ = blockDepth * 0.8
   cubeSizeY = blockHeight * 0.32
   
   
   cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
   cmds.move((cubeSizeY/2.0), moveY=True)
   
   for i in range(blockWidth):
      for j in range(blockDepth):
         cmds.polyCylinder(r=0.25, h=0.20)
         cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
         cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
         cmds.move(((j * 0.8) - (cubeSizeZ/2.0) + 0.4), moveZ=True, a=True)
         
         
   myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
   cmds.setAttr(nsTmp+":blckMat.color",rgb[0],rgb[1],rgb[2], typ='double3')
   
   cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
   cmds.delete(ch=True)
   cmds.hyperShade(assign=(nsTmp+":blckMat"))
   
   cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)
   
###########################SLOPED BLOCK FUNCTION###############################  

def slopedBlock():
    blockHeight = 3
    blockWidth = cmds.intSliderGrp('slopedWidth', q=True, v=True)
    blockDepth = cmds.intSliderGrp('slopedDepth', q=True, v=True)
    rgb = cmds.colorSliderGrp('slopedColour', q=True, rgbValue=True) 

    global nextBlockId
    nsTmp = "Block" + str(nextBlockId)
    nextBlockId = nextBlockId + 1

    cmds.select(clear=True)
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)

    cubeSizeX = blockWidth * 0.8
    cubeSizeZ = blockDepth * 0.8
    cubeSizeY = blockHeight * 0.32
    
    cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ, sz=blockDepth)
    cmds.move((cubeSizeY/2.0), y=True, a=True)

    for i in range(blockWidth):
        cmds.polyCylinder(r=0.25, h=0.20)
        cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
        cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
        cmds.move((0 -(cubeSizeZ/2.0) + 0.4), moveZ=True)
    
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color", rgb[0], rgb[1], rgb[2], typ='double3')
    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    cmds.hyperShade(assign=(nsTmp+":blckMat"))

    cmds.select((nsTmp+":"+nsTmp+".e[1]"), r=True)
    cmds.move(0, -0.8, 0, r=True) 

    if blockDepth == 4:
        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[8]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[6]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)
        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[9]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[7]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)
    if blockDepth >= 3:
        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[6]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[4]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)
        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[7]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[5]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)
    cmds.namespace( removeNamespace=":"+nsTmp, mergeNamespaceWithParent = True)
 
##############################HOLE BLOCK FUNCTION#################################

def HoleBlock():
    
    blockWidth = cmds.intSliderGrp('HoleWidth', q = True, v= True)
    global nextBlockId
    nsTmp = "Block" + str(nextBlockId)
    nextBlockId = nextBlockId + 1
    
    rgb = cmds.colorSliderGrp('HoleColour', q=True, rgbValue=True) 

    cmds.select(clear=True)
    cmds.namespace(set=":")
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)
    
    
    #Cube
    cmds.polyCube(width = 1, height = 1, depth = 1, sh = 2, sd = 2)
    cmds.move(-.5, 0, 0,nsTmp+":pCube1.scalePivot", nsTmp+":pCube1.rotatePivot")
    cmds.move(0, .5, 0)
    cmds.scale(blockWidth, scaleX =True)

    for i in range(blockWidth-1):
        hole = "pCube"
        pokeHole(.3, i+.5, .6, nsTmp, hole)

  
    for i in range(blockWidth):
        sect = "PolySurface" + str(i + 1)

        #Create pipe, used to make bump
        cmds.polyPipe(r=.25, h=.5, t=.05)
        cmds.move(i, 1, 0)
        cmds.polyBoolOp( nsTmp + ":pPipe1", nsTmp + ":pCube1", op=1, n=sect)  
        cmds.delete(nsTmp + ":" + sect, ch = True)
        cmds.select(nsTmp + ":" + sect)
        cmds.rename("pCube1")
    
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color", rgb[0], rgb[1], rgb[2], typ='double3')

    cmds.select(nsTmp +":pCube1")
    cmds.rename(nsTmp)
    
    cmds.hyperShade(assign=(nsTmp+":blckMat"))
    cmds.namespace( removeNamespace=":"+nsTmp, mergeNamespaceWithParent = True)
    
#############################BEAM BLOCK FUNCTION###################################### 
   
def BeamBlock():
    
    blockWidth = cmds.intSliderGrp('BeamWidth', q = True, v= True)
    global nextBlockId
    nsTmp = "Block" + str(nextBlockId)
    nextBlockId = nextBlockId + 1
    
    rgb = cmds.colorSliderGrp('BeamColour', q=True, rgbValue=True) 

    cmds.select(clear=True)
    cmds.namespace(set=":")
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)
    
    cubeX = .8
    cubeZ = .32
    cubeY = .8
    radius = .25

    for i in range(blockWidth):
        offset = i * cubeX
        if i == 0:
            beamTip(cubeX , cubeY, cubeZ , radius, 1, offset, nsTmp, "start")
        if i == (blockWidth - 1):
            beamTip(cubeX , cubeY, cubeZ , radius, -1, offset, nsTmp, "end")
        if i > 0 and i <(blockWidth-1):
            cmds.polyCube(width = cubeX , height = cubeY, depth = cubeZ)
            cmds.move(offset, (cubeY * .5), 0)
            pokeHole(radius, offset, (cubeY * .5), nsTmp, "mid1")
            
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color", rgb[0], rgb[1], rgb[2], typ='double3')

    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    cmds.hyperShade(assign=(nsTmp+":blckMat"))
    cmds.namespace( removeNamespace=":"+nsTmp, mergeNamespaceWithParent = True)

#################################HOLE POCKING FUNCTION#################################

def pokeHole(rad, posX, posY, NSTMP, name):

    cmds.polyCylinder(r=rad, h=2)
    cmds.move(posX, posY, 0)
    cmds.rotate(90, rotateX=True)

    BOOL(NSTMP, ":pCube1", ":pCylinder1", 2, name)
    
##################################BEAM ENDS FUNCTION####################################  
  
def beamTip(Height, Width, Depth, rad, flatSurf, baseX, NSTMP, name):    
    cmds.polyCylinder(r=(Height*.5), h=Depth)
    cmds.move(baseX, (Height*.5), 0)
    cmds.rotate(90, rotateX=True)

    cmds.polyCube(width = (Width *.5), height = Height, depth = Depth)
    cmds.move(((Width*.25 * flatSurf) + baseX), (Height * .5), 0)

    BOOL(NSTMP, ":pCylinder1", ":pCube1", 2, "polySurface1")
    
    cmds.polyCube(width = (Width *.5), height = Height, depth = Depth)
    cmds.move(((Width*.25 *flatSurf) + baseX), (Height * .5), 0)

    BOOL(NSTMP, ":polySurface1", ":pCube1", 1, "pCube1")
    pokeHole(rad, baseX, (Height * .5), NSTMP, name)
    
#########################################################################################

def BOOL(NSTMP, obj1, obj2, OP, RENAME):
    cmds.polyBoolOp(NSTMP + obj1, NSTMP + obj2, op=OP, uth = True, n = "union")
    cmds.delete(NSTMP + ":union", constructionHistory = True)
    cmds.rename(RENAME)
    
#######################################WHEEL###############################################   
 
def Wheel():
    
    global nextWheelId
    nsTmp = "Wheel" + str(nextWheelId)
    nextWheelId = nextWheelId + 1
    
    cmds.select(clear=True)
    cmds.namespace(set=":")
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)
    
    #Create cylinder
    WheelSize = cmds.intSliderGrp('WheelSize', q = True, v= True)
    WheelThickness = cmds.intSliderGrp('WheelThickness', q = True, v= True)
    Wheel = cmds.polyCylinder(name="wheel", r=WheelSize*0.3, h=WheelThickness*0.1, sa = 50)
    rgb = cmds.colorSliderGrp('WheelColour', q=True, rgbValue=True) 
    
    
    FaceCount = cmds.polyEvaluate(Wheel, face=True)
    for i in range(0, FaceCount-2):
        FaceName = ":wheel" + ".f[" + str(i) + "]"
        WheelName = nsTmp + FaceName
        if i % 2 ==0:
            cmds.polyExtrudeFacet(WheelName, ltz=((WheelSize*0.1)/4))##EXTRUDE EVEYR SECOND FACE
            
    Wheel2 = cmds.polyCylinder(name="wheel2", r=WheelSize*0.3, h=WheelThickness*0.1, sa = 50)
    FaceCount = cmds.polyEvaluate(Wheel2, face=True)
    for i in range(0, FaceCount-2):
        FaceName = ":wheel2" + ".f[" + str(i) + "]"
        WheelName = nsTmp + FaceName
        if i % 2 ==0:
            cmds.polyExtrudeFacet(WheelName, ltz=((WheelSize*0.1)/4))##EXTRUDE EVEYR SECOND FACE
    cmds.select(Wheel2)    
    cmds.rotate(7, Wheel2, rotateY=True)
    cmds.move((WheelThickness*0.1), moveY=True)
    
    myShader = cmds.shadingNode('lambert', asShader=True, name="WheelColour")
    cmds.setAttr(nsTmp+":WheelColour.color",rgb[0],rgb[1],rgb[2], typ='double3')
   
    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    cmds.hyperShade(assign=(nsTmp+":WheelColour"))
   
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)
     
    WheelHole = cmds.polyCylinder(name="wheelHole", r=WheelSize*0.175, h=WheelThickness/2, sa = 50)
    cmds.polyCBoolOp( nsTmp, "wheelHole", op=2) ## DIFFERENCE BOOLEAN
    cmds.delete(ch=True)
    
######################################################################################################    
    
    
   
     
    

