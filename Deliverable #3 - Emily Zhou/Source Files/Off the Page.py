from Tkinter import *
from PIL import Image, ImageTk
import cv2
import cv
import numpy as np
import time
import math
#for images2gif, see citation at makeWalkGIF
from images2gif import writeGif
import os

def keyPressed(canvas,event):
    if canvas.charPage:
        if event.keysym == "u":
            canvas.charCoord.pop()
        elif (event.keysym == "Return" and 
            len(canvas.charCoord) == 2):
            canvas.charPage = False
            canvas.legPage = True
    elif canvas.legPage:
        if event.keysym == "u":
            canvas.legCoord.pop()
        elif (event.keysym == "Return" and 
            len(canvas.legCoord) == 2):
            canvas.legPage = False
            canvas.legWidthPage = True
    elif canvas.legWidthPage:
        if event.keysym ==  "u":
            canvas.legWidthCoord.pop()
        elif (event.keysym == "Return" and 
            len(canvas.legWidthCoord) == 2):
            canvas.legWidthPage = False
            canvas.bodyPage = True
    elif canvas.bodyPage:
        if event.keysym ==  "u":
            canvas.bodyCoord.pop()
        elif (event.keysym == "Return" and 
            len(canvas.bodyCoord) == 2):
            canvas.bodyPage = False
            canvas.coordPage = True
            canvas.noCoordErr = False
    elif canvas.interactPage:
        if event.keysym == "Right" and canvas.jumping == False: 
            canvas.dancing = False
            canvas.bobbing = False
            canvas.jumping = False
            canvas.sitting = False
            if canvas.turned == True:
                #make character stay in same spot despite flip in image
                canvas.x = canvas.x + abs(canvas.rightBound - canvas.leftBound)
            canvas.walking = True
            canvas.turned = False
            canvas.dw = abs(canvas.dw)
        elif event.keysym == "Left" and canvas.jumping == False: 
            canvas.dancing = False
            canvas.bobbing = False
            canvas.jumping = False
            canvas.sitting = False
            if canvas.turned == False: 
                canvas.x = canvas.x -abs(canvas.rightBound - canvas.leftBound)
            canvas.walking = True
            canvas.turned = True
            canvas.dw = -abs(canvas.dw)
        elif (event.keysym == "Down" and canvas.sitting == False 
            and canvas.jumping == False): 
            canvas.dancing = False
            canvas.bobbing = False
            canvas.sitting = True
            canvas.walking = False
            sit(canvas)
        elif event.keysym == "Up" and canvas.jumping == False: 
            canvas.dancing = False
            canvas.bobbing = False
            canvas.sitting = False
            canvas.walking = False
            canvas.jumping = True
            canvas.jumpbend = True
            makeJumpFrames(canvas)
        elif (event.keysym == "d" and canvas.jumping == False 
            and canvas.sitting == False and canvas.dancing == False):
            canvas.bobbing = False
            canvas.walking = False
            canvas.dancing = True
            if canvas.turned:
                canvas.x = canvas.x + abs(canvas.rightBound - canvas.leftBound)
        elif (event.keysym == "b" and canvas.jumping == False 
            and canvas.sitting == False and canvas.bobbing == False):
            canvas.dancing = False
            canvas.walking = False
            canvas.bobbing = True
    redrawAll(canvas)  

def makeJumpFrames(canvas):
    im = canvas.data["character"].convert("RGBA")
    veryBentLeg = canvas.data["very bent leg"].convert("RGBA")

    (x1,y1) = canvas.legCoord[0]
    (x2,y2) = canvas.legCoord[1]
    (vbentw,vbenth) = veryBentLeg.size
    legWidth = canvas.legWidthCoord[1][0] - canvas.legWidthCoord[0][0]
    bodyLeft = canvas.bodyCoord[0][0]
    bodyRight = canvas.bodyCoord[1][0]
    bodyCenter = int(round((bodyRight+bodyLeft)/2))
    bodyLength = bodyRight-bodyLeft

    #make bending legs frame
    coord1ToPasteVeryBentLeg = (bodyCenter - vbentw/2-bodyLength/6,y1-10)               
    im.paste(veryBentLeg,coord1ToPasteVeryBentLeg,mask=veryBentLeg)
    coord2ToPasteVeryBentLeg = (bodyCenter - vbentw/2-bodyLength/6 + 
        legWidth,y1-10)                                  
    im.paste(veryBentLeg,coord2ToPasteVeryBentLeg,mask=veryBentLeg)
    im.save("jumpBend.jpg")

    jumpBendIm = Image.open("jumpBend.jpg")
    jumpBend = ImageTk.PhotoImage(jumpBendIm)
    canvas.data["jump bend"] = jumpBend 
    reverseJumpBend = jumpBendIm.transpose(Image.FLIP_LEFT_RIGHT)
    reverseJumpBend.save("reverseJumpBend.jpg")
    photoRJB = Image.open("reverseJumpBend.jpg")
    frameRJB = ImageTk.PhotoImage(photoRJB)
    canvas.data["reverse jump bend"] = frameRJB

    #make jump frame (legs straight)
    im = canvas.data["character"].convert("RGBA")
    leg = canvas.data["leg"].convert("RGBA")
    (legw,legh) = leg.size

    leg = leg.rotate(330, expand = 1)
    legTransparent = makeBackgroundTransparent(canvas,leg)
    (legw,legh) = leg.size

    theta = (2*math.pi)*30/360
    (dx,dy) = findDxDy(canvas,theta)

    coord1ToPasteLeg = (bodyCenter - dx - bodyLength/6,y1-(
        canvas.legLength-dy)/4)                                                   
    im.paste(legTransparent,coord1ToPasteLeg,mask=legTransparent)
    coord2ToPasteLeg = (bodyCenter - dx - bodyLength/6+legWidth,y1-(
        canvas.legLength-dy)/4)                                                   
    im.paste(legTransparent,coord2ToPasteLeg,mask=legTransparent)                                   
    im.save("jumpExtend.jpg")

    jumpExtendIm = Image.open("jumpExtend.jpg")
    jumpExtend = ImageTk.PhotoImage(jumpExtendIm)
    canvas.data["jump extend"] = jumpExtend  
    reverseJump = jumpExtendIm.transpose(Image.FLIP_LEFT_RIGHT)
    reverseJump.save("reverseJump.jpg")
    photoRJ = Image.open("reverseJump.jpg")
    frameRJ = ImageTk.PhotoImage(photoRJ)
    canvas.data["reverse jump"] = frameRJ

#helper function to find changes in x y coords after rotations
def findDxDy(canvas,theta): 
    dx = int(round(canvas.halfLegLength*math.sin(theta)))
    dy = int(round(canvas.halfLegLength*math.cos(theta)))
    return (dx,dy)

def sit(canvas):
    sitPhoto = Image.open("sitImage.jpg")
    sitImage = ImageTk.PhotoImage(sitPhoto)
    canvas.data["sit image"] = sitImage

    sitReverse = sitPhoto.transpose(Image.FLIP_LEFT_RIGHT)
    sitReverse.save("sitReverse.jpg")
    sitReverseIm = Image.open("sitReverse.jpg")
    sitReverse = ImageTk.PhotoImage(sitReverseIm)
    canvas.data["sit reverse"] = sitReverse

#helper function for sit
def removeLegs(canvas):
    im = Image.open("houghlinesnew.jpg")
    (x1,y1) = canvas.legCoord[0]
    (x2,y2) = canvas.legCoord[1]
    getRidOfArea(canvas,im,(x1,y1,x2,y2))
    im.save("sitImage.jpg")

