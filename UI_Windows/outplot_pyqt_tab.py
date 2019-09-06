from __future__ import unicode_literals
from matplotlib.pyplot import figure, show
import sys
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

################################################################
# Mouse events to zoom,pan... on plot
################################################################

class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        

    def zoom_function(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()
            
        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_function(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press
        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()
        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion
    
    def Zoom_Extent(self, ax,xl,yl):
        def ondblClick(event):
            if event.dblclick and event.inaxes == ax:
                # Plotting back to full extent or zoom extent of figure
                ax.set_xlim(0,xl)
                ax.set_ylim(yl,0)
                ax.figure.canvas.draw()
        fig = ax.get_figure()
        fig.canvas.mpl_connect('button_press_event',ondblClick)

################################################################
# Canvas to plot figure
################################################################
class MplCanvas(FigureCanvas):
    def __init__(self,parent,data,dt,rx,rxc):
        self.dt = dt
        self.data = data
        self.fig = plt.figure(figsize=(20, 10), facecolor='w', edgecolor='w')
        self.axis = self.fig.add_subplot(111)
        self.im = self.axis.imshow(data,extent=[0, data.shape[1], data.shape[0] * dt*pow(10,9), 0], 
                         interpolation='nearest', aspect='auto', cmap='seismic', 
                         vmin=-np.amax(np.abs(data)), vmax=np.amax(np.abs(data)))
#        self.im = self.axis.imshow(data,extent=[0, data.shape[1], data.shape[0] * dt*pow(10,9), 0], 
#                         interpolation='nearest', aspect='auto', cmap='seismic')
        self.axis.set_xlabel('Trace number')
        self.axis.set_ylabel('Time [ns]')
        self.axis.grid()
        # Adjusting padding/margins of the plot in all directions 
        self.fig.subplots_adjust(right=0.95,
                                 left=0.07,
                                 top=0.93,
                                 bottom=0.08)
        
        # colorbar Label Based on Data plotted
#        if 'E' in rxc:
#            cb.set_label('Field strength [V/m]')
#        elif 'H' in rxc:
#            cb.set_label('Field strength [A/m]')
#        elif 'I' in rxc:
#            cb.set_label('Current [A]')
#        elif 'P' in rxc:
#            cb.set_label('Power [dB]')
        plt.close(self.fig)
        FigureCanvas.__init__(self, self.fig)    
        self.setParent(None)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)          
        
        # For Zoom and pan functions with mouse buttons
        zp = ZoomPan()
        zp.zoom_function(self.axis, base_scale = 1.1)
        zp.pan_function(self.axis)
        xl,yl= data.shape[1], data.shape[0] * dt*pow(10,9) # Default extent of figure.
        zp.Zoom_Extent(self.axis,xl,yl)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)
        
        # Navigation toolbar
        
        self.Nav_toolbar = NavigationToolbar(self,self)
        # check Box to toggle grid on and off
        grid_cBox = QtWidgets.QCheckBox('Grid', self)
        grid_cBox.move(1300,18)
        grid_cBox.setChecked(True)
        grid_cBox.stateChanged.connect(self.grid_toggle)
        
        t_dist_cBox = QtWidgets.QCheckBox('Depth-Distance*', self)
        t_dist_cBox.move(1000,18)
        t_dist_cBox.stateChanged.connect(self.depth_Distance)
        cBar_cBox = QtWidgets.QCheckBox('Colorbar', self)
        cBar_cBox.move(1200,18)
        cBar_cBox.stateChanged.connect(self.cBar_toggle)
        # adding check box tools to navigation Toolbar
