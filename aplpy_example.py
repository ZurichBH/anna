#short python routine which uses aplpy to
#plot a series of stamps in fits format
#you might want to adjust the figure size depending on
#how big your plot is meant to be and how big your images are

#aplpy website: http://aplpy.github.io
#aplpy documentation: http://aplpy.readthedocs.org/en/v0.9.11/

#!!careful: I'm using tabs here!!

import matplotlib
#change matplotlib backend for inactive use of aplpy
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
import copy
import os
import aplpy


#------------------------------------------------------------
def plot(or_parameters):

	para = copy.copy(or_parameters)

	#number of subplots needed
	num_plots = len(para['imglist'])
	
	#create figure
	f = plt.figure(facecolor='w', figsize=(1.6*num_plots, 2.5), dpi=600)

	#create gridspec (very useful for multiple subplots)
	#here we're creating one row with num_plots columns
	gs = gridspec.GridSpec(1, num_plots)

	for i in range(0, num_plots):

		#create axis for each subplot
		ax = plt.subplot(gs[0, i])
		#create quadratic plots
		ax.set_aspect('equal')
		#turn off ticks
		ax.axes.get_xaxis().set_ticks([]); ax.axes.get_yaxis().set_ticks([])
		#update canvas before filling it with images 
		#(equal aspect will now be applied)
		f.canvas.draw()

		if para['label']:
			ax.set_title(para['labellist'][i], size = 18, fontname = 'serif')
		#update canvas again
		f.canvas.draw()

		#check if image really exists
		if os.path.exists(para['imglist'][i]):

			print 'Plotting :', para['imglist'][i]

			#create aplpy figure
			fa = aplpy.FITSFigure(para['imglist'][i], figure = f, 
				subplot = list(ax.get_position().bounds))
			#use grayscale and invert image, use same scaling for all images (sqrt)
			fa.show_grayscale(invert = True, stretch = 'sqrt', vmin = 0)

			#hide axis and tick labels 
			#(makes everything confusing if you're showing many plots)
			fa.axis_labels.hide_x()
			fa.axis_labels.hide_y()
			fa.tick_labels.hide_x()
			fa.tick_labels.hide_y()
			#but do show little ticks
			fa.ticks.show_x()
			fa.ticks.show_y()

			if para['scalebar']:

				#convert scalebar size into deg
				fa.add_scalebar(para['scalebar_size']/3600.)
				fa.scalebar.show(para['scalebar_size']/3600.)
				#determine position of scalebar
				fa.scalebar.set_corner('top left')
				#set linewidth
				fa.scalebar.set_linewidth(3)
				#set color (white might be useful if you're not inverting your images)
				fa.scalebar.set_color('black')
				#set font and fontsize of scalebar
				fa.scalebar.set_font(size = 'medium', style = 'normal')
				#set label
				fa.scalebar.set_label(str(para['scalebar_size'])+'"')

			if para['circle']:
				fa.show_circles(para['circle_pos'][0], para['circle_pos'][1], 
					para['circle_rad']/3600., linewidth=1, color=para['circle_color'])
		#print error message if image doesn't exist
		else:
			print para['imglist'][i], ' does not exist!'

	#save figure
	f.savefig(para['output_path'])

#------------------------------------------------------------
#set input parameters

para = {}
#list of images including path
para['imglist'] = ['150_b_stamp.fits', '150_v_stamp.fits', 
'150_i_stamp.fits', '150_z_stamp.fits',
'150_f105w_stamp.fits', '150_f125w_stamp.fits', '150_f160w_stamp.fits']

#do you want labels above your images?
para['label'] = True
#list with labels, should be the same length as imglist
para['labellist'] = ['B', 'V', 'i', 'z', 'Y', 'J', 'H']

#do you want to show a scalebar?
para['scalebar'] = True
#size of scalebar in arcseconds
para['scalebar_size'] = 2

#do you want to show a circle, e.g. to highlight the position of your object?
para['circle'] = True
#circle radius in arcsec
para['circle_rad'] = 1
#position of circle RA, DEC in deg
para['circle_pos'] = [53.0399583333, -27.7984722222]
#circle color
para['circle_color'] = 'magenta'

#ouput path for plot
para['output_path'] = 'aplpy_example.eps'

plot(para)
