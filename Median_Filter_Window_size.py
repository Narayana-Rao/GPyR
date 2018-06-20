

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(334, 174)
        self.gridLayout = QtWidgets.QGridLayout(dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(dialog)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 8)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBox = QtWidgets.QSpinBox(dialog)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(10)
        self.spinBox.setFont(font)
        self.spinBox.setWrapping(False)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(500)
        self.spinBox.setProperty("value", 2)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.label = QtWidgets.QLabel(dialog)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox_2 = QtWidgets.QSpinBox(dialog)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(10)
        self.spinBox_2.setFont(font)
        self.spinBox_2.setWrapping(False)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(500)
        self.spinBox_2.setProperty("value", 2)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout.addWidget(self.spinBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(self.onOk)# Added
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        self.buttonBox.accepted.connect(dialog.accept)# displaced
        
    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Enter Window Size"))
        self.label_2.setText(_translate("dialog", "Window Size"))
        self.label.setText(_translate("dialog", "X"))
        ############ Added
    def onOk(self):
        win_s1 = str(self.spinBox.text())
        win_s2 = str(self.spinBox_2.text())
        return int(win_s1), int(win_s2)
        ############
        
#
