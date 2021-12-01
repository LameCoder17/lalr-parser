from copy import deepcopy

class State:
    stateCount = -1
    def __init__(self, new_state):
        self.state = deepcopy(new_state)
        self.actions = {}
        self.parent = ()
        State.stateCount += 1
        self.stateNo = self.stateCount

    def updateGoTo(self, X, N):
        self.actions[X] = N.stateNo

    def updateParentName(self,I,X):
        self.parent = (I.stateNo, X)


class lalrState(State):
    stateCount = 0
    def __init__(self,state):
        super(lalrState, self).__init__(state.state)
        self.parentList = []
        self.actions = deepcopy(state.actions)
        self.parent = deepcopy(state.parent)
        lalrState.stateCount += 1

    def updateParentList(self,I):
        self.parentList.append(I.stateCount)

    def updateMapping(self,mapping):
        if self.parent != ():
            self.parent = (mapping[self.parent[0]],self.parent[1])
        for key, val in self.actions.items():
            self.actions[key] = mapping[val]
