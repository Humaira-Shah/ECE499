import cv2.cv as cv
import cv2
import numpy as np

# returns binary black and white image
# white parts signify color found, black signifies color not found
# I used this to get an idea of what RGB values constituted green in the image
def getColor(img, color, nx, ny):

	binaryImg = img

	for i in range(nx):
		for j in range(ny):
			match = np.array(img[j,i]) == np.array(color)
			if(match.all()):
				binaryImg.itemset((j,i,0),255)
				binaryImg.itemset((j,i,1),255)
				binaryImg.itemset((j,i,2),255)
			else:
				binaryImg.itemset((j,i,0),0)
				binaryImg.itemset((j,i,1),0)
				binaryImg.itemset((j,i,2),0)

	return binaryImg

# takes parameters img, nx, and ny where img is the image we are searching for center
# of green in, nx is the horizontal length of pixels of the image and ny is the
# vertical length of pixels of the image
# get center of green on image
def getGreenCenter(img, nx, ny):
	
	# to compute center of green in image
	sumx = 0
	sumy = 0
	divisor = 0

	# look at every pixel in image, if it meets green requirements then add the x and y coordinates to
	# the average to get average location (in other words the center) of the green
	for i in range(nx):
		for j in range(ny):
			if((img.item(j,i,1) > 100) and (img.item(j,i,0) == 0) and (img.item(j,i,2) == 0)):
				sumx += i
				sumy += j
				divisor += 1

	# when no green is found, third parameter of returned list will reflect this	
	if divisor == 0:
		return [0,0,0]
	else:
		averageX = sumx/divisor
		averageY = sumy/divisor
		return [averageX,averageY,1]	

