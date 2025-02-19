# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trial_form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_trial_form(object):
    def setupUi(self, trial_form):
        if not trial_form.objectName():
            trial_form.setObjectName(u"trial_form")
        trial_form.resize(383, 105)
        self.buttonBox = QDialogButtonBox(trial_form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 60, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.trialNameLabel = QLabel(trial_form)
        self.trialNameLabel.setObjectName(u"trialNameLabel")
        self.trialNameLabel.setGeometry(QRect(30, 30, 71, 21))
        font = QFont()
        font.setFamilies([u"Microsoft JhengHei UI Light"])
        self.trialNameLabel.setFont(font)
        self.trialNameField = QLineEdit(trial_form)
        self.trialNameField.setObjectName(u"trialNameField")
        self.trialNameField.setGeometry(QRect(110, 30, 261, 21))
        self.trialNameField.setFont(font)

        self.retranslateUi(trial_form)
        self.buttonBox.accepted.connect(trial_form.accept)
        self.buttonBox.rejected.connect(trial_form.reject)

        QMetaObject.connectSlotsByName(trial_form)
    # setupUi

    def retranslateUi(self, trial_form):
        trial_form.setWindowTitle(QCoreApplication.translate("trial_form", u"New Trial", None))
        self.trialNameLabel.setText(QCoreApplication.translate("trial_form", u"Trial Name", None))
        self.trialNameField.setPlaceholderText(QCoreApplication.translate("trial_form", u"e.g. Trendelenburg", None))
    # retranslateUi

