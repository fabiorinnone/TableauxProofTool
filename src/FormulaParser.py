'''
FormulaParser.py

@author: fabior
'''

from pyparsing import Word, alphas, Keyword, ParserElement, operatorPrecedence, opAssoc

class Parser(object):
    
    def parse(self, formulaStr):
        ParserElement.enablePackrat()
        
        formulaStr = self.fixFormulaStr(formulaStr)
        
        propLetter = Word(alphas, exact = 1)
        
        notOp = Keyword('~')
        andOp = Keyword('&')
        orOp = Keyword('|')
        impliesOp = Keyword('->')
        
        atomicFormula = propLetter
        
        formula = operatorPrecedence(atomicFormula,
            [(notOp, 1, opAssoc.RIGHT),
             (andOp, 2, opAssoc.LEFT),
             (orOp, 2, opAssoc.LEFT),
             (impliesOp, 2, opAssoc.LEFT)]
            )
            
        res = formula.parseString(formulaStr, parseAll=True)
        
        l = res.asList()
        return l
    
    def fixFormulaStr(self, formulaStr):
        formulaStrFixed = ''
        
        for i in range(len(formulaStr)):
            if formulaStr[i] == '~' and formulaStr[i+1] != ' ':
                formulaStrFixed = formulaStrFixed + formulaStr[i] + ' '
            if formulaStr[i] != '~':
                formulaStrFixed = formulaStrFixed + formulaStr[i]
                
        return formulaStrFixed
            
def getStringFormula(formula):
    if type(formula) is str:
        return formula
    elif type(formula) is list and len(formula) == 1:
        return '('+formula[0]+')'
    elif len(formula) == 2:
        operator = getStringFormula(formula[0])
        subFormula = getStringFormula(formula[1])
        if len(formula[1]) == 1 and type(formula[1]) is str:
            return operator+subFormula
        else:
            if type(formula[1]) is str:
                return operator+' '+subFormula
            else:
                return operator+' ('+str(subFormula)+')'
    else:
        subFormulaOne = getStringFormula(formula[0])
        operator = getStringFormula(formula[1])
        subFormulaTwo = getStringFormula(formula[2])
        if len(formula[0]) == 1 and len(formula[2]) > 1:
            if type(formula[0]) is str:
                return str(subFormulaOne)+' '+str(operator)+' ('+str(subFormulaTwo)+')'
            else:
                return '('+str(subFormulaOne)+') '+str(operator)+' ('+str(subFormulaTwo)+')'
        elif len(formula[0]) > 1 and len(formula[2]) == 1:
            if type(formula[2]) is str:
                return '('+str(subFormulaOne)+') '+str(operator)+' '+str(subFormulaTwo)
            else:
                return '('+str(subFormulaOne)+') '+str(operator)+' ('+str(subFormulaTwo)+')'
        elif len(formula[0]) == 1 and len(formula[2]) == 1:
            if type(formula[0]) is str and not type(formula[2] is str):
                return str(subFormulaOne)+str(operator)+'('+str(subFormulaTwo)+')'
            elif not type(formula[0]) is str and type(formula[2]) is str:
                return '('+str(subFormulaOne)+') '+str(operator)+' '+str(subFormulaTwo)
            elif type(formula[0]) is str and type(formula[2]) is str:
                return str(subFormulaOne)+' '+str(operator)+' '+str(subFormulaTwo)
        else:
            return '('+str(subFormulaOne)+') '+str(operator)+' ('+str(subFormulaTwo)+')'