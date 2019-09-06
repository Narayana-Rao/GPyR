

"""
    This is a Basic level Ground Penetrating Radar (GPR) data processing GUI.
    
    *Requirements
     -bitstruct
     -h5py
     -PyQt5

"""


import h5py
import sys
import numpy as np
from os import path
from PyQt5 import QtGui, QtWidgets,QtCore

# Local Scripts


from IO.read_out import get_output_data
from Processing.Filters import (mean_removal_func, median_removal_func, time_gain_func, 
                     median_Filter_func, gauss_Filter_func,
                     FIR_lp_func, FIR_hp_func,FIR_bp_func,FIR_bs_func,
                     field_to_Power_func)
from IO.read_DZT import readgssi
import UI_Windows.Median_Filter_Window_size as Median_Filter_Window_size
import UI_Windows.FIR_LHP as FIR_LHP
import UI_Windows.FIR_B_PS as FIR_B_PS
from UI_Windows.outplot_pyqt_tab import MplCanvas as mplt_plot

################ Main Window Class ######################
class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setGeometry(100, 100, 1500, 900)
#        self.showFullScreen()
#        self.showMaximized()

        self.setWindowTitle("GPyR")
        self.setWindowIcon(QtGui.QIcon('./icons/Main_window_icon.png'))
        self.statusBar()
        self.menu()
        self.center()
        self.progressBar = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setFixedSize(250,30)
        self.statusBar().showMessage('Ready')

        # Variables
        self.f_type = None
        self.t_index  = None
        self.data_avail  = {}
        self.data_list = []
        self.raw_data = None
        self.header = None
        self.fname = None
        self.rx = None
        self.rx_component = None

