

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(493, 232)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        
#        self.onlyInt = 
#        self.test = self.lineEdit.textChanged[str].connect()
        self.lineEdit.setValidator(QtGui.QIntValidator())
        
        
        
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
#        self.lineEdit_2.textChanged[str].connect(self.onChanged)
        self.lineEdit_2.setValidator(QtGui.QDoubleValidator())
        
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 1)
        
        
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.onOk)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.buttonBox.accepted.connect(Dialog.accept)
        ##### pass params
#        self.buttonBox.accepted.connect(lambda: self.onOk("param"))
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "        No. of taps : "))
        self.label_3.setText(_translate("Dialog", "  Cutoff Frequency : "))
        self.comboBox.setItemText(0, _translate("Dialog", "Window 1"))
        self.comboBox.setItemText(1, _translate("Dialog", "Window 2"))
        self.comboBox.setItemText(2, _translate("Dialog", "Window 3"))
        self.comboBox.setItemText(3, _translate("Dialog", "Window 4"))
        self.comboBox.setItemText(4, _translate("Dialog", "Window 5"))
        self.comboBox.setItemText(5, _translate("Dialog", "Window 6"))
        self.label_4.setText(_translate("Dialog", "              Window : "))
        
    def onOk(self):
#        print("Ok Pressed  "+text)
        self.numtaps = self.lineEdit.text()
        self.frequency = self.lineEdit_2.text()
        self.window = str(self.comboBox.currentText())        
#        print(self.numtaps+"\n"+self.frequency+'\n'+self.window)
        return self.numtaps, self.frequency,self.window
#        Dialog.accept()
#        return self.numtaps, self.frequency,self.window

#if __name__ == "__main__":
#
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    Dialog = QtWidgets.QDialog()
#    ui = Ui_Dialog()
#    ui.setupUi(Dialog)
#    Dialog.show()
#    sys.exit(app.exec_())