#switches frames for constant walking
def changeFrames(canvas):
    if canvas.index == 3:
        canvas.index = 0
    else:
        canvas.index += 1

#switches frames when bobbing enabled
def changeDanceBobFrames(canvas):
    if canvas.danceBobIndex == 1:
        canvas.danceBobIndex = 0
    else:
        canvas.danceBobIndex = 1

#changes x coord for walking
def moveImage(canvas):
    canvas.x += canvas.dw
    if (canvas.x < 0 - canvas.rightBound): 
        canvas.turned = False
        canvas.dw = -canvas.dw
        canvas.x = 0 - canvas.rightBound
    elif (canvas.x > canvas.width - canvas.frameWidth + canvas.rightBound):
        canvas.turned = True
        canvas.dw = -canvas.dw
        canvas.x = canvas.width - canvas.frameWidth + canvas.rightBound 

def mousePressed(canvas,event):
    if ((canvas.charPage and len(canvas.charCoord) < 2) or 
        (canvas.legPage and len(canvas.legCoord) < 2) or 
        (canvas.legWidthPage and len(canvas.legWidthCoord) < 2) or
        (canvas.bodyPage and len(canvas.bodyCoord) < 2)):
        if (event.x > canvas.width/6 and event.x < canvas.width and 
            event.y > canvas.height/5 and event.y < canvas.height):
            if canvas.charPage:
                canvas.charCoord.append((event.x-canvas.width/6,
                event.y-canvas.height/5))
            elif canvas.legPage:
                canvas.legCoord.append((event.x-canvas.width/6,
                event.y-canvas.height/5))
            elif canvas.legWidthPage:
                canvas.legWidthCoord.append((event.x-canvas.width/6,
                event.y-canvas.height/5))
            else:
                canvas.bodyCoord.append((event.x-canvas.width/6,
                event.y-canvas.height/5))
        else:
            print "Not a valid coordinate!"
    redrawAll(canvas)