##############################################################################         
    def menu(self):
        
        """""""""""""""
        Tab Widget for Plotting
        """""""""""""""
        self.main_widget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.main_widget)
        self.tabWidget = QtWidgets.QTabWidget(self.main_widget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.gridLayout.addWidget(self.tabWidget)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)  
        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.tab = QtWidgets.QWidget()    
        
        """""""""""""""
        Tool Bars
        """""""""""""""
        extractAction1 = QtWidgets.QAction(QtGui.QIcon('./icons/fileopen.png'), 'Open File', self)
        extractAction2 = QtWidgets.QAction(QtGui.QIcon('./icons/save.png'), 'Save File', self)
        
        self.toolBar1 = self.addToolBar("File Operations")
        self.toolBar1.addAction(extractAction1)
        extractAction1.triggered.connect(self.File_Open_window)
        self.toolBar1.addAction(extractAction2)


        #########
        extractAction1_t2 = QtWidgets.QAction(QtGui.QIcon('./icons/Test3.png'), 'Test', self)
        extractAction2_t2 = QtWidgets.QAction(QtGui.QIcon('./icons/Test4.png'), 'Test', self)       
        self.toolBar2 = self.addToolBar("Filters2")
        self.toolBar2.addAction(extractAction1_t2)
        extractAction1_t2.triggered.connect(self.add_tab)
        self.toolBar2.addAction(extractAction2_t2)
        #########

        """""""""""""""
        Main Menu 
        """""""""""""""
        '''File Menu'''
        File_open = QtWidgets.QAction("Open", self)
        File_open.setShortcut("Ctrl+O")
        File_open.setStatusTip('Open a File')
        File_open.triggered.connect(self.File_Open_window)
        
        File_saveas = QtWidgets.QAction("Save as", self)
        File_saveas.setShortcut("Ctrl+s")
        File_saveas.setStatusTip('Save File')
        
        File_Exit = QtWidgets.QAction("Exit", self)
        File_Exit.setShortcut("Ctrl+Q")
        File_Exit.setStatusTip('Leave the App')
        File_Exit.triggered.connect(self.close_application)
        
        '''Process Menu'''
        trim_Data = QtWidgets.QAction("Trim Data*", self)
        trim_Data.setStatusTip('Trim Data*')
        trim_Data.triggered.connect(self.trim_Data)
        
        field_to_Pow = QtWidgets.QAction("Field strength to Power (dB)", self)
        field_to_Pow.setStatusTip('Field strength to Power (dB)')
        field_to_Pow.triggered.connect(self.field_to_Power)
        
        
        mean_removal = QtWidgets.QAction("Mean Removal", self)
        mean_removal.setStatusTip('Mean Removal')
        mean_removal.triggered.connect(self.mean_R)
        
        median_removal = QtWidgets.QAction("Median Removal", self)
        median_removal.setStatusTip('Median Removal')
        median_removal.triggered.connect(self.median_R)
        
        time_Gain = QtWidgets.QAction("Time Gain", self)
        time_Gain.setStatusTip('Time Gain')
        time_Gain.triggered.connect(self.time_gain)
        
        median_Filter = QtWidgets.QAction("Median Filter", self)
        median_Filter.setStatusTip('Median Filter')
        median_Filter.triggered.connect(self.median_Filter_callBack)
        
        gauss_Filter = QtWidgets.QAction("Gaussian Filter", self)
        gauss_Filter.setStatusTip('Gaussian Filter')
        gauss_Filter.triggered.connect(self.gauss_Filter_callBack)
        
        FIR_lp = QtWidgets.QAction("Lowpass", self)
        FIR_lp.setStatusTip('FIR Lowpass Filter')
        FIR_lp.triggered.connect(self.FIR_lp_callBack)
        
        FIR_hp = QtWidgets.QAction("Highpass", self)
        FIR_hp.setStatusTip('FIR Highpass Filter')
        FIR_hp.triggered.connect(self.FIR_hp_callBack)              
        
        FIR_bp = QtWidgets.QAction("Bandpass", self)
        FIR_bp.setStatusTip('FIR bandpass Filter')
        FIR_bp.triggered.connect(self.FIR_bp_callBack)   
        
        FIR_bs = QtWidgets.QAction("Bandstop", self)
        FIR_bs.setStatusTip('FIR bandstop Filter')
        FIR_bs.triggered.connect(self.FIR_bs_callBack)   
        
        about = QtWidgets.QAction("About", self)
        about.setShortcut("f10")
        about.setStatusTip('About')
        about.triggered.connect(self.about)
        documentation = QtWidgets.QAction("Documentation", self)
        documentation.setShortcut("f1")
        documentation.setStatusTip('Documentation')
        
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(File_open)
        fileMenu.addAction(File_saveas)
        fileMenu.addSeparator()
        fileMenu.addAction(File_Exit)
        
        
        processMenu = mainMenu.addMenu('&Process')
        FIR = QtWidgets.QMenu("FIR Filter", self)
        global_remove = QtWidgets.QMenu("Global remove", self) 
        processMenu.addAction(trim_Data)
        processMenu.addAction(field_to_Pow)
        processMenu.addAction(time_Gain)
        processMenu.addAction(median_Filter)
        processMenu.addAction(gauss_Filter)
        processMenu.addMenu(global_remove)
        global_remove.addAction(mean_removal)
        global_remove.addAction(median_removal)
        processMenu.addSeparator()
        processMenu.addMenu(FIR)
        FIR.addAction(FIR_lp)
        FIR.addAction(FIR_hp)
        FIR.addAction(FIR_bp)
        FIR.addAction(FIR_bs)
        
        '''Window Menu''' 
        windowMenu = mainMenu.addMenu('&Window')
        
        w_windows_style = QtWidgets.QAction("Windows", self)
        w_windows_style.setStatusTip('Change Window Style to Windows')
        w_windows_style.triggered.connect(lambda: self.set_Style('windows'))
        
        w_Fusion_style = QtWidgets.QAction("Fusion", self)
        w_Fusion_style.setStatusTip('Change Window Style to Fusion')
        w_Fusion_style.triggered.connect(lambda: self.set_Style('Fusion'))
        
        w_wVista_style = QtWidgets.QAction("Windows Vista", self)
        w_wVista_style.setStatusTip('Change Window Style to windows Vista')
        w_wVista_style.triggered.connect(lambda: self.set_Style('WindowsVista'))
        
        window_style  = QtWidgets.QMenu("Window style", self)
        windowMenu.addMenu(window_style)
        window_style.addAction(w_windows_style)
        window_style.addAction(w_Fusion_style)
        window_style.addAction(w_wVista_style)
        '''Help Menu'''
        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(documentation)
        helpMenu.addAction(about)
        
        
