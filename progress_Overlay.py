import math, sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor,QBrush,QPainter,QPen,QPalette
from PyQt5 import QtWidgets
class Overlay(QtWidgets.QWidget):
 
    def __init__(self, parent = None):
     
        QtWidgets.QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
       
    def paintEvent(self, event):
       
       painter = QPainter()
       painter.begin(self)
       painter.setRenderHint(QPainter.Antialiasing)
       painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
       painter.setPen(QPen(Qt.NoPen))
       
       for i in range(6):
           if (self.counter / 5) % 6 == i:
               painter.setBrush(QBrush(QColor(0 ,(150+i*7), 0)))
               print(self.counter)
#                painter.setBrush(QBrush(QColor(127 + (self.counter % 5)*32, 0, 200)))
           else:
               painter.setBrush(QBrush(QColor(100, 200, 100)))
           painter.drawEllipse(
               self.width()/2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
               self.height()/2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
                   20, 20)
       painter.end()
   
    def showEvent(self, event):
       self.timer = self.startTimer(100)
       self.counter = 0
       print('showEvent')
    def timerEvent(self, event):
       print('timerEvent')
       self.counter += 5
       self.update()
    def kill_Timer(self):
           self.killTimer(self.timer)
           self.hide()
#class MainWindow(QtWidgets.QMainWindow):
#   
#    def __init__(self, parent = None):
#   
#        QtWidgets.QMainWindow.__init__(self, parent)
#   
#        widget = QtWidgets.QWidget(self)
#        self.editor = QtWidgets.QTextEdit()
#        self.editor.setPlainText("0123456789"*100)
#        layout = QtWidgets.QGridLayout(widget)
##        layout.addWidget(self.editor, 0, 0, 1, 3)
#        button = QtWidgets.QPushButton("Start")
#        layout.addWidget(button, 1, 1, 1, 1)
#        
#        button1 = QtWidgets.QPushButton("Stop")
#        layout.addWidget(button1, 2, 1, 1, 1)
#        
#        self.setCentralWidget(widget)
#        self.tabWidget = QtWidgets.QTabWidget(widget)
#        self.tabWidget.setTabsClosable(True)
#        self.tabWidget.setMovable(True)
#        layout.addWidget(self.tabWidget)
#        self.tab = QtWidgets.QWidget()
#        self.tabWidget.addTab(self.tab, "Title")
#        
#        self.overlay = Overlay(self.tab)
#        self.overlay.hide()
#        button.clicked.connect(self.overlay.show)
#        button1.clicked.connect(self.overlay.kill_Timer)
#    def resizeEvent(self, event):
#        self.overlay.resize(event.size())
#        event.accept()
#        print('resize')
   
#   
#if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    window = MainWindow()
#    window.show()
#    sys.exit(app.exec_())