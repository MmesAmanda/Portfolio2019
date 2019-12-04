import maya.cmds as cmds
import math 

PtOrigin=[0, 0, 0]
ZV = 0.000000000000000000001
def findIntersect(): 
  
    selectedList = cmds.ls(selection=True)                     

   
    if len(selectedList) < 2:
        print ("Not enough objects selected. PLease select 2 objects")
        return False
    elif len(selectedList) > 2:
        print ("Too many objects. 2 will be used")
        selectedList = selectedList[0:2]
    
    Selection1 = selectedList[0]       
    Selection2 = selectedList[1]
    
    PtLine = []
    
    PtLine = NumVTX(Selection1)  
    Facet(Selection2, PtLine)   
    
    
    
    cmds.textScrollList('uiPointList', edit=True, append=[ptText])
 
def NumVTX(object):
    vtxAmount = cmds.polyEvaluate(object, vertex=True)
    meshTransform = cmds.xform(object, query=True, matrix=True, worldSpace=True)
    
    PtList = []
    
    for vtxIndex in range(0,vtxAmount):
            vtxName = object + ".vt[" + str(vtxIndex) + "]"
            PtA = cmds.getAttr(vtxName)
            PtA = list(PtA[0]) 
            PtA= matrixMult(meshTransform, PtA)
            
            PtList.append(PtA)
   
            #Line Seg Drawing
            cmds.curve( p=[(PtA[0],PtA[1],PtA[2]), PtOrigin])
            print (vtxName, "position is", PtA) 
            
    return PtList
            
            
            
def CrossProd(VecAB, VecAC):
     nrmVec = [0.0,0.0,0.0]
     nrmVec[0] = (VecAB[1] * VecAC[2]) - (VecAB[2] * VecAC[1])
     nrmVec[1] = (VecAB[2] * VecAC[0]) - (VecAB[0] * VecAC[2])
     nrmVec[2] = (VecAB[0] * VecAC[1]) - (VecAB[1] * VecAC[0])
     
     nrmMagnitude=Magnitude(nrmVec)
     
     nrmVec[0] = nrmVec[0] / nrmMagnitude;
     nrmVec[1] = nrmVec[1] / nrmMagnitude;
     nrmVec[2] = nrmVec[2] / nrmMagnitude;

     return nrmVec

def DotProd(Vec1, Vec2):
    result = (Vec1[0] * Vec2[0]) + (Vec1[1] * Vec2[1]) + (Vec1[2] * Vec2[2])
    
    return result 
        
    
def Magnitude(nrmVec):
    nrmMagnitude = ((nrmVec[0] ** 2) + (nrmVec[1] ** 2) + (nrmVec[2] ** 2)) ** 0.5 
    
    return nrmMagnitude
    
def NormalVec(VTXA, VTXB, VTXC):
     VecAB = [0,0,0]
     VecAC = [0,0,0]
     
     VecAB[0] = VTXB[0] - VTXA[0]
     VecAB[1] = VTXB[1] - VTXA[1]
     VecAB[2] = VTXB[2] - VTXA[2]
     
     VecAC[0] = VTXC[0] - VTXA[0]
     VecAC[1] = VTXC[1] - VTXA[1]
     VecAC[2] = VTXC[2] - VTXA[2]
     
    
     
     nrmVec = CrossProd(VecAB, VecAC)#
     PlaneEquValues = PlaneEqu(nrmVec, VTXA)#
     
    
     return PlaneEquValues
     

def TValue(PlaneVals, Pt1, Pt2): 
   Denominator = 0.0
   Nominator = 0.0
   
   Nominator = (PlaneVals[0]*Pt1[0]) + (PlaneVals[1]*Pt1[1]) + (PlaneVals[2]*Pt1[2]) + (PlaneVals[3])
   Denominator = (PlaneVals[0]*(Pt1[0]-Pt2[0])) + (PlaneVals[1]*(Pt1[1]-Pt2[1])) +(PlaneVals[2]*(Pt1[2]-Pt2[2]))
    
  
   if(abs(Denominator) < ZV):
     print ("Denominator is Zero")
     return False

   
   tValue = Nominator/Denominator
   
   return tValue

    
