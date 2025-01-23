

import soqcs, sys
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, MCXGate
from math import pi
from qiskit.quantum_info import Statevector
 
def qisKitTest():
    qc = QuantumCircuit(1)
    qc.measure_all()
    qc.remove_final_measurements()  
    psi = Statevector(qc)
    print("Before:")
    print(psi.to_dict())    
    #qc.rx(pi, 0)
    qc.x(0)

    #print(qc)
    qc.measure_all()
    qc.remove_final_measurements()  
    psi = Statevector(qc)
    print("After:")
    print(psi.to_dict())  

def rZ(state, theta): 
    return 0

def pauliX(state):
    simulator = soqcs.simulator()
    pX = state
    pX.separator()

    qmap = [[0], [1]]
    outcome = simulator.run_st(pX.input(), pX.circuit())
    qubit = outcome.encode(qmap, pX.circuit())
    
    print("Before:")
    qubit.prnt_state(column=1)
    

    pX.beamsplitter(0, 1, 270.0, 0)  
    pX.detector(0)
    pX.detector(1)
    # pX.show(depth=7, sizexy=70)
    qmap = [[0], [1]]
    outcome = simulator.run_st(pX.input(), pX.circuit())
    qubit = outcome.encode(qmap, pX.circuit())
    
    print("After:")
    qubit.prnt_state(column=1)
    return 0

def rX(state, theta):
    simulator = soqcs.simulator()
    rX = state
    rX.separator()

    qmap = [[0], [1]]
    outcome = simulator.run_st(rX.input(), rX.circuit())
    qubit = outcome.encode(qmap, rX.circuit())
    
    print("Before:")
    qubit.prnt_state(column=1)
    

    rX.beamsplitter(0, 1, theta / 2, 90.0)  
    rX.detector(0)
    rX.detector(1)
    # rX.show(depth=7, sizexy=70)
    qmap = [[0], [1]]
    outcome = simulator.run_st(rX.input(), rX.circuit())
    qubit = outcome.encode(qmap, rX.circuit())
    
    print("After:")
    qubit.prnt_state(column=1)
    return 0
def rY(state, theta):
    simulator = soqcs.simulator()
    rY = state
    rY.separator()

    qmap = [[0], [1]]
    outcome = simulator.run_st(rY.input(), rY.circuit())
    qubit = outcome.encode(qmap, rY.circuit())
    qubit.prnt_state(column=1)
    
    rY.beamsplitter(0, 1, theta / 2, 0)  
    rY.detector(0)
    rY.detector(1)
    # rY.show(depth=7, sizexy=70)
    qmap = [[0], [1]]
    outcome = simulator.run_st(rY.input(), rY.circuit())
    qubit = outcome.encode(qmap, rY.circuit())
    
    print("After:")
    qubit.prnt_state(column=1)
    

def main():

    test = soqcs.qodev(2,2)
    test.add_photons(0, 1) # adds a 0 state to channel 0
    test.add_photons(1, 0) # adds a 0 state to channel 0
    
    #rY(test, 270)
    #rX(test, 180)
    #rX(test, 180)
    pauliX(test)
    qisKitTest()
    
 
    

if __name__=="__main__":
    main()
   