###############################################################################
        '''Main menu Callback Functions''' 
############################################################################### 

    def File_Open_window(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a File',
                                                          filter=
                                                          "gprMax file (*.out);;GSSI File (*.DZT);;All (*)")
        if file_name[0]:
            self.fname = file_name[0]
            self.f_type = path.splitext(file_name[0])
            (self.directory, self.filename) = path.split(self.fname)
            
            if self.f_type[1]=='.out' :
                f = h5py.File(self.fname, 'r')
                self.nrx = f.attrs['nrx']
                f.close()
                rx_c_list = ('Ez','Ex','Ey','Hx','Hy','Hz','Ix','Iy','Iz')
                self.rx_component, ok = QtWidgets.QInputDialog.getItem(self,"Select component to plot",
                                                                       "Rx Component",rx_c_list,0,False) 
                if ok:
                    for self.rx in range(1, self.nrx + 1):
                        self.raw_data, self.dt = get_output_data(self.fname, self.rx, self.rx_component)
                        tab_Var = mplt_plot(self.tab,self.raw_data,self.dt,self.rx,self.rx_component)
                        self.t_index = self.tabWidget.addTab(tab_Var, str(self.filename))
                        self.tabWidget.setCurrentIndex(self.t_index)
#                        out_plot(self.fname,self.raw_data,self.dt,self.rx,self.rx_component)
                        self.data_avail['Raw Data']= self.raw_data
                        if 'Raw Data' not in self.data_list:
                            self.data_list.append('Raw Data')
                        print(np.min(self.raw_data),np.max(self.raw_data))

            elif self.f_type[1]=='.DZT':
                (self.directory, self.filename) = path.split(self.fname)
                self.header, self.raw_data = readgssi(self.fname)
                print(np.min(self.raw_data),np.max(self.raw_data))
                self.data_avail['Raw Data']= self.raw_data
                if 'Raw Data' not in self.data_list:
                    self.data_list.append('Raw Data')
                self.dt=(self.header['rhf_range']/(self.header['rh_nsamp']-1))*pow(10,-9)
                self.rx = 1
                self.nrx = 1
                self.rx_component = 'Ez'
                tab_Var = mplt_plot(self.tab,self.raw_data,self.dt,self.rx,self.rx_component)
                self.t_index = self.tabWidget.addTab(tab_Var, str(self.filename))
                self.tabWidget.setCurrentIndex(self.t_index)
                print(' File                   : ',self.header['infile'],'\n',
                      'Antenna                : ',self.header['rh_antname'],'\n',
                      'Bit Rate               : ',self.header['rh_bits'],'\n',
                      'Scans per Second       : ',self.header['rhf_sps'],'\n',
                      'Samples per Scan       : ',self.header['rh_nsamp'],'\n',
                      'Sampling interval (ns) : ',self.dt*pow(10,9),'\n',
                      'Range in ns            : ',self.header['rhf_range'],'\n',
                      'Scans per pass         : ',self.header['rh_npass'],'\n',
                      'Scans per m            : ',self.header['rhf_spm'],'\n',
                      'Scan Spacing           : ',1/self.header['rhf_spm'],'\n',
                      'Di-electric Const      : ',self.header['rhf_epsr'],'\n',
                      'Appearent Depth(m)     : ',self.header['rhf_depth'],'\n')