def Facet(object, PlanePts):
    facetCnt = cmds.polyEvaluate(object, face=True)
    meshTransform = cmds.xform(object, query=True, matrix=True, worldSpace=True)
    
    for face in range(0, facetCnt):
        fName = object + ".f[" + str(face) + "]"
        VTXLst = cmds.polyInfo(fName, faceToVertex=True)
        VTXIdx = str(VTXLst[0]).split()
        VTXIdx = VTXIdx[2:]
        
        VTXA = cmds.getAttr(object + ".vt[" + VTXIdx[0] + "]")
        VTXB = cmds.getAttr(object + ".vt[" + VTXIdx[1] + "]")
        VTXC = cmds.getAttr(object + ".vt[" + VTXIdx[2] + "]")
        VTXD = cmds.getAttr(object + ".vt[" + VTXIdx[3] + "]")
           
        VTXA = list(VTXA[0])
        VTXB = list(VTXB[0])
        VTXC = list(VTXC[0])
        VTXD = list(VTXD[0])
        
        VTXA = matrixMult(meshTransform, VTXA)
        VTXB = matrixMult(meshTransform, VTXB)
        VTXC = matrixMult(meshTransform, VTXC)
        VTXD = matrixMult(meshTransform, VTXD)
        
        planeEQ = NormalVec(VTXA, VTXB, VTXC)
        
        
        for j in range (0, len(PlanePts)):
            
            PP = PlanePts[j]
            PPx = PP[0]
            PPy = PP[1]
            PPz = PP[2]
            pI = [0.0, 0.0, 0.0]

            kValueA = (planeEQ[0] * PPx)+(planeEQ[1] * PPy)+(planeEQ[2] * PPz) + planeEQ[3]
            kValueB = (planeEQ[0] * PtOrigin[0]) + (planeEQ[1] * PtOrigin[1]) + (planeEQ[2] * PtOrigin[2]) + planeEQ[3]

            if(((kValueA>=0.0) and (kValueB>=0.0)) or ((kValueA<=0.0) and (kValueB<=0.0))):
                continue
            
            
            tValue = TValue(planeEQ, PlanePts[j], PtOrigin)
            
            
            if tValue == False:
                continue
                
            PtInterset = [0.0, 0.0, 0.0] 
            PtInterset[0] = PlanePts[j][0] + (tValue * (PtOrigin[0] - PlanePts[j][0])) 
            PtInterset[1] = PlanePts[j][1] + (tValue * (PtOrigin[1] - PlanePts[j][1])) 
            PtInterset[2] = PlanePts[j][2] + (tValue * (PtOrigin[2] - PlanePts[j][2]))
            
                 
             
            Q = findTriangle(VTXA, VTXB, VTXC, PtInterset)
            R = findTriangle(VTXA, VTXD, VTXC, PtInterset)
            
            PointCounter = 0
            
            # print COOB
            if Q == False:
                if R==True:
                    cmds.polyCube(width=0.1, height=0.1, depth=0.1)
                    cmds.move(PtInterset[0], PtInterset[1], PtInterset[2])
                    PointCounter += 1
                    
            elif Q == True:
               cmds.polyCube(width=0.1, height=0.1, depth=0.1)
               cmds.move(PtInterset[0], PtInterset[1], PtInterset[2])
                
            
        
        
           
        print ("Vertex A:", VTXA)
        print ("Vertex B:", VTXB)
        print ("Vertex C:", VTXC)
        
        
        
        ####
        area = FaceArea(VTXA, VTXB, VTXC)
        nrmVec = NormalVec(VTXA, VTXB, VTXC)
        DistToPlane = DistanceToPlane(ValueA, ValueB, ValueC, ValueD, Pt1)
        theta = VecAngle(nrmVec, LineVec)
        ####
        
        
        ptText = "[" + str(PointCounter) + " Pnt(x,y,z): " + str(round(PtInterset[0],2)) + str(round(PtInterset[1],2)) + str(round(PtInterset[2],2))
        ptText1 += ";Area: " + str(round(area,2))
        ptText2 += "; NV: " + str(nrmVec[0]) + ", " + str(nrmVec[1]) + ", " + str(nrmVec[2])
        ptText3 += "; Distance:" + str(round(DistToPlane,2))
        ptText4 +="; Angle:" + atr(round(theta, 2)) + "rads"
       
        ptTextFinal = str (ptText) + str (ptText1) + str (ptText2) + str (ptText3) + str (ptText4)
        cmds.textScrollList('uiPointList', edit=True, append=[ptTextFinal])
           

