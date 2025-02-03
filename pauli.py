import soqcs, sys
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

'''
https://homes.psd.uchicago.edu/~sethi/Teaching/P243-W2021/Final%20Papers/LOQC-Dardia.pdf
'''
def qisKitPauliTest(rotation, state):
    qc = QuantumCircuit(1)
    qc.measure_all()
    qc.remove_final_measurements()  
    psi = Statevector(qc)
    print("Before:")
    initState = psi.to_dict() 
    for k, v in initState.items():
        print(f"{k} : {v}")  
    
    if rotation == 'x':
        qc.x(state)
    elif rotation == 'y':
        qc.y(state)
    elif rotation == 'z':
        qc.z(state)
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

def pauliGate(state, rotation):
    simulator = soqcs.simulator()
    state.separator()

    qmap = [[0], [1]]
    outcome = simulator.run_st(state.input(), state.circuit())
    qubit = outcome.encode(qmap, state.circuit())
    
    print("Before:")
    qubit.prnt_state(column=1)
    
    # <0, 1> | <1, 0>
    if rotation == 'x':
        state.beamsplitter(0, 1, 270.0, 0)  
    # <0, i> | <-i, 0>
    elif rotation == 'y':
        state.beamsplitter(0, 1, -90.0, 90.0)  
    # <1, 0> | <0, -1>
    # Recall phase-shifter multiplies state by an e^i(phi)
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
def main():
    
    test = soqcs.qodev(2,2)
    # |01> is encoding the logical 0 qubit
    test.add_photons(0, 0) 
    test.add_photons(1, 1) 
    
    rotationType = 'x'
    
  
   
    
    pauliGate(test, rotationType)
    qisKitPauliTest(rotationType, 0)
 
    