def timerFired(canvas):
    canvas.time += 1
    if canvas.interactPage and canvas.noCoordErr == False:
        if canvas.walking:
            if canvas.time%2 == 0:
                changeFrames(canvas)
                moveImage(canvas)
                redrawAll(canvas)
        elif canvas.jumping:
            redrawAll(canvas)
            canvas.jumpbend = False
            canvas.jumpextend = True
            if canvas.jumpextend:
                if canvas.land == False:
                    canvas.jumpY += 300
                    canvas.land = True
                elif canvas.land:
                    canvas.jumpY -= 300
                    canvas.land = False
                    canvas.jumpextend = False
                    canvas.jumping = False
                    canvas.walking = True
            redrawAll(canvas)
        elif ((canvas.dancing or canvas.bobbing) and canvas.time%2 == 0):
            changeDanceBobFrames(canvas)
            redrawAll(canvas)
    elif canvas.makeCharWalkPage and canvas.walking:
        if canvas.time%2 == 0:
            changeFrames(canvas)
            redrawAll(canvas)
    elif canvas.makeCharDancePage or canvas.makeCharBobPage:
        if ((canvas.dancing or canvas.bobbing) and canvas.time%2 == 0):
            changeDanceBobFrames(canvas)
            redrawAll(canvas)
    delay = 100 # milliseconds
    def f():
        timerFired(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

def redrawAll(canvas):
    canvas.delete(ALL)
    if canvas.scanDrawingPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        example = Image.open("example.jpg")
        example = ImageTk.PhotoImage(example)
        canvas.data["example"] = example
        canvas.create_image(canvas.width/6,canvas.height/3 + 100, 
            image=canvas.data["example"])
        canvas.create_text(canvas.width/2,canvas.height/8,text = "SCAN DRAWING"
            ,font = "Chalkboard 80 bold", fill = "LightSeaGreen")
        canvas.create_text(canvas.width/2,canvas.height/2 - 40,text = 
            """ 
            Instructions: 
               1) Draw a character on a white sheet of paper with a 
                  dark marker/pen. It must face the RIGHT and have
                  only ONE leg (see example on the left)
               2) Hold drawing in front of the camera (character in the center)
               3)             to scan drawing (avoid shaking)
               4)             to enable edge detection
               5)                   to accept scanned drawing

            Press 'ESCAPE' to close camera or try again
            """, fill = "aquamarine", font = "Chalkboard 30 bold")
        canvas.create_text(canvas.width/3,canvas.height/2 - 20,
            text = "PRESS 'S'",fill = "misty rose", 
            font = "Chalkboard 30 bold")
        canvas.create_text(canvas.width/3,canvas.height/2 + 20,
            text = "PRESS 'E'",fill = "misty rose", 
            font = "Chalkboard 30 bold")
        canvas.create_text(canvas.width/3 + 38,canvas.height/2 + 57,
            text = "PRESS 'ENTER'",fill = "misty rose", 
            font = "Chalkboard 30 bold")
        canvas.create_text(canvas.width/2 - 60,2*canvas.height/3,text = 
"""Note: paper edges/other objects accidentally captured will be removed later""",
           fill = "aquamarine", font = "Chalkboard 20 italic")

        b4 = canvas.data["button4"]
        canvas.create_window(canvas.width/2, 5*canvas.height/6, window=b4)
        b10 = canvas.data["button10"]
        canvas.create_window(canvas.height/15, 7*canvas.height/8, window=b10)
    elif canvas.animatePage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b10 = canvas.data["button10"]
        canvas.create_window(canvas.height/15, 7*canvas.height/8, window=b10)
        if canvas.noScannedImageErr:
            canvas.create_text(canvas.width/2,canvas.height/3,text = 
                "You have not scanned a drawing yet!", 
                fill = "HotPink", font= "Chalkboard 70 bold")
            noScannedImageErr = False
        else:
            canvas.create_text(canvas.width/2,canvas.height/4,text = 
                """   First set up your coordinates. 
Then, choose an animation method!""", 
                fill = "LightSeaGreen", font = "Chalkboard 70 bold")
            b2 = canvas.data["button2"]
            canvas.create_window(canvas.width/2,canvas.height/2-80, window=b2)
            b7 = canvas.data["button7"]
            canvas.create_window(canvas.width/2,canvas.height/2+20, window=b7)
            b8 = canvas.data["button8"]
            canvas.create_window(canvas.width/2,canvas.height/2+80, window=b8)
            b9 = canvas.data["button9"]
            canvas.create_window(canvas.width/2,canvas.height/2+140, window=b9)
            b6 = canvas.data["button6"]
            canvas.create_window(canvas.width/2,canvas.height/2+240, window=b6)
    elif canvas.charPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        canvas.create_text(canvas.width/2,canvas.height/10, 
            text = "CHOOSE CHARACTER COORDINATES", fill = "LightSeaGreen", font = 
            "Chalkboard 80 bold")
        image = canvas.data["image"]
        imageSize = ( (image.width(), image.height()) )
        canvas.create_image(canvas.width/6, canvas.height/5, anchor = NW, 
            image=image)
        drawCoordInstruct(canvas,3)
        showChosenCoord(canvas,3)
    elif canvas.legPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        canvas.create_text(canvas.width/2,canvas.height/10, 
            text = "CHOOSE LEG COORDINATES", fill = "LightSeaGreen", font = 
            "Chalkboard 80 bold")
        image = canvas.data["image"]
        imageSize = ( (image.width(), image.height()) )
        canvas.create_image(canvas.width/6, canvas.height/5, anchor = NW, 
            image=image)
        drawCoordInstruct(canvas,0)
        showChosenCoord(canvas,0)
    elif canvas.legWidthPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        canvas.create_text(canvas.width/2,canvas.height/10, 
                text = "CHOOSE LEG WIDTH COORDINATES", fill = "LightSeaGreen", 
                font = "Chalkboard 80 bold")
        image = canvas.data["image"]
        imageSize = ( (image.width(), image.height()) )
        canvas.create_image(canvas.width/6, canvas.height/5, anchor = NW, 
            image=image)
        drawCoordInstruct(canvas,1)
        showChosenCoord(canvas,1)
    elif canvas.bodyPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        canvas.create_text(canvas.width/2,canvas.height/10, 
                text = "CHOOSE BODY COORDINATES", fill = "LightSeaGreen", 
                font = "Chalkboard 80 bold")
        image = canvas.data["image"]
        imageSize = ( (image.width(), image.height()) )
        canvas.create_image(canvas.width/6, canvas.height/5, anchor = NW, 
            image=image)
        drawCoordInstruct(canvas,2)
        showChosenCoord(canvas,2)
    elif canvas.coordPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        canvas.create_text(canvas.width/2,canvas.height/3, text = """
                Your coordinates have been stored. 
  Return to the Animation menu and test out your character! """, 
            fill = "LightSeaGreen",font = "Chalkboard 50 bold")
    elif canvas.makeCharDancePage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        if canvas.noCoordErr:
            canvas.create_text(canvas.width/2,canvas.height/3,text = 
                "You have not set up coordinates yet!", 
                fill = "HotPink", font= "Chalkboard 70 bold")
            canvas.noCoordErr = False
        else:
            canvas.create_text(canvas.width/2-100,canvas.height/8, 
                text = """
                Your dancing animation has been created! Open your working
                directory to find the file named "dancing_animation.gif".

                Note: remember to copy the file and save it somewhere else 
                before creating a new dancing animation!
                """, fill = "medium slate blue",font = "Chalkboard 30 bold")
            canvas.create_image(200, canvas.height/4, anchor = NW, 
                        image=canvas.danceFrames[canvas.danceBobIndex]) 
    elif canvas.makeCharBobPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        if canvas.noCoordErr:
            canvas.create_text(canvas.width/2,canvas.height/3,text = 
                "You have not set up coordinates yet!", 
                fill = "HotPink", font= "Chalkboard 70 bold")
            canvas.noCoordImageErr = False
        else:
            canvas.create_text(canvas.width/2-100,canvas.height/8, 
                text = """
                Your bobbing animation has been created! Open your working
                directory to find the file named "bobbing_animation.gif".

                Note: remember to copy the file and save it somewhere else 
                before creating a new bobbing animation!
                """, fill = "medium slate blue",font = "Chalkboard 30 bold")
            canvas.create_image(200, canvas.height/4, anchor = NW, 
                        image=canvas.bobFrames[canvas.danceBobIndex]) 
    elif canvas.interactPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        if canvas.noCoordErr:
            canvas.create_text(canvas.width/2,canvas.height/3,text =
                "You have not set up coordinates yet!", 
                fill = "HotPink", font= "Chalkboard 70 bold")
            canvas.noCoordImageErr = False
        else:
            canvas.create_text(canvas.width/5,9*canvas.height/10, 
                text = """
                Left Arrow Key: move left    Right Arrow Key: move right
                """, font = "Chalkboard 20", fill = "white")
            canvas.create_text(canvas.width/2 + 60,9*canvas.height/10, 
                text = """
                Up Arrow Key: jump    Down Arrow Key: sit
                """, font = "Chalkboard 20", fill = "white")
            canvas.create_text(4*canvas.width/5,9*canvas.height/10, 
                text = """
                "d" Key: dance    "b" Key: bob
                """, font = "Chalkboard 20", fill = "white")
            if canvas.walking:
                if canvas.turned == True:
                    canvas.create_image(canvas.x, 0, anchor = NW, 
                        image=canvas.reversedFrames[canvas.index])  
                else:
                    canvas.create_image(canvas.x, 0, anchor = NW, 
                        image=canvas.frames[canvas.index])    
            elif canvas.sitting:
                if canvas.turned == False:
                    canvas.create_image(canvas.x, canvas.legLength, anchor=NW, 
                        image=canvas.data["sit image"])    
                else:
                    canvas.create_image(canvas.x, canvas.legLength, anchor=NW, 
                        image=canvas.data["sit reverse"])  
            elif canvas.jumping:
                if canvas.jumpbend and canvas.turned == False:
                    canvas.create_image(canvas.x, canvas.legLength, anchor=NW, 
                        image=canvas.data["jump bend"]) 
                elif canvas.jumpbend and canvas.turned:
                    canvas.create_image(canvas.x, canvas.legLength, anchor=NW, 
                        image=canvas.data["reverse jump bend"]) 
                elif canvas.jumpextend and canvas.turned == False:
                    canvas.create_image(canvas.x, canvas.legLength - 
                        canvas.jumpY, anchor = NW, 
                        image=canvas.data["jump extend"])  
                elif canvas.jumpextend and canvas.turned:
                    canvas.create_image(canvas.x, canvas.legLength - 
                        canvas.jumpY, anchor = NW, 
                        image=canvas.data["reverse jump"])
            elif canvas.dancing:
                canvas.create_image(canvas.x, 0, anchor = NW, 
                        image=canvas.danceFrames[canvas.danceBobIndex])     
            elif canvas.bobbing:
                if canvas.turned == False:
                    canvas.create_image(canvas.x, 0, anchor = NW, 
                        image=canvas.bobFrames[canvas.danceBobIndex]) 
                else:
                    canvas.create_image(canvas.x, 0, anchor = NW, 
                        image=canvas.bobReverseFrames[canvas.danceBobIndex])           
    elif canvas.makeCharWalkPage:
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        b11 = canvas.data["button11"]
        canvas.create_window(canvas.height/22, 8*canvas.height/9, window=b11)
        if canvas.noCoordErr:
            canvas.create_text(canvas.width/2,canvas.height/3,text = 
                "You have not set up coordinates yet!", 
                fill = "HotPink", font= "Chalkboard 70 bold")
            canvas.noCoordImageErr = False
        else:
            canvas.create_text(canvas.width/2-100,canvas.height/8, 
                text = """
                Your walking animation has been created! Open your working
                directory to find the file named "walking_animation.gif".

                Note: remember to copy the file and save it somewhere else 
                before creating a new walking animation!
                """, fill = "medium slate blue",font = "Chalkboard 30 bold")
            canvas.create_image(200, canvas.height/4, anchor = NW, 
                        image=canvas.frames[canvas.index])  
    else:
        #main menu/home
        if canvas.failedAnimate:
            canvas.noScannedImageErr = False
            canvas.failedAnimate = False
        canvas.create_rectangle(0,0,canvas.width,canvas.height,fill="black")
        drawTitle(canvas)
        b1 = canvas.data["button1"]
        canvas.create_window(canvas.width/2, canvas.height/2+150, window=b1)
        b5 = canvas.data["button5"]
        canvas.create_window(canvas.width/2, canvas.height/2+210, window=b5)
        b3 = canvas.data["button3"]
        canvas.create_window(canvas.width/2, canvas.height/2+270, window=b3)

#following frames are for walking
def makeFrame1(canvas):
    im = canvas.data["character"].convert("RGBA")
    leg = canvas.data["leg"].convert("RGBA")
    bentLeg = canvas.data["bent leg"].convert("RGBA")

    #prepare both leg shapes
    (x1,y1) = canvas.legCoord[0]
    (x2,y2) = canvas.legCoord[1]
    (bentw,benth) = bentLeg.size
    canvas.bodyLeft = canvas.bodyCoord[0][0]
    canvas.bodyRight = canvas.bodyCoord[1][0]
    bentLeg = bentLeg.rotate(330, expand = 1)
    (newbentw,newbenth) = bentLeg.size

    canvas.bodyCenter = int(round((canvas.bodyRight+canvas.bodyLeft)/2))
    canvas.bodyLength = canvas.bodyRight-canvas.bodyLeft

    theta = (2*math.pi)*30/360
    (dx,dy) = findDxDy(canvas,theta)

    #must make images transparent (shouldnt block other parts of image)
    bentLegTransparent = makeBackgroundTransparent(canvas,bentLeg)
                                     
    coordToPasteBentLeg = (canvas.bodyCenter-newbentw/2-dx-
        canvas.bodyLength/6,y1-(newbenth/2-dy))
    im.paste(bentLegTransparent,coordToPasteBentLeg,mask=bentLegTransparent)
    leg = leg.rotate(30, expand = 1)
    (legw,legh) = leg.size
    legTransparent = makeBackgroundTransparent(canvas,leg)

    (legw,legh) = legTransparent.size
    coordToPasteLeg = (canvas.bodyCenter - legw/2 + canvas.bodyLength/6,y1-(
        canvas.legLength-dy)/2)     
    im.paste(legTransparent,coordToPasteLeg,mask=legTransparent)

    # make the character bounce
    (w,h) = im.size
    frame1 = Image.new(im.mode, (w,h+60))
    frame1.paste(im,(0,30))

    canvas.data["frame1"] = frame1                                    
    frame1.save("frame1.jpg")

def makeFrame2(canvas):
    im = canvas.data["character"].convert("RGBA")
    bentLeg = canvas.data["bent leg"].convert("RGBA")
    veryBentLeg = canvas.data["very bent leg"].convert("RGBA")

    (x1,y1) = canvas.legCoord[0]
    (x2,y2) = canvas.legCoord[1]
    (bentw,benth) = bentLeg.size
    (vbentw,vbenth) = veryBentLeg.size
    bentLeg = bentLeg.rotate(30, expand = 1)
    bentLegTransparent = makeBackgroundTransparent(canvas,bentLeg)
    (newbentw,newbenth) = bentLeg.size

    theta = (2*math.pi)*30/360
    (dx,dy) = findDxDy(canvas,theta)

    coordToPasteVeryBentLeg = (canvas.bodyCenter - vbentw/2-
        canvas.bodyLength/6,y1-10)               
    im.paste(veryBentLeg,coordToPasteVeryBentLeg,mask=veryBentLeg)

    coordToPasteBentLeg = (canvas.bodyCenter - newbentw/2+canvas.bodyLength/6, 
        y1-(canvas.legLength-dy)/2)                                  
    im.paste(bentLegTransparent,coordToPasteBentLeg,mask=bentLegTransparent)

    (w,h) = im.size
    frame2 = Image.new(im.mode, (w,h+60))
    frame2.paste(im,(0,60))

    canvas.data["frame2"] = frame2                                           
    frame2.save("frame2.jpg")


def makeFrame3(canvas):
    im = canvas.data["character"].convert("RGBA")
    leg = canvas.data["leg"].convert("RGBA")
    veryBentLeg = canvas.data["very bent leg"].convert("RGBA")
    (x1,y1) = canvas.legCoord[0]
    (x2,y2) = canvas.legCoord[1]
    (legw,legh) = leg.size
    (vbentw,vbenth) = veryBentLeg.size

    leg = leg.rotate(340, expand = 1)
    (legw,legh) = leg.size
    legTransparent = makeBackgroundTransparent(canvas,leg)

    theta = (2*math.pi)*20/360
    (dx,dy) = findDxDy(canvas,theta)

    coordToPasteLeg = (canvas.bodyCenter - legw/2 ,y1-(canvas.legLength-dy)/4)                                
    im.paste(legTransparent,coordToPasteLeg,mask=legTransparent)

    veryBentLeg = veryBentLeg.rotate(10, expand = 1)
    veryBentLegTransparent = makeBackgroundTransparent(canvas,veryBentLeg)
    (newvbentw,newvbenth) = veryBentLeg.size
    theta = (2*math.pi)*10/360
    (dx,dy) = findDxDy(canvas,theta)

    coordToPasteVeryBentLeg = (canvas.bodyCenter-newvbentw/2 + dx,y1-(
        canvas.legLength-dy)/4)                                
    im.paste(veryBentLegTransparent,coordToPasteVeryBentLeg,
        mask=veryBentLegTransparent)

    (w,h) = im.size
    frame3 = Image.new(im.mode, (w,h+60))
    frame3.paste(im,(0,30))

    canvas.data["frame3"] = frame3                                                                 
    frame3.save("frame3.jpg")

def makeFrame4(canvas):
    im = canvas.data["character"].convert("RGBA")
    leg = canvas.data["leg"].convert("RGBA")
    veryBentLeg = canvas.data["very bent leg"].convert("RGBA")
    (x1,y1) = canvas.legCoord[0]
    (x2,y2) = canvas.legCoord[1]
    (legw,legh) = leg.size
    (vbentw,vbenth) = veryBentLeg.size

    leg = leg.rotate(330, expand = 1)
    legTransparent = makeBackgroundTransparent(canvas,leg)
    (legw,legh) = leg.size

    theta = (2*math.pi)*30/360
    (dx,dy) = findDxDy(canvas,theta)

    coordToPasteLeg = (canvas.bodyCenter -legw/2 - dx - 
        canvas.bodyLength/6,y1-(canvas.legLength-dy)/4)                                                   
    im.paste(legTransparent,coordToPasteLeg,mask=legTransparent)

    veryBentLeg = veryBentLeg.rotate(50, expand = 1)
    veryBentLegTransparent = makeBackgroundTransparent(canvas,veryBentLeg)
    (newvbentw,newvbenth) = veryBentLeg.size
    theta = (2*math.pi)*50/360
    (dx,dy) = findDxDy(canvas,theta)

    coordToPasteVeryBentLeg = (canvas.bodyCenter-newvbentw/2 +dx + 
        canvas.bodyLength/6,y1-(canvas.legLength-dy)/2)                                          
    im.paste(veryBentLegTransparent,coordToPasteVeryBentLeg,
        mask=veryBentLegTransparent)

    (w,h) = im.size
    frame4 = Image.new(im.mode, (w,h+60))
    frame4.paste(im,(0,0))

    canvas.data["frame4"] = frame4                                                                 
    frame4.save("frame4.jpg")

# THE CODE IMPORTED TO MAKE CONVERT FRAMES TO A GIF WAS TAKEN FROM THE INTERNET
# http://visvis.googlecode.com/hg/vvmovie/images2gif.py
# CODE IS OWNED BY: Almar Klein, Ant1, Marius van Voorden

def makeWalkGIF(canvas):
    file_names=sorted((fn for fn in os.listdir('.') if fn.startswith("frame")))
    images = [Image.open(fn) for fn in file_names]
    filename = "walking_animation.GIF"
    writeGif(filename, images, duration=0.2)

def makeDanceGIF(canvas):
    file_names=sorted((fn for fn in os.listdir('.') if fn.startswith("dance")))
    images = [Image.open(fn) for fn in file_names]
    filename = "dancing_animation.GIF"
    writeGif(filename, images, duration=0.2)

def makeBobGIF(canvas):
    file_names=sorted((fn for fn in os.listdir('.') if fn.startswith("bob_")))
    images = [Image.open(fn) for fn in file_names]
    filename = "bobbing_animation.GIF"
    writeGif(filename, images, duration=0.2)

def convertLegToImages(canvas):
    #first, clean up image
    im = Image.open("houghlinesnew.jpg")
    (width, height) = im.size
    im = cleanUpImage(canvas,im)
    im.save("houghlinesnew.jpg")
    
    # make leg shape 1: straight leg
    (x1,y1) = canvas.legCoord[0]
    (x2,y2) = canvas.legCoord[1]
    cropBox = (x1,y1,x2,y2)
    legIm = im.crop(cropBox)
    canvas.data["leg"] = legIm

    temp = legIm.copy().convert("RGBA")
    (tempW,tempH) = temp.size

    # make leg shape 2: slightly bent leg
    canvas.legLength = y2-y1                                                                                                                 ####
    canvas.halfLegLength = int(round(canvas.legLength/2))
    legWidth = canvas.legWidthCoord[1][0] - canvas.legWidthCoord[0][0]
    bottomHalfCoord = (0,tempH/2,tempW,tempH)
    topHalfCoord = (0,0,tempW,tempH/2)
    tempTopHalf = temp.crop(topHalfCoord)
    topHalfTransparent = makeBackgroundTransparent(canvas,tempTopHalf)
    tempBotHalf = temp.crop(bottomHalfCoord)                                                      

    # rotate it and expand it's canvas so the corners don't get cut off:
    tempBotHalfRotated = tempBotHalf.rotate(320, expand = 1)
    (botw,both) = tempBotHalfRotated.size

    botHalfTransparent = makeBackgroundTransparent(canvas,tempBotHalfRotated)
    canvas.bentImSize = (tempW*2,3*tempH/2)
    bentIm = Image.new(temp.mode, canvas.bentImSize)
    bentIm.paste(topHalfTransparent,(tempW,0),mask=topHalfTransparent)

    theta = (2*math.pi)*40/360
    (dx,dy) = findDxDy(canvas,theta)

    bentIm.paste(botHalfTransparent, (tempW-dx + 10,tempH/2 - 
        (canvas.halfLegLength/2)), mask = botHalfTransparent)

    bentImTransparent = makeBackgroundTransparent(canvas,bentIm)
    canvas.data["bent leg"] = bentImTransparent

    # make leg shape 3: very bent leg
    tempBotHalfRotated2 = tempBotHalf.rotate(280, expand = 1)
    botHalfTransparent2 = makeBackgroundTransparent(canvas,tempBotHalfRotated2)
    bentIm2 = Image.new(temp.mode, canvas.bentImSize)
    bentIm2.paste(topHalfTransparent,(tempW,0),mask=topHalfTransparent)

    theta = (2*math.pi*80)/360
    (dx,dy) = findDxDy(canvas,theta)
    bentIm2.paste(botHalfTransparent2, (tempW-dx,tempH/2 - dy - legWidth), 
        mask = botHalfTransparent2)
    bentImTransparent2 = makeBackgroundTransparent(canvas,bentIm2)
    canvas.data["very bent leg"] = bentImTransparent2

    #get rid of leg in original picture
    getRidOfArea(canvas,im,(x1,y1,x2,y2))
    canvas.data["character"] = im

def cleanUpImage(canvas,image):
    (x1,y1) = canvas.charCoord[0]
    (x2,y2) = canvas.charCoord[1]
    (width, height) = image.size
    #get rid of everything above character
    getRidOfArea(canvas,image,(0,0,width,y1))
    #get rid of everything below character
    getRidOfArea(canvas,image,(0,y2,width,height))
    #get rid of everything to left of character
    getRidOfArea(canvas,image,(0,y1,x1,y2))
    #get rid of everything to right of character
    getRidOfArea(canvas,image,(x2,y1,width,y2))
    return image

def makeCharWalk(canvas):
    canvas.makeCharWalkPage = True
    convertLegToImages(canvas)
    makeWalkFrames(canvas)
    makeWalkGIF(canvas)
    redrawAll(canvas)

def makeWalkFrames(canvas):
    makeFrame1(canvas)
    makeFrame2(canvas)
    makeFrame3(canvas)
    makeFrame4(canvas)
    removeLegs(canvas)

def makeCharDance(canvas):
    canvas.makeCharDancePage = True
    makeDanceFrames(canvas)
    makeDanceGIF(canvas)
    redrawAll(canvas)

def makeCharBob(canvas):
    canvas.makeCharBobPage = True
    makeBobFrames(canvas)
    makeBobGIF(canvas)
    redrawAll(canvas)

def makeDanceFrames(canvas):
    frame4 = Image.open("frame4.jpg")
    (width,height) = frame4.size
    newHeight = height + 100
    frame4New = Image.new(frame4.mode, (width,newHeight))
    frame4New.paste(frame4,(0,0))
    leanLeft = frame4New.rotate(35)
    leanLeftNew = leanLeft.crop((0,60,width,newHeight))
    leanLeftNew.save("dance1.jpg")
    leanRight = leanLeftNew.transpose(Image.FLIP_LEFT_RIGHT)
    leanRight.save("dance2.jpg")

def makeBobFrames(canvas):
    (x1,y1) = canvas.legCoord[0]
    (x2,y2) = canvas.legCoord[1]

    original = Image.open("houghlinesnew.jpg").convert("RGBA")
    (width,height) = original.size
    bobUp = Image.open("houghlinesnew.jpg")
    legCropBox = (x1,y1,x2,y2)
    legIm = original.crop(legCropBox)
    legIm = makeBackgroundTransparent(canvas,legIm)

    #make bob up frame
    coord1ToPasteLeg = (canvas.bodyLeft,y1)
    getRidOfArea(canvas,bobUp,(x1,y1,x2,y2))         
    bobUp.paste(legIm,coord1ToPasteLeg)
    coord2ToPasteLeg = (canvas.bodyCenter,y1)
    bobUp.paste(legIm,coord2ToPasteLeg)
    bobUp.save("bob_1.jpg")

    #make bob down frame
    bobDown = bobUp.copy()
    bodyCropBox = (0,0,width,y1)
    bodyIm = original.crop(bodyCropBox)
    getRidOfArea(canvas,bobDown,bodyCropBox) 
    coordToPasteBody = (0,canvas.legLength/2) 
    bobDown.paste(bodyIm,coordToPasteBody)
    bobDown.save("bob_2.jpg")

#helper function to make an area all black
def getRidOfArea(canvas,im,coord):
    (x1,y1,x2,y2) = coord
    pix = im.load()
    allPixels = []
    for x in xrange(x1,x2):
        for y in xrange(y1,y2):
            allPixels.append((x,y))

    value = (0, 0, 0, 0)

    for (x,y) in allPixels:
        pix[x, y] = value 

#gives certain pixels 100% transparency 
def makeBackgroundTransparent(canvas,img):
    img = img.convert("RGBA")
    pixdata = img.load()

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 100:
                pixdata[x, y] = (0, 0, 0, 0)
    return img

def drawCoordInstruct(canvas,num):
    canvas.create_rectangle(0,200,canvas.width/3+100,3*canvas.height/4,fill="black")
    msg = canvas.instructions[num]
    canvas.create_text(canvas.width/6,canvas.height/3, text = msg,
       font = "Chalkboard 20", fill = "aquamarine")    

def showChosenCoord(canvas,num):
    if num == 0:
        coords = canvas.legCoord
    elif num == 1:
        coords = canvas.legWidthCoord
    elif num ==2:
        coords = canvas.bodyCoord
    else:
        coords = canvas.charCoord

    if len(coords) == 0:
        canvas.create_text(canvas.width/6,canvas.height/2 + 30,
        text = "No chosen coordinates yet!", 
        font = "Chalkboard 20", fill = "aquamarine")
    elif len(coords) == 1:
        coord1 = coords[0]
        if num == 0 or num == 3:
            oneCoordMsg = ("Top Left: " + str(coord1))
        else:
            oneCoordMsg = ("Left: " + str(coord1))
        canvas.create_text(canvas.width/6,canvas.height/2+ 30,
        text = oneCoordMsg, font = "Chalkboard 20",
        fill = "aquamarine")
    elif len(coords) == 2:
        coord1 = coords[0]
        coord2 = coords[1]
        if num == 0 or num == 3:
            twoCoordMsg = ("Top Left: " + str(coord1) + " Bottom Right: " 
            + str(coord2))
        else:
            twoCoordMsg = ("Left: " + str(coord1) + " Right: " + str(coord2))
        canvas.create_text(canvas.width/6,canvas.height/2+ 30,
        text = twoCoordMsg, font = "Chalkboard 20",
        fill = "aquamarine")
        if num == 0 or num == 3:
            w = canvas.width/6 #extra space
            h = canvas.height/5
            canvas.create_line(w+coord1[0],h+coord1[1],w+coord2[0],h+coord1[1],
                fill = "white", width = 3)
            canvas.create_line(w+coord2[0],h+coord1[1],w+coord2[0],h+coord2[1],
                fill = "white", width = 3)
            canvas.create_line(w+coord1[0],h+coord2[1],w+coord2[0],h+coord2[1],
                fill = "white", width = 3)
            canvas.create_line(w+coord1[0],h+coord1[1],w+coord1[0],h+coord2[1],
                fill = "white", width = 3)
        else:
            w = canvas.width/6 #extra space
            h = canvas.height/5
            canvas.create_line(w+coord1[0],h+coord1[1],w+coord2[0],h+coord2[1],
                fill = "white", width = 3)

def drawTitle(canvas):
    canvas.create_text(canvas.width/8,canvas.height/6, anchor =NW, text="OFF",
        font = "Chalkboard 100 bold", fill = "LightGreen")
    canvas.create_text(canvas.width/4,canvas.height/5, anchor =NW, text="THE",
        font = "Chalkboard 150 bold", fill = "LightGreen")
    canvas.create_text(canvas.width/3 + 150,canvas.height/4, 
        anchor = NW, text="PAGE!", font = "Chalkboard 250 bold", 
        fill = "LightGreen")
    canvas.create_text(canvas.width/2,7*canvas.height/8, 
        text="Scan a drawing of a character and animate it!", 
        font = "Chalkboard 30 italic", fill = "white")
    burger1 = Image.open("1.gif")
    burger1 = ImageTk.PhotoImage(burger1)
    canvas.data["burger1"] = burger1
    burger2 = Image.open("2.gif")
    burger2 = ImageTk.PhotoImage(burger2)
    canvas.data["burger2"] = burger2
    burger3 = Image.open("3.gif")
    burger3 = ImageTk.PhotoImage(burger3)
    canvas.data["burger3"] = burger3
    burger4 = Image.open("4.gif")
    burger4 = ImageTk.PhotoImage(burger4)
    canvas.data["burger4"] = burger4
    burger5 = Image.open("5.gif")
    burger5 = ImageTk.PhotoImage(burger5)
    canvas.data["burger5"] = burger5
    canvas.create_image(canvas.width/3 + 520, canvas.height/4 - 40, anchor = NW, 
            image=canvas.data["burger1"])
    canvas.create_image(canvas.width/3 + 600, canvas.height/4 - 40, anchor = NW, 
            image=canvas.data["burger2"])
    canvas.create_image(canvas.width/3 + 680, canvas.height/4 - 40, anchor = NW, 
            image=canvas.data["burger3"])
    canvas.create_image(canvas.width/3 + 760, canvas.height/4 - 40, anchor = NW, 
            image=canvas.data["burger4"])
    canvas.create_image(canvas.width/3 + 860, canvas.height/4 , anchor = NW, 
            image=canvas.data["burger5"])

def scanDrawingPage(canvas):
    if canvas.scanDrawingPage == True:
        canvas.scanDrawingPage = False
    else:
        canvas.scanDrawingPage = True
    redrawAll(canvas)

def button1Pressed(canvas):
    scanDrawingPage(canvas)

def button2Pressed(canvas):
    canvas.animatePage = False
    canvas.charCoord = []
    canvas.legCoord = []
    canvas.legWidthCoord = []
    canvas.bodyCoord = []
    canvas.charPage = True
    redrawAll(canvas)
        
def noScannedImageErr(canvas):
    canvas.noScannedImageErr = True
    redrawAll(canvas)

def noCoordErr(canvas):
    canvas.noCoordErr = True
    redrawAll(canvas)

def button3Pressed(canvas):
    print "OFF THE PAGE!"
    sys.exit()

# ALTHOUGH SLIGHTLY ALTERED, THE ALGORITHM BELOW WAS TAKEN FROM THE INTERNET
# https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/houghlines.py
def button4Pressed(canvas): 
    #Take a picture from webcam
    canvas.closedCamera = False
    cv.NamedWindow("Scan Drawing", 1)

    capture = cv.CaptureFromCAM(0)
    c = cv.WaitKey(5000)
    while True:
        img = cv.QueryFrame(capture)
        cv.ShowImage("Scan Drawing", img)
        k = cv.WaitKey(20)
        if k == ord('s'):
            cv.SaveImage('Scanned.jpg', img)
            break 
        elif k == 27: #escape
            canvas.closedCamera = True
            cv2.destroyAllWindows()
            break

    #now, the image is saved to working directory
    #use this image below

    if canvas.closedCamera == False:
        im = cv2.imread('Scanned.jpg')
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,150,200,apertureSize = 3)

        cv2.imshow('houghlines',im)

        width, height = cv.GetSize(img)
        blank_image = np.zeros((height,width,3), np.uint8)

        while(True):
            img = im.copy()
            k = cv2.waitKey(0)

            if k == ord('e'):
                lines = cv2.HoughLinesP(edges,1,np.pi/180,1, 
                    minLineLength = 0, maxLineGap = 0)
                for x1,y1,x2,y2 in lines[0]:
                    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.line(blank_image,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.imshow('houghlines',img)

            k2 = cv2.waitKey(0)
            if k2 == 13:    # Press 'ENTER' to exit
                cv2.imwrite('houghlines.jpg',img)
                cv2.imwrite('houghlinesnew.jpg',blank_image)
                scanDrawingPage(canvas)
                break
            elif k2 == 27:
                break

    cv2.destroyAllWindows()
    
def button5Pressed(canvas):
    try:
        photo = Image.open("houghlinesnew.jpg")
        image = ImageTk.PhotoImage(photo)
        canvas.data["image"] = image
        canvas.animatePage = True
    except:
        noScannedImageErr(canvas)
        canvas.animatePage = True
        canvas.failedAnimate = True
    redrawAll(canvas)

def button6Pressed(canvas):
    canvas.animatePage = False
    canvas.walking = True
    canvas.charPage = False
    if canvas.legCoord == []:
        noCoordErr(canvas)
        canvas.interactPage = True
    else:
        convertLegToImages(canvas)
        makeWalkFrames(canvas)
        makeDanceFrames(canvas)
        makeBobFrames(canvas)
        photo = Image.open("frame1.jpg")
        (width,height) = photo.size
        image = ImageTk.PhotoImage(photo)
        loadFrames(canvas)
        canvas.leftBound = findLeftBound(photo,width,height)
        canvas.rightBound=canvas.frameWidth-findRightBound(photo,width,height)
        canvas.interactPage = True
    redrawAll(canvas)

def button7Pressed(canvas):
    canvas.animatePage = False
    canvas.charPage = False
    if canvas.legCoord == []:
        noCoordErr(canvas)
        canvas.makeCharWalkPage = True
    else:
        #need to create all frames for loadFrames to work
        #dont know which button user will press first (7,8 or 9)
        convertLegToImages(canvas)
        makeWalkFrames(canvas)
        makeDanceFrames(canvas)
        makeBobFrames(canvas)
        loadFrames(canvas)
        makeCharWalk(canvas)
        canvas.makeCharWalkPage = True
        canvas.walking = True
    redrawAll(canvas)

def button8Pressed(canvas):
    canvas.animatePage = False
    canvas.charPage = False
    if canvas.legCoord == []:
        noCoordErr(canvas)
        canvas.makeCharDancePage = True
    else:
        convertLegToImages(canvas)
        makeWalkFrames(canvas)
        makeDanceFrames(canvas)
        makeBobFrames(canvas)
        loadFrames(canvas)
        makeCharDance(canvas)
        canvas.makeCharDancePage = True
        canvas.dancing = True
    redrawAll(canvas)

def button9Pressed(canvas):
    canvas.animatePage = False
    canvas.charPage = False
    if canvas.legCoord == []:
        noCoordErr(canvas)
        canvas.makeCharBobPage = True
    else:
        convertLegToImages(canvas)
        makeWalkFrames(canvas)
        makeDanceFrames(canvas)
        makeBobFrames(canvas)
        loadFrames(canvas)
        makeCharBob(canvas)
        canvas.makeCharBobPage = True
        canvas.bobbing = True
    redrawAll(canvas)

def button10Pressed(canvas):
    canvas.scanDrawingPage = False
    canvas.animatePage = False
    redrawAll(canvas)

def button11Pressed(canvas):
    canvas.charPage = False
    canvas.legPage = False
    canvas.legWidthPage = False
    canvas.bodyPage = False
    canvas.coordPage = False
    canvas.makeCharWalkPage = False
    canvas.makeCharDancePage = False
    canvas.makeCharBobPage = False
    canvas.interactPage = False
    canvas.animatePage = True
    redrawAll(canvas)

#finds first pixel from the left that is green
def findLeftBound(image,width,height):
    pix = image.load()
    for col in xrange(width):
        for row in xrange(height):
            if pix[col,row][1] > 100:
                return col

#finds first pixel from the right that is green
def findRightBound(image,width,height):
    pix = image.load()
    for col in xrange(width-1,-1,-1):
        for row in xrange(height):
            if pix[col,row][1] > 100:
                return col

def loadFrames(canvas):
    photo1 = Image.open("frame1.jpg")
    (canvas.frameWidth,canvas.frameHeight) = photo1.size
    frame1 = ImageTk.PhotoImage(photo1)
    canvas.data["frame1"] = frame1
    reverse1 = photo1.transpose(Image.FLIP_LEFT_RIGHT)
    reverse1.save("reverse1.jpg")
    photoR1 = Image.open("reverse1.jpg")
    frameR1 = ImageTk.PhotoImage(photoR1)
    canvas.data["reverse1"] = frameR1

    photo2 = Image.open("frame2.jpg")
    frame2 = ImageTk.PhotoImage(photo2)
    canvas.data["frame2"] = frame2
    reverse2 = photo2.transpose(Image.FLIP_LEFT_RIGHT)
    reverse2.save("reverse2.jpg")
    photoR2 = Image.open("reverse2.jpg")
    frameR2 = ImageTk.PhotoImage(photoR2)
    canvas.data["reverse2"] = frameR2

    photo3 = Image.open("frame3.jpg")
    frame3 = ImageTk.PhotoImage(photo3)
    canvas.data["frame3"] = frame3
    reverse3 = photo3.transpose(Image.FLIP_LEFT_RIGHT)
    reverse3.save("reverse3.jpg")
    photoR3 = Image.open("reverse3.jpg")
    frameR3 = ImageTk.PhotoImage(photoR3)
    canvas.data["reverse3"] = frameR3

    photo4 = Image.open("frame4.jpg")
    frame4 = ImageTk.PhotoImage(photo4)
    canvas.data["frame4"] = frame4
    reverse4 = photo4.transpose(Image.FLIP_LEFT_RIGHT)
    reverse4.save("reverse4.jpg")
    photoR4 = Image.open("reverse4.jpg")
    frameR4 = ImageTk.PhotoImage(photoR4)
    canvas.data["reverse4"] = frameR4

    dphoto1 = Image.open("dance1.jpg")
    dance1 = ImageTk.PhotoImage(dphoto1)
    canvas.data["dance1"] = dance1

    dphoto2 = Image.open("dance2.jpg")
    dance2 = ImageTk.PhotoImage(dphoto2)
    canvas.data["dance2"] = dance2

    bphoto1 = Image.open("bob_1.jpg")
    bob1 = ImageTk.PhotoImage(bphoto1)
    canvas.data["bob1"] = bob1

    bphoto2 = Image.open("bob_2.jpg")
    bob2 = ImageTk.PhotoImage(bphoto2)
    canvas.data["bob2"] = bob2

    bobReverse1 = bphoto1.transpose(Image.FLIP_LEFT_RIGHT)
    bobReverse1.save("reversebob1.jpg")
    bobReverse1 = Image.open("reversebob1.jpg")
    bobReverse1 = ImageTk.PhotoImage(bobReverse1)
    canvas.data["bob reverse1"] = bobReverse1

    bobReverse2 = bphoto2.transpose(Image.FLIP_LEFT_RIGHT)
    bobReverse2.save("reversebob2.jpg")
    bobReverse2 = Image.open("reversebob2.jpg")
    bobReverse2 = ImageTk.PhotoImage(bobReverse2)
    canvas.data["bob reverse2"] = bobReverse2

    canvas.frames = [canvas.data["frame1"],canvas.data["frame2"],
        canvas.data["frame3"],canvas.data["frame4"]]

    canvas.reversedFrames = [canvas.data["reverse1"],
        canvas.data["reverse2"],canvas.data["reverse3"],
        canvas.data["reverse4"]]

    canvas.danceFrames = [canvas.data["dance1"],canvas.data["dance2"]]

    canvas.bobFrames = [canvas.data["bob1"],canvas.data["bob2"]]

    canvas.bobReverseFrames = [canvas.data["bob reverse1"],
        canvas.data["bob reverse2"]]

def init(root,canvas):
    canvas.land = False
    canvas.jumpY = 0
    canvas.jumpbend = False
    canvas.jumpextend = False
    canvas.sitting = False
    canvas.legLength = 0
    canvas.halfLegLength = 0
    canvas.walking = True
    canvas.jumping = False
    canvas.dancing = False
    canvas.bobbing = False
    canvas.scanDrawingPage = False
    canvas.coordPage = False
    canvas.bodyPage = False
    canvas.charPage = False
    canvas.legPage = False
    canvas.animatePage = False
    canvas.legWidthPage = False
    canvas.interactPage = False
    canvas.makeCharWalkPage = False
    canvas.makeCharDancePage = False
    canvas.makeCharBobPage = False
    canvas.noScannedImageErr = False
    canvas.closedCamera = False
    canvas.noCoordErr = False
    canvas.acceptedScan = True
    (canvas.bodyLeft,canvas.bodyRight) = (0,0)
    (canvas.bodyLength,canvas.bodyCenter) = (0,0)
    canvas.charCoord = []
    canvas.legCoord = []
    canvas.bodyCoord = []
    canvas.legWidthCoord = []
    canvas.failedAnimate = False
    canvas.instructions = [
    """
        Instructions:
        Mark a box around your character's leg
        (including the foot if there is one) by:
        1) Clicking the location to place the top 
           left corner of the box (avoid clicking on 
           your character)
        2) Clicking the location to place the bottom 
           right corner of the box (avoid clicking on 
           your character)
        
        Press 'u' to erase a click 
        Press 'ENTER' to accept chosen bounds
        """,
    """
        Instructions:
        Mark the width of your character's leg 
        (if there is a foot, IGNORE it!) by:
        1) Clicking the leftmost side of the leg
           (you may click on the character itself)
        2) Clicking the rightmost side of the leg
           (you may click on the character itself)

        Press 'u' to erase a click 
        Press 'ENTER' to accept chosen bounds
        """,
     """
        Instructions:
        Mark the width of your character's body by:
        1) Clicking the leftmost side of the lower body
           (you may click on the character itself)
        2) Clicking the rightmost side of the lower body
           (you may click on the character itself)

        Press 'u' to erase a click 
        Press 'ENTER' to accept chosen bounds
        """,
    """ 
        Instructions:
        Mark a box around your entire character by:
        1) Clicking the location to place the top 
           left corner of the box (avoid clicking on 
           your character)
        2) Clicking the location to place the bottom 
           right corner of the box (avoid clicking on 
           your character)

        Press 'u' to erase a click
        Press 'ENTER' to accept chosen bounds"""]
    canvas.data["leg"] = None
    canvas.data["bent leg"] = None
    canvas.data["character"] = None
    canvas.data["frame1"] = None
    canvas.frameWidth = None
    canvas.frameHeight = None
    canvas.turned = False
    canvas.index = 0
    canvas.danceBobIndex = 0
    canvas.dw = 50
    canvas.x = 0
    canvas.time =0
    (canvas.leftBound,canvas.rightBound) = (None,None)
    canvas.width = canvas.winfo_reqwidth()-4
    canvas.height = canvas.winfo_reqheight()-4
    
    #buttons made at http://dabuttonfactory.com/
    def b1Pressed(): button1Pressed(canvas)
    button1Image = PhotoImage(file="buttonscandrawing.gif")
    b1 = Button(canvas, image=button1Image, width=250, height=40, 
        highlightbackground="black", command=b1Pressed)
    b1.image = button1Image 
    canvas.data["button1"] = b1
    def b2Pressed(): button2Pressed(canvas)
    button2Image = PhotoImage(file="buttonset.gif")
    b2 = Button(canvas, image=button2Image, width=500, height=60, 
        highlightbackground="black", command=b2Pressed)
    b2.image = button2Image 
    canvas.data["button2"] = b2
    def b3Pressed(): button3Pressed(canvas)
    button3Image = PhotoImage(file="buttonexit.gif")
    b3 = Button(canvas, image=button3Image, width=250, height=40, 
        highlightbackground="black", command=b3Pressed)
    b3.image = button3Image 
    canvas.data["button3"] = b3
    def b4Pressed(): button4Pressed(canvas)
    button4Image = PhotoImage(file="buttonscan.gif")
    b4 = Button(canvas, image=button4Image, width=250, height=60, 
        highlightbackground="black", command=b4Pressed)
    b4.image = button4Image 
    canvas.data["button4"] = b4
    def b5Pressed(): button5Pressed(canvas)
    button5Image = PhotoImage(file="buttonanimate.gif")
    b5 = Button(canvas, image=button5Image, width=250, height=40, 
        highlightbackground="black", command=b5Pressed)
    b5.image = button5Image 
    canvas.data["button5"] = b5
    def b6Pressed(): button6Pressed(canvas)
    button6Image = PhotoImage(file="buttoninteract.gif")
    b6 = Button(canvas, image=button6Image, width=500, height=60, 
        highlightbackground="black", command=b6Pressed)
    b6.image = button6Image 
    canvas.data["button6"] = b6
    def b7Pressed(): button7Pressed(canvas)
    button7Image = PhotoImage(file="buttonwalk.gif")
    b7 = Button(canvas, image=button7Image, width=500, height=40, 
        highlightbackground="black", command=b7Pressed)
    b7.image = button7Image 
    canvas.data["button7"] = b7
    def b8Pressed(): button8Pressed(canvas)
    button8Image = PhotoImage(file="buttondance.gif")
    b8 = Button(canvas, image=button8Image, width=500, height=40, 
        highlightbackground="black", command=b8Pressed)
    b8.image = button8Image 
    canvas.data["button8"] = b8
    def b9Pressed(): button9Pressed(canvas)
    button9Image = PhotoImage(file="buttonbob.gif")
    b9 = Button(canvas, image=button9Image, width=500, height=40, 
        highlightbackground="black", command=b9Pressed)
    b9.image = button9Image 
    canvas.data["button9"] = b9
    def b10Pressed(): button10Pressed(canvas)
    button10Image = PhotoImage(file="homebutton.gif")
    b10 = Button(canvas, image=button10Image, width=100, height=80, 
        highlightbackground="black", highlightthickness = 0, command=b10Pressed)
    b10.image = button10Image 
    canvas.data["button10"] = b10
    def b11Pressed(): button11Pressed(canvas)
    button11Image = PhotoImage(file="backbutton.gif")
    b11 = Button(canvas, image=button11Image, width=60, height=60, 
        highlightbackground="black", highlightthickness = 0, command=b11Pressed)
    b11.image = button11Image 
    canvas.data["button11"] = b11
    canvas.pack()
    redrawAll(canvas)

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    root.resizable(width=True, height=True)
    canvas = Canvas(root, width=1600, height=1000)
    canvas.pack(fill=BOTH, expand=YES)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(root,canvas)
    # set up events
    def f(event): 
        mousePressed(canvas,event)
    root.bind("<Button-1>", f)
    def g(event): 
        keyPressed(canvas,event)
    root.bind("<KeyPress>", g)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)\
    print "OFF THE PAGE!"
