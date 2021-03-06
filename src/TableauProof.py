'''
TableauProof.py

@author: fabior
'''

import TableauTree, FormulaParser, time, copy

from PyQt4 import QtCore
from pyparsing import ParseException

'''
Class Tableau
'''
class Tableau(QtCore.QThread):
    
    def __init__(self, strategy, inputString): #rimuovere window per il multithreading
        QtCore.QThread.__init__(self)
        self.strategy = strategy
        self.inputString = inputString
        #self.window = window
        self.formulaList = None
        self.endedProof = False
        self.closed = False
        self.step = 1
        self.currentContraddiction = []
        self.branches = []
        self.branchesClosed = []
        self.checkedFormula = False
        
    def run(self):
        self.checkFormula()
        if self.strategy == 0:
            msg = 'Proof strategy: Classic Tableau'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutputGui'), msg)
        elif self.strategy == 1:
            msg = 'Proof strategy: M-Tableau'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutputGui'), msg)
        elif self.strategy == 2:
            msg = 'Proof strategy: L-Tableau'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutputGui'), msg)
        else:
            msg = 'Proof strategy: KE-Tableau'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutputGui'), msg)
        self.startProof()
        
    def checkFormula(self):
        msg = 'Checking formula'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        self.emit(QtCore.SIGNAL('setProgressBarValue'), 10)
        formulaParser = FormulaParser.Parser()
        self.emit(QtCore.SIGNAL('setProgressBarValue'), 20)
        try:
            self.formulaList = formulaParser.parse(self.inputString)
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100)
            self.checkedFormula = True         
        except ParseException as detail:
            msg = 'Error parsing formula: '
            print msg + detail
            #self.window.appendTextToOutput(msg + detail)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg + str(detail))
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100)
            self.checkedFormula = False
        else:
            #print self.formulaList.__str__()
            msg = 'Formula '+ self.inputString.strip()+' checked: no errors'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            self.formula = self.formulaList[0]
            self.createTableauTree(self.formula)
                
    def negateFormula(self, formula):
        return ['~', formula]
        
    def startProof(self):
        #self.checkFormula() #rimuovere quando attivo il multithreading
        if self.checkedFormula:
            self.startTime = time.time()
            msg = 'Starting proof'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 70)
            self.proofStep()
        else:
            msg = 'Proof not executed'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100)
                    
    def closeTableau(self):
        msg = 'Trying to close tableau'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        self.branches = self.tableauTree.getBranches(self.tableauTree.getRoot())
        self.printTableauBranches()
        count = 1
        self.branchesClosed = []
        branchNum = 1
        for branch in self.branches:
            contraddiction = self.isBranchClosed(branch, branchNum)
            if contraddiction:
                c = ': ['+self.currentContraddiction[0]+'; '+self.currentContraddiction[1]+']'
                msg = 'Contraddiction found in branch: '+ str(count) + c
                print msg
                #self.window.appendTextToOutput(msg)
                self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            else:
                msg = 'No contraddiction found in branch: '+ str(count)
                print msg
                #self.window.appendTextToOutput(msg)
                self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            self.branchesClosed.append(contraddiction)
            count = count + 1
            branchNum = branchNum + 1
        if False in self.branchesClosed:
            self.closed = False
            msg = 'Tableau has any branches not closed'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        else:
            self.closed = True
            msg = 'Tableau has all branches closed'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            
    def applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation):
        key = keyFormulaAnnotation[0]
        formula = keyFormulaAnnotation[1]
        annotation = keyFormulaAnnotation[2]
        formulaStr = FormulaParser.getStringFormula(formula)
        msg = 'Processing double negation formula ('+str(key)+'): '+str(formulaStr)+' ('+str(annotation)+')'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Applying double negation rule'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        doubleNegationComponent = self.getDoubleNegationFormulaComponent(formula)
        doubleNegationComponentStr = FormulaParser.getStringFormula(doubleNegationComponent)
        msg = 'Component: '+str(doubleNegationComponentStr)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        #self.branches = self.tableauTree.getBranches(node)
        branch = self.tableauTree.getBranch(branchNum)
        nodeToExpand = branch[len(branch)-1]
        self.count = self.count + 1
        annotation = 'Formula derived from ('+str(key)+') by double negation rule'
        self.tableauTree.put(self.count, doubleNegationComponent, annotation, nodeToExpand)
        msg = 'Formula ('+str(self.count)+'): '+doubleNegationComponentStr+' appended to branch '+str(branchNum)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        return [[self.count, doubleNegationComponent, annotation]]
        
    def applyAlphaRule(self, branchNum, index, keyFormulaAnnotation):
        key = keyFormulaAnnotation[0]
        formula = keyFormulaAnnotation[1]
        annotation = keyFormulaAnnotation[2] 
        formulaStr = FormulaParser.getStringFormula(formula)
        msg = 'Processing alpha formula ('+str(key)+'): '+str(formulaStr)+' ('+str(annotation)+')'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Applying alpha rule'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        alphaComponents = self.getAlphaFormulaComponents(formula)
        alphaComponentOneStr = FormulaParser.getStringFormula(alphaComponents[0])
        alphaComponentTwoStr = FormulaParser.getStringFormula(alphaComponents[1])
        msg = 'Alpha component 1: '+str(alphaComponentOneStr)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Alpha component 2: '+str(alphaComponentTwoStr)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        #self.branches = self.tableauTree.getBranches(node)
        branch = self.tableauTree.getBranch(branchNum)
        nodeToExpand = branch[len(branch)-1]
        self.count = self.count + 1
        annotation1 = 'Formula derived from ('+str(key)+') by alpha rule'
        self.tableauTree.put(self.count, alphaComponents[0], annotation1, nodeToExpand)
        msg = 'Formula ('+str(self.count)+'): '+alphaComponentOneStr+' appended to branch '+str(branchNum)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        annotation2 = 'Formula derived from ('+str(key)+') by alpha rule'
        self.tableauTree.put(self.count+1, alphaComponents[1], annotation2, nodeToExpand.getLeftChild())
        msg = 'Formula ('+str(self.count+1)+'): '+alphaComponentTwoStr+' appended to branch '+str(branchNum)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        return [[self.count-1, alphaComponents[0], annotation1],[self.count, alphaComponents[1], annotation2]]
        
    def applyBetaRule(self, branchNum, index, keyFormulaAnnotation):
        key = keyFormulaAnnotation[0]
        formula = keyFormulaAnnotation[1]
        annotation = keyFormulaAnnotation[2]
        formulaStr =  FormulaParser.getStringFormula(formula)
        msg = 'Processing beta formula ('+str(key)+'): '+str(formulaStr)+' ('+str(annotation)+')'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Applying beta rule'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        betaComponents = self.getBetaFormulaComponents(formula)
        betaComponentOneStr = FormulaParser.getStringFormula(betaComponents[0])
        betaComponentTwoStr = FormulaParser.getStringFormula(betaComponents[1])
        msg = 'Beta component 1: '+str(betaComponentOneStr)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Beta component 2: '+str(betaComponentTwoStr)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        branch = self.tableauTree.getBranch(branchNum)
        nodeToExpand = branch[len(branch)-1]
        self.count = self.count + 2
        annotation1 = 'Formula derived from ('+str(key)+') by beta rule'
        annotation2 = 'Formula derived from ('+str(key)+') by beta rule'
        self.tableauTree.split(self.count-1, betaComponents[0], annotation1, self.count, betaComponents[1], annotation2, nodeToExpand)
        msg = 'Branch '+str(branchNum)+ ' splitted'
        print msg 
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Formula ('+str(self.count-1)+') '+betaComponentOneStr+' appended to branch '+str(branchNum)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Formula ('+str(self.count)+') '+betaComponentTwoStr+' appended to branch '+str(branchNum+1)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        return [[self.count-1, betaComponents[0], annotation1], [self.count, betaComponents[1], annotation2]]
            
    def endProof(self):
        msg = 'No other formula to expand'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Proof ended'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        self.endedProof = True
        
    def isBranchClosed(self, branch, branchNum):
        contraddiction = False
        for node in branch:
            formula = node.getValue()
            negFormula = getNegation(formula)
            for n in branch:
                if negFormula == n.getValue():
                    contraddiction = True
                    #self.removeNotExpandableFormulasFromLists(branch, branchNum)
                    self.currentContraddiction = [FormulaParser.getStringFormula(formula), FormulaParser.getStringFormula(negFormula)]
        if not contraddiction:
            self.currentContraddiction = None
        return contraddiction
                    
    def isInOtherBranches(self, node, branchNum):
        num = 1
        for branch in self.branches:
            if not branchNum == num:
                for n in branch:
                    if n.getKey() == node.getKey():
                        return True
                return False
            num = num + 1
        return False
    
    def insertIntoNotAnalysedFormulasList(self, branchNum, key, formula, annotation):
        if not isAtomicFormula(formula) and not isNegationAtomicFormula(formula):
            branchFormulas = self.notAnalysedFormulas[branchNum]
            branchFormulas.append([key, formula, annotation])
            self.notAnalysedFormulas[branchNum] = branchFormulas
            return True
        return False
                    
    def splitNotAnalysedFormulaList(self, branchNum):
        for num in range(len(self.notAnalysedFormulas),branchNum-1,-1):
            self.notAnalysedFormulas[num+1] = self.notAnalysedFormulas[num]    
        #myList = self.notAnalysedFormulas.values()[len(self.notAnalysedFormulas.values())-1]
        myList = self.notAnalysedFormulas[branchNum]
        tmp = copy.deepcopy(myList)
        #tmp.append([key, formula, annotation])
        #tmp[len(tmp)-1] = [key, formula, annotation]
        #self.notAnalysedFormulas[len(self.notAnalysedFormulas)+1] = tmp
        self.notAnalysedFormulas[branchNum] = tmp
            
    def removeFromNotAnalysedFormulasList(self, keyFormulaAnnotation, branchNum):
        formula = keyFormulaAnnotation[1]
        if keyFormulaAnnotation in self.notAnalysedFormulas[branchNum]:
            self.notAnalysedFormulas[branchNum].remove(keyFormulaAnnotation)
            return True
        return False
        
    def isTableauClosed(self):
        return self.closed
    
    def isProofEnded(self):
        return self.endedProof
    
    def getAlphaFormulaComponents(self, formula):
        if isConjunctionFormula(formula):
            return [formula[0], formula[2]]
        elif isDisjunctionNegationFormula(formula):
            subFormula = formula[1]
            return [['~', subFormula[0]], ['~', subFormula[2]]]
        elif isImplicationNegationFormula(formula):
            subFormula = formula[1]
            return [subFormula[0], ['~', subFormula[2]]]
        else:
            return None
    
    def getBetaFormulaComponents(self, formula):
        if isDisjunctionFormula(formula):
            return [formula[0], formula[2]]
        elif isImplicationFormula(formula):
            return [['~', formula[0]], formula[2]]
        elif isConjunctionNegationFormula(formula):
            subFormula = formula[1]
            return [['~', subFormula[0]], ['~', subFormula[2]]]
        else:
            return None
    
    def getDoubleNegationFormulaComponent(self, formula):
        subFormula = formula[1]
        return subFormula[1]
    
    def printTableauBranches(self):
        i = 1
        for branch in self.branches:
            branchStr = '{'
            j = 1
            for node in branch:
                formula = node.getValue()
                if j != 1:
                    branchStr = branchStr + '; ' + str(FormulaParser.getStringFormula(formula))
                else:
                    branchStr = branchStr + str(FormulaParser.getStringFormula(formula))
                j = j + 1
            branchStr = branchStr + '}'
            msg = 'Branch ' + str(i) + ': ' + branchStr
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            i = i + 1
    