#        self.Nav_toolbar.addWidget(cBar_cBox)
#        self.Nav_toolbar.addWidget(grid_cBox)

    def grid_toggle(self,state):
        if state == QtCore.Qt.Checked:
            self.axis.grid(True)
        else:
            self.axis.grid(False)
    #Funtion to toggle colobar on/off
    def cBar_toggle(self,state):
        if state == QtCore.Qt.Checked:
            self.cb = self.fig.colorbar(self.im) # Adding colorbar
            self.fig.subplots_adjust(right=1.0) # Adjusting Right Padding
        else:
            self.cb.remove() # Removing Colorbar 
            self.fig.subplots_adjust(right=0.95) # Adjusting Right Padding            
    def depth_Distance(self,state):
        if state == QtCore.Qt.Checked:
#            size_x = np.size(self.data,0)
            self.auto_xticks = self.axis.get_xticks()
            self.auto_yticks = self.axis.get_yticks()
            x_labels = []
            y_labels = []
            eps = 5 
            Vel = 3*pow(10,8)/math.sqrt(eps)
            dy = self.dt*Vel/2
            dx = 0.025
#            print(self.dt,'Vel',Vel,'dy',dy,'Depth',dy*512)
#            print('dt:',self.dt,'total time',self.dt*size_x*pow(10,9),
#                  '\n Depth',(self.dt*size_x*Vel/2))
            for i in range(0,np.size(self.auto_xticks)):
                 x_labels.append(str(self.auto_xticks[i]*dx))
            for i in range(0,np.size(self.auto_yticks)):
                 y_labels.append(str(round(self.auto_yticks[i]*dy*10,2)))
            self.axis.set_xticklabels(x_labels)
            self.axis.set_yticklabels(y_labels)
            self.axis.set_ylabel('Appparent depth [m]')
            self.axis.set_xlabel('Distance [m]')
        else:
            self.axis.set_xticklabels(self.auto_xticks)
            self.axis.set_yticklabels(self.auto_yticks)
            self.axis.set_xlabel('Trace number')
            self.axis.set_ylabel('Time [ns]')
    # Function to display x and y positions of mouse pointer
    def on_plot_hover(self,event):
        if self.im.contains(event)[0]:
            x = int(event.xdata)
            y = int(event.ydata)
            
#            Window.self.progressBar.setText('.....')
#            print(self.data[y,x])
#            print(x,y)
#    def mouse_moved(self):
#        print('moved')
#class ApplicationWindow(QtWidgets.QMainWindow):
#    def __init__(self):
#        QtWidgets.QMainWindow.__init__(self)
#        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
##        self.setWindowTitle("application main window")
#        self.main_widget = QtWidgets.QWidget(self)
#        self.gridLayout = QtWidgets.QGridLayout(self.main_widget)
#        self.tabWidget = QtWidgets.QTabWidget(self.main_widget)
#        self.tabWidget.setTabsClosable(True)
#        self.tabWidget.setMovable(True)
#        self.tabWidget.tabCloseRequested.connect(self.close_tab)
#        self.gridLayout.addWidget(self.tabWidget)
##        self.main_widget.setFocus()
#        self.setCentralWidget(self.main_widget)  
#        add_tab(self)
#        layout = QtWidgets.QVBoxLayout(self.tab)
#        data = np.random.random((1000,2000))
#        dt = 0.000000034
#        rx = 1
#        rxc = 'E'
#        plot_canvas = MplCanvas(self.tab,data,dt,rx,rxc)
#        layout.addWidget(plot_canvas)
#        self.tabWidget.setFocus()
#        self.setCentralWidget(self.tabWidget)
#        
#    def close_tab(self,index):    
#        self.tabWidget.removeTab(index)
#            
#def add_tab(ApplicationWindow):
#    ApplicationWindow.tab = QtWidgets.QWidget()
#    ApplicationWindow.tabWidget.addTab(ApplicationWindow.tab, "Title")
#
#
#qApp = QtWidgets.QApplication(sys.argv)
#aw = ApplicationWindow()
##aw.setWindowTitle("%s" % progname)
#
#aw.show()
#sys.exit(qApp.exec_())
##qApp.exec_()
#
#
