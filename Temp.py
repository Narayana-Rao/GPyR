import sys
from PyQt5 import QtWidgets

class progress_bar(QtWidgets.QDialog):

    def __init__(self):
        super(progress_bar, self).__init__()
        self.ui()
        self.center()
        
    def ui(self):
        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setGeometry(100, 30, 300, 20)
        self.setGeometry(50, 50, 500, 100)
        self.setWindowTitle("Loading!")
        v_Layout = QtWidgets.QVBoxLayout()
        v_Layout.addStretch(1)
        v_Layout.addWidget(self.progress)
        self.progress.setValue(50)
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

app = QtWidgets.QApplication(sys.argv)
GUI = progress_bar()
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
sys.exit(app.exec_())

#from read_DZT import readgssi
#from plot_out_Data import out_plot
#file = 'FILE____143_SF_DF5_IIR_600_300.DZT '
#frequency = '400 MHz'
#
#
#header, data = readgssi(file,frequency)
##def out_plot(filename, outputdata, dt, rxnumber, rxcomponent)
#out_plot("Test",data,2e11,1,'E')




