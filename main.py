

from stat import SF_IMMUTABLE
import soqcs, sys
from math import sqrt, acos, pi
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
def cNot():
    sim=soqcs.simulator()

    cnot = soqcs.qodev(2,6);
    cnot.add_photons(0, 0)
    cnot.add_photons(0, 1)
    cnot.add_photons(1, 2)
    cnot.add_photons(0, 3)
    cnot.add_photons(1, 4)
    cnot.add_photons(0, 5)
    cnot.separator()
    cnot.beamsplitter(3,4, -45.0,0.0)
    cnot.separator()
    cnot.beamsplitter(0,1,180*acos(1.0/sqrt(3.0))/pi,0.0)
    cnot.beamsplitter(2,3,180*acos(1.0/sqrt(3.0))/pi,0.0)
    cnot.beamsplitter(4,5,180*acos(1.0/sqrt(3.0))/pi,0.0)
    cnot.separator()
    cnot.beamsplitter(3,4, -45.0,0.0)
    cnot.separator()
    cnot.phase_shifter(1, 180)
    cnot.phase_shifter(3, 180)
    cnot.separator()
    cnot.detector(0,0)
    cnot.detector(1)
    cnot.detector(2)
    cnot.detector(3)
    cnot.detector(4)
    cnot.detector(5,0)
    # cnot.show(sizexy=80,depth=13)
    
    qmap=[[1, 3],
         [2, 4]]
    
   
    cnot.show(depth=20,slin=1)                       
    outcome=sim.run(cnot)                 
    encoded=outcome.translate(qmap, cnot)  
    encoded.show(sizex=5,dpi=70)             
    
    outcome = sim.run_st(cnot.input(), cnot.circuit())
    qubit = outcome.encode(qmap, cnot.circuit())
    
    qubit.prnt_state(column=1)
    
'''
Using: https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.3.043031.

An entanglement generator replicating Figure 1b, with a 1/9 probability of generating an entangled state.
'''
def entanglementGenV2():
     
    simulator = soqcs.simulator()

    qmap=[[1, 2],
          [3, 4]]
    
    entangle_v2 = soqcs.qodev(4,5)
    entangle_v2.add_photons(1, 0)
    entangle_v2.add_photons(1, 1)
    entangle_v2.add_photons(1, 2)
    entangle_v2.add_photons(0, 3)
    entangle_v2.add_photons(1, 4)
    
    entangle_v2.separator()
    
    entangle_v2.beamsplitter(0, 1, 45.0, 0)
    entangle_v2.phase_shifter(0, 90.0)
    entangle_v2.beamsplitter(0, 2, 180*acos(sqrt(2.0)/sqrt(3.0))/pi, 0)
    entangle_v2.beamsplitter(1, 2, 45.0, 0)
    entangle_v2.beamsplitter(3, 4, 180*acos(1.0/sqrt(3.0))/pi, 0)
    entangle_v2.beamsplitter(0, 4, 45.0, 0)
    
    entangle_v2.separator()
  
    entangle_v2.detector(0)
  
    outcome=simulator.run(entangle_v2)                 
    encoded=outcome.translate(qmap, entangle_v2)  
    encoded.show(sizex=5,dpi=70)             
    
    outcome = simulator.run_st(entangle_v2.input(), entangle_v2.circuit())
    entangle_v2.input().prnt_state(column=1)
    outcome.prnt_state(column=1)
    qubit = outcome.encode(qmap, entangle_v2.circuit())
    
    outcome=simulator.run(entangle_v2)

    qubit.prnt_state(column=1)
    
'''
Using: https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.3.043031.

An entanglement generator replicating Figure 1a, with a 2/27 probability of generating an entangled state.
'''
def entanglementGenV1():
    
    simulator = soqcs.simulator()

    qmap=[[1, 4],
          [3, 5], 
          [0, 2]]
    
    entangle_v1 = soqcs.qodev(4,6)
    entangle_v1.add_photons(1, 0)
    entangle_v1.add_photons(0, 1)
    entangle_v1.add_photons(1, 2)
    entangle_v1.add_photons(0, 3)
    entangle_v1.add_photons(1, 4)
    entangle_v1.add_photons(1, 5)
    
    entangle_v1.separator()
    
    entangle_v1.beamsplitter(0, 1, 45.0, 0)
    entangle_v1.beamsplitter(2, 3, 45.0, 0)
    entangle_v1.beamsplitter(4, 5, 45.0, 0)
    
    entangle_v1.separator()
    entangle_v1.beamsplitter(0, 5, 180*acos(sqrt(2.0)/sqrt(3.0))/pi, 0)
    entangle_v1.beamsplitter(2, 4, 180*acos(sqrt(2.0)/sqrt(3.0))/pi, 0)
    
    entangle_v1.separator()
    
    entangle_v1.phase_shifter(4, 180.0)
    
    entangle_v1.separator()
    entangle_v1.detector(0)
    entangle_v1.detector(2)
    
    outcome=simulator.run(entangle_v1)                 
    encoded=outcome.translate(qmap, entangle_v1)  
    encoded.show(sizex=5,dpi=70)             
    
    outcome = simulator.run_st(entangle_v1.input(), entangle_v1.circuit())
    entangle_v1.input().prnt_state(column=1)
    outcome.prnt_state(column=1)
    qubit = outcome.encode(qmap, entangle_v1.circuit())
    
    outcome=simulator.run(entangle_v1)

    qubit.prnt_state(column=1)
def main():
    
    test = soqcs.qodev(2,2)
    
    # |01> is encoding the logical 0 qubit
    test.add_photons(0, 0) 
    test.add_photons(1, 1) 
    
    angle = 90
    rotationType = 'x'
    
    # rotationTransformation(test, angle, rotationType)
    # qisKitRotationTest(angle, rotationType, 0)
    #cNot()
    #entanglementGenV1()
    entanglementGenV2()
    
    #pauliGate(test, rotationType)
    #qisKitPauliTest(rotationType, 0)
 
    

if __name__=="__main__":
    main()
   