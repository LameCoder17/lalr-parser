import sys
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from design import Ui_MainWindow

from impl import calculate_first, term_and_nonterm, get_augmented , find_states, combine_states, get_parse_table
from  state import State, lalrState

class parser(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        '''
        Default constructor
        Connects buttons and some UI design
        '''
        QtWidgets.QMainWindow.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1024, 720)
        self.setWindowTitle("LALR Parser")

        self.init()

        self.ui.displayButton.clicked.connect(self.disp)
        self.ui.firstButton.clicked.connect(self.disp_first)
        self.ui.clr1Button.clicked.connect(self.disp_lr1_states)
        self.ui.lalrButton.clicked.connect(self.disp_lalr_states)
        self.ui.parseTableButton.clicked.connect(self.disp_parse_table)
        self.ui.parse.clicked.connect(self.disp_parsing)
        self.ui.inputScreen.textChanged.connect(self.check_changed)
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionExit.triggered.connect(self.exit_app)
        
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
        self.augment_grammar = []
        self.first = {}
        self.term = []
        self.non_term = []
        self.states = []
        self.lalr_states = []
        self.parse_table = []
        State.state_count = -1
        lalrState.state_count = 0
        self.ambiguous = False

    def check_changed(self):
        '''
        Checks if the grammar is changed or not
        '''
        self.changed = True


    def open_file(self):
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


    def read_input(self):
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
                    line_list = line.split('->')
        
                    if line_list[0].isupper() and line_list[1] != '':
                        if '|' in line_list[1]:
                            prod_list = line_list[1].split('|')
                            for prod in prod_list:
                                self.grammar.append([line_list[0],prod])
                        else:
                            self.grammar.append(line_list)
                    else:
                        self.ui.displayScreen.clear()
                        self.ui.displayScreen.setText("Invalid grammar")
                        self.grammar = []
    
            if self.grammar != []:
                term_and_nonterm(self.grammar,self.term,self.non_term)
                calculate_first(self.grammar,self.first,self.term,self.non_term)
                get_augmented(self.grammar,self.augment_grammar)
                find_states(self.states,self.augment_grammar,self.first,self.term,self.non_term)
                combine_states(self.lalr_states, self.states)
                self.ambiguous = get_parse_table(self.parse_table,self.lalr_states,self.augment_grammar)
                self.changed = False

        except (KeyError, IndexError):
            self.ui.displayScreen.clear()
            self.ui.displayScreen.setText("Invalid grammar")
            self.init()
            
    def disp(self):
        '''
        Displays the grammar inputted
        '''
        self.ui.displayScreen.clear()
        if self.grammar == [] or self.changed:
            self.read_input()

        if self.grammar != []:
            for prod in self.grammar:
                s =  prod[0]+ ' -> ' + prod[1]+'\n'
                self.ui.displayScreen.append(s)
            self.ui.displayScreen.append("\nNon Terminals : "+' '.join(self.non_term)+"\nTerminals : "+' '.join(self.term))
        
    def disp_first(self):
        '''
        Displays the first of the given grammar
        '''
        if self.first == {} or self.changed:
            self.read_input()
        if self.first != {}:
            self.ui.displayScreen.clear()
            for nonterm in self.non_term:
                self.ui.displayScreen.append('First('+nonterm+') : '+' '.join(self.first[nonterm])+'\n')

    def disp_lr1_states(self):
        '''
        Makes the CLR(1) states DFA
        '''
        if self.states == [] or self.changed:
            self.read_input()
        if self.states != []:
            self.ui.displayScreen.clear()
            self.ui.displayScreen.append("Number of LR(1) states : "+ str(self.states[len(self.states)-1].state_num + 1))
            for state in self.states:
                self.ui.displayScreen.append('----------------------------------------------------------------')
                if state.state_num == 0:
                    self.ui.displayScreen.append("\nI"+str(state.state_num)+' : '+'\n')
                else:
                    self.ui.displayScreen.append("\nI"+str(state.state_num)+' : '+' goto ( I'+str(state.parent[0])+" -> '"+ str(state.parent[1]) +"' )\n")
                for item in state.state:
                    self.ui.displayScreen.append(item[0]+ ' -> ' + item[1]+' ,  [ '+ ' '.join(item[2])+' ]')
                if state.actions != {}:
                    self.ui.displayScreen.append('\nActions : ')
                    for k,v in state.actions.items():
                        self.ui.displayScreen.insertPlainText(str(k)+' -> '+str(abs(v))+'\t')

    def disp_lalr_states(self):
        '''
        Makes the LALR(1) states
        '''
        if self.lalr_states == [] or self.changed:
            self.read_input()
        if self.lalr_states != []:
            self.ui.displayScreen.clear()
            self.ui.displayScreen.append("Number of LALR states : " + str(lalrState.state_count))
            for state in self.lalr_states:
                self.ui.displayScreen.append('----------------------------------------------------------------')
                if state.state_num == 0:
                    self.ui.displayScreen.append("\nI"+str(state.state_num)+' : '+'\tGot by -> '+str(state.parent_list)+'\n')
                else:
                    self.ui.displayScreen.append("\nI"+str(state.state_num)+' : '+' goto ( I'+str(state.parent[0])+" -> '"+ str(state.parent[1]) +"' )"+'\tGot by -> '+str(state.parent_list)+'\n')
                for item in state.state:
                    self.ui.displayScreen.append(item[0]+ ' -> ' + item[1]+' ,   [ '+ ' '.join(item[2])+' ]')
                if state.actions != {}:
                    self.ui.displayScreen.append('\nActions : ')
                    for k,v in state.actions.items():
                        self.ui.displayScreen.insertPlainText(str(k)+' -> '+str(abs(v))+'\t')

    def disp_parse_table(self):
        '''
        Displays the parsing table
        '''
        if self.grammar == [] or self.changed:
            self.read_input()

        if self.grammar != []:
            self.ui.displayScreen.clear()
            
            if self.ambiguous:
                self.ui.displayScreen.append("Ambiguous Grammar Detected \n\n Choosing Shift over Reduce\n\n")
                
            all_symb = []
            all_symb.extend(self.term)
            all_symb.append('$')
            all_symb.extend(self.non_term)
            if 'e' in all_symb:
                all_symb.remove('e')

            head = '{0:12}'.format(' ')
            for X in all_symb:
                head = head + '{0:12}'.format(X)
            self.ui.displayScreen.append(head+'\n')
            s = '------------'*len(all_symb)
            self.ui.displayScreen.append(s)

            for index, state in enumerate(self.parse_table):
                line = '{0:<12}'.format(index)
                for X in all_symb:
                    if X in state.keys():
                        if X in self.non_term:
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

    def disp_parsing(self):
        '''
        Takes the string for parsing
        '''
        if self.grammar == [] or self.changed:
            self.read_input()
        if self.grammar != []:
            self.ui.displayScreen.clear()
            line_input = self.ui.lineEdit.text()
            self.parse(self.parse_table, self.augment_grammar, line_input)

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
                    self.ui.displayScreen.append('ACCEPT\n')
                    break
        except KeyError:
            self.ui.displayScreen.append('\n\nERROR\n')

    def exit_app(self):
        '''
        Exits the program
        '''
        QtGui.QApplication.quit()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = parser()
    myapp.show()
    sys.exit(app.exec())
