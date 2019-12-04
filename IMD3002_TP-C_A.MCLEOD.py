import maya.cmds as cmds
import random as random

#checks if a GUI window is already opened
#if so, then it closes the already opened window and opens a new one
if 'myWin' in globals():
   if cmds.window(myWin, exists=True):
      cmds.deleteUI(myWin, window=True)

#the different id's for each of the items
if 'nextCityBlock' not in globals():
    nextCityBlock = 1
    
if 'nextBuilding' not in globals():
    nextBuilding = 1
    
if 'nextStreet' not in globals():
    nextStreet = 1
    
if 'nextStreetLine' not in globals():
    nextStreetLine = 1
    
if 'nextSidewalk' not in globals():
    nextSidewalk = 1
    
if 'nextLightId' not in globals():
    nextLightId = 1
    
if 'nextCanId' not in globals():
    nextCanId = 1
    
if 'nextBenchId' not in globals():
    nextBenchId = 1
    
#the GUI for the city generator
myWin = cmds.window(title="CITY GENERATOR", menuBar=True)
cmds.menu(label="Basic Options")
cmds.menuItem(label="New Scene", command=('cmds.file(new=True, force=True)'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))

#sliders to pick how many blocks for the width and height
cmds.frameLayout(collapsable=True, label="City Generator", width=475, height=140)
cmds.text("How Many City Blocks?")
cmds.intSliderGrp('cityHeight',l="Height", f=True, min=1, max=10, value=1)
cmds.intSliderGrp('cityWidth', l="Width", f=True, min=1, max=10, value=1) 

#colour picker for the buildings
cmds.text("Choose Building Colours")
cmds.colorSliderGrp('buildingColour1', label="Colour 1", hsv=(120, 1, 1))
cmds.colorSliderGrp('buildingColour2', label="Colour 2", hsv=(240, 1, 1))
cmds.colorSliderGrp('buildingColour3', label="Colour 3", hsv=(360, 1, 1))

#colour picker for the bench
cmds.text("Choose Bench Colour")
cmds.colorSliderGrp('benchColour', label="Colour", hsv=(120, 1, 1))

#colour picker for the garbage can
cmds.text("Choose Garbage Can Colour")
cmds.colorSliderGrp('canColour', label="Colour", hsv=(120, 1, 1)) 

##colour picker for the lights
cmds.text("Choose Street Light Colour")
cmds.colorSliderGrp('lightColour', label="Colour", hsv=(120, 1, 1)) 

#colour picker for the street
cmds.text("Choose Street Colour")
cmds.colorSliderGrp('streetColour', label="Colour", hsv=(120, 1, 1)) 

#colour picker for the street line
cmds.text("Choose Street Line Colour")
cmds.colorSliderGrp('lineColour', label="Colour", hsv=(120, 1, 1)) 

#colour picker for the sidewalk
cmds.text("Choose Sidewalk Colour")
cmds.colorSliderGrp('sidewalkColour', label="Colour 1", hsv=(120, 1, 1)) 

