# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'patient_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_patient_form(object):
    def setupUi(self, patient_form):
        patient_form.setObjectName("patient_form")
        patient_form.setWindowModality(QtCore.Qt.WindowModal)
        patient_form.resize(400, 207)
        self.buttonBox = QtWidgets.QDialogButtonBox(patient_form)
        self.buttonBox.setGeometry(QtCore.QRect(30, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(patient_form)
        self.label.setGeometry(QtCore.QRect(160, 10, 91, 21))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(patient_form)
        self.widget.setGeometry(QtCore.QRect(90, 40, 207, 116))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.firstNameField = QtWidgets.QLineEdit(self.widget)
        self.firstNameField.setText("")
        self.firstNameField.setObjectName("firstNameField")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.firstNameField)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lastNameField = QtWidgets.QLineEdit(self.widget)
        self.lastNameField.setText("")
        self.lastNameField.setObjectName("lastNameField")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lastNameField)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.heightField = QtWidgets.QLineEdit(self.widget)
        self.heightField.setText("")
        self.heightField.setObjectName("heightField")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.heightField)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.weightField = QtWidgets.QLineEdit(self.widget)
        self.weightField.setText("")
        self.weightField.setObjectName("weightField")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.weightField)

        self.retranslateUi(patient_form)
        self.buttonBox.accepted.connect(patient_form.accept) # type: ignore
        self.buttonBox.rejected.connect(patient_form.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(patient_form)

    def retranslateUi(self, patient_form):
        _translate = QtCore.QCoreApplication.translate
        patient_form.setWindowTitle(_translate("patient_form", "Patient Form"))
        self.label.setText(_translate("patient_form", "Patient Details"))
        self.label_2.setText(_translate("patient_form", "First Name"))
        self.label_3.setText(_translate("patient_form", "Last Name"))
        self.label_4.setText(_translate("patient_form", "Height (m)"))
        self.label_5.setText(_translate("patient_form", "Weight (kg)"))
