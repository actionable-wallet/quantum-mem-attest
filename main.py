from rotation import hadamardGate
import soqcs, sys
from math import sqrt, acos, pi
from pauli import pauliGate, qisKitPauliTest
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector

def getState():
    #sim = soqcs.simulator()
    state = soqcs.qodev(2,2)
    rotation = 'y'
    
    # |01> = 0
    # |10> = 1
    
    hadamardGate = getHadamardGate()
    notGate = pauliGate(rotation)
    
    chlist = [0, 1]
    state.add_gate(chlist, hadamardGate, "H")
    state.add_gate(chlist, notGate, "Y")
    # state.show()
    return state
    
    # qmap = [[0], [1]]
    # outcome = sim.run_st(state.input(), state.circuit())
    # qubit = outcome.encode(qmap, state.circuit())
    # qubit.prnt_state(column=1)
    # qisKitPauliTest(rotation)

def teleport():
  
    simulator=soqcs.simulator()
    
    teleporationCircuit = soqcs.qodev(5,9)
    #teleportedState = getState()
    
    # We want to transfer the state (1, 0)
    teleporationCircuit.add_photons(1, 0)
    teleporationCircuit.add_photons(0, 1)
    teleporationCircuit.beamsplitter(0, 1, 45.0, 0)
    #teleporationCircuit.add_gate([0, 1], getHadamardGate(), 'H')
    
    teleporationCircuit.add_photons(1, 2)
    teleporationCircuit.add_photons(1, 3)
    teleporationCircuit.add_photons(1, 4)
    teleporationCircuit.add_photons(0, 5)
    teleporationCircuit.add_photons(1, 6)
    
    # ancillas for cnot gate
    teleporationCircuit.add_photons(0, 7)
    teleporationCircuit.add_photons(0, 8)
    # Alice and Bob share this state
    entangledState = getEntanglementGenerator()
    
    chlist = [3, 4, 5, 6, 7]
    teleporationCircuit.add_gate(chlist, entangledState, "Entangle")
    # chlist = [7, 0, 1, 3, 4, 8]
    
    # cNotGate = cNot()
    # teleporationCircuit.add_gate(chlist, cNotGate, "cnot")
    bellMeasurement = getMeasureGate()
    chlist = [0, 1, 3, 4]
    teleporationCircuit.add_gate(chlist, bellMeasurement, "measure")
    # Alice has (3, 5)
    # Bob has (4, 6)
    qmap = [[0, 3, 5], [1, 4, 6]]
    # qmap=[[4, 5],
    #       [6, 7]]
    outcome = simulator.run_st(teleporationCircuit.input(), teleporationCircuit.circuit())
    teleporationCircuit.input().prnt_state(column=1)
    outcome.prnt_state(column=1)
    
    outcome = simulator.run_st(teleporationCircuit.input(), teleporationCircuit.circuit())
    aliceQubit = outcome.encode(qmap, teleporationCircuit.circuit())
    aliceQubit.prnt_state(column=1)
   
    
'''
Function which returns a 50:50 beam splitter
'''   
def getHadamardGate():
    hadamardGate = soqcs.qodev(1,2) 
    hadamardGate.beamsplitter(0,1, 45.0,0.0) 
    return hadamardGate
def cNot():

    cnot = soqcs.qodev(2,6)
    
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

    return cnot

'''
Function which returns a quantum device which conducts a bell measurement
'''
def getMeasureGate():
    
    # Consider decoding state into dual-rail encoding

    # qmap=[[1, 2],
    #      [3, 4]]
    qmap= [[0, 2],
           [1, 3]]
    
    bellMeasurement = soqcs.qodev(4,4)
    bellMeasurement.empty_channel(0)
    bellMeasurement.empty_channel(1)
    bellMeasurement.empty_channel(2)
    bellMeasurement.empty_channel(3)
    # bellMeasurement = state

    bellMeasurement.separator()
    
    bellMeasurement.beamsplitter(0, 3, 45.0, 0)
    bellMeasurement.beamsplitter(1, 2, 45.0, 0)
    
    bellMeasurement.separator()
  
    bellMeasurement.detector(0)
    bellMeasurement.detector(1)
    bellMeasurement.detector(2)
    bellMeasurement.detector(3)
    
    return bellMeasurement
    
    # bellMeasurement.show(sizexy=30,depth=30)
    # outcome=simulator.run(bellMeasurement)                 
    # encoded=outcome.translate(qmap, bellMeasurement)  
    # encoded.show(sizex=5,dpi=70)    
    
    # outcome = simulator.run_st(bellMeasurement.input(), bellMeasurement.circuit())
    # bellMeasurement.input().prnt_state(column=1)
    # outcome.prnt_state(column=1)
    # qubit = outcome.encode(qmap, bellMeasurement.circuit())
    # qubit.prnt_state(column=1)
   
