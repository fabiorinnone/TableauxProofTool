'''
Created on 12/lug/2014

@author: fabior
'''

import FormulaParser

from PyQt4 import QtCore
from pyparsing import ParseException

class CheckFormulaThread(QtCore.QThread):
    
    def __init__(self, inputString):
        QtCore.QThread.__init__(self)
        self.inputString = inputString
        
    def run(self):
        self.emit(QtCore.SIGNAL('addTextToOutput'), 'Checking formula')
        self.emit(QtCore.SIGNAL('setProgressBarValue'), 10)
        formulaParser = FormulaParser.Parser()
        self.emit(QtCore.SIGNAL('setProgressBarValue'), 20)
        try:
            self.formula = formulaParser.parse(self.inputString)
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100)
        except ParseException as detail:
            print 'Error parsing formula: ', detail
            self.emit(QtCore.SIGNAL('addTextToOutput'), 'Error parsing formula: '+ str(detail))
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100)
        else:
            #print self.formula.__str__()
            self.emit(QtCore.SIGNAL('addTextToOutput'), 'Formula ' + self.inputString.strip() +' checked: no errors')
        