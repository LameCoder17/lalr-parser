from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        '''
        Sets up the UI on the screen
        '''
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1024, 720)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.evaluationBox = QtWidgets.QGroupBox(self.centralwidget)
        self.evaluationBox.setGeometry(QtCore.QRect(600, 100, 401, 141))
        self.evaluationBox.setTitle(_fromUtf8(""))
        self.evaluationBox.setObjectName(_fromUtf8("evaluationBox"))
        
        self.enterExpressionLabel = QtWidgets.QLabel(self.evaluationBox)
        self.enterExpressionLabel.setGeometry(QtCore.QRect(10, 20, 371, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.enterExpressionLabel.setFont(font)
        self.enterExpressionLabel.setObjectName(_fromUtf8("enterExpressionLabel"))
        
        self.lineEdit = QtWidgets.QLineEdit(self.evaluationBox)
        self.lineEdit.setGeometry(QtCore.QRect(10, 50, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        
        self.parse = QtWidgets.QPushButton(self.evaluationBox)
        self.parse.setGeometry(QtCore.QRect(270, 90, 121, 41))
        self.parse.setObjectName(_fromUtf8("parse"))
        
        self.rowWithButtons = QtWidgets.QGroupBox(self.centralwidget)
        self.rowWithButtons.setGeometry(QtCore.QRect(20, 300, 140, 350))
        self.rowWithButtons.setTitle(_fromUtf8(""))
        self.rowWithButtons.setObjectName(_fromUtf8("rowWithButtons"))
        
        self.displayButton = QtWidgets.QPushButton(self.rowWithButtons)
        self.displayButton.setGeometry(QtCore.QRect(10, 10, 110, 30))
        self.displayButton.setObjectName(_fromUtf8("displayButton"))
        
        self.firstButton = QtWidgets.QPushButton(self.rowWithButtons)
        self.firstButton.setGeometry(QtCore.QRect(10, 75, 110, 30))
        self.firstButton.setObjectName(_fromUtf8("firstButton"))
        
        self.clr1Button = QtWidgets.QPushButton(self.rowWithButtons)
        self.clr1Button.setGeometry(QtCore.QRect(10, 150, 110, 30))
        self.clr1Button.setObjectName(_fromUtf8("clr1Button"))
        
        self.lalrButton = QtWidgets.QPushButton(self.rowWithButtons)
        self.lalrButton.setGeometry(QtCore.QRect(10, 225, 110, 30))
        self.lalrButton.setObjectName(_fromUtf8("lalrButton"))
        
        self.parseTableButton = QtWidgets.QPushButton(self.rowWithButtons)
        self.parseTableButton.setGeometry(QtCore.QRect(10, 300, 111, 31))
        self.parseTableButton.setObjectName(_fromUtf8("parseTableButton"))
        
        self.displayScreen = QtWidgets.QTextBrowser(self.centralwidget)
        self.displayScreen.setGeometry(QtCore.QRect(200, 300, 800, 350)) 
        font = QtGui.QFont()
        font.setPointSize(12)
        self.displayScreen.setFont(font)
        self.displayScreen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.displayScreen.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.displayScreen.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.displayScreen.setObjectName(_fromUtf8("displayScreen"))
        
        self.inputScreen = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.inputScreen.setGeometry(QtCore.QRect(23, 80, 550, 181))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inputScreen.setFont(font)
        self.inputScreen.setObjectName(_fromUtf8("inputScreen"))
        
        self.enterGrammarLabel = QtWidgets.QLabel(self.centralwidget)
        self.enterGrammarLabel.setGeometry(QtCore.QRect(20, 50, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.enterGrammarLabel.setFont(font)
        self.enterGrammarLabel.setObjectName(_fromUtf8("enterGrammarLabel"))
        
        self.headingLabel = QtWidgets.QLabel(self.centralwidget)
        self.headingLabel.setGeometry(QtCore.QRect(380, 10, 261, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(26)
        font.setBold(True)
        self.headingLabel.setFont(font)
        self.headingLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.headingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headingLabel.setObjectName(_fromUtf8("headingLabel"))
        
        self.epsilonBox = QtWidgets.QGroupBox(self.centralwidget)
        self.epsilonBox.setGeometry(QtCore.QRect(900, 60, 100, 30))
        self.epsilonBox.setTitle(_fromUtf8(""))
        self.epsilonBox.setObjectName(_fromUtf8("epsilonBox"))
        
        self.epsilonLabel = QtWidgets.QLabel(self.epsilonBox)
        self.epsilonLabel.setGeometry(QtCore.QRect(10, 0, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.epsilonLabel.setFont(font)
        self.epsilonLabel.setObjectName(_fromUtf8("epsilonLabel"))
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        
        self.enterExpressionLabel.setBuddy(self.lineEdit)
        self.enterGrammarLabel.setBuddy(self.inputScreen)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.inputScreen, self.lineEdit)
        MainWindow.setTabOrder(self.lineEdit, self.parse)
        MainWindow.setTabOrder(self.parse, self.displayButton)
        MainWindow.setTabOrder(self.displayButton, self.firstButton)
        MainWindow.setTabOrder(self.firstButton, self.clr1Button)
        MainWindow.setTabOrder(self.clr1Button, self.lalrButton)
        MainWindow.setTabOrder(self.lalrButton, self.parseTableButton)
        MainWindow.setTabOrder(self.parseTableButton, self.displayScreen)

    def retranslateUi(self, MainWindow):
        '''
        Sets text for various buttons and labels and some UI design
        '''
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.enterExpressionLabel.setText(_translate("MainWindow", "Enter expression to evaluate :", None))
        self.parse.setText(_translate("MainWindow", "Parse", None))
        self.displayButton.setText(_translate("MainWindow", "Display", None))
        self.firstButton.setText(_translate("MainWindow", "First", None))
        self.clr1Button.setText(_translate("MainWindow", "CLR(1) items", None))
        self.lalrButton.setText(_translate("MainWindow", "LALR(1) items", None))
        self.parseTableButton.setText(_translate("MainWindow", "Parsing Table", None))
        self.enterGrammarLabel.setText(_translate("MainWindow", "Enter grammar :", None))
        self.headingLabel.setText(_translate("MainWindow", "LALR Parser", None))
        self.epsilonLabel.setText(_translate("MainWindow", "\'e\' : epsilon", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.actionOpen.setText(_translate("MainWindow", "&Open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionExit.setText(_translate("MainWindow", "&Exit", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        
        self.parse.setStyleSheet("background-color: white; border: 2px solid black; color: black;")
        self.displayButton.setStyleSheet("background-color: white; border: 2px solid black; color: black;")
        self.firstButton.setStyleSheet("background-color: white; border: 2px solid black; color: black;")
        self.clr1Button.setStyleSheet("background-color: white; border: 2px solid black; color: black;")
        self.lalrButton.setStyleSheet("background-color: white; border: 2px solid black; color: black;")
        self.parseTableButton.setStyleSheet("background-color: white; border: 2px solid black; color: black;")
        self.headingLabel.setStyleSheet("color: black;")
        self.enterGrammarLabel.setStyleSheet("color: black;")
        self.enterExpressionLabel.setStyleSheet("color: black;")
        self.epsilonLabel.setStyleSheet("color: black;")
        
        self.enterGrammarLabel.adjustSize()
        self.enterExpressionLabel.adjustSize()
        self.epsilonLabel.adjustSize()
        self.epsilonBox.adjustSize()

