import sys
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from design import Ui_MainWindow

from impl import calculateFirst, getTerminalsAndNonTerminals, getAugmented , findStates, combineStates, makeParseTable
from  state import State, lalrState

class parser(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1024, 720)
        self.setWindowTitle("LALR Parser")
        
        self.init()
        
        self.ui.action_Exit.triggered.connect(self.exitProgram)
        self.ui.displayButton.clicked.connect(self.displayGrammar)
        self.ui.firstButton.clicked.connect(self.displayFirst)
        self.ui.lr1Button.clicked.connect(self.displayLR1States)
        self.ui.lalrButton.clicked.connect(self.displayLALRStates)
        self.ui.parseTableButton.clicked.connect(self.displayParseTable)
        self.ui.plainTextEdit.textChanged.connect(self.checkChanged)
        self.ui.parse.clicked.connect(self.displayParsing)
        self.ui.actionAuthor.triggered.connect(self.showAuthor)
        self.ui.action_Open.triggered.connect(self.openFile)
        
        self.ui.evaluationBox.setStyleSheet("color: black; border: 0px solid black;")
        self.ui.rowWithButtons.setStyleSheet("color: black; border: 1px solid black;")
        self.ui.epsilonBox.setStyleSheet("color: black; border: 0px solid black;")
        self.ui.displayScreen.setStyleSheet("color: black; border: 4px solid black;")  # Display screen
        self.ui.plainTextEdit.setStyleSheet("color: black; border: 4px solid black;")  # Screen for input


    def init(self):
        self.grammar = []
        self.augmentedGrammar = []
        self.first = {}
        self.term = []
        self.nonTerminals = []
        self.states = []
        self.lalrStates = []
        self.parseTable = []
        State.stateCount = -1
        lalrState.stateCount = 0

    def checkChanged(self):
        self.changed = True


    def openFile(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self,'Open Grammar file')
        if file[0] != '':
            file = open(file[0],'r')
            self.ui.plainTextEdit.setPlainText(file.read())
            file.close()
            self.ui.lineEdit.clear()
            self.ui.displayScreen.clear()


    def readInputGrammar(self):
        self.init()
        lines = self.ui.plainTextEdit.toPlainText()         #string
        lines_list = lines.split('\n')                      #converting into list of lines

        try:
            for line in lines_list:
                line = line.replace(' ' ,'')
        
                if line != '':
                    listOfLines = line.split('->')
        
                    if listOfLines[0].isupper() and listOfLines[1] != '':
                        if '|' in listOfLines[1]:
                            prod_list = listOfLines[1].split('|')
                            for prod in prod_list:
                                self.grammar.append([listOfLines[0],prod])
                        else:
                            self.grammar.append(listOfLines)
                    else:
                        self.ui.displayScreen.clear()
                        self.ui.displayScreen.setText("Invalid grammar")
                        self.grammar = []
    
            if self.grammar != []:
                getTerminalsAndNonTerminals(self.grammar,self.term,self.nonTerminals)
                calculateFirst(self.grammar,self.first,self.term,self.nonTerminals)
                getAugmented(self.grammar,self.augmentedGrammar)
                findStates(self.states,self.augmentedGrammar,self.first,self.term,self.nonTerminals)
                combineStates(self.lalrStates, self.states)
                makeParseTable(self.parseTable,self.lalrStates,self.augmentedGrammar)
                self.changed = False

        except (KeyError, IndexError):
            self.ui.displayScreen.clear()
            self.ui.displayScreen.setText("Invalid grammar")
            self.init()
            
