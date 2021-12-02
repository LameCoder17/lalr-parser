from state import State, lalrState
from copy import deepcopy

def getTerminalsAndNonTerminals(grammar,term,nonTerminals):
    '''
    Finds terminal and non-terminal symbols
    '''
    for prod in grammar:
        if prod[0] not in nonTerminals:
            nonTerminals.append(prod[0])
        for char in prod[1]:
            if not char.isupper():
                if char not in term:
                    term.append(char)


def calculateFirst(grammar,first,term,nonTerminals):
    '''
    Calculates first
    '''
    for t in term:
        first[t] = t;
    for nt in nonTerminals:
        first[nt] = set({})
    for nt in nonTerminals:
        getFirst(nt,grammar,first,term)


def getFirst(nt,grammar,first,term):
    '''
    Finds first
    '''
    for prod in grammar:
        if nt in prod[0]:
            rhs = prod[1]
            firstChar = rhs[0]
            if firstChar in term:
                first[nt].add(first[firstChar])
            else:
                for char in rhs:
                    if not first[char] and nt != char:
                        getFirst(char,grammar,first,term)

                i = 0
                while i < len(rhs) and 'e' in first[rhs[i]]:
                    for elem in first[rhs[i]]:
                        if 'e' != elem:
                            first[nt].add(elem)
                    i += 1
                if i == len(rhs):
                    first[nt].add('e')
                else:
                    for elem in first[rhs[i]]:
                        first[nt].add(elem)


def getAugmented(grammar,augmentedGrammar):
    '''
    Finds augmented grammar
    '''
    augmentedGrammar.append([grammar[0][0]+"'",grammar[0][0]])
    augmentedGrammar.extend(grammar)

def closure(I,augmentedGrammar,first,nonTerminal):
    '''
    Finds closure
    '''
    while True:
        isNewItemAdded = False
        for item in I:
            position = item[1].index('.')
            if position == (len(item[1])-1):
                continue
            next = item[1][position+1]
            if next in nonTerminal:
                for prod in augmentedGrammar:
                    if next == prod[0]:
                        if prod[1] == 'e':
                            rhs = 'e.'
                        else:
                            rhs = '.' + prod[1]
                        lookAhead = []                                    
                        if position < (len(item[1]) - 2):
                            Ba = item[1][position+2]
                            for firs in first[Ba]:
                                if 'e' == firs:
                                    for elem in item[2]:
                                        if elem not in lookAhead:
                                            lookAhead.append(elem)
                                else:
                                    if firs not in lookAhead:
                                        lookAhead.append(firs)
                        else:
                            lookAhead = deepcopy(item[2])

                        newItem = [next,rhs,lookAhead]    
                        
                        if newItem not in I:
                            sameStateWithDifferentLookAhead = False
                            for item_ in I:
                                if item_[0] == newItem[0] and item_[1] == newItem[1]:
                                    sameStateWithDifferentLookAhead = True
                                    for las in lookAhead:
                                        if las not in item_[2]:
                                            item_[2].append(las)
                                            isNewItemAdded = True
                            if not sameStateWithDifferentLookAhead:
                                I.append(newItem)
                                isNewItemAdded = True

        if not isNewItemAdded:
            break


def goto(I,X,augmentedGrammar,first,nonTerminals):
    '''
    Finds goto
    '''
    J =[]
    for item in I:
        position = item[1].index('.')
        if position < len(item[1])-1:
            next = item[1][position+1]
            if next == X :
                newRHS = item[1].replace('.'+X,X+'.')
                newItem = [item[0],newRHS,item[2]]
                J.append(newItem)
    closure(J,augmentedGrammar,first,nonTerminals)
    return J



def isSame(states,newState,I,X):
    '''
    Checks if same state exists or not
    '''
    for J in states:
        if J.state == newState:
            I.updateGoTo(X,J)
            return True
    return False



def initFirst(augmentedGrammar,first,nonTerminals):
    '''
    Initializes
    '''
    I = [[augmentedGrammar[0][0],'.'+augmentedGrammar[0][1],['$']]]
    closure(I,augmentedGrammar,first,nonTerminals)
    return I


def findStates(states,augmentedGrammar,first,terminals,nonTerminals):
    '''
    Finds the states of CLR(1)
    '''
    state1 = initFirst(augmentedGrammar,first,nonTerminals)
    I = State(state1)
    states.append(I)
    allSymbols = nonTerminals + terminals
    while True:
        isNewStateAdded = False
        for I in states:
            for X in allSymbols:
                newState = goto(I.state,X,augmentedGrammar,first,nonTerminals)            
                if (newState != [] ) and not isSame(states,newState,I,X):
                    N = State(newState)
                    I.updateGoTo(X,N)
                    N.updateParentName(I,X)
                    states.append(N)
                    isNewStateAdded = True

        if not isNewStateAdded:
            break


def combineStates(lalrStates,states):
    '''
    Combines the states of CLR(1) 
    '''
    first = lalrState(states[0])
    first.updateParentList(states[0])
    lalrStates.append(first)
    mapping = [0]
    for I in states[1:]:
        isStateFound = False
        for J in lalrStates:
            if J.state[0][:2] == I.state[0][:2] :
                isStateFound = True
                mapping.append(J.stateNo)
                J.updateParentList(I)
                for index, item in enumerate(J.state):
                    for la in I.state[index][2]:
                        if la not in item[2]:
                            item[2].append(la)

        if not isStateFound:
            newState = lalrState(I)
            newState.updateParentList(I)

            lalrStates.append(newState)
            mapping.append(newState.stateNo)

    for I in lalrStates:
        I.updateMapping(mapping)



def makeParseTable(parseTable,states,augmentedGrammar): 
    '''
    Makes the parse table
    '''         
    ambiguous = False
    for index, I in enumerate(states):
        parseTable.append(I.actions)
        for item in I.state:
            RHS = item[1].split('.')
            if RHS[1] == '':
                productionNo = augmentedGrammar.index([item[0],RHS[0]])
                for la in item[2]:
                    if la in parseTable[index].keys():
                        ambiguous = True
                    else:
                        parseTable[index][la] = -productionNo

    if ambiguous:
        print("Ambiguous Grammar Detected!!")
        
    return ambiguous
