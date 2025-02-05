import soqcs, sys
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

'''
https://homes.psd.uchicago.edu/~sethi/Teaching/P243-W2021/Final%20Papers/LOQC-Dardia.pdf
'''
def qisKitPauliTest(rotation):
    qc = QuantumCircuit(1)
    
    qc.h(0)
    # # qc.measure_all()
    # # qc.remove_final_measurements()  
    # # psi = Statevector(qc)
    # # print("Before:")
    # # initState = psi.to_dict() 
    # for k, v in initState.items():
    #     print(f"{k} : {v}")  
    
    if rotation == 'x':
        qc.x(0)
    elif rotation == 'y':
        qc.y(0)
    elif rotation == 'z':
        qc.z(0)
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

def pauliGate(rotation):
    gate = soqcs.qodev(2,2)
    
    # <0, 1> | <1, 0>
    if rotation == 'x':
        gate.beamsplitter(0, 1, -90.0, 0)  
        return gate
    # <0, i> | <-i, 0>
    elif rotation == 'y':
        gate.beamsplitter(0, 1, -90.0, 90.0)  
        return gate
    # <1, 0> | <0, -1>
    # Recall phase-shifter multiplies state by an e^i(phi)
    elif rotation == 'z':
        gate.phase_shifter(0, 180.0)  
        return gate
    else:
        print("Incorrect usage: Choose 'x', 'y' or 'z'")
        sys.exit(1)
    

 
    