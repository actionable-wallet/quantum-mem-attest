#!/usr/bin/python3

import soqcs, sys

def rotationX(state, theta):
    # 0 -> rotate around x-axis
    simulator = soqcs.simulator()
    rX = state
    rX.beamsplitter(0, 1, 45.0, theta)
    
    rX.detector(0)
    rX.detector(1)
    
    rX.show(depth=7,sizexy=70)
    qmap = [[0], [1]]
    outcome = simulator.run_st(rX.input(), rX.circuit())
    qubit = outcome.encode(qmap, rX.circuit())
    qubit.prnt_state()
    

def hadamardGate(state):
    
    # 50:50 beam splitter
    simulator = soqcs.simulator()
    test = state
    # consists of a 90 degree rotation about the y-axis
    # then a 180 degree rotation about the x-axis
    test.beamsplitter(0, 1, 45.0, 0)  
    # phase shift by 180
    test.beamsplitter(1, 1, 0.0, 180.0)

    test.detector(0)
    test.detector(1)
    #test.show(depth=7,sizexy=70)
    #test.show()
    qmap = [[0], [1]]
    outcome = simulator.run_st(test.input(), test.circuit())
    qubit = outcome.encode(qmap, test.circuit())
    qubit.prnt_state(column=1)
    


def main():
    # Maximum number of photons = 2 (parameter 1)
    # Creates two channels (parameter 2)
    initState = soqcs.qodev(2,2)
    initState.add_photons(0, 0) # adds a 0 state to channel 0
    initState.add_photons(1, 1) # adds a 1 state to channel 1
    rotationX(initState, 90)
    hadamardGate(initState)


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
   