cmds.button(label="Generate City", command=('createCityBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.showWindow( myWin )

###############################City Block###################################
def createCityBlock():
    #gets the height and width of the city from the GUI sliders
    cityHeight = cmds.intSliderGrp('cityHeight', q=True, v=True)
    cityWidth = cmds.intSliderGrp('cityWidth', q=True, v=True)
    
    #hard-coded values for the length and width of the city blocks
    blockLength = 3
    blockWidth = 2
    
    #for loop that loops through the number of blocks the user inputed for the width and length of the city
    for i in range(cityHeight):
        for j in range(cityWidth):
            
            #creates name for each block
            global nextCityBlock
            tempNamespace = "cityBlock" + str(nextCityBlock)
            nextCityBlock = nextCityBlock + 1
            
            #creates a cube to represent a city block and moves it the proper offset
            cmds.polyCube(w=blockLength, d=blockWidth, h=0.1, sx=3, sy=2, n=tempNamespace)
            cmds.move(j*5, x=True)
            cmds.move(i*4, z=True)
            cmds.move(0.05, moveY=True)
            
            #variables that hold the offset so that they can be used to position the rest of the city elements
            offsetI = i*4
            offsetJ = j*5
            
            #creates a street, yellow lines for the streets, the sidewalk, and buildings for each block by calling the repsective functions
            createStreet(offsetI, offsetJ, tempNamespace)
            createStreetLine(offsetI, offsetJ)
            createSidewalk(offsetI, offsetJ, tempNamespace)
            buildingBuilder(offsetI, offsetJ, tempNamespace)    
            
            #calls the garbage can function four times and passes in the appropriate offsets
            createGarbageCan(offsetI+0.5, offsetJ-1.6, tempNamespace)
            createGarbageCan(offsetI-0.5, offsetJ+1.6, tempNamespace)
            createGarbageCan(offsetI+1.1, offsetJ, tempNamespace)
            createGarbageCan(offsetI-1.1, offsetJ, tempNamespace)
            
            #calls the bench function six times and passes in the appropriate offsets
            createBench(offsetI, offsetJ-1.7, tempNamespace, 180)
            createBench(offsetI, offsetJ+1.7, tempNamespace, 0)
            createBench(offsetI+1.2, offsetJ+0.5, tempNamespace, -90)
            createBench(offsetI+1.2, offsetJ-0.5, tempNamespace, -90)
            createBench(offsetI-1.2, offsetJ+0.5, tempNamespace, 90)
            createBench(offsetI-1.2, offsetJ-0.5, tempNamespace, 90)
            
            #calls the street light function ten times and passes in the appropriate offsets
            createStreetLight(offsetI+0.9, offsetJ-1.6, tempNamespace, 90)
            createStreetLight(offsetI-0.9, offsetJ-1.6, tempNamespace, 90)
            createStreetLight(offsetI+0.9, offsetJ+1.6, tempNamespace, -90)
            createStreetLight(offsetI-0.9, offsetJ+1.6, tempNamespace, -90)
            createStreetLight(offsetI-1.1, offsetJ+1.3, tempNamespace, 0)
            createStreetLight(offsetI-1.1, offsetJ-1.3, tempNamespace, 0)
            createStreetLight(offsetI-1.1, offsetJ-0.2, tempNamespace, 0)
            createStreetLight(offsetI+1.1, offsetJ+1.3, tempNamespace, 180)
            createStreetLight(offsetI+1.1, offsetJ-1.3, tempNamespace, 180)
            createStreetLight(offsetI+1.1, offsetJ+0.2, tempNamespace, 180)


###############################City Building###################################
def buildingBuilder(offsetI, offsetJ, blockNum):
       
    #loops through the two rows of the city block and determines how many buildings between 1 and 3 will be generated for each row
    #and then the second for loop loops through the number of buildings for that row
    for i in range(2):
        #number of buildings for each row of the city block
        numBuildings = randomInt(2) + 1
        
        for j in range(numBuildings):
            
            #name for the buildings
            global nextBuilding
            buildingName = blockNum + "Building" + str(nextBuilding)
            nextBuilding = nextBuilding + 1
            
            #determines what colour the building will be from the three colours the user chose in the GUI
            buildingColourNum = randomInt(2) + 1
            
            #if statements that sets the building colour depending on what number was generated for the buildingColourNum variable
            if buildingColourNum == 1:
                buildingColour = cmds.colorSliderGrp('buildingColour1', q=True, rgbValue=True)
                
            if buildingColourNum == 2:
                buildingColour = cmds.colorSliderGrp('buildingColour2', q=True, rgbValue=True)
                
            if buildingColourNum == 3:
                buildingColour = cmds.colorSliderGrp('buildingColour3', q=True, rgbValue=True)
            
            #random height, width, and length generated for each building
            buildingHeight = randomInt(2) + 1
            buildingWidth = randomFloat(0.6) + 0.3
            buildingDepth = randomFloat(0.6) + 0.3
            
            #depending on the height, different offsets are used for extruding faces to make windows
            if buildingHeight == 1:
                offset = 0.03
                zOffset = 0.03
            if buildingHeight == 2:
                offset = 0.02
                zOffset = 0.02
            if buildingHeight == 3:
                offset = 0.01 
                zOffset = 0.02
            
            #creates the building and gives it 5 subdivisions along each axis
            cmds.polyCube(w=buildingWidth, d=buildingDepth, h=buildingHeight, sx=5, sy=5, sz=5, n=buildingName)
            
            #the number of faces is found for the buildings
            #the for loop goes through all the faces, makes sure not to touch the faces
            #on the top and bottom of the buildings (which is why the if statements are weird)
            #once the right faces are checked, then it extrudes every second face of the building
            #a bit towards the center and then extrudes that face backwards
            faceCount = cmds.polyEvaluate(buildingName, face=True)
            for r in range(0, faceCount):
                faceName = buildingName + ".f[" + str(r) + "]"
                if (r >= 0 and r < 25) or (r > 49 and r <75) or (r > 99 and r < faceCount): 
                    print("Face: " + faceName)
                    if r%2 == 0:
                        cmds.polyExtrudeFacet(faceName, off=offset)
                        cmds.polyExtrudeFacet(faceName, ltz=zOffset*-1)
            
            #applies the colour chosen by the user
            myShader = cmds.shadingNode('lambert', asShader=True, name="buildingCol")
            cmds.setAttr(myShader+'.color', buildingColour[0], buildingColour[1], buildingColour[2], type='double3')
            cmds.select(buildingName)
            cmds.hyperShade(assign=myShader)
            
            #moves the buildings using the offsets
            cmds.move((j-1) + offsetJ, x=True)
            cmds.move((i-1) + offsetI + 0.5, z=True)
            cmds.move((buildingHeight/2.0)+0.1, y=True)


###############################City Light###################################
def createStreetLight(offsetI, offsetJ, blockNum, rotateVal):
    
    #grabs the colour the user chose
    rgb = cmds.colorSliderGrp('lightColour', q=True, rgbValue=True)
    
    #name for the street light
    global nextLightId
    lightName = blockNum + "Light" + str(nextLightId)
    nextLightId = nextLightId + 1
    
    #Create cylinder 1 base 
    LightSize = 1
    LightThickness = 50
    cmds.polyCylinder(name="Light", r=LightSize*0.3, h=LightThickness*0.1, sa = 10)
     

    #Create cylinder 2 light pole 
    cmds.polyCylinder(name="LightPole", r=LightSize*0.1, h=LightThickness/20, sa = 10)
    cmds.move(LightThickness - 48, y=True)
    cmds.move(LightThickness - 51.25, z=True)
    cmds.rotate(90, "LightPole", rotateX=True)
    
    #Create light lamp
    cmds.polySphere(name = "Lamp", r= 0.5)
    cmds.rotate(180, "Lamp", rotateX=True)
    cmds.move(LightThickness - 48.40, y=True)
    cmds.move(LightThickness - 52.25, z=True)

    #Poly Unite 
    cmds.polyUnite('Light', 'LightPole', 'Lamp', n=lightName)
    cmds.select(lightName)
    cmds.delete(ch=True)
    
    #selects the light and scales 
    cmds.select(lightName)
    cmds.scale(0.18, 0.18, 0.18)
    cmds.move(offsetI, moveZ=True)
    cmds.move(offsetJ, moveX=True)
    cmds.move(0.5, moveY=True)
    cmds.rotate(rotateVal, rotateY=True)
    
    #applies the colour the user chose
    myShader = cmds.shadingNode('lambert', asShader=True, name="LightColour")
    cmds.setAttr(myShader+".color",rgb[0],rgb[1],rgb[2], typ='double3')
    cmds.select(lightName)
    cmds.hyperShade(assign=myShader)
   
###############################City Bench###################################    
def createBench(offsetI, offsetJ, blocNum, rotateVal):
    
    #grabbing colour user
    rgb = cmds.colorSliderGrp('benchColour', q=True, rgbValue=True) 
    
    global nextBenchId
    benchName = blocNum + "Bench" + str(nextBenchId)
    nextBenchId = nextBenchId + 1
    
    #Create cylinder 1 
    BenchSize = 1
    BenchThickness = 10
    cmds.polyCylinder(name="BenchBase1", r=BenchSize*0.3, h=BenchThickness*0.1, sa = 50)

    #Create cylinder 2 
    cmds.polyCylinder(name="BenchBase2", r=BenchSize*0.3, h=BenchThickness*0.1, sa = 50)
    cmds.move(BenchThickness - 15, z=True)
   
    #Create cylinder 3 
    BenchBase3 = cmds.polyCylinder(name="BenchBase3", r=BenchSize*0.3, h=BenchThickness*0.1, sa = 50)
    cmds.move(BenchThickness - 15, z=True)
    cmds.move(BenchThickness - 12.5, x=True)
    
    #Create cylinder 4 
    BenchBase4 = cmds.polyCylinder(name="BenchBase4", r=BenchSize*0.3, h=BenchThickness*0.1, sa = 50)
    cmds.move(BenchThickness - 12.5, x=True)
    
    #Create Seat 
    cmds.polyCube(name="Seat", w=3, h=0.5, d=7)
    cmds.move(BenchThickness - 12.5, z=True)
    cmds.move(BenchThickness - 11.25, x=True)
    cmds.move(BenchThickness - 9.5, y=True)
    #Create Back Rest
    Back = cmds.polyCube(name="Back",w=2.25, h=0.5, d=7)
    cmds.move(BenchThickness - 12.5, z=True)
    cmds.move(BenchThickness - 12.70, x=True)
    cmds.move(BenchThickness - 8.25, y=True)
    cmds.rotate(100, Back, rotateZ=True)
    
    #Poly Unite 
    cmds.polyUnite( 'BenchBase1', 'BenchBase2', 'BenchBase3', 'BenchBase4', 'Seat', 'Back', n=benchName)
    cmds.select(benchName)
    cmds.delete(ch=True)
    
    #select the bench and scale it down then move to its position and rotate if needed
    cmds.select(benchName)
    cmds.scale(0.05, 0.05, 0.05)
    cmds.move(offsetI, moveZ=True)
    cmds.move(offsetJ, moveX=True)
    cmds.move(0.12, moveY=True)
    cmds.rotate(rotateVal, rotateY=True)
    
    myShader = cmds.shadingNode('lambert', asShader=True, name="benchColour")
    cmds.setAttr(myShader+".color",rgb[0],rgb[1],rgb[2], typ='double3')
    cmds.select(benchName)
    cmds.hyperShade(assign=myShader)


###############################City Street###################################        
def createStreet(offsetI, offsetJ, blockNum):
    
    #grab the colour the user chose 
    streetColour = cmds.colorSliderGrp('streetColour', q=True, rgbValue=True)
    
    #name for street
    global nextStreet
    streetName = blockNum + "Street" + str(nextStreet)
    nextStreet = nextStreet + 1
    
    #creates the plane that represents the street and moves it
    cmds.polyPlane(w=7, h=6, sx=1, sy=1, n=streetName)
    cmds.move(offsetI, moveZ=True)
    cmds.move(offsetJ, moveX=True)
    
    #applies the colour
    myShader = cmds.shadingNode('lambert', asShader=True, name="streetCol")
    cmds.setAttr(myShader+'.color', streetColour[0], streetColour[1], streetColour[2], type='double3')
    cmds.select(streetName)
    cmds.hyperShade(assign=myShader)

###############################City Yellow Lines###################################        
def createStreetLine(offsetI, offsetJ):
    
    #gets the colour for the stree lines
    lineColour = cmds.colorSliderGrp('lineColour', q=True, rgbValue=True)
    
    #name for the street lines
    global nextStreetLine
    streetLine = "StreetLine" + str(nextStreetLine)
    nextStreetLine = nextStreetLine + 1
    
    #draws four different planes as the street lines and moves them properly
    cmds.polyPlane(w=3.5, h=0.1, sx=1, sy=1, n="part1")
    cmds.move(offsetI-2, moveZ=True)
    cmds.move(offsetJ, moveX=True)
    
    cmds.polyPlane(w=3.5, h=0.1, sx=1, sy=1, n="part2")
    cmds.move(offsetI+2, moveZ=True)
    cmds.move(offsetJ, moveX=True)
    
    cmds.polyPlane(w=0.1, h=2.5, sx=1, sy=1, n="part3")
    cmds.move(offsetI, moveZ=True)
    cmds.move(offsetJ-2.5, moveX=True)
    
    cmds.polyPlane(w=0.1, h=2.5, sx=1, sy=1, n="part4")
    cmds.move(offsetI, moveZ=True)
    cmds.move(offsetJ+2.5, moveX=True)
    
    #unit all the stree lines together
    cmds.polyUnite('part1', 'part2', 'part3', 'part4', n=streetLine)
    cmds.select(streetLine)
    cmds.move(0.01, moveY=True)
    cmds.delete(ch=True)
    
    #apply the colour
    myShader = cmds.shadingNode('lambert', asShader=True, name="streetCol")
    cmds.setAttr(myShader+'.color', lineColour[0], lineColour[1], lineColour[2], type='double3')
    cmds.select(streetLine)
    cmds.hyperShade(assign=myShader)

###############################City Sidewalks###################################            
def createSidewalk(offsetI, offsetJ, blockNum):
    
    #grabbing the colour the user chose
    sidewalkColour = cmds.colorSliderGrp('sidewalkColour', q=True, rgbValue=True)
    
    #name for the sidewalk
    global nextSidewalk
    sidewalkName = blockNum + "Sidewalk" + str(nextSidewalk)
    nextSidewalk = nextSidewalk + 1
    
    #make the cube that will be deleted from the bigger cube to make the sidewalk
    cmds.polyCube(w=3, d=2, h=1, n='innerPart')
    cmds.move(offsetI, moveZ=True)
    cmds.move(offsetJ, moveX=True)
    
    #make the cube for the outer sidewalk and move it
    cmds.polyCube(w=3.5, d=2.5, h=0.1, sx=10, sz=8, n='sidewalk')
    cmds.move(offsetI, moveZ=True)
    cmds.move(offsetJ, moveX=True)
    cmds.move(0.1/2, moveY=True)
    
    #combine the geometry to make the final sidewalk
    cmds.polyBoolOp('sidewalk', 'innerPart', op=2, n=sidewalkName)
    cmds.select(sidewalkName)
    
    #delete the history after combining the geometry
    cmds.delete(ch=True)
    
    #apply the colour
    myShader = cmds.shadingNode('lambert', asShader=True, name="streetCol")
    cmds.setAttr(myShader+'.color', sidewalkColour[0], sidewalkColour[1], sidewalkColour[2], type='double3')
    cmds.select(sidewalkName)
    cmds.hyperShade(assign=myShader)

###############################City Garbage Cans###################################        
def createGarbageCan(offsetI, offsetJ, blocNum):
    
    #grabbing the colour the user selected
    rgb = cmds.colorSliderGrp('canColour', q=True, rgbValue=True)
    
    #name for the can
    global nextCanId
    canName = blocNum + "Can" + str(nextCanId)
    nextCanId = nextCanId + 1
    
    #defining the can dimensions
    CanSize = 1
    CanThickness = 7
    
    #create the cylinder for the can
    cmds.polyCylinder(n="Can", r=CanSize*0.3, h=CanThickness*0.1, sa = 50)
    
    #find the number of faces for the garbage can and extrude every second one
    FaceCount = cmds.polyEvaluate("Can", face=True)
    for i in range(0, FaceCount-2):
        FaceName = "Can" + ".f[" + str(i) + "]"
        
        if i % 2 ==0:
            cmds.polyExtrudeFacet(FaceName, ltz=((CanSize*0.1)/4))##EXTRUDE EVERY SECOND FACE
   
    #make a cylinder for the can hole
    cmds.polyCylinder(name="CanHole", r=CanSize*0.225, h=CanThickness/4, sa = 50)
    cmds.move(CanThickness - 6.75, y=True)
    cmds.polyBoolOp( "Can", "CanHole", op=2, n=canName) ## DIFFERENCE BOOLEAN
    cmds.select(canName)
    cmds.delete(ch=True)
    
    #scale the garbage can down and then move it
    cmds.scale(0.2, 0.2, 0.2)
    cmds.move(offsetI, moveZ=True)
    cmds.move(offsetJ, moveX=True)
    cmds.move(0.16, moveY=True)
    
    #apply the colour
    myShader = cmds.shadingNode('lambert', asShader=True, name="CanColour")
    cmds.setAttr(myShader+'.color', rgb[0], rgb[1], rgb[2], type='double3')
    cmds.select(canName)
    cmds.hyperShade(assign=myShader)
    
#https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/
#This website helped with greating the interger random number generator
def randomInt(maximum):
    randomNum = random.randint(0, maximum)
    
    return randomNum

#https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range
#This website helped with creating ther float interger number generator
def randomFloat(maximum):
    randomNum = random.uniform(0, maximum)
    
    return randomNum