'''
Class ClassicTableau
'''    
class ClassicTableau(Tableau):
    
    def __init__(self, strategy, inputString): #rimuovere window per il multithreading
        Tableau.__init__(self, strategy, inputString)
        
    def createTableauTree(self, formula):
        self.tableauTree = TableauTree.Tree()
        negFormula = self.negateFormula(formula)
        msg = 'Negation of formula: ' + FormulaParser.getStringFormula(negFormula)
        #self.window.appendTextToOutput(msg)
        print msg
        self.emit(QtCore.SIGNAL('addTextToOutputGui'), msg)
        self.count = 1
        root = self.tableauTree.getRoot()
        annotation = 'Initial formula'
        self.tableauTree.put(self.count, negFormula, annotation, root) # putting first formula on tableau tree
        #self.doubleNegationFormulasList = []
        #self.alphaFormulasList = []
        #self.betaFormulasList = []
        self.notAnalysedFormulas = {}
        self.notAnalysedFormulas[1] = []
        self.insertIntoNotAnalysedFormulasList(1, self.count, negFormula, annotation)
        self.branchesClosed.append(False) # controllare
        self.emit(QtCore.SIGNAL('setProgressBarValue'), 60)
        return [[self.count, negFormula, annotation]]
    
    def proofStep(self):
        msg = 'Proof step '+str(self.step)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        self.step = self.step + 1
        branchNum = 1
        ruleApplied = False
        for closed in self.branchesClosed:
            if not closed and len(self.notAnalysedFormulas[branchNum]) > 0:
                self.applyRule(branchNum)
                ruleApplied = True
                self.closeTableau()
                break
            branchNum = branchNum + 1
        if not ruleApplied:
            self.endProof()
        if self.isTableauClosed():
            msg = 'Formula is a tautology'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100)
        elif self.isProofEnded():
            msg = 'Formula is not a tautology'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100) 
        if self.isTableauClosed() or self.isProofEnded():
            self.endTime = time.time()
            print 'Time elapsed: ' + str(self.endTime - self.startTime)
        else:
            self.proofStep()
            
    def applyRule(self, branchNum):
        if self.thereAreDoubleNegationFormulasToExpand(branchNum):
            index = self.getDoubleNegationFormulaIndexToExpand(branchNum)
        elif self.thereAreAlphaFormulasToExpand(branchNum):
            index = self.getAlphaFormulaIndexToExpand(branchNum)
        else :
            index = self.getBetaFormulaIndexToExpand(branchNum)
        keyFormulaAnnotation = self.notAnalysedFormulas[branchNum][index]
        formula = keyFormulaAnnotation[1]
        if isDoubleNegationFormula(formula):
            self.applyDoubleNegationRule(branchNum, index, keyFormulaAnnotation)
        elif isAlphaFormula(formula):
            self.applyAlphaRule(branchNum, index, keyFormulaAnnotation)
        elif isBetaFormula(formula):
            self.applyBetaRule(branchNum, index, keyFormulaAnnotation)
            
    def applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation):
        expandedFormulasList = Tableau.applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation)
        doubleNegationComponentList = expandedFormulasList[0]
        doubleNegationComponent = doubleNegationComponentList[1]
        annotation = doubleNegationComponentList[2]
        self.insertIntoNotAnalysedFormulasList(branchNum, self.count, doubleNegationComponent, annotation)
        self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        
    def applyAlphaRule(self, branchNum, index, keyFormulaAnnotation):
        expandedFormulasList = Tableau.applyAlphaRule(self, branchNum, index, keyFormulaAnnotation)
        firstAlphaComponentList = expandedFormulasList[0]
        secondAlphaComponentList = expandedFormulasList[1]
        firstAlphaComponent = firstAlphaComponentList[1]
        annotation1 = firstAlphaComponentList[2]
        secondAlphaComponent = secondAlphaComponentList[1]
        annotation2 = secondAlphaComponentList[2]
        self.insertIntoNotAnalysedFormulasList(branchNum, self.count, firstAlphaComponent, annotation1)
        self.count = self.count + 1
        self.insertIntoNotAnalysedFormulasList(branchNum, self.count, secondAlphaComponent, annotation2)
        self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
    
    def applyBetaRule(self, branchNum, index, keyFormulaAnnotation):
        expandedFormulasList = Tableau.applyBetaRule(self, branchNum, index, keyFormulaAnnotation)
        firstBetaComponentList = expandedFormulasList[0]
        secondBetaComponentList = expandedFormulasList[1]
        firstBetaComponent = firstBetaComponentList[1]
        annotation1 = firstBetaComponentList[2]
        secondBetaComponent = secondBetaComponentList[1]
        annotation2 = secondBetaComponentList[2]
        self.splitNotAnalysedFormulaList(branchNum)
        self.insertIntoNotAnalysedFormulasList(branchNum, self.count-1, firstBetaComponent, annotation1)
        self.insertIntoNotAnalysedFormulasList(branchNum+1, self.count, secondBetaComponent, annotation2)
        self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum+1)
        
    def thereAreFormulasToExpand(self, branchNum):
        if(len(self.notAnalysedFormulas[branchNum]) == 0):
            return False
        else:
            return True
        
    def thereAreDoubleNegationFormulasToExpand(self, branchNum):
        if not self.thereAreFormulasToExpand(branchNum):
            return False
        formulasToExpand = self.notAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isDoubleNegationFormula(formula):
                return True
        return False
        
    def thereAreAlphaFormulasToExpand(self, branchNum):
        if not self.thereAreFormulasToExpand(branchNum):
            return False
        formulasToExpand = self.notAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isAlphaFormula(formula):
                return True
        return False
    
    def thereAreBetaFormulasToExpand(self, branchNum):
        if not self.thereAreFormulasToExpand(branchNum):
            return False
        formulasToExpand = self.notAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isBetaFormula(formula):
                return True
        return False
    
    def getDoubleNegationFormulaIndexToExpand(self, branchNum):
        index = 0
        formulasToExpand = self.notAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isDoubleNegationFormula(formula):
                return index
            index = index + 1
        return None

    def getAlphaFormulaIndexToExpand(self, branchNum):
        index = 0
        formulasToExpand = self.notAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isAlphaFormula(formula):
                return index
            index = index + 1
        return None

    def getBetaFormulaIndexToExpand(self, branchNum):
        index = 0
        formulasToExpand = self.notAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isBetaFormula(formula):
                return index
            index = index + 1
        return None
    
