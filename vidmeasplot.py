from __future__ import division
from moviepy.editor import VideoFileClip
from PIL import Image
import numpy as np
from scipy import misc
import time as timer
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import frame_manip as fm

# Calibration zone and other settings
x_boundary_min = 370
x_boundary_max = 440
y_boundary_min = 280
y_boundary_max = 320
px_per_mm = 11
clip_nb = 90


def update_progress(progress, item, total):
    print "\r {0}: [{1:15s}] {2:.1f}%	{3}/{4} frames".format(progress, '#' * int((item/total) * 15), (item/total) * 100, item, int(total)),

# data=np.loadtxt('../data/wp50_1-3MAR.txt')
# t = data[:,0] # s
# h = data[:,1] # cm

time = np.zeros(0)
height = np.zeros(0)

# clip = VideoFileClip('../../Solitons/Videos/Week 6/%ideg.wmv'%clip_nb, audio=False)
clip = VideoFileClip('../Videos/Week 5/90.wmv', audio=False)
# f, (ax1, ax2) = plt.subplots(2,1)

# SET UP PLOT
f = plt.figure()
ax1 = plt.subplot2grid((3,5), (0,0), colspan=5)
ax2 = plt.subplot2grid((3,5), (1,0), colspan=4, rowspan=2)
ax3 = plt.subplot2grid((3,5), (1,4), rowspan=2)

# data plot
ax1.set_ylim(4,10)
# ax1.plot(t, h, 'ro', mec='r')
plot, = ax1.plot(time, height, 'bo', mec='b')
text = ax1.text(0.9,0.1,'5', transform=ax1.transAxes)

# frame plot
view = ax2.imshow(misc.imread('frame.png'), interpolation='nearest', cmap='gray')

# calibration plot
ax3.set_xlim(0, x_boundary_max - x_boundary_min)
ax3.set_ylim(y_boundary_max - y_boundary_min, 0)
vcalib = ax3.imshow(misc.imread('calib.png'), interpolation='nearest', cmap='gray', origin='upper')

plt.ion()

# Go through all the frames of the video
frame_nb = 0
for frame in clip.iter_frames():
	start = timer.time()
	frame_nb = frame_nb + 1
	update_progress('measuring', frame_nb, clip.duration*clip.fps)

	# Update plot
	f.canvas.set_window_title('%ideg.wmv - %.1f'%(clip_nb,(frame_nb/(clip.duration*clip.fps))*100))
	ax1.set_xlim(frame_nb/clip.fps - 5,frame_nb/clip.fps + 1)

	# Convert Frame to Greyscale
	frame = np.array(Image.fromarray(frame).convert('L'))

	calib_zone = frame[y_boundary_min:y_boundary_max, x_boundary_min:x_boundary_max]
	calib_zone = fm.binary_frame(calib_zone, 0.90)
	# misc.imsave('calib.png', calib_zone)

	# Make measurements
	eight_cm = fm.calibration(calib_zone) # position of the 8cm graduation relative to calibration zone.
	eight_cm = eight_cm + y_boundary_min # position of the 8cm relative to frame.

	eta = fm.eta_measure(frame, eight_cm, px_per_mm) # measure water level from frame
	frame = fm.graduation(frame, eight_cm, px_per_mm, eta) # make graduation on frame

	# Add newly measure data point to plot
	time = np.append(time, frame_nb/clip.fps)
	height = np.append(height, ((80 - (eta-eight_cm)/px_per_mm)/10))

	# Update plot
	view.set_data(frame)
	vcalib.set_data(calib_zone)
	plot.set_data(time, height)
	text.set_text('%.2fcm' %(height[-1]))
	plt.draw()

	end = timer.time()
	# print ' -- calculation time: %.2fs' % (end-start)
	plt.pause(0.000001)

# plt.savefig('fig25deg.png')
fm.save_to_file('%i.txt'%clip_nb, time, height)