def matrixMult(MTX, Pt): 
    PointOut = [0.0, 0.0, 0.0, 0.0]
    PointIn = [Pt[0], Pt[1], Pt[2], 1]    
    PointOut[0] =(MTX[0]*PointIn[0])+(MTX[4]*PointIn[1])+(MTX[8]*PointIn[2])+(MTX[12]*PointIn[3])
    PointOut[1] =(MTX[1]*PointIn[0])+(MTX[5]*PointIn[1])+(MTX[9]*PointIn[2])+(MTX[13]*PointIn[3])
    PointOut[2] =(MTX[2]*PointIn[0])+(MTX[6]*PointIn[1])+(MTX[10]*PointIn[2])+(MTX[14]*PointIn[3])
    PointOut[3] =(MTX[3]*PointIn[0])+(MTX[7]*PointIn[1])+(MTX[11]*PointIn[2])+(MTX[15]*PointIn[3])
    
    return(PointOut)
    
def PlaneEqu(nrmVec, VTXA):
    
    PlaneEquValues = [0.0, 0.0, 0.0, 0.0] 
    
    ValueA = nrmVec[0]
    ValueB = nrmVec[1]
    ValueC = nrmVec[2]
    ValueD = ValueA * VTXA[0] + ValueB * VTXA[1] + ValueC * VTXA[2]
    ValueD = ValueD * -1
    
    PlaneEquValues = [ValueA , ValueB, ValueC, ValueD]
    
     # Check if they are colinear
    if((abs(PlaneEquValues[0]) < ZV) and (abs(PlaneEquValues[1]) < ZV) and (abs(PlaneEquValues[2]) < ZV)):
        print("Error Points are Colinear")
        return False
    
    return PlaneEquValues 
   
    
def DistanceToPlane(ValueA, ValueB, ValueC, ValueD, Pt1):
    Nom = 0.0
    Den = 0.0
    
    Nom = ((ValueA*Pt1[0]) + (ValueB*Pt1[1]) + (ValueC*Pt1[2]) + (ValueD))
    Den = ((ValueA**2) + (ValueB**2) + (ValueC**2))** 0.5
    DistToPlane = Nom/Den
    
    return DistToPlane
     
def VecAngle(nrmVec, LineVec):
    DotProduct = DotProd(nrmVec, LineVec)
    nrmMag = Magnitude(nrmVec)
    LineMag = Magnitude(lineVec)
    
    theta = math.acos(DotProd /(nrmMag * LineMag))
    
    return theta
    
def FaceArea(pt1, pt2, pt3):
    Vec1 = MakeVec (pt1, pt2)
    Vec2 = MakeVec (pt3, pt2)
    CrossProduct = CrossProd(Vec1, Vec2)
    area = Magnitude (CrossProd)
    area = area * 2   
    
    return area
    
def MakeVec (pt1, pt2): ##
     vec = [0.0, 0.0, 0.0]##
     vec[0] = pt2[0]- pt1[0]##
     vec[1] = pt2[1]- pt1[1]##
     vec[2] = pt2[2]- pt1[2]##
         
def initializeVector(pA, pB):
    VecAB = [0,0,0]
    VecAB[0] = pB[0] - pA[0]
    VecAB[1] = pB[1] - pA[1]
    VecAB[2] = pB[2] - pA[2]
    return VecAB

def findTriangle(VTXA, VTXB,VTXC,p):

    VecBA = initializeVector(VTXB,VTXA)
    VecCA = initializeVector(VTXC,VTXA)
    VecPA = initializeVector(p,VTXA)

    dotBABA = DotProd(VecBA, VecBA)
    dotBACA = DotProd(VecBA, VecCA)
    dotBAPA = DotProd(VecBA, VecPA)
    dotCACA = DotProd(VecCA, VecCA)
    dotCAPA = DotProd(VecCA, VecPA)

    revDenominator = 1 / (dotBABA * dotCACA - dotBACA * dotBACA)
    u = (dotCACA * dotBAPA - dotBACA * dotCAPA) * revDenominator
    v = (dotBABA * dotCAPA - dotBACA * dotBAPA) * revDenominator

    if (u >= 0) and (v >= 0) and (u + v < 1):
        return True
    else:
        return False


if 'MyUI' in globals():
    if cmds.window(MyUI, exists=True):
        cmds.deleteUI(MyUI, window=True)
MyUI = cmds.window(title='My UI', menuBar=True, widthHeight=(500,300))

cmds.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=500)
cmds.button( label='Find Intersection', command='findIntersect()', width=(500))
cmds.setParent("..")

cmds.paneLayout()
cmds.textScrollList('uiPointList', numberOfRows=8, allowMultiSelection=False)


cmds.showWindow(MyUI)