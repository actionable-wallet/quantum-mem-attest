from math import pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
 
from qiskit.quantum_info import Statevector
 
def qisKitTeleportation():
    q = QuantumRegister(3)
    c = ClassicalRegister(3)
    qc = QuantumCircuit(q, c)
    # This is the state Alice wants to send
    qc.h(q[0])
    # CNOT Gate with control at 0 and target at 1
    
    # Generate a bell state
    qc.h(q[1])
    qc.cx(q[1], q[2])
    
    qc.measure_all()
    qc.remove_final_measurements()  
    psi = Statevector(qc)
    print("Teleporation Test")
    finalState = psi.to_dict()
    
    for k, v in finalState.items():
        print(f"{k} : {v}")  
    
def qisKitDenseCoding(data):
    qc = QuantumCircuit(2)
    qc.h(0)
    # CNOT Gate with control at 0 and target at 1
    qc.cx(0, 1)
    
    if data == '01':
        qc.z(0)
    elif data == '10':
        qc.x(0)
    elif data == '11':
        qc.x(0)
        qc.z(0)    
    qc.cx(0, 1)
    qc.h(0)
    qc.measure_all()
    qc.remove_final_measurements()  
    psi = Statevector(qc)
    print(f"Super-dense coding of {data}")
    finalState = psi.to_dict()
    
    for k, v in finalState.items():
        print(f"{k} : {v}")  
'''
Using qisKit to generate one of the Bell States namely 1/sqrt(2) (|00> + |11>)
'''
def qisKitEntanglement():
    qc = QuantumCircuit(2)
    qc.h(0)
    # CNOT Gate with control at 0 and target at 1
    qc.cx(0, 1)
    qc.measure_all()
    qc.remove_final_measurements()  
    psi = Statevector(qc)
    print("Generating the phi^+ state")
    finalState = psi.to_dict()
    
    for k, v in finalState.items():
        print(f"{k} : {v}")  
