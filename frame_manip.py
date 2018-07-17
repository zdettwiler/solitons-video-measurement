from __future__ import division
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt

x_boundary_min = 370
x_boundary_max = 440#400 #+70
y_boundary_min = 280#240
y_boundary_max = 320#280 #+40

def greyscale(frame):
	''' Receives a colour RGB frame.
		Returns a greyscale frame. '''

	greyscale = np.zeros((len(frame), len(frame[0])), dtype='uint8')
	for i in range(len(greyscale)):
		for j in range(len(greyscale[0])):
			# ITU-R 601-2 luma transform
			greyscale[i,j] = frame[i,j,0] * 299/1000 + frame[i,j,1] * 587/1000 + frame[i,j,2] * 114/1000

	return greyscale

def binary_frame(frame, bg_sensitivity):
	''' Receives a greyscale frame.
		Returns a binary frame (only black or white pixels). '''
	threshold = bg_sensitivity*np.average(frame) # bg_sensitivity * np.max(frame)
	binary_frame = np.zeros((frame.shape), dtype='uint8')

	for i in range(len(frame)):
		for j in range(len(frame[0])):
			if frame[i,j] > threshold:
				binary_frame[i,j] = 255#1

	return binary_frame

def calibration(frame):
	''' Receives a binary frame[y,x].
		Returns the height of the 8cm graduation on the ruler
			or, if not found, the middle of the frame. '''

	for y in range(len(frame)):
		if frame[y,len(frame[0])/2] == 0: # for binary_frame, 0=black, 1=white
			eight_cm = y+2 # graduation 8cm. 2px adjustmen to reach the middle of the line.
			break
		else:
			eight_cm = int(len(frame)/2)

	return eight_cm


def graduation(frame, eight_cm, px_per_mm, eta=0):
	''' Receives a greyscale image.
		Returns a graduated frame. '''

	px_per_mm = 11
	for y in range(eight_cm,0,-px_per_mm):
		frame[y:y+2,350:360]=255 # makes horizontal white graduations below the 8cm graduation.

	for y in range(eight_cm,len(frame),px_per_mm):
		frame[y:y+2,350:360]=255 # makes horizontal white graduations above the 8cm graduation.

	frame[eight_cm:eight_cm+3,350:370] = 200 # makes graduation for the 8cm mark.
	frame[eta:eta+3,300:350] = 255 # makes graduation for the water level (eta)

	# make a box around the calibration zone
	frame[y_boundary_max,                x_boundary_min:x_boundary_max] = 255
	frame[y_boundary_min:y_boundary_max, x_boundary_max]                = 255
	frame[y_boundary_min,                x_boundary_min:x_boundary_max+1] = 255
	frame[y_boundary_min:y_boundary_max, x_boundary_min]                = 255

	return frame

def eta_measure(frame, eight_cm, px_per_mm):
	''' Receives a binary_frame. '''
	contours = plt.contour(frame, 2, origin='lower')
	cntr = contours.collections[0].get_paths()[0].vertices
	for i in range(len(cntr)):
		if int(cntr[i,0])==300:#200:
			water_h = cntr[i,1]

	for coll in contours.collections:
		plt.gca().collections.remove(coll)
	# print ' -- water_h = ', water_h
	return water_h#((80 - (water_h-eight_cm)/px_per_mm)/10)

def save_to_file(filename, time, height):
	log_file = open(filename, "wb")
	for i in range(len(time)):
		log_file.write('%.3f	%.2f\r\n' %(time[i], height[i]))
		# log_file.write("\n")
	log_file.close()