'''
Class ExtendedTableau
'''
class ExtendedTableau(ClassicTableau):
    
    def contains(self, deltaM, deltaN):
        res = True
        for item in deltaN:
            if not item in deltaM:
                res = False
        return res
        
'''
Class LTableau
'''
class LTableau(ExtendedTableau):
    
    def __init__(self, strategy, inputString): #rimuovere window per il multithreading
        ClassicTableau.__init__(self, strategy, inputString)
        
    def applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation):
        lemmaAppended = self.applyLemmaIfPossible(keyFormulaAnnotation[0], keyFormulaAnnotation[1])
        if not lemmaAppended:
            ClassicTableau.applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation)
        else:
            #self.doubleNegationFormulasList.remove(self.doubleNegationFormulasList[0])
            self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        
    def applyAlphaRule(self, branchNum, index, keyFormulaAnnotation):
        lemmaAppended = self.applyLemmaIfPossible(keyFormulaAnnotation[0], keyFormulaAnnotation[1])
        if not lemmaAppended:
            ClassicTableau.applyAlphaRule(self, branchNum, index, keyFormulaAnnotation)
        else:
            #self.alphaFormulasList.remove(self.alphaFormulasList[0])
            self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        
    def applyBetaRule(self, branchNum, index, keyFormulaAnnotation):
        lemmaAppended = self.applyLemmaIfPossible(keyFormulaAnnotation[0], keyFormulaAnnotation[1])
        if not lemmaAppended:
            ClassicTableau.applyBetaRule(self, branchNum, index, keyFormulaAnnotation)
        else:
            #self.betaFormulasList.remove(self.betaFormulasList[0])
            self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        
    def applyLemmaIfPossible(self, key, formula):
        self.branches = self.tableauTree.getBranches(self.tableauTree.getRoot())
        myNode = self.tableauTree.getNode(key)
        lemmaAppended = False
        nodeBranchNum = self.tableauTree.getBranchNum(myNode)
        for branch in self.branches:
            currentBranchNum = 1
            if not currentBranchNum == nodeBranchNum:
                for node in branch:
                    if node.getValue() == myNode.getValue() and node.getDepth() < myNode.getDepth():
                        deltaN = self.tableauTree.getParents(node)
                        deltaM = self.tableauTree.getParents(myNode)
                        if self.contains(deltaM, deltaN):
                            self.applyLemma(nodeBranchNum, self.count, getNegation(formula), 'Lemma from ('+str(node.getKey())+')', myNode)
                            self.count = self.count + 1
                            lemmaAppended = True
                        break
            if lemmaAppended:
                break
            currentBranchNum = currentBranchNum + 1
        return lemmaAppended
                
    def applyLemma(self, branchNum, count, formula, annotation, node):
        msg = 'Applying lemma'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        self.tableauTree.put(count, formula, annotation, node)
        self.insertIntoNotAnalysedFormulasList(branchNum, self.count, formula, annotation) #VERIFICARE    
        
