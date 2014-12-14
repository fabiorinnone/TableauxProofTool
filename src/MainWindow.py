'''
MainWindow.py

@author: fabior
'''

import TableauProof, CheckFormula

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        print 'Loading GUI'
        self.setupUi(self)
        
    def setupUi(self, MainWindow):
        self.setObjectName("MainWindow")
        
        self.INPUT_CHANGED = 0
        self.INPUT_NEW = 1
        self.INPUT_SAVED = 0
        self.INPUT_OPENED = 0
        
        self.LAST_INPUT_SAVED = ''
        
        self.TABLEAUX_STRATEGY = 0
        
        self.INITIAL_INPUT = ''
        
        # Dimensioni finestra
        self.setMinimumSize(QtCore.QSize(800, 600)) 
        self.showMaximized()
        
        # Centra finestra
        self.center()
        
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setObjectName("centralwidget")
        
        self.mainGrid = QtGui.QGridLayout(self.centralWidget)
        
        self.inputLabel = QtGui.QLabel(self.centralWidget)
        self.inputLabel.setObjectName("inputLabel")
        self.inputLabel.setFixedHeight(20)
        
        self.inputTextEdit = QtGui.QPlainTextEdit(self.centralWidget)
        self.inputTextEdit.setObjectName("inputTextEdit")
        self.inputTextEdit.setToolTip("Insert Formula Here")
        
        self.strategyLabel = QtGui.QLabel(self.centralWidget)
        self.strategyLabel.setObjectName("strategyLabel")
        self.strategyLabel.setFixedHeight(20)
        
        self.strategyComboBox = QtGui.QComboBox(self.centralWidget)
        self.strategyComboBox.setObjectName("strategyComboBox")
        self.strategyComboBox.addItem("")
        self.strategyComboBox.addItem("")
        self.strategyComboBox.addItem("")
        self.strategyComboBox.addItem("")
        self.strategyComboBox.setToolTip("Select Tableaux Strategy")
        self.strategyComboBox.activated[str].connect(self.onActivated)
        
        self.startProofButton = QtGui.QPushButton(self.centralWidget)
        self.startProofButton.setGeometry(QtCore.QRect(560, 70, 111, 41))
        self.startProofButton.setObjectName("startProofButton")
        self.startProofButton.setToolTip("Start Proof")
        self.connect(self.startProofButton, QtCore.SIGNAL('clicked()'), self.startProof)
        
        self.checkFormulaButton = QtGui.QPushButton(self.centralWidget)
        self.checkFormulaButton.setGeometry(QtCore.QRect(680, 70, 111, 41))
        self.checkFormulaButton.setObjectName("checkFormulaButton")
        self.checkFormulaButton.setToolTip("Check Formula")
        self.connect(self.checkFormulaButton, QtCore.SIGNAL('clicked()'), self.checkFormula)
        
        self.progressBar = QtGui.QProgressBar(self.centralWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        
        self.outputLabel = QtGui.QLabel(self.centralWidget)
        self.outputLabel.setObjectName("outputLabel")
        self.outputLabel.setFixedHeight(20)
        
        self.outputTextBrowser = QtGui.QTextBrowser(self.centralWidget)
        self.outputTextBrowser.setObjectName("outputTextBrowser")
        
        self.mainGrid.addWidget(self.inputLabel, 0, 0, 1, 4)
        self.mainGrid.addWidget(self.inputTextEdit, 1, 0, 3, 4)
        self.mainGrid.addWidget(self.strategyLabel, 0, 4, 1, 2)
        self.mainGrid.addWidget(self.strategyComboBox, 1, 4, 1, 2)
        self.mainGrid.addWidget(self.startProofButton, 2, 4, 1, 1)
        self.mainGrid.addWidget(self.checkFormulaButton, 2, 5, 1, 1)
        self.mainGrid.addWidget(self.progressBar, 3, 4, 1, 2)
        self.mainGrid.addWidget(self.outputLabel, 4, 0, 1, 6)
        self.mainGrid.addWidget(self.outputTextBrowser, 5, 0, 4, 6)
        
        self.setCentralWidget(self.centralWidget)
        
        # Barra Menu
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        
        # Barra Menu File
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        # Barra Menu Edit
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        
        # Barra Menu Help
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        
        self.setMenuBar(self.menubar)
        
        # Pulsante New
        self.actionNew = QtGui.QAction(QtGui.QIcon("icons/new.png"),"",self)
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.setStatusTip("Create new File")
        self.actionNew.setObjectName("actionNew")
        self.connect(self.actionNew, QtCore.SIGNAL('triggered()'), self.newFile)  
        
        # Pulsante Open
        self.actionOpen = QtGui.QAction(QtGui.QIcon("icons/open.png"),"",self)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStatusTip("Open File")
        self.actionOpen.setObjectName("actionOpen")
        self.connect(self.actionOpen, QtCore.SIGNAL('triggered()'), self.openFile)
        
        # Pulsante Save Input
        self.actionSaveInput = QtGui.QAction(QtGui.QIcon("icons/save.png"),"",self)
        self.actionSaveInput.setStatusTip("Save Input as...")
        self.actionSaveInput.setShortcut("Ctrl+S")
        self.actionSaveInput.setObjectName("actionSaveInput")
        self.connect(self.actionSaveInput, QtCore.SIGNAL('triggered()'), self.saveInput)
        
        # Pulsante Save Output
        self.actionSaveOutput = QtGui.QAction(self)
        self.actionSaveOutput.setStatusTip("Save Output as...")
        self.actionSaveOutput.setObjectName("actionSaveOutput")
        self.connect(self.actionSaveOutput, QtCore.SIGNAL('triggered()'), self.saveOutput)      
        
        # Pulsante Quit
        self.actionClose = QtGui.QAction(QtGui.QIcon("icons/exit.png"),"",self)
        self.actionClose.setShortcut("Ctrl+Q")
        self.actionClose.setStatusTip("Quit Application")
        self.actionClose.setObjectName("actionClose")
        self.connect(self.actionClose, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        #self.connect(self.actionClose, QtCore.SIGNAL('triggered()'), self.quit)
        
        # Pulsante Undo
        self.actionUndo = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"",self)
        self.actionUndo.setShortcut("Ctrl+Z")
        self.actionUndo.setStatusTip("Undo Typing")
        self.actionUndo.setObjectName("actionUndo")
        self.connect(self.actionUndo, QtCore.SIGNAL('triggered()'), self.inputTextEdit.undo)
        
        # Pulsante Redo
        self.actionRedo = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"",self)
        self.actionRedo.setShortcut("Ctrl+Y")
        self.actionRedo.setStatusTip("Redo Typing")
        self.actionRedo.setObjectName("actionRedo")
        self.connect(self.actionRedo, QtCore.SIGNAL('triggered()'), self.inputTextEdit.redo)  
        
        # Pulsante Cut
        self.actionCut = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"",self)
        self.actionCut.setShortcut("Ctrl+X")
        self.actionCut.setStatusTip("Cut Selection")
        self.actionCut.setObjectName("actionCut")
        self.connect(self.actionCut, QtCore.SIGNAL('triggered()'), self.inputTextEdit.cut)  
        
        # Pulsante Copy
        self.actionCopy = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"",self)
        self.actionCopy.setShortcut("Ctrl+C")
        self.actionCopy.setStatusTip("Copy Selection")
        self.actionCopy.setObjectName("actionCopy")
        self.connect(self.actionCopy, QtCore.SIGNAL('triggered()'), self.inputTextEdit.copy)  
        
        # Pulsante Paste
        self.actionPaste = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"",self)
        self.actionPaste.setShortcut("Ctrl+V")
        self.actionPaste.setStatusTip("Redo Typing")
        self.actionPaste.setObjectName("actionPaste")
        self.connect(self.actionPaste, QtCore.SIGNAL('triggered()'), self.paste)  
        
        # Pulsante Select All
        self.actionSelectAll = QtGui.QAction(self)
        self.actionSelectAll.setShortcut("Ctrl+A")
        self.actionSelectAll.setStatusTip("Select All Text")
        self.actionSelectAll.setObjectName("actionSelectAll")
        self.connect(self.actionSelectAll, QtCore.SIGNAL('triggered()'), self.inputTextEdit.selectAll)  
        
        # Pulsante Help
        self.actionTableauxProofTool_Help = QtGui.QAction(QtGui.QIcon("icons/help.png"),"",self)
        self.actionTableauxProofTool_Help.setObjectName("actionTableauxProofTool_Help")
        self.actionTableauxProofTool_Help.setShortcut("F1")
        self.connect(self.actionTableauxProofTool_Help, QtCore.SIGNAL('triggered()'), self.help)
        
        # Pulsante About
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setShortcut("Ctrl+A")
        self.actionAbout.setStatusTip("About TableauProofTool")
        self.actionAbout.setObjectName("actionAbout")
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.showInfo)
        
        # Menu File
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveInput)
        self.menuFile.addAction(self.actionSaveOutput)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        
        # Menu Edit
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSelectAll)
        
        # Menu Help
        self.menuHelp.addAction(self.actionTableauxProofTool_Help)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        
        # Adding Menu to Menubar
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        # Status Bar
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "TableauxProofTool", None, QtGui.QApplication.UnicodeUTF8))
        self.strategyComboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "Classic Tableau", None, QtGui.QApplication.UnicodeUTF8))
        self.strategyComboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "M-Tableau", None, QtGui.QApplication.UnicodeUTF8))
        self.strategyComboBox.setItemText(2, QtGui.QApplication.translate("MainWindow", "L-Tableau", None, QtGui.QApplication.UnicodeUTF8))
        self.strategyComboBox.setItemText(3, QtGui.QApplication.translate("MainWindow", "KE-Tableau", None, QtGui.QApplication.UnicodeUTF8))
        self.startProofButton.setText(QtGui.QApplication.translate("MainWindow", "Start Proof", None, QtGui.QApplication.UnicodeUTF8))
        self.inputLabel.setText(QtGui.QApplication.translate("MainWindow", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.strategyLabel.setText(QtGui.QApplication.translate("MainWindow", "Tableau Strategy", None, QtGui.QApplication.UnicodeUTF8))
        self.checkFormulaButton.setText(QtGui.QApplication.translate("MainWindow", "Check Formula", None, QtGui.QApplication.UnicodeUTF8))
        self.outputLabel.setText(QtGui.QApplication.translate("MainWindow", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveInput.setText(QtGui.QApplication.translate("MainWindow", "Save Input", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo.setText(QtGui.QApplication.translate("MainWindow", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setText(QtGui.QApplication.translate("MainWindow", "Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelectAll.setText(QtGui.QApplication.translate("MainWindow", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTableauxProofTool_Help.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveOutput.setText(QtGui.QApplication.translate("MainWindow", "Save Output", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        
    def showInfo(self):
        QtGui.QMessageBox.information(self, "About", "TableauxProofTool v0.1.1\nDeveloped by Fabio Rinnone")
        
    def openFile(self):
        self.checkInput()
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open", "Open new File", self.tr("All Files (*);;Text Files (*in)"))
        if fileName.isEmpty() == False:
            file = open(fileName, 'r')
            self.inputTextEdit.clear()
            self.outputTextBrowser.clear()
            self.content = file.read()
            self.inputTextEdit.appendPlainText(self.content)
            self.INITIAL_INPUT = self.content
            file.close()
            self.INPUT_OPENED = 1
            self.INPUT_CHANGED = 0
            self.INPUT_NEW = 0
            self.INPUT_SAVED = 0
            self.setProgressBarValue(0)
            
    def saveInput(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save", "Save Input", self.tr("All Files (*);;Text Files (*in)"))
        if fileName.isEmpty() == False:
            file = open(fileName, 'w')
            file.write(self.inputTextEdit.toPlainText())
            file.close()
            self.INPUT_OPENED = 0
            self.INPUT_CHANGED = 0
            self.INPUT_NEW = 0
            self.INPUT_SAVED = 1
            self.LAST_INPUT_SAVED = self.inputTextEdit.toPlainText()
             
    def saveOutput(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save", "Save Output", self.tr("All Files (*);;Text Files (*in)"))
        if fileName.isEmpty() == False:
            file = open(fileName, 'w')
            file.write(self.outputTextBrowser.toPlainText())
            file.close()
        
    def newFile(self):
        self.checkInput()
        self.inputTextEdit.clear()
        self.outputTextBrowser.clear()
        self.INPUT_OPENED = 0
        self.INPUT_CHANGED = 0
        self.INPUT_NEW = 1
        self.INPUT_SAVED = 0
        self.setProgressBarValue(0)
        
    def paste(self):
        if self.inputTextEdit.canPaste():
            self.inputTextEdit.paste()
        else:
            QtGui.QMessageBox.critical(self,"Error","Impossible to paste text",QtGui.QMessageBox.Ok)
        
    def help(self):
        #print "Help"
        return
        
    def checkInput(self):
        #if len(str(self.inputTextEdit.toPlainText())) != 0:
        if str(self.inputTextEdit.toPlainText()) != self.INITIAL_INPUT:
            self.INPUT_CHANGED = 1
        if (str(self.inputTextEdit.toPlainText()) != self.LAST_INPUT_SAVED and self.INPUT_OPENED != 1) or self.INPUT_CHANGED:
            self.msgSaveInput()
            
    def msgSaveInput(self):
        self.questionSave = QtGui.QMessageBox.question(self,"Input changed","Save current Input?",
                                                           QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if self.questionSave == QtGui.QMessageBox.Yes:
            self.saveInput()
    
    def closeEvent(self, event):
        self.checkInput()
        event.accept()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def onActivated(self, text):
        if text == "Classic Tableau":
            self.TABLEAUX_STRATEGY = 0
        elif text == "M-Tableau":
            self.TABLEAUX_STRATEGY = 1
        elif text == "L-Tableau":
            self.TABLEAUX_STRATEGY = 2
        else:
            self.TABLEAUX_STRATEGY = 3
        
    def startProof(self):
        #self.checkFormula()
        
        #self.progressBar.setValue(50)
        
        inputString = str(self.inputTextEdit.toPlainText());
        
        if self.TABLEAUX_STRATEGY == 0:
            #self.classicTableauxProof(self.TABLEAUX_STRATEGY, inputString)
            self.proofThread = TableauProof.ClassicTableau(self.TABLEAUX_STRATEGY, inputString)
            self.connect(self.proofThread, QtCore.SIGNAL('addTextToOutput'), self.addTextToOutput)
            self.connect(self.proofThread, QtCore.SIGNAL('setProgressBarValue'), self.setProgressBarValue)
            self.proofThread.start()
        elif self.TABLEAUX_STRATEGY == 1:
            #self.mTableauxProof(self.TABLEAUX_STRATEGY, inputString)
            self.proofThread = TableauProof.MTableau(self.TABLEAUX_STRATEGY, inputString)
            self.connect(self.proofThread, QtCore.SIGNAL('addTextToOutput'), self.addTextToOutput)
            self.connect(self.proofThread, QtCore.SIGNAL('setProgressBarValue'), self.setProgressBarValue)
            self.proofThread.start()
        elif self.TABLEAUX_STRATEGY == 2:
            #self.lTableauxProof(self.TABLEAUX_STRATEGY, inputString)
            self.proofThread = TableauProof.LTableau(self.TABLEAUX_STRATEGY, inputString)
            self.connect(self.proofThread, QtCore.SIGNAL('addTextToOutput'), self.addTextToOutput)
            self.connect(self.proofThread, QtCore.SIGNAL('setProgressBarValue'), self.setProgressBarValue)
            self.proofThread.start()
        else:
            #self.keTableauxProof(self.TABLEAUX_STRATEGY, inputString)
            self.proofThread = TableauProof.KETableau(self.TABLEAUX_STRATEGY, inputString)
            self.connect(self.proofThread, QtCore.SIGNAL('addTextToOutput'), self.addTextToOutput)
            self.connect(self.proofThread, QtCore.SIGNAL('setProgressBarValue'), self.setProgressBarValue) 
            self.proofThread.start()
        
        #self.progressBar.setValue(100)
        
    def addTextToOutput(self, text):
        self.outputTextBrowser.append(text)
    
    def stopProof(self):
        return
    
    def classicTableauxProof(self, strategy, inputString):
        tableauProof = TableauProof.ClassicTableau(strategy, inputString)
        tableauProof.startProof()
        
    def mTableauxProof(self, strategy, inputString):
        
        tableauProof = TableauProof.MTableau(strategy, inputString)
        tableauProof.startProof()
        
    def lTableauxProof(self, strategy, inputString):
        tableauProof = TableauProof.LTableau(strategy, inputString)
        tableauProof.startProof()
        
    def keTableauxProof(self, strategy, inputString):
        tableauProof = TableauProof.KETableau(strategy, inputString)
        tableauProof.startProof()
        
    def checkFormula(self):
        #self.progressBar.setValue(0)
        
        inputString = str(self.inputTextEdit.toPlainText());
    
        self.checkFormula = CheckFormula.CheckFormulaThread(inputString)
        self.connect(self.checkFormula, QtCore.SIGNAL('addTextToOutput'), self.addTextToOutput)
        self.connect(self.checkFormula, QtCore.SIGNAL('setProgressBarValue'), self.setProgressBarValue)
        self.checkFormula.start()
        
        #formulaParser = FormulaParser.Parser()
        #self.formula = formulaParser.parse(inputString)
        
        #self.progressBar.setValue(100)
        
    def setProgressBarValue(self, value):
        self.progressBar.setValue(value)
        
    def appendTextToOutput(self, msg):
        self.outputTextBrowser.append(msg)
        