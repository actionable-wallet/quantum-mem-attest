import random
import soqcs, sys
import subprocess
from pauli import pauliGate
from random import randrange
from math import sqrt, acos, pi

SEPERATOR = "==============================================================================="

randomTheta = 0

'''
NOTE: Alice is the sender, Bob is the receiver of the teleported qubit.
alice() represents all of Alice's actions during the teleportation process. To be more specific,
the function stops at the point where Alice measures her two qubits, namely the TELEPORTED qubit and her HALF of the ENTANGLED qubit.
It is at this point whereby she sends two classical bits of information to notify Bob of what transformation he needs to induce on his
half of the ENTANGLED qubit.
'''
def alice():
    sim=soqcs.simulator(mem=20000)
   
    # Note changing from (9, 11) did not change anything
    teleportation = soqcs.qodev(5, 7)
    
    # Generate the |0> state
    teleportation.add_photons(0, 0)
    teleportation.add_photons(1, 1)
    
    # Apply a random unitary operation on |0> state, this will be our teleported state
    teleportation.add_gate([0, 1], getRandomUnitaryGate(inverse=False), "U")
    # print(SEPERATOR)
    print("(Teleported state)")
    qmap =[[0], [1]]
    printState(teleportation, qmap)
    # Ancillary mode
    teleportation.add_photons(1, 2)
    
    # Channels which will encode our entanglement circuit
    teleportation.add_photons(1, 3)
    teleportation.add_photons(1, 4)
    teleportation.add_photons(0, 5)
    teleportation.add_photons(1, 6)
    
    entangledState = getEntanglementGenerator()
    
    chlist = [2, 3, 4, 5, 6]
    teleportation.add_gate(chlist, entangledState, "Entangle")
    teleportation.detector(2)
    
    bellMeasurement = getMeasureGate()
   
    
    chlist = [0, 1, 3, 5]
    teleportation.add_gate(chlist, bellMeasurement, "measure") 
    
    #teleportation.add_gate([4, 6], getRandomUnitaryGate(inverse=True), 'Ψ')
    #teleportation.add_gate([4, 6], pauliGate('z'), 'Z')
    teleportation.detector(0)
    teleportation.detector(1)
    teleportation.detector(3)
    teleportation.detector(5)
    outcome = sim.run_st(teleportation.input(), teleportation.circuit())
    outcome.prnt_state(column=1)

def printState(dev, qmap):
    print(SEPERATOR)
    simulator = soqcs.simulator()
    outcome = simulator.run_st(dev.input(), dev.circuit())
    outcome=dev.apply_condition(outcome)
    outcome.normalize()
    state = outcome.encode(qmap, dev.circuit())
    state.prnt_state(column=1)

def getRandomUnitaryGate(inverse):
    state = soqcs.qodev(1, 2)
    # Keep real and ensure we assign it once only
    global randomTheta
    if not inverse:
        randomTheta = randrange(0, 90)
        state.beamsplitter(0, 1, randomTheta, 0.0)
    else:
        state.beamsplitter(0, 1, -randomTheta, 0.0)
    return state


def controlZ():
    # Create circuit
    csign = soqcs.qodev(4, 8)
    #Initialize qubit channels

    csign.separator()
    csign.beamsplitter(0,2,45.0,0.0)
    csign.NSX(0, 4, 5)
    csign.NSX(2, 6, 7)
    csign.beamsplitter(0,2,-45.0,0.0)
    
    csign.separator()
    # csign.detector(0)
    # csign.detector(1)
    # csign.detector(2)
    # csign.detector(3)
    csign.detector(4,1)
    csign.detector(5,0)
    csign.detector(6,1)
    csign.detector(7,0)
   
    return csign

    # Print the result
  
def getMeasureGateV2():
    bellMeasurement = soqcs.qodev(4,6)
    
    bellMeasurement.beamsplitter(0, 1, 45.0, 0)
    bellMeasurement.beamsplitter(1, 2, 45,0, 0)
    bellMeasurement.beamsplitter(0, 3, 45.0, 0)
    bellMeasurement.beamsplitter(2, 5, 45.0, 0)
    bellMeasurement.beamsplitter(3, 4, 45.0, 0)
  
    
    return bellMeasurement 
'''
Function which returns a quantum device which conducts a bell measurement
'''
def getMeasureGate():
    bellMeasurement = soqcs.qodev(4,4)
    #bellMeasurement.rewire(1, 2)
    bellMeasurement.beamsplitter(1, 2, 180*acos(1.0/sqrt(2.0))/pi, 0)
    bellMeasurement.beamsplitter(0, 3, 180*acos(1.0/sqrt(2.0))/pi, 0)
  
    
    return bellMeasurement   
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
    
    # entangle_v2.detector(0)
    
    return entangle_v2
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
    alice()

if __name__=="__main__":
    main()
   