'''
Class MTableau
'''
class MTableau(ExtendedTableau):
    
    def __init__(self, strategy, inputString): #rimuovere window per il multithreading
        ClassicTableau.__init__(self, strategy, inputString)
        self.checkedBranches = []
        self.branchesClosedOrChecked = []
        
    def applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation):
        branchChecked = self.applyMergingIfPossible(keyFormulaAnnotation[0], keyFormulaAnnotation[1])
        if not branchChecked:
            ClassicTableau.applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation)
        else:
            #self.doubleNegationFormulasList.remove(self.doubleNegationFormulasList[0])
            self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        
    def applyAlphaRule(self, branchNum, index, keyFormulaAnnotation):
        branchChecked = self.applyMergingIfPossible(keyFormulaAnnotation[0], keyFormulaAnnotation[1])
        if not branchChecked:
            ClassicTableau.applyAlphaRule(self, branchNum, index, keyFormulaAnnotation)
        else:
            #self.alphaFormulasList.remove(self.alphaFormulasList[0])
            self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        
    def applyBetaRule(self, branchNum, index, keyFormulaAnnotation):
        branchChecked = self.applyMergingIfPossible(keyFormulaAnnotation[0], keyFormulaAnnotation[1])
        if not branchChecked:
            ClassicTableau.applyBetaRule(self, branchNum, index, keyFormulaAnnotation)
        else:
            #self.betaFormulasList.remove(self.betaFormulasList[0])
            self.removeFromNotAnalysedFormulasList(keyFormulaAnnotation, branchNum)
            
    def applyMergingIfPossible(self, key, formula):
        self.branches = self.tableauTree.getBranches(self.tableauTree.getRoot())
        myNode = self.tableauTree.getNode(key)
        branchChecked = False
        nodeBranchNum = self.tableauTree.getBranchNum(myNode)
        for branch in self.branches:
            currentBranchNum = 1
            if not currentBranchNum == nodeBranchNum:
                for node in branch:
                    if node.getValue() == myNode.getValue() and node.getDepth() < myNode.getDepth():
                        deltaN = self.tableauTree.getParents(node)
                        deltaM = self.tableauTree.getParents(myNode)
                        if self.contains(deltaM, deltaN):
                            self.checkBranch(nodeBranchNum)
                            msg = 'Applying merging'
                            print msg
                            self.window.appendTextToOutput(msg)
                            #self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
                            msg = 'Branch '+str(nodeBranchNum)+' checked'
                            print msg
                            self.window.appendTextToOutput(msg)
                            #self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
                            branchChecked = True
                        break
            if branchChecked:
                break
            currentBranchNum = currentBranchNum + 1
        return branchChecked
    
    def checkBranch(self, currentBranchNum):
        self.checkedBranches.append(currentBranchNum)
    
    def closeTableau(self):
        Tableau.closeTableau(self)
        branchNum = 1
        self.branchesClosedOrChecked = []
        for item in self.branchesClosed:
            if item == False:
                if branchNum in self.checkedBranches:
                    self.branchesClosedOrChecked.append(True)
                else:
                    self.branchesClosedOrChecked.append(self.branchesClosed[branchNum-1])
            branchNum = branchNum + 1  
        if False in self.branchesClosedOrChecked:
            self.closed = False
            msg = 'Tableau has any branches not closed or not checked'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        else:
            self.closed = True
            msg = 'Tableau has all branches closed or checked'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)    
            
