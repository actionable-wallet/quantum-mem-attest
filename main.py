

import soqcs, sys
from math import sqrt, acos, pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

 
def qisKitRotationTest(angle, rotation, state):
    angle = (pi * angle) / 180
    qc = QuantumCircuit(1)
    qc.measure_all()
    qc.remove_final_measurements()  
    psi = Statevector(qc)
    print("Before:")
    print(psi.to_dict())  
    if rotation == 'x':
        qc.rx(angle, state)
    elif rotation == 'y':
        qc.ry(angle, state)
    elif rotation == 'z':
        qc.rz(angle, state)
    else:
        print("Incorrect usage: Choose 'x', 'y' or 'z'")
        sys.exit(1)
    qc.measure_all()
    qc.remove_final_measurements()  
    psi = Statevector(qc)
    print("After:")
    print(psi.to_dict())  

'''
Representing a 50:50 beam splitter
'''
def hadamardGate(ch1, ch2, state):
    return state.beamsplitter(ch1, ch2, 45.0, 0)

def pauliGate(state, rotation):
    simulator = soqcs.simulator()
    state.separator()

    qmap = [[0], [1]]
    outcome = simulator.run_st(state.input(), state.circuit())
    qubit = outcome.encode(qmap, state.circuit())
    
    print("Before:")
    qubit.prnt_state(column=1)
    
    if rotation == 'x':
        state.beamsplitter(0, 1, 270.0, 0)  
    elif rotation == 'y':
        state.beamsplitter(0, 1, 90.0, 90.0)  
    elif rotation == 'z':
        state.phase_shifter(0, 180.0)  
    else:
        print("Incorrect usage: Choose 'x', 'y' or 'z'")
        sys.exit(1)
    state.detector(0)
    state.detector(1)
        
    # state.show(depth=7, sizexy=70)
    qmap = [[0], [1]]
    outcome = simulator.run_st(state.input(), state.circuit())
    qubit = outcome.encode(qmap, state.circuit())
    
    print("After:")
    qubit.prnt_state(column=1)
def rotationTransformation(state, theta, rotation):
    simulator = soqcs.simulator()
    state.separator()

    qmap = [[0], [1]]
    outcome = simulator.run_st(state.input(), state.circuit())
    qubit = outcome.encode(qmap, state.circuit())
    
    print("Before:")
    qubit.prnt_state(column=1)
    
    if rotation == 'x':
        state.beamsplitter(0, 1, theta / 2, 90.0)  
    elif rotation == 'y':
        state.beamsplitter(0, 1, theta / 2, 0)  
    elif rotation == 'z':
        # apply <0, 1> | <1, 0> matrix
        # apply 
        state.phase_shifter(0, theta / 2)  
        state.phase_shifter(1, -theta / 2)
    else:
        print("Incorrect usage: Choose 'x', 'y' or 'z'")
        sys.exit(1)
    state.detector(0)
    state.detector(1)
    # state.show(depth=7, sizexy=70)
    qmap = [[0], [1]]
    outcome = simulator.run_st(state.input(), state.circuit())
    qubit = outcome.encode(qmap, state.circuit())
    
    print("After:")
    qubit.prnt_state(column=1)


def entanglementGenerator():
    simulator = soqcs.simulator()
    
    test = soqcs.qodev(6,6)
    test.add_photons(1, 0) 
    test.add_photons(0, 1) 
    test.add_photons(1, 2) 
    test.add_photons(0, 3) 
    test.add_photons(1, 4) 
    test.add_photons(1, 5) 
    
    test.separator()
    
    test.beamsplitter(0, 1, 45.0, 0)
    test.beamsplitter(2, 3, 45.0, 0)
    test.beamsplitter(4, 5, 45.0, 0)
    
    test.separator()
    
    test.beamsplitter(0, 5, acos(sqrt(2)/sqrt(3)) * (180 / pi), 0)
    test.beamsplitter(2, 4, acos(sqrt(2)/sqrt(3)) * (180 / pi), 0)
    
    test.separator()
    
    test.phase_shifter(4, 180.0)
    
    test.separator()
    
    test.detector(0)
    test.detector(2)
    
    test.show(sizexy=50,depth=16)
    
    qmap = [[0], [1]]
    outcome = simulator.run_st(test.input(), test.circuit())
    qubit = outcome.encode(qmap, test.circuit())
    qubit.prnt_state(column=1)
 
def main():
    
    test = soqcs.qodev(2,2)
    
    # |01>
    test.add_photons(0, 0) 
    test.add_photons(1, 1) 
    
    angle = 45
    rotationType = 'z'
    
    rotationTransformation(test, angle, rotationType)
    qisKitRotationTest(angle, rotationType, 0)
    
    #rY(test, 270)
    #rX(test, 180)
    #rX(test, 180)
    #pauliX(test)
    #qisKitTest()

 
    

if __name__=="__main__":
    main()
   