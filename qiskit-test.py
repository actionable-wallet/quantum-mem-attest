from math import pi
from qiskit import QuantumCircuit
 
from qiskit.quantum_info import Statevector
 
def hadamardTest():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.crx(pi / 2, 0, 1)

    print(qc)
    psi = Statevector(qc)
    print(psi)

def bellState():
 
    qc = QuantumCircuit(1)
    qc.x(0)
    qc.measure_all()
    qc.remove_final_measurements()  # no measurements allowed
    statevector = Statevector(qc)
    print(statevector.to_dict())
    
bellState()

