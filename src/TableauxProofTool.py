'''
TableauxProofTool.py

version 0.1.1

@author: fabior
'''

import sys, MainWindow

from PyQt4 import QtGui

# Start GUI
print 'Starting TableauxProofTool'
app = QtGui.QApplication(sys.argv)
main = MainWindow.Ui_MainWindow()
main.show()
sys.exit(app.exec_())
