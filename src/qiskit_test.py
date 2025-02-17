from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, array_to_latex
from qiskit.result import marginal_distribution
from qiskit.circuit.library import UGate
from numpy import pi, random
def qisKitExampleTele():
    qubit = QuantumRegister(1, "Q")
    ebit0 = QuantumRegister(1, "A")
    ebit1 = QuantumRegister(1, "B")
    a = ClassicalRegister(1, "a")
    b = ClassicalRegister(1, "b")
    

    protocol = QuantumCircuit(qubit, ebit0, ebit1, a, b)
    protocol.h(qubit)
    random_gate = UGate(
    theta=random.random() * 2 * pi,
    phi=random.random() * 2 * pi,
    lam=random.random() * 2 * pi)
    protocol.append(random_gate, qubit)

    # Prepare ebit used for teleportation
    protocol.h(ebit0)
    protocol.cx(ebit0, ebit1)
    protocol.barrier()

    # Alice's operations
    protocol.cx(qubit, ebit0)
    protocol.h(qubit)
    protocol.barrier()

    # Alice measures and sends classical bits to Bob
    protocol.measure(ebit0, a)
    protocol.measure(qubit, b)
    protocol.barrier()

    # Bob uses the classical bits to conditionally apply gates
    with protocol.if_test((a, 1)):
        protocol.x(ebit1)
    with protocol.if_test((b, 1)):
        protocol.z(ebit1)
        
    protocol.append(random_gate.inverse(), ebit1)
    result = ClassicalRegister(1, "Result")
    protocol.add_register(result)
    protocol.measure(ebit1, result)
    
    result = AerSimulator().run(protocol).result()
    statistics = result.get_counts()
    filtered_statistics = marginal_distribution(statistics, [2])
    print(filtered_statistics)

qisKitExampleTele()

def qisKitTeleportation():
    q = QuantumRegister(3)
    c = ClassicalRegister(3)
    qc = QuantumCircuit(q, c)
    # This is the state Alice wants to send
    # CNOT Gate with control at 0 and target at 1
    qc.h(q[0])
    psi = Statevector(qc)
    print("(Teleported State)")
    finalState = psi.to_dict()
    
    for k, v in finalState.items():
        print(f"{k} : {v}")  
    
    # Generate a bell state
    qc.h(q[1])
    qc.cx(q[1], q[2])
    
    qc.cx(q[0], q[1])
    qc.h(q[0])
    
    qc.measure_all()
    # qc.remove_final_measurements()  
    psi = Statevector(qc)
    print("Teleporation Test")
    finalState = psi.to_dict()
    
    for k, v in finalState.items():
        print(f"{k} : {v}")  
    

# qisKitTeleportation()

def qisKitDenseCoding(data):
    qc = QuantumCircuit(2)
    
    # entangling a qubit
    qc.h(0)
    # CNOT Gate with control at 0 and target at 1
    qc.cx(0, 1)
    
    # if we want to send 01, rotate by z
    if data == '01':
        qc.z(0)
    elif data == '10':
        qc.x(0)
    elif data == '11':
        qc.x(0)
        qc.z(0)    
    else:
        print("identity gate")
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
