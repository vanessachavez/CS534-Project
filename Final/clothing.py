from PIL import Image
import cv2
import numpy as np
import sys

# Author: Teryl Schmidt
# Contact: tschmidt6@wisc.edu
# Date: 2018

# How to run:
# The two pictures that you want the shirt swapped should be named 'background1.jpg' and 'background2.jpg'
# You can use the shell script: $sh runClothing.sh
# Or you can type: $python clothing.py 
# Then use the other script: $sh Clean.sh


# Function to overlay a transparent image on background
def transparentOverlay(src , overlay , pos=(0,0),scale = 1):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay,(0,0),fx=scale,fy=scale)
    h,w,_ = overlay.shape  # Size of foreground
    rows,cols,_ = src.shape  # Size of background Image
    y,x = pos[0],pos[1]    # Position of foreground/overlay image
    
    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x+i >= rows or y+j >= cols:
                continue
            alpha = float(overlay[i][j][3]/255.0) # read the alpha channel 
            src[x+i][y+j] = alpha*overlay[i][j][:3]+(1-alpha)*src[x+i][y+j]
    return src

# Function to turn black pixels transparent
def removeBlack(infile, outfile):
	img = Image.open(infile)
	img = img.convert("RGBA")
	datas = img.getdata()

	newData = []
	for item in datas:
    		if item[0] == 0 and item[1] == 0 and item[2] == 0:
        		newData.append((0, 0, 0, 0))
    		else:
        		newData.append(item)

	img.putdata(newData)
	img.save(outfile, "PNG")


def main():
    try:

    # ----------------------- Read In The Files ----------------------- #

    	# Open the background picture (you standing there) 
        #background = cv2.imread('background.png') # background = cv2.imread(sys.argv[1])
        background1 = cv2.imread('background1.jpg')
        background2 = cv2.imread('background2.jpg')

        background1 = cv2.resize(background1, (300,500))
        background2 = cv2.resize(background2, (300,500))


 	# NOTE: Requires the mask of the image generated using Fashion.py

	# Put a bounding box around the ROI (Region of Intrest) in the backgroundmask.jpg
	# Gets the coordinates of the bounding box as:
	# x: Distance from the left side of background.jpg to the left edge of the bounding box
	# y: Distance from the top of background.jpg to the top edge of the bounding box
	# w: Total width of the bounding box
	# h: Total height of the bounding box

    # ----------------------- Put Bounding Box Around Object ----------------------- #
    # Need both x,y,w,h coordinates so for now having double is ok
	backgroundmask = cv2.imread('background1mask.png')
	active_px = np.argwhere(backgroundmask!=0)
	active_px = active_px[:,[1,0]]
	x,y,w,h = cv2.boundingRect(active_px)
	roi1 = backgroundmask[y:y+h, x:x+w]
	cv2.imwrite('roi1.png', roi1) # Crop picture to only contain the ROI
	cv2.rectangle(backgroundmask,(x,y),(x+w,y+h),(255,0,0),1)
	cv2.imwrite('backgroundbounding1.png', backgroundmask)

	backgroundmask2 = cv2.imread('background2mask.png')
	active_px = np.argwhere(backgroundmask2!=0)
	active_px = active_px[:,[1,0]]
	x2,y2,w2,h2 = cv2.boundingRect(active_px)
	roi2 = backgroundmask2[y2:y2+h2, x2:x2+w2]
	cv2.imwrite('roi2.png', roi2) # Crop picture to only contain the ROI
	cv2.rectangle(backgroundmask2,(x2,y2),(x2+w2,y2+h2),(255,0,0),1)
	cv2.imwrite('backgroundbounding2.png', backgroundmask2)


  	# ----------------------- Change Black Pixels to Transparent ----------------------- #
	removeBlack('roi1.png', 'roiExtract1.png')
	removeBlack('roi2.png', 'roiExtract2.png')
	

	# ----------------------- Place Image onto background ----------------------- #
	# Overlay the foreground image onto the background image where the bounding box (x,y) coordinates are
	resizedforeground1 = cv2.imread('roiExtract1.png', cv2.IMREAD_UNCHANGED)
	resizedforeground2 = cv2.imread('roiExtract2.png', cv2.IMREAD_UNCHANGED) 

	# Background must be JPG read in using: cv2.imread('filename.jpg')
	# Foreground must be PNG read in using: cv2.imread('filename.png', cv2.IMREAD_UNCHANGED)
	output1 = transparentOverlay(background1, resizedforeground2, (x,y), 1)
	output2 = transparentOverlay(background2, resizedforeground1, (x2,y2), 1)

	cv2.imwrite('Output1.png', output1)
	cv2.imwrite('Output2.png', output2)


	# ----------------------- Display the result ----------------------- # 
	# Comment this out if you don't want a popup window in the output
	
	# cv2.imshow("Output1" , output1)
	# cv2.imshow("Output2" , output2)
	# cv2.waitKey()
	# cv2.destroyAllWindows()

    except IOError:
        pass


if __name__ == "__main__":
    main()