############################         DISPLAY          ################################

    def displayGrammar(self):
        self.ui.displayScreen.clear()
        if self.grammar == [] or self.changed:
            self.readInputGrammar()

        if self.grammar != []:
            for prod in self.grammar:
                s =  prod[0]+ ' -> ' + prod[1]+'\n'
                self.ui.displayScreen.append(s)
            self.ui.displayScreen.append("\nNon Terminals : "+' '.join(self.nonTerminals)+"\nTerminals : "+' '.join(self.term))
        
    def displayFirst(self):
        if self.first == {} or self.changed:
            self.readInputGrammar()
        if self.first != {}:
            self.ui.displayScreen.clear()
            for nonterm in self.nonTerminals:
                self.ui.displayScreen.append('First('+nonterm+') : '+' '.join(self.first[nonterm])+'\n')

    def displayLR1States(self):
        if self.states == [] or self.changed:
            self.readInputGrammar()
        if self.states != []:
            self.ui.displayScreen.clear()
            self.ui.displayScreen.append("Number of LR(1) states : "+ str(self.states[len(self.states)-1].stateNo + 1))
            for state in self.states:
                self.ui.displayScreen.append('----------------------------------------------------------------')
                if state.stateNo == 0:
                    self.ui.displayScreen.append("\nI"+str(state.stateNo)+' : '+'\n')
                else:
                    self.ui.displayScreen.append("\nI"+str(state.stateNo)+' : '+' goto ( I'+str(state.parent[0])+" -> '"+ str(state.parent[1]) +"' )\n")
                for item in state.state:
                    self.ui.displayScreen.append(item[0]+ ' -> ' + item[1]+' ,  [ '+ ' '.join(item[2])+' ]')
                if state.actions != {}:
                    self.ui.displayScreen.append('\nActions : ')
                    for k,v in state.actions.items():
                        self.ui.displayScreen.insertPlainText(str(k)+' -> '+str(abs(v))+'\t')

    def displayLALRStates(self):
        if self.lalrStates == [] or self.changed:
            self.readInputGrammar()
        if self.lalrStates != []:
            self.ui.displayScreen.clear()
            self.ui.displayScreen.append("Number of LALR states : " + str(lalrState.stateCount))
            for state in self.lalrStates:
                self.ui.displayScreen.append('----------------------------------------------------------------')
                if state.stateNo == 0:
                    self.ui.displayScreen.append("\nI"+str(state.stateNo)+' : '+'\tGot by -> '+str(state.parentList)+'\n')
                else:
                    self.ui.displayScreen.append("\nI"+str(state.stateNo)+' : '+' goto ( I'+str(state.parent[0])+" -> '"+ str(state.parent[1]) +"' )"+'\tGot by -> '+str(state.parentList)+'\n')
                for item in state.state:
                    self.ui.displayScreen.append(item[0]+ ' -> ' + item[1]+' ,   [ '+ ' '.join(item[2])+' ]')
                if state.actions != {}:
                    self.ui.displayScreen.append('\nActions : ')
                    for k,v in state.actions.items():
                        self.ui.displayScreen.insertPlainText(str(k)+' -> '+str(abs(v))+'\t')

    def displayParseTable(self):
        if self.grammar == [] or self.changed:
            self.readInputGrammar()

        if self.grammar != []:
            self.ui.displayScreen.clear()
            allSymbols = []
            allSymbols.extend(self.term)
            allSymbols.append('$')
            allSymbols.extend(self.nonTerminals)
            if 'e' in allSymbols:
                allSymbols.remove('e')

            head = '{0:12}'.format(' ')
            for X in allSymbols:
                head = head + '{0:12}'.format(X)
            self.ui.displayScreen.setText(head+'\n')
            s = '------------'*len(allSymbols)
            self.ui.displayScreen.append(s)

            for index, state in enumerate(self.parseTable):
                line = '{0:<12}'.format(index)
                for X in allSymbols:
                    if X in state.keys():
                        if X in self.nonTerminals:
                            action = state[X]
                        else:
                            if state[X] > 0:
                                action = 's' + str(state[X])
                            elif state[X] < 0:
                                action = 'r' + str(abs(state[X]))
                            elif state[X] == 0:
                                action = 'accept'
                        
                        line = line + '{0:<12}'.format(action)
                    else:
                        line = line + '{0:<12}'.format("")
    
                self.ui.displayScreen.append(line)
                self.ui.displayScreen.append(s)

    def displayParsing(self):
        if self.grammar == [] or self.changed:
            self.readInputGrammar()
        if self.grammar != []:
            self.ui.displayScreen.clear()
            line_input = self.ui.lineEdit.text()
            self.parse(self.parseTable, self.augmentedGrammar, line_input)

    def parse(self,parse_table,augment_grammar,inpt):
        inpt = list(inpt+'$')
        stack = [0]
        a = inpt[0]
        try:
            head = '{0:50} {1:50} {2:50}'.format("Stack","Input", "Actions")
            self.ui.displayScreen.setText(head)
            while True:
                x = ''.join(inpt)
                string = f'\n {str(stack):50} {str(x):50} '
                s = stack[len(stack)-1]
                action = parse_table[s][a]
                if action > 0:
                    inpt.pop(0)
                    stack.append(action)
                    self.ui.displayScreen.append(string + 'Shift ' + a+ '\n')
                    a = inpt[0]
                elif action < 0:
                    prod = augment_grammar[-action]
                    if prod[1] != 'e':
                        for i in prod[1]:
                            stack.pop()
                    t = stack[len(stack)-1]
                    stack.append(parse_table[t][prod[0]])
                    self.ui.displayScreen.append(string + 'Reduce ' + prod[0] + ' -> '+ prod[1] + '\n')
                elif action == 0:
                    self.ui.displayScreen.append('ACCEPTED\n')
                    break
        except KeyError:
            self.ui.displayScreen.append('\n\nREJECTED\n')

    def exitProgram(self):
        QtGui.QApplication.quit()
        
    def showAuthor(self):
        QtWidgets.QMessageBox.information(self, "About", "LALR PARSER\n\nAuthor:\n  Akshay Hebbar Y S\t", QtWidgets.QMessageBox.Ok)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = parser()
    myapp.show()
    sys.exit(app.exec())
