##################################################
### Real time data plotter in opencv (python)  ###
## Plot integer data for debugging and analysis ##
## Contributors - Vinay @ www.connect.vin       ##
## For more details, check www.github.com/2vin  ##
##################################################

import cv2
import numpy as np

# Plot values in opencv program
class Plotter:
    def __init__(self, plot_width, plot_height):
        self.width = plot_width
        self.height = plot_height
        self.color = (255, 255 ,255)
        self.val = []
        self.plot_canvas = np.ones((self.height, self.width, 3))*0

	# Update new values in plot
    def plot(self, val, label = "plot"):
        self.val.append(int(val))
        while len(self.val) > self.width:
            self.val.pop(0)
        self.show_plot(label)

    # Show plot using opencv imshow
    def show_plot(self, label):
        self.plot_canvas = np.ones((self.height, self.width, 3))*0
        for i in range(len(self.val)-1):
            cv2.line(self.plot_canvas, (i, int(self.height) - self.val[i]), (i+1, int(self.height) - self.val[i+1]), self.color, 3)
        

## Test on sample data