'''
Using: https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.3.043031.

An entanglement generator replicating Figure 1b, with a 1/9 probability of generating an entangled state.
'''
def getEntanglementGenerator():
     
    # simulator = soqcs.simulator()

    # qmap=[[1, 2],
    #      [3, 4]]
    
    entangle_v2 = soqcs.qodev(4,5)
     
    entangle_v2.separator()
    
    entangle_v2.beamsplitter(0, 1, 45.0, 0)
    entangle_v2.phase_shifter(0, 90.0)
    entangle_v2.beamsplitter(0, 2, 180*acos(sqrt(2.0)/sqrt(3.0))/pi, 0)
    entangle_v2.beamsplitter(1, 2, 45.0, 0)
    entangle_v2.beamsplitter(3, 4, 180*acos(1.0/sqrt(3.0))/pi, 0)
    entangle_v2.beamsplitter(0, 4, 45.0, 0)
    
    entangle_v2.detector(0)
    
    return entangle_v2
  
    
    
    # outcome=simulator.run(entangle_v2)                 
    # encoded=outcome.translate(qmap, entangle_v2)  
    # encoded.show(sizex=5,dpi=70)             
    
    # outcome = simulator.run_st(entangle_v2.input(), entangle_v2.circuit())
    # entangle_v2.input().prnt_state(column=1)
    # outcome.prnt_state(column=1)
    # qubit = outcome.encode(qmap, entangle_v2.circuit())
    
    # outcome=simulator.run(entangle_v2)

    # qubit.prnt_state(column=1)
'''
Using: https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.3.043031.

An entanglement generator replicating Figure 1a, with a 2/27 probability of generating an entangled state. 
'''

# NOTE: Move channels around but have an equivalent circuit (same qubit encoding => output)
def entanglementGenV1():
    
    simulator = soqcs.simulator()

    entangle_v1 = soqcs.qodev(4, 6)

    entangle_v1.add_photons(1, 0)  
    entangle_v1.add_photons(1, 2)  
    entangle_v1.add_photons(1, 4)  
    entangle_v1.add_photons(1, 5)  

    entangle_v1.separator()


    entangle_v1.beamsplitter(0, 1, 45, 0)
    entangle_v1.beamsplitter(2, 3, 45, 0)
    entangle_v1.beamsplitter(4, 5, 45, 0)

    entangle_v1.separator()

    theta = 180 * acos(sqrt(2.0) / sqrt(3.0)) / pi
    entangle_v1.beamsplitter(2, 4, theta, 0)  
    
    # this beam splitter seems to be causing issues
    entangle_v1.beamsplitter(0, 5, theta, 0)  

    entangle_v1.separator()

    entangle_v1.phase_shifter(4, 180)

    entangle_v1.separator()

    entangle_v1.detector(0)
    entangle_v1.detector(2)

    entangle_v1.input().prnt_state(column=1)

    outcome = simulator.run_st(entangle_v1.input(), entangle_v1.circuit())
    outcome.prnt_state(column=1)

    qmap = [[1, 5], 
            [3, 4]]

    qubit = outcome.encode(qmap, entangle_v1.circuit())

    # Final simulation
    outcome = simulator.run(entangle_v1)
    qubit.prnt_state(column=1)
def main():
    # simulator=soqcs.simulator()
    
    # state = soqcs.qodev(8,8)
    # state.add_photons(1, 0)
    # state.add_photons(1, 1)
    # state.add_photons(1, 2)
    # state.add_photons(0, 3)
    # state.add_photons(1, 4)
    # state.add_photons(0, 5)
    # state.add_photons(1, 6)
    # state.add_photons(0, 7)
    # entangle = getEntanglementGenerator()
    
    # state.add_gate([0, 1, 2, 3, 4], entangle, 'entangle')
    
    # outcome = simulator.run_st(state.input(), state.circuit())
    # state.input().prnt_state(column=1)
    # outcome.prnt_state(column=1)
    
    # qmap=[[1, 2],
    #       [3, 4]]
    # qubit = outcome.encode(qmap, state.circuit())
    
    # outcome=simulator.run(state)

    # qubit.prnt_state(column=1)
    teleport()
 

if __name__=="__main__":
    main()
   