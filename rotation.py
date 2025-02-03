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
    initState = psi.to_dict()
    print(initState)

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
    finalState = psi.to_dict()
    
    for k, v in finalState.items():
        print(f"{k} : {v}")  

'''
Representing a 50:50 beam splitter
'''
def hadamardGate(ch1, ch2, state):
    return state.beamsplitter(ch1, ch2, 45.0, 0)


def rotationTransformation(state, theta, rotation):
    simulator = soqcs.simulator()
    state.separator()

    qmap = [[0], [1]]
    outcome = simulator.run_st(state.input(), state.circuit())
    qubit = outcome.encode(qmap, state.circuit())
    
    print("Before:")
    qubit.prnt_state(column=1)
    
    # refer to NOTE.md
    if rotation == 'x':
        state.beamsplitter(0, 1, theta / 2, 90.0)  
    # Had to modify to -theta / 2
    elif rotation == 'y':
        state.beamsplitter(0, 1, -theta / 2, 0)  
    elif rotation == 'z':
        state.phase_shifter(0, theta / 2)  
        state.phase_shifter(1, -theta / 2)
    else:
        print("Incorrect usage: Choose 'x', 'y' or 'z'")
        sys.exit(1)
    state.detector(0)
    state.detector(1)
    qmap = [[0], [1]]
    outcome = simulator.run_st(state.input(), state.circuit())
    qubit = outcome.encode(qmap, state.circuit())
    
    qubit.prnt_state(column=1)
def main():
    
    test = soqcs.qodev(2,2)
    
    # |01> is encoding the logical 0 qubit
    test.add_photons(0, 0) 
    test.add_photons(1, 1) 
    
    angle = 90
    rotationType = 'x'
    
    rotationTransformation(test, angle, rotationType)
    qisKitRotationTest(angle, rotationType, 0)
  