#                print(self.header)  
            elif self.f_type[1] and self.raw_data is None:
                QtWidgets.QMessageBox.warning(self,'File Type Error!',
                                                   'Invalid file Type \nPlease select valid file',
                                                   QtWidgets.QMessageBox.Ok)

        elif self.raw_data is None:
            self.infile_error()

    def close_application(self):
        choice = QtWidgets.QMessageBox.question(self, 'Warning!',
                                            "Do you really want to Exit?",
                                            QtWidgets.QMessageBox.Yes | 
                                            QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("App Closed!")
            sys.exit()
        else:
            pass
    def trim_Data(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:
                xmin,xmax,ymin,ymax = 0,300,0,300
                Data = self.data_avail[str(data_var)]
                tr_Data = Data[xmin:xmax,ymin:ymax]
                self.data_avail['Trimmed Data']= tr_Data # Updating available datasets
                if 'Trimmed Data' not in self.data_list:
                    self.data_list.append('Trimmed Data')#Updating the available dataset list
                tab_Var = mplt_plot(self.tab,tr_Data,self.dt,self.rx,self.rx_component)
                self.t_index = self.tabWidget.addTab(tab_Var, 'Trimmed Data')
                self.tabWidget.setCurrentIndex(self.t_index)   
                
    def mean_R(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:
                mean_r_data = mean_removal_func('Mean trace Removed',
                              self.data_avail[str(data_var)],self.dt,self.nrx,self.rx_component)
                self.data_avail['Mean Removed Data']= mean_r_data # Updating available datasets
                if 'Mean Removed Data' not in self.data_list:
                    self.data_list.append('Mean Removed Data')#Updating the available dataset list
                tab_Var = mplt_plot(self.tab,mean_r_data,self.dt,self.rx,self.rx_component)
                self.t_index = self.tabWidget.addTab(tab_Var, 'Mean Trace Removed')
                self.tabWidget.setCurrentIndex(self.t_index)

    def median_R(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:
                median_r_Data = median_removal_func('Median trace Removed',
                                self.data_avail[str(data_var)],self.dt,self.nrx,self.rx_component)
                self.data_avail['Median Removed Data']= median_r_Data # Updating available datasets
                if 'Median Removed Data' not in self.data_list:
                    self.data_list.append('Median Removed Data') #Updating the available dataset list
                tab_Var = mplt_plot(self.tab,median_r_Data,self.dt,self.rx,self.rx_component)
                self.t_index = self.tabWidget.addTab(tab_Var, 'Median Trace Removed')
                self.tabWidget.setCurrentIndex(self.t_index)
                
    def field_to_Power(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:
                self.dx, okPressed = QtWidgets.QInputDialog.getDouble(self,
                                     "Enter dx(m)","Descretisation Size (m)",0.002,0.0001,0.5,4)
                if self.dx and okPressed:
                    f_Power = field_to_Power_func('Power (dB)',
                              self.data_avail[str(data_var)],self.dt,self.nrx,self.rx_component,self.dx)
                    self.data_avail['Field Power(dB)']= f_Power # Updating available datasets
                    if 'Field Power(dB)' not in self.data_list:
                        self.data_list.append('Field Power(dB)') #Updating the available dataset list
                    tab_Var = mplt_plot(self.tab,f_Power,self.dt,self.rx,'P')
                    self.t_index = self.tabWidget.addTab(tab_Var, 'Converted Powerplot (dB) for dx = '+str(self.dx))
                    self.tabWidget.setCurrentIndex(self.t_index)
    def time_gain(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:
                time_pow, okPressed = QtWidgets.QInputDialog.getDouble(self,
                                      "Enter time Power","Time Power",2,0.1,20,4)
                if time_pow:
                    t_Data  = time_gain_func('Time Gain '+ str(time_pow)+'Applied',
                                   self.data_avail[str(data_var)],self.dt,self.nrx,self.rx_component,time_pow)
                    self.data_avail['Time Gain Applied Data']= t_Data # Updating available datasets
                    if 'Time Gain Applied Data' not in self.data_list:
                        self.data_list.append('Time Gain Applied Data') #Updating the available dataset list
                    tab_Var = mplt_plot(self.tab,t_Data,self.dt,self.rx,self.rx_component)
                    self.t_index = self.tabWidget.addTab(tab_Var, 'Time Gain Applied with ''t''power = '+str(time_pow))
                    self.tabWidget.setCurrentIndex(self.t_index)

    def median_Filter_callBack(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:
                input_dialog = QtWidgets.QDialog()
                input_ui = Median_Filter_Window_size.Ui_dialog()
                input_ui.setupUi(input_dialog)
                input_dialog.show()
                if input_dialog.exec():
                    win1, win2 = input_ui.onOk()
                    if win1 and win2:  
                         self.med_filt_Data = median_Filter_func('Median Filtered with '+ str(win1) +'x'+str(win2)+' window',
                                                                 self.data_avail[str(data_var)],self.dt,self.nrx,self.rx_component,win1,win2)
                         self.data_avail['Median Filtered Data']= self.med_filt_Data # Updating available datasets
                         if 'Median Filtered Data' not in self.data_list:
                             self.data_list.append('Median Filtered Data') #Updating the available dataset list                         
                         tab_Var = mplt_plot(self.tab,self.med_filt_Data,self.dt,self.rx,self.rx_component)
                         self.t_index = self.tabWidget.addTab(tab_Var, 'Median Filtered with '+ str(win1) +'x'+str(win2)+' window')
                         self.tabWidget.setCurrentIndex(self.t_index)
    def gauss_Filter_callBack(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok: 
                sigma, okPressed = QtWidgets.QInputDialog.getInt(self,"Enter Sigma ","Sigma",2,1,4,1)        
                if sigma:   
                    gauss_filt_Data = gauss_Filter_func('Gaussian Filtered with sigma '+str(sigma),
                                      self.data_avail[str(data_var)],self.dt,self.nrx,self.rx_component,sigma)
                    self.data_avail['Gaussian Filtered Data']= gauss_filt_Data # Updating available datasets
                    if 'Gaussian Filtered Data' not in self.data_list:
                        self.data_list.append('Gaussian Filtered Data') #Updating the available dataset list 
                    tab_Var = mplt_plot(self.tab,gauss_filt_Data,self.dt,self.rx,self.rx_component)
                    self.t_index = self.tabWidget.addTab(tab_Var, 'Gaussian Filtered with sigma '+str(sigma))
                    self.tabWidget.setCurrentIndex(self.t_index)
            
    def FIR_lp_callBack(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:
                input_dialog = QtWidgets.QDialog()
                input_ui = FIR_LHP.Ui_FIR_Design()
                input_ui.setupUi(input_dialog)
                input_dialog.show()
                if input_dialog.exec():
                    ntaps, freq, win = input_ui.onOk()
                    if ntaps and freq:
                        if ntaps%2 ==0:
                            ntaps=ntaps+1 # converitng to Odd number of taps
                        FIR_lp_Data = FIR_lp_func('FIR lowpass Filtered with taps '+str(ntaps),
                                    self.data_avail[str(data_var)],self.dt,self.nrx,self.rx_component,ntaps,freq,win)
                        self.data_avail['FIR Lowpass Data']= FIR_lp_Data # Updating available datasets
                        if 'FIR Lowpass Data' not in self.data_list:
                            self.data_list.append('FIR Lowpass Data') #Updating the available dataset list                        
                        tab_Var = mplt_plot(self.tab,FIR_lp_Data,self.dt,self.rx,self.rx_component)
                        self.t_index = self.tabWidget.addTab(tab_Var, 'FIR lowpass Filtered with taps '+str(ntaps))
                        self.tabWidget.setCurrentIndex(self.t_index)
        
    def FIR_hp_callBack(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:            
                input_dialog = QtWidgets.QDialog()
                input_ui = FIR_LHP.Ui_FIR_Design()
                input_ui.setupUi(input_dialog)
                input_dialog.show()
                if input_dialog.exec():
                    ntaps, freq, win = input_ui.onOk()
                    if ntaps and freq:
                        if ntaps%2 ==0:
                            ntaps=ntaps+1 # converitng to Odd number of taps
                        
                        FIR_hp_Data = FIR_hp_func('FIR highpass Filtered with taps '+ str(ntaps),
                                    self.data_avail[str(data_var)],self.dt,self.nrx,self.rx_component,ntaps,freq,win)
                        self.data_avail['FIR Highpass Data']= FIR_hp_Data # Updating available datasets
                        if 'FIR Highpass Data' not in self.data_list:
                            self.data_list.append('FIR Highpass Data') #Updating the available dataset list   
                        tab_Var = mplt_plot(self.tab,FIR_hp_Data,self.dt,self.rx,self.rx_component)
                        self.t_index = self.tabWidget.addTab(tab_Var, 'FIR highpass Filtered with taps '+ str(ntaps))
                        self.tabWidget.setCurrentIndex(self.t_index)

    def FIR_bp_callBack(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            # prompt the user to select the dataset to Process
            data_var, ok = QtWidgets.QInputDialog.getItem(self,"Select Dataset to process",
                                                          "Dataset",self.data_list,0,False)
            if ok:
                input_dialog = QtWidgets.QDialog()
                input_ui = FIR_B_PS.Ui_FIR_Design()
                input_ui.setupUi(input_dialog)
                input_dialog.show()
                if input_dialog.exec():
                    ntaps, freq1,freq2, win = input_ui.onOk()
                    if ntaps%2 ==0:
                        ntaps=ntaps+1 # converitng to Odd number of taps
                    self.FIR_bp_Data = FIR_bp_func('FIR Bandpass Filtered with taps '+str(ntaps),
                                self.raw_data,self.dt,self.nrx,self.rx_component,ntaps,freq1,freq2, win)
                    tab_Var = mplt_plot(self.tab,self.FIR_bp_Data,self.dt,self.rx,self.rx_component)
                    self.t_index = self.tabWidget.addTab(tab_Var, 'FIR Bandpass Filtered with taps '+ str(ntaps))
                    self.tabWidget.setCurrentIndex(self.t_index)
    def FIR_bs_callBack(self):
        if self.raw_data is None:
            self.infile_error()
        else:
            input_dialog = QtWidgets.QDialog()
            input_ui = FIR_B_PS.Ui_FIR_Design()
            input_ui.setupUi(input_dialog)
            input_dialog.show()
            if input_dialog.exec():
                ntaps, freq1,freq2, win = input_ui.onOk()
                if ntaps%2 ==0:
                    ntaps=ntaps+1 # converitng to Odd number of taps
                    
                self.FIR_bs_Data = FIR_bs_func('FIR Bandpass Filtered with taps '+str(ntaps),
                            self.raw_data,self.dt,self.nrx,self.rx_component,ntaps,freq1,freq2, win)
                tab_Var = mplt_plot(self.tab,self.FIR_bs_Data,self.dt,self.rx,self.rx_component)
                self.t_index = self.tabWidget.addTab(tab_Var, 'FIR Bandstop Filtered with taps '+ str(ntaps))
                self.tabWidget.setCurrentIndex(self.t_index)
                
    def infile_error(self):
        choice = QtWidgets.QMessageBox.question(self, 'File Error!',
                                        "No File Selected  \nWant to Select File?",
                                        QtWidgets.QMessageBox.Yes | 
                                        QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            self.File_Open_window()
            
    def about(self):
        QtWidgets.QMessageBox.about(self, "About","""GPyR Version 1.0.0""")
        
    def close_tab(self,index):
#        print(index)
        self.tabWidget.removeTab(index)
        
    def add_tab(self):
        tab =QtWidgets.QWidget(self.tabWidget)
        self.tabWidget.addTab(tab,'Title')
        
        ''' Main Window Alighnment and Style'''              
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def set_Style(self,win_style=''):
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create(win_style))
        
        
###############################################################################   
def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
#    app.setStyleSheet('QMainWindow{background-color: white; border:1px solid blue;}')
    app.setStyleSheet('QMainWindow{background-color: white;}')
#    app.showFullScreen()
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())
    
###############################################################################   
    
if __name__ == "__main__":
    run()

    



