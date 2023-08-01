#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neopixel LED Mirror Image Display Code (Neopixel LED Mirror - Super Make Something Episode 20) - https://youtu.be/Ew0HmLy_Td8
by: Alex - Super Make Something
by: Alex - Super Make Something
date: November 18, 2019
license: Creative Commons - Attribution - Non Commercial.  More information at: http://creativecommons.org/licenses/by-nc/3.0/
description: This script loads a desired image and displays it on the Neopixel Mirror
"""

# Import required libraries
from PIL import Image
import numpy as np
import sys

def extractROI(image, x, y):
    
    imWidth, imHeight = image.size
    roiImage = image.resize((x, y))

    return roiImage

def discretizeImage(roiImage,noLevels):

    image=np.array(roiImage)#Image.fromarray(roiImage,'RGB')
    normalizedImage=image/255
    discretizedImage=np.floor(normalizedImage*noLevels).astype(int)
    multiplier=255/noLevels
    discretizedImage=np.floor(discretizedImage*multiplier).astype(np.uint8) #Rescale to range 0-255
    return discretizedImage

def imageToLED(discreteImageRaw,pixels):
    discreteImageR=discreteImageRaw[:,:,0]
    discreteImageG=discreteImageRaw[:,:,1]
    discreteImageB=discreteImageRaw[:,:,2]
    discreteImageR=discreteImageR.flatten()
    discreteImageG=discreteImageG.flatten()
    discreteImageB=discreteImageB.flatten()
    pixelArray=np.zeros((len(discreteImageR),3))
    pixelArray[:,0]=discreteImageR
    pixelArray[:,1]=discreteImageG
    pixelArray[:,2]=discreteImageB
    pixelArray=(pixelArray).astype(int)# Convert to int
    pixelTuple=[tuple(x) for x in pixelArray] #Convert to correctly dimensioned tuple array
    pixels[:]=pixelTuple
        
    return pixels
    
#Parameters
noLevels=255 #No of LED brightness discretization levels
numNeopixels_x = 24 #Declare number of Neopixels in grid
numNeopixels_y = 24
pixels = []

numPixels=numNeopixels_x*numNeopixels_y


while 1:
    newImage = Image.open('yoshi.png')
    newImageROI = extractROI(newImage, numNeopixels_x, numNeopixels_y) #Extract base image ROI
    discretizedImage=discretizeImage(newImageROI,noLevels) #Discretize image and scale values   
    #pixels=imageToLED(discretizedImage,pixels) #Convert the image to an LED value array and assign them to the string of Neopixels
    print("\x1b[2J\x1b[H", end="")
    for y in range(0, numNeopixels_y):
        for x in range(0, numNeopixels_x):              
              px_r = discretizedImage[y, x, 0]
              px_g = discretizedImage[y, x, 1]
              px_b = discretizedImage[y, x, 2]
              print(f"\x1b[48;2;{px_r};{px_g};{px_b}m   ", end="")
        print("\x1b[0m")      
    sys.stdout.flush()
    