'''
Class KETableau
'''             
class KETableau(Tableau):
    
    def __init__(self, strategy, inputString): #rimuovere window per il multithreading
        Tableau.__init__(self, strategy, inputString)
        self.notEAnalysedFormulas = {}
        self.branchesECompleted = []
        self.notFulfilledBetaFormulas = {}
        self.branchesCompleted = []
        #self.branchesClosedAndCompleted = []
        
    def createTableauTree(self, formula):
        self.tableauTree = TableauTree.Tree()
        negFormula = self.negateFormula(formula)
        msg = 'Negation of formula: ' + FormulaParser.getStringFormula(negFormula)
        #self.window.appendTextToOutput(msg)
        print msg
        self.emit(QtCore.SIGNAL('addTextToOutputGui'), msg)
        self.count = 1
        root = self.tableauTree.getRoot()
        annotation = 'Initial formula'
        self.tableauTree.put(self.count, negFormula, annotation, root) # putting first formula on tableau tree
        self.branchesClosed.append(False) # controllare
        self.emit(QtCore.SIGNAL('setProgressBarValue'), 60)
        keyFormulaAnnotation = [self.count, negFormula, annotation]
        self.notEAnalysedFormulas[1] = [keyFormulaAnnotation]
        formula = keyFormulaAnnotation[1]
        if isBetaFormula(formula):
            self.notFulfilledBetaFormulas[1] = [keyFormulaAnnotation]
        return [[self.count, negFormula, annotation]]
            
    def proofStep(self):
        msg = 'Proof step '+str(self.step)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        self.step = self.step + 1
        branchNum = 1
        for closed in self.branchesClosed:
            if not closed and not self.isBranchCompleted(branchNum):
                branch = self.tableauTree.getBranch(branchNum)
                if len(self.notFulfilledBetaFormulas) == 0:
                    self.notFulfilledBetaFormulas[branchNum] = []
                while not self.isBranchECompleted(branchNum):
                    self.applyRule(branchNum)
                    msg = 'Proof step '+str(self.step)
                    print msg
                    #self.window.appendTextToOutput(msg)
                    self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
                    self.step = self.step + 1
                branch = self.tableauTree.getBranch(branchNum)
                if not self.isBranchClosed(branch, branchNum) and not self.isBranchCompleted(branchNum):
                    if len(self.notFulfilledBetaFormulas[branchNum]) > 0:
                        betaFormulaNotFulfilled = self.notFulfilledBetaFormulas[branchNum][0]
                        branch = self.tableauTree.getBranch(branchNum) #verificare se possibile omettere
                        formula = betaFormulaNotFulfilled[1]
                        betaComponents = self.getBetaFormulaComponents(formula)
                        beta2 = betaComponents[1]
                        self.applyBivalenceRule(betaFormulaNotFulfilled, beta2, branch, branchNum)
                        #self.closeTableau()
                #self.closeTableau()
            else:
                branchNum = branchNum + 1
        if self.isTableauCompleted():
            self.endProof()
        self.closeTableau()
        if self.isTableauClosed():
            msg = 'Formula is a tautology'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100)
        elif self.isProofEnded():
            msg = 'Formula is not a tautology'
            print msg
            #self.window.appendTextToOutput(msg)
            self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
            self.emit(QtCore.SIGNAL('setProgressBarValue'), 100) 
        if self.isTableauClosed() or self.isProofEnded():
            self.endTime = time.time()
            print 'Time elapsed: ' + str(self.endTime - self.startTime)
        else:
            self.proofStep()
            
    def applyRule(self, branchNum):
        if self.thereAreDoubleNegationFormulasToExpand(branchNum):
            index = self.getDoubleNegationFormulaIndexToExpand(branchNum)
        elif self.thereAreAlphaFormulasToExpand(branchNum):
            index = self.getAlphaFormulaIndexToExpand(branchNum)
        else :
            index = self.getBetaFormulaIndexToExpand(branchNum)
        keyFormulaAnnotation = self.notEAnalysedFormulas[branchNum][index]
        formula = keyFormulaAnnotation[1]
        if isDoubleNegationFormula(formula):
            self.applyDoubleNegationRule(branchNum, index, keyFormulaAnnotation)
        elif isAlphaFormula(formula):
            self.applyAlphaRule(branchNum, index, keyFormulaAnnotation)
        elif isBetaFormula(formula):
            self.applyBetaRule(branchNum, index, keyFormulaAnnotation)
        #self.insertIntoNotEAnalysedFormulasList(branch, branchNum)
        #self.insertIntoNotFulfilledBetaFormulasList(branch, branchNum)
                    
    def applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation):
        Tableau.applyDoubleNegationRule(self, branchNum, index, keyFormulaAnnotation)
        branch = self.tableauTree.getBranch(branchNum)
        self.removeFormulaFromNotEAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        self.insertIntoNotEAnalysedFormulasList(branch, branchNum)
        self.insertIntoNotFulfilledBetaFormulasList(branch, branchNum)
        self.removefromNotFullfilledBetaFormulasList(branch, branchNum)
                
    def applyAlphaRule(self, branchNum, index, keyFormulaAnnotation):
        Tableau.applyAlphaRule(self, branchNum, index, keyFormulaAnnotation)
        branch = self.tableauTree.getBranch(branchNum)
        self.removeFormulaFromNotEAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        self.insertIntoNotEAnalysedFormulasList(branch, branchNum)
        self.insertIntoNotFulfilledBetaFormulasList(branch, branchNum)
        self.removefromNotFullfilledBetaFormulasList(branch, branchNum)
        self.count = self.count + 1
                
    def applyBetaRule(self, branchNum, index, keyFormulaAnnotation):
        key = keyFormulaAnnotation[0]
        formula = keyFormulaAnnotation[1]
        annotation = keyFormulaAnnotation[2]
        formulaStr =  FormulaParser.getStringFormula(formula)
        msg = 'Processing beta formula ('+str(key)+'): '+str(formulaStr)+' ('+str(annotation)+')'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Trying to applying beta rule'
        print msg 
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        betaComponents = self.getBetaFormulaComponents(formula)
        beta1 = betaComponents[0]
        beta2 = betaComponents[1]
        if isDoubleNegationFormula(beta1):
            beta1 = self.getDoubleNegationFormulaComponent(beta1)
        if isDoubleNegationFormula(beta2):
            beta2 = self.getDoubleNegationFormulaComponent(beta2)
        negBeta1 = getNegation(beta1)
        negBeta2 = getNegation(beta2)
        if isDoubleNegationFormula(negBeta1):
            negBeta1 = self.getDoubleNegationFormulaComponent(negBeta1)
        if isDoubleNegationFormula(negBeta2):
            negBeta2 = self.getDoubleNegationFormulaComponent(negBeta2)    
        msg = 'Searching any negations of beta components in branch'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        #node = self.tableauTree.getNode(key)
        #self.branches = self.tableauTree.getBranches(node)
        betaRuleApplied = False
        beta1Appended = False
        beta2Appended = False
        #branchNum = self.tableauTree.getBranchNum(node)
        branch = self.tableauTree.getBranch(branchNum)
        #for branch in self.branches:
        for currentNode in branch:
            value = currentNode.getValue()
            if value == negBeta1:
                annotation = 'Formula derived from ('+str(key)+') by beta rule'
                msg = 'Found negation of beta component 1: '+FormulaParser.getStringFormula(negBeta1)
                print msg
                #self.window.appendTextToOutput(msg)
                self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
                self.appendToTableauTree(key, beta2, branch, branchNum)
                #self.insertFormulaIntoNotEAnalysedFormulasList([self.count, beta2, annotation], branchNum)
                betaRuleApplied = True
                beta2Appended = True
                expandedKeyFormulaAnnotation = [self.count, beta2, annotation]
                break
            elif value == negBeta2:
                annotation = 'Formula derived from ('+str(key)+') by beta rule'
                msg = 'Found negation of beta component 2: '+FormulaParser.getStringFormula(negBeta2)
                print msg
                #self.window.appendTextToOutput(msg)
                self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
                self.appendToTableauTree(key, beta1, branch, branchNum)
                #self.insertFormulaIntoNotEAnalysedFormulasList([self.count, beta1, annotation], branchNum)
                betaRuleApplied = True
                beta1Appended = True
                expandedKeyFormulaAnnotation = [self.count, beta1, annotation]
                break
        branch = self.tableauTree.getBranch(branchNum)
        self.removeFormulaFromNotEAnalysedFormulasList(keyFormulaAnnotation, branchNum)
        #self.removeFormulaFromNotFulfilledBetaFormulasList(keyFormulaAnnotation, branchNum)
        self.removefromNotFullfilledBetaFormulasList(branch, branchNum)
        self.insertIntoNotEAnalysedFormulasList(branch, branchNum)
        self.insertIntoNotFulfilledBetaFormulasList(branch, branchNum)    
        if beta1Appended:
            return [[self.count, beta1, annotation]]
        elif beta2Appended:
            return [[self.count, beta2, annotation]]
        else:
            return None
        
    def applyBivalenceRule(self, keyFormulaAnnotation, beta2, branch, branchNum):
        key = keyFormulaAnnotation[0]
        notBeta2 = getNegation(beta2)
        nodeToExpand = branch[len(branch)-1]
        self.count = self.count + 2
        annotation1 = 'Formula derived from ('+str(key)+') by bivalence rule'
        annotation2 = 'Formula derived from ('+str(key)+') by bivalence rule'
        self.tableauTree.split(self.count - 1, beta2, annotation1, self.count, notBeta2, annotation2, nodeToExpand)
        msg = 'Branch '+str(branchNum)+ ' splitted'
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Formula ('+str(self.count-1)+') '+str(FormulaParser.getStringFormula(beta2))+' appended to branch '+str(branchNum)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        msg = 'Formula ('+str(self.count)+') '+str(FormulaParser.getStringFormula(notBeta2))+' appended to branch '+str(branchNum+1)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        self.splitNotEAnalysedFormulasList(branchNum)
        self.splitNotFulfilledBetaFormulasList(branchNum)
        branch = self.tableauTree.getBranch(branchNum)
        newBranch = self.tableauTree.getBranch(branchNum+1)
        #self.removeFormulaFromNotFulfilledBetaFormulasList(keyFormulaAnnotation, branchNum)
        #self.removeFormulaFromNotFulfilledBetaFormulasList(keyFormulaAnnotation, branchNum+1) #omettere?
        self.removefromNotFullfilledBetaFormulasList(branch, branchNum)
        self.removefromNotFullfilledBetaFormulasList(branch, branchNum+1)
        self.insertIntoNotEAnalysedFormulasList(branch, branchNum)
        self.insertIntoNotEAnalysedFormulasList(newBranch, branchNum+1)
        self.insertIntoNotFulfilledBetaFormulasList(branch, branchNum)
        self.insertIntoNotFulfilledBetaFormulasList(newBranch, branchNum+1)
        
    def thereAreFormulasToExpand(self, branchNum):
        if(len(self.notEAnalysedFormulas[branchNum]) == 0):
            return False
        else:
            return True
        
    def thereAreDoubleNegationFormulasToExpand(self, branchNum):
        if not self.thereAreFormulasToExpand(branchNum):
            return False
        formulasToExpand = self.notEAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isDoubleNegationFormula(formula):
                return True
        return False
        
    def thereAreAlphaFormulasToExpand(self, branchNum):
        if not self.thereAreFormulasToExpand(branchNum):
            return False
        formulasToExpand = self.notEAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isAlphaFormula(formula):
                return True
        return False
    
    def thereAreBetaFormulasToExpand(self, branchNum):
        if not self.thereAreFormulasToExpand(branchNum):
            return False
        formulasToExpand = self.notEAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isBetaFormula(formula):
                return True
        return False
    
    def getDoubleNegationFormulaIndexToExpand(self, branchNum):
        index = 0
        formulasToExpand = self.notEAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isDoubleNegationFormula(formula):
                return index
            index = index + 1
        return None

    def getAlphaFormulaIndexToExpand(self, branchNum):
        index = 0
        formulasToExpand = self.notEAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isAlphaFormula(formula):
                return index
            index = index + 1
        return None

    def getBetaFormulaIndexToExpand(self, branchNum):
        index = 0
        formulasToExpand = self.notEAnalysedFormulas[branchNum]
        for keyFormulaAnnotation in formulasToExpand:
            formula = keyFormulaAnnotation[1]
            if isBetaFormula(formula):
                return index
            index = index + 1
        return None
    
    def appendToTableauTree(self, key, formula, branch, branchNum):
        nodeToExpand = branch[len(branch)-1]
        self.count = self.count + 1
        annotation = 'Formula derived from ('+str(key)+') by beta rule'
        self.tableauTree.put(self.count, formula, annotation, nodeToExpand)
        msg = 'Formula ('+str(self.count)+'): '+str(FormulaParser.getStringFormula(formula))+' appended to branch '+str(branchNum)
        print msg
        #self.window.appendTextToOutput(msg)
        self.emit(QtCore.SIGNAL('addTextToOutput'), msg)
        self.insertFormulaIntoNotEAnalysedFormulasList([self.count, formula, annotation], branchNum)
            
    def splitNotEAnalysedFormulasList(self, branchNum):
        for num in range(len(self.notEAnalysedFormulas),branchNum-1,-1):
            self.notEAnalysedFormulas[num+1] = self.notEAnalysedFormulas[num]    
        myList = self.notEAnalysedFormulas[branchNum]
        tmp = copy.deepcopy(myList)
        self.notEAnalysedFormulas[branchNum] = tmp
    
    def splitNotFulfilledBetaFormulasList(self, branchNum):
        for num in range(len(self.notFulfilledBetaFormulas),branchNum-1,-1):
            self.notFulfilledBetaFormulas[num+1] = self.notFulfilledBetaFormulas[num]    
        myList = self.notFulfilledBetaFormulas[branchNum]
        tmp = copy.deepcopy(myList)
        self.notFulfilledBetaFormulas[branchNum] = tmp            
    
    def insertIntoNotEAnalysedFormulasList(self, branch, branchNum):
        for node in branch:
            keyFormulaAnnotation = [node.getKey(), node.getValue(), node.getAnnotation()]
            if not keyFormulaAnnotation in self.notEAnalysedFormulas[branchNum]:
                self.insertFormulaIntoNotEAnalysedFormulasList(keyFormulaAnnotation, branchNum)
            
    def insertFormulaIntoNotEAnalysedFormulasList(self, keyFormulaAnnotation, branchNum):
        formula = keyFormulaAnnotation[1]
        if not isAtomicFormula(formula) and not isNegationAtomicFormula(formula):
            if not self.isFormulaEAnalysed(formula, branchNum):
                self.notEAnalysedFormulas[branchNum].append(keyFormulaAnnotation)
                return True
        return False
    
    def removeFormulaFromNotEAnalysedFormulasList(self, keyFormulaAnnotation, branchNum):
        formula = keyFormulaAnnotation[1]
        if keyFormulaAnnotation in self.notEAnalysedFormulas[branchNum]:
            if self.isFormulaEAnalysed(formula, branchNum):
                self.notEAnalysedFormulas[branchNum].remove(keyFormulaAnnotation)
                return True
        return False
    
    def insertIntoNotFulfilledBetaFormulasList(self, branch, branchNum):
        for node in branch:
            keyFormulaAnnotation = [node.getKey(), node.getValue(), node.getAnnotation()]
            if not keyFormulaAnnotation in self.notFulfilledBetaFormulas[branchNum]:
                self.insertFormulaIntoNotFulfilledBetaFormulasList(keyFormulaAnnotation, branchNum)
        
    def insertFormulaIntoNotFulfilledBetaFormulasList(self, keyFormulaAnnotation, branchNum):
        formula = keyFormulaAnnotation[1]
        if isBetaFormula(formula):
            if not self.isBetaFormulaFulfilled(formula, branchNum):
                self.notFulfilledBetaFormulas[branchNum].append(keyFormulaAnnotation)
                return True
        return False
    
    def removefromNotFullfilledBetaFormulasList(self, branch, branchNum):
        for node in branch:
            keyFormulaAnnotation = [node.getKey(), node.getValue(), node.getAnnotation()]
            if keyFormulaAnnotation in self.notFulfilledBetaFormulas[branchNum]:
                self.removeFormulaFromNotFulfilledBetaFormulasList(keyFormulaAnnotation, branchNum)
    
    def removeFormulaFromNotFulfilledBetaFormulasList(self, keyFormulaAnnotation, branchNum):
        formula = keyFormulaAnnotation[1]
        if isBetaFormula(formula):
            if keyFormulaAnnotation in self.notFulfilledBetaFormulas[branchNum]:
                if self.isBetaFormulaFulfilled(formula, branchNum):
                    self.notFulfilledBetaFormulas[branchNum].remove(keyFormulaAnnotation)
                    return True
        return False
    
    def isFormulaEAnalysed(self, formula, branchNum):
        if isDoubleNegationFormula(formula):
            return self.isDoubleNegationFormulaEAnalysed(formula, branchNum)
        elif isAlphaFormula(formula):
            return self.isAlphaFormulaEAnalysed(formula, branchNum)
        elif isBetaFormula(formula):
            return self.isBetaFormulaEAnalysed(formula, branchNum)
        else:
            return False
    
    def isDoubleNegationFormulaEAnalysed(self, doubleNegationFormula, branchNum):
        doubleNegationComponent = self.getDoubleNegationFormulaComponent(doubleNegationFormula)
        branch = self.tableauTree.getBranch(branchNum)
        for node in branch:
            value = node.getValue()
            if value == doubleNegationComponent:
                return True
        return False
    
    def isAlphaFormulaEAnalysed(self, alphaFormula, branchNum):
        alphaFormulaComponents = self.getAlphaFormulaComponents(alphaFormula)
        alphaComponent1 = alphaFormulaComponents[0]
        alphaComponent2 = alphaFormulaComponents[1]
        if isDoubleNegationFormula(alphaComponent1):
            alphaComponent1 = self.getDoubleNegationFormulaComponent(alphaComponent1)
        if isDoubleNegationFormula(alphaComponent2):
            alphaComponent2 = self.getDoubleNegationFormulaComponent(alphaComponent2)
        branch = self.tableauTree.getBranch(branchNum)
        for node in branch:
            value = node.getValue()
            if value == alphaComponent1:
                for newNode in branch:
                    newValue = newNode.getValue()
                    if newValue == alphaComponent2:
                        return True
        return False
    
    def isBetaFormulaEAnalysed(self, betaFormula, branchNum):
        betaFormulaComponents = self.getBetaFormulaComponents(betaFormula)
        firstBetaComponent = betaFormulaComponents[0]
        secondBetaComponent = betaFormulaComponents[1]
        if isDoubleNegationFormula(firstBetaComponent):
            firstBetaComponent = self.getDoubleNegationFormulaComponent(firstBetaComponent)
        if isDoubleNegationFormula(secondBetaComponent):
            secondBetaComponent = self.getDoubleNegationFormulaComponent(secondBetaComponent)
        negFirstBetaComponent = self.negateFormula(firstBetaComponent)
        negSecondBetaComponent = self.negateFormula(secondBetaComponent)
        if isDoubleNegationFormula(negFirstBetaComponent):
            negFirstBetaComponent = self.getDoubleNegationFormulaComponent(negFirstBetaComponent)
        if isDoubleNegationFormula(negSecondBetaComponent):
            negSecondBetaComponent = self.getDoubleNegationFormulaComponent(negSecondBetaComponent)    
        branch = self.tableauTree.getBranch(branchNum)
        firstBetaComponentInBranch = self.isFormulaInBranch(firstBetaComponent, branch)
        secondBetaComponentInBranch = self.isFormulaInBranch(secondBetaComponent, branch)
        negFirstBetaComponentInBranch = self.isFormulaInBranch(negFirstBetaComponent, branch)
        negSecondBetaComponentInBranch = self.isFormulaInBranch(negSecondBetaComponent, branch)
        if not negFirstBetaComponentInBranch and not negSecondBetaComponentInBranch:
            return True
        if negFirstBetaComponentInBranch and not secondBetaComponentInBranch:
            if negSecondBetaComponentInBranch and firstBetaComponentInBranch:
                return True
            else:
                return False
        elif negFirstBetaComponentInBranch and secondBetaComponentInBranch:
            return True
        elif negSecondBetaComponentInBranch and not firstBetaComponentInBranch:
            if negFirstBetaComponentInBranch and secondBetaComponentInBranch:
                return True
            else:
                return False
        else:
            return True
                    
    def isFormulaInBranch(self, formula, branch):
        for node in branch:
            value = node.getValue()
            if value == formula:
                return True
        return False
        
    def isBranchECompleted(self, branchNum):
        if self.areAllFormulasEAnalysed(branchNum):
            return True
        else:
            return False
        
    def areAllFormulasEAnalysed(self, branchNum):
        if len(self.notEAnalysedFormulas[branchNum]) == 0:
            return True
        else:
            return False
        
    def isBetaFormulaFulfilled(self, betaFormula, branchNum):
        branch = self.tableauTree.getBranch(branchNum)
        betaFormulaComponents = self.getBetaFormulaComponents(betaFormula)
        betaComponent1 = betaFormulaComponents[0]
        betaComponent2 = betaFormulaComponents[1]
        if isDoubleNegationFormula(betaComponent1):
            betaComponent1 = self.getDoubleNegationFormulaComponent(betaComponent1)
        if isDoubleNegationFormula(betaComponent2):
            betaComponent2 = self.getDoubleNegationFormulaComponent(betaComponent2)
        if self.branchContainsFormula(branch, betaComponent1) or self.branchContainsFormula(branch, betaComponent2):
            return True
        else:
            return False
        
    def branchContainsFormula(self, branch, formula):
        for node in branch:
            value = node.getValue()
            if value == formula:
                return True
        return False
        
    def areAllBetaFormulasFulfilled(self, branchNum):
        if len(self.notFulfilledBetaFormulas[branchNum]) == 0:
            return True
        else:
            return False
        
    def isBranchCompleted(self, branchNum):
        if self.isBranchECompleted(branchNum) and self.areAllBetaFormulasFulfilled(branchNum):
            return True
        else:
            return False
    
    def isTableauCompleted(self):
        branches = self.tableauTree.getBranches(self.tableauTree.getRoot())
        branchNum = 1
        for branch in branches:
            if not self.isBranchCompleted(branchNum):
                return False
            branchNum = branchNum + 1
        return True
            
