import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from design import MainWindow
from impl import calculateFirst, getTerminalsAndNonTerminals, getAugmented , findStates, combineStates, makeParseTable
from state import State, lalrState

class LALRParser(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        '''
        Default constructor
        Connects buttons and some UI design
        '''
        QtWidgets.QMainWindow.__init__(self,parent)
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1024, 720)
        self.setWindowTitle("LALR Parser")
        
        self.init()
        
        self.ui.displayButton.clicked.connect(self.displayGrammar)
        self.ui.firstButton.clicked.connect(self.displayFirst)
        self.ui.clr1Button.clicked.connect(self.displayCLR1States)
        self.ui.lalrButton.clicked.connect(self.displayLALRStates)
        self.ui.parseTableButton.clicked.connect(self.displayParseTable)
        self.ui.parse.clicked.connect(self.displayParsing)
        self.ui.inputScreen.textChanged.connect(self.checkChanged)
        self.ui.actionOpen.triggered.connect(self.openFile)
        self.ui.actionExit.triggered.connect(self.exitProgram)
        
        self.ui.evaluationBox.setStyleSheet("color: black; border: 0px solid black;")
        self.ui.rowWithButtons.setStyleSheet("color: black; border: 0px solid black;")
        self.ui.epsilonBox.setStyleSheet("color: black; border: 0px solid black;")
        self.ui.displayScreen.setStyleSheet("color: black; border: 4px solid black;")
        self.ui.inputScreen.setStyleSheet("color: black; border: 4px solid black;")  


    def init(self):
        '''
        Initializes all variables needed
        '''
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
        self.isAmbiguous = False

    def checkChanged(self):
        '''
        Checks if the grammar is changed or not
        '''
        self.changed = True


    def openFile(self):
        '''
        Opens a file and reads the grammar written on it
        '''
        file = QtWidgets.QFileDialog.getOpenFileName(self,'Open Grammar file')
        if file[0] != '':
            file = open(file[0],'r')
            self.ui.inputScreen.setPlainText(file.read())
            file.close()
            self.ui.lineEdit.clear()
            self.ui.displayScreen.clear()


    def readInputGrammar(self):
        '''
        Reads the grammar from the inputScreen
        '''
        self.init()
        lines = self.ui.inputScreen.toPlainText()        
        lines_list = lines.split('\n')                     
        
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
                        self.ui.displayScreen.setText("Invalid grammar !")
                        self.grammar = []
    
            if self.grammar != []:
                getTerminalsAndNonTerminals(self.grammar,self.term,self.nonTerminals)  
                calculateFirst(self.grammar,self.first,self.term,self.nonTerminals)
                getAugmented(self.grammar,self.augmentedGrammar)
                findStates(self.states,self.augmentedGrammar,self.first,self.term,self.nonTerminals)
                combineStates(self.lalrStates, self.states)
                self.isAmbiguous = makeParseTable(self.parseTable,self.lalrStates,self.augmentedGrammar)
                self.changed = False

        except (KeyError, IndexError):
            self.ui.displayScreen.clear()
            self.ui.displayScreen.setText("Invalid grammar")
            self.init()
            
    def displayGrammar(self):
        '''
        Displays the grammar inputted
        '''
        self.ui.displayScreen.clear()
        if self.grammar == [] or self.changed:
            self.readInputGrammar()

        if self.grammar != []:
            for prod in self.grammar:
                s =  prod[0]+ ' -> ' + prod[1]+'\n'
                self.ui.displayScreen.append(s)
            self.ui.displayScreen.append("\nNon Terminals : "+' '.join(self.nonTerminals)+"\nTerminals : "+' '.join(self.term))
        
    def displayFirst(self):
        '''
        Displays the first of the given grammar
        '''
        if self.first == {} or self.changed:
            self.readInputGrammar()
        if self.first != {}:
            self.ui.displayScreen.clear()
            for nonterm in self.nonTerminals:
                self.ui.displayScreen.append('First('+nonterm+') : '+' '.join(self.first[nonterm])+'\n')

    def displayCLR1States(self):
        '''
        Makes the CLR(1) states DFA
        '''
        if self.states == [] or self.changed:
            self.readInputGrammar()
        if self.states != []:
            self.ui.displayScreen.clear()
            self.ui.displayScreen.append("Number of CLR(1) states : "+ str(self.states[len(self.states)-1].stateNo + 1))
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
                        self.ui.displayScreen.insertPlainText(str(k)+' -> '+ str(abs(v))+'\t')

    def displayLALRStates(self):
        '''
        Makes the LALR(1) states
        '''
        if self.lalrStates == [] or self.changed:
            self.readInputGrammar()
        if self.lalrStates != []:
            self.ui.displayScreen.clear()
            self.ui.displayScreen.append("Number of LALR(1) states : " + str(lalrState.stateCount))
            for state in self.lalrStates:
                if int(state.parentList[0]) >= int(self.states[len(self.states)-1].stateNo + 1):
                    for i in range(len(state.parentList)):
                        state.parentList[i] = int(int(state.parentList[i]) - int(self.states[len(self.states)-1].stateNo + 1) + i)
                        
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
        '''
        Displays the parsing table
        '''
        if self.grammar == [] or self.changed:
            self.readInputGrammar()

        if self.grammar != []:
            self.ui.displayScreen.clear()
            
            print(self.isAmbiguous)
            if self.isAmbiguous:
                self.ui.displayScreen.append("Ambiguous Grammar Detected \n\n Choosing Shift over Reduce\n\n")
            
            allSymbols = []
            allSymbols.extend(self.term)
            allSymbols.append('$')
            allSymbols.extend(self.nonTerminals)
            if 'e' in allSymbols:
                allSymbols.remove('e')

            head = '{0:12}'.format(' ')
            for X in allSymbols:
                head = head + '{0:12}'.format(X)
            self.ui.displayScreen.append(head+'\n')
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
        '''
        Takes the string for parsing
        '''
        if self.grammar == [] or self.changed:
            self.readInputGrammar()
        if self.grammar != []:
            self.ui.displayScreen.clear()
            line_input = self.ui.lineEdit.text()
            self.parse(self.parseTable, self.augmentedGrammar, line_input)

    def parse(self,parse_table,augment_grammar,inpt):
        '''
        Parses the inputted string with the given grammar
        '''
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
                    self.ui.displayScreen.append(string + 'Shift ' + a + '\n')
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
        '''
        Exits the program
        '''
        QtGui.QApplication.quit()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = LALRParser()
    myapp.show()
    sys.exit(app.exec())
