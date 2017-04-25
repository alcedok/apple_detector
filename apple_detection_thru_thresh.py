"""
============================================
Apple Detection Thru Thresholding and
Morphological Operations
============================================
author: @kevin_alcedo
Fall 2015 

"""

'''
The following script performs thresholding 
on a pre-set range of color in HSV color-space
converting the input RGB inmage to binary.
It then performs morphological operations on 
the binary results, removing noise and clumping
blobs of interest. The script concludes by 
executing blob analysis on the image and
displaying the detected objects with circles. 

Dependencies: 
	python 2.7.x
	OpenCV 2.4.X
	numpy  1.9.X	

How to run:
python script.py inputfolder/inputname.jpg outputfolder

File structure:
script.py
| inputfolder
|| inputname.jpg
| outputfolder
|| outputname.jpg

'''
print(__doc__)
import cv2
import numpy as np
import sys


def color_extraction(img):

	# convert to HSV color-space
	img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# colors of interest and mask those outside
	lower_red = np.array([0,50,50])
	upper_red = np.array([10,255,255])
	mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
 
	lower_red = np.array([170,50,50])
	upper_red = np.array([180,255,255])
	mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

	# join masks
	mask = mask0+mask1

	# set output img to zero everywhere except my mask
	output_img = img.copy()
	output_img[np.where(mask==0)] = 0
	return output_img

def morph_ops(binary_img):

	# structural element defined as a circle
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

	# transform image by opening
	# this is useful for removing noise and small specks in image
	open_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel,iterations = 3)

	# transform image by closing 
	# this is useful for closing small holes inside foreground objects
	close_img = cv2.morphologyEx(open_img, cv2.MORPH_CLOSE, kernel,iterations = 3)

	return close_img

def contours(image):

	# functions finds countours and keeps each in a list
	contours, hierarchy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	
	# minimum area of apple (assuming circle): pi*(r*r), r in pixels
	filtered_contours = []

	# create an objct to hold indeces of countours
	number_of_contours = np.ndindex(np.shape(contours)[0])
	min_area = (3.14)*(2*2)
	max_area = (3.14)*(10*10)

	# go through contours and filter out small objects
	for index in number_of_contours:
		# if the area of the contour is between the desired range then keep it 
		if (cv2.contourArea(contours[index[0]]) > min_area) and (cv2.contourArea(contours[index[0]]) < max_area):
			filtered_contours = filtered_contours + [contours[index[0]]]

	# total number of detected objects
	number_detected = np.shape(filtered_contours)[0]

	return number_detected,filtered_contours

def resize_for_display(image):
	# this function is useful for resizing output

	h,w = orig_img.shape[:2]
	if h > 800:
		ratio = 800.0 / w
		new_dimension = (800 , int(h*ratio))
		resized_image = cv2.resize(image , new_dimension , interpolation = cv2.INTER_AREA) 
		return resized_image
	else:
		return image

if __name__ == '__main__':
	# check for correct user input 
	if len(sys.argv) != 3:
		print ('function must be called with: python apple_detection_thru_thresh.py inputfolder/inputname.jpg outputfolder')
		sys.exit(1)

	input_filename_and_path = sys.argv[1]
	file_path = (input_filename_and_path.split('/'))[0]
	filename = (input_filename_and_path.split('/'))[1]

	output_path = sys.argv[2]


	# read image from subfolder
	file_path = filename
	
	# read image	
	orig_img = cv2.imread(input_filename_and_path)

	# threshold image by color
	segmented_img = color_extraction(orig_img)

	# display output of segmentation
	resized_segmented_img = resize_for_display(segmented_img)
	cv2.imshow("contour_1", resized_segmented_img)
	# uncomment to save this output
	# cv2.imwrite(output_path+'/'+'segmented_'+filename,np.asarray(segmented_img))

	# convert segmented image into binary 
	gray_img = cv2.cvtColor(segmented_img,cv2.COLOR_BGR2GRAY)
	thresh, binary_img = cv2.threshold(gray_img, 0, 255 , cv2.THRESH_BINARY)

	# perform morphological operations on binary image
	morphed_img = morph_ops(binary_img)

	# display output of morphological segmentation
	resized_morphed_img = resize_for_display(morphed_img)
	cv2.imshow("contour_2", resized_morphed_img)
	# uncomment to save this output
	# cv2.imwrite(output_path+'/'+'blob_'+filename,np.asarray(morphed_img))

	# find contours that satisfy criteria
	number_detected,filtered_contours = contours(morphed_img)

	print "---"
	print number_detected, " objects detected"
	print "---"

	# draw circles on detected blobs
	for contour in filtered_contours: 
		(x,y),radius = cv2.minEnclosingCircle(contour)
		center = (int(x),int(y))
		radius = int(radius)
		cv2.circle(orig_img,center,radius,(0,255,0),2)

	# display output after detection
	im_resize = resize_for_display(orig_img)
	cv2.imshow("contour", im_resize)

	#save output
	cv2.imwrite(output_path+'/'+filename,orig_img)

	# hit key to close images
	cv2.waitKey(0)