run()

#############################################################
#### TEST FUNCTIONS FOR NON IMAGE-BASED HELPER FUNCTIONS ####
#############################################################

"""
import math

def findDxDyForEasierTesting(theta): 
    dx = int(round(2*math.sin(theta)))
    dy = int(round(2*math.cos(theta)))
    return (dx,dy)

def testFindDxDy():
    print "testing findDxDy...",
    assert(findDxDyForEasierTesting(math.pi/3)== (2,1))
    print "Passed all tests!"

def changeFramesForEasierTesting(currentFrameIndex):
    if currentFrameIndex == 3:
        currentFrameIndex = 0
    else:
        currentFrameIndex += 1
    return currentFrameIndex

def testChangeFrames():
    print "testing changeFrames...",
    assert(changeFramesForEasierTesting(0) == 1)
    assert(changeFramesForEasierTesting(3) == 0)
    print "Passed all tests!"

def moveImageForEasierTesting(x,dw):
    x += dw
    if (x < 10): 
        dw = -dw
    elif (x > 20):
        dw = -dw
    return (x,dw)

def testMoveImage():
    print "testing moveImage...",
    assert(moveImageForEasierTesting(3,5) == (8,-5))
    assert(moveImageForEasierTesting(15,5) == (20,5))
    assert(moveImageForEasierTesting(40,5) == (45,-5))
    print "Passed all tests!"

def testAll():
    testFindDxDy()
    testChangeFrames()
    testMoveImage()

def main():
    testAll()

if __name__ == "__main__":
    main()
"""