def isAtomicFormula(formula):
    if len(formula) == 1:
        return True
    else:
        return False
    
def isNegationAtomicFormula(formula):
    if len(formula) == 2 and isAtomicFormula(formula[1]):
        return True
    else:
        return False

def isNegationFormula(formula):
    if len(formula) == 2 and formula[0] == '~':
        return True
    else:
        return False

def isDoubleNegationFormula(formula):
    if len(formula) == 2:
        subFormula = formula[1]
        if formula[0] == '~' and isNegationFormula(subFormula):
            return True
        else:
            return False

def isAlphaFormula(formula):
    if isConjunctionFormula(formula):
        return True
    elif isDisjunctionNegationFormula(formula):
        return True
    elif isImplicationNegationFormula(formula):
        return True
    else:
        return False

def isBetaFormula(formula):
    if isDisjunctionFormula(formula):
        return True
    elif isImplicationFormula(formula):
        return True
    elif isConjunctionNegationFormula(formula):
        return True
    else:
        return False
    
def isConjunctionFormula(formula):
    if len(formula) == 3 and formula[1] == '&':
        return True
    else:
        return False

def isDisjunctionNegationFormula(formula):
    if len(formula) == 2  and formula[0] == '~' and isDisjunctionFormula(formula[1]):
        return True
    else:
        return False
        
def isImplicationNegationFormula(formula):
    if len(formula) == 2 and formula[0] == '~' and isImplicationFormula(formula[1]):
        return True
    else:
        return False

def isConjunctionNegationFormula(formula):
    if len(formula) == 2 and formula[0] == '~' and isConjunctionFormula(formula[1]):
        return True
    else:
        return False

def isDisjunctionFormula(formula):
    if len(formula) == 3 and formula[1] == '|':
        return True
    else:
        return False

def isImplicationFormula(formula):
    if len(formula) == 3 and formula[1] == '->':
        return True
    else:
        return False
    
def areInContraddiction(formulaOne, formulaTwo):
    if len(formulaOne) == 2 and formulaOne[0] == '~':
        if len(formulaTwo) == 1 and formulaTwo == formulaOne[1]:
            return True
        else:
            return False
    elif len(formulaTwo) == 2 and formulaTwo[0] == '~':
        if len(formulaOne) == 1 and formulaOne == formulaTwo[2]:
            return True
        else:
            return False
    else:
        return False
    
def getNegation(formula):
    if len(formula) == 2 and formula[0] == '~':
        return formula[1]
    elif len(formula) == 1 or len(formula) == 3:
        return ['~', formula]
    else:
        return None