import soqcs, sys
from pauli import pauliGate
from random import randrange
from math import sqrt, acos, pi

SEPERATOR = "==============================================================================="

randomTheta = 0


def getRandomUnitaryGate(inverse):
    state = soqcs.qodev(1, 2)
    # simulator = soqcs.simulator()
    # state.add_photons(0, 0)
    # state.add_photons(1, 1)
    
    # Keep real and ensure we assign it once only
    global randomTheta
    if not inverse:
        randomTheta = randrange(0, 90)
        # temp val 
        randomTheta = -45
        state.beamsplitter(0, 1, randomTheta, 0.0)
    else:
        state.beamsplitter(0, 1, -randomTheta, 0.0)
    # qmap = [[0], [1]]
    # outcome = simulator.run_st(state.input(), state.circuit())
    # bobQubit = outcome.encode(qmap, state.circuit())
    # bobQubit.prnt_state(column=1)
    return state

def teleport():
    simulator=soqcs.simulator(mem=20000)
   
    teleportation = soqcs.qodev(9, 11)
    
    print(SEPERATOR)
    print("s_0")
    teleportation.add_photons(0, 0)
    teleportation.add_photons(1, 1)
    qmap=[[0], [1]]
    
    outcome = simulator.run_st(teleportation.input(), teleportation.circuit())
    outcome=teleportation.apply_condition(outcome)
    state = outcome.encode(qmap, teleportation.circuit())
    state.prnt_state(column=1)
    
    teleportation.add_gate([0, 1], getRandomUnitaryGate(inverse=False), 'Ψ')
    print(SEPERATOR)
    print("s_1 (Teleported state)")
    qmap =[[0], [1]]
    outcome = simulator.run_st(teleportation.input(), teleportation.circuit())
    outcome=teleportation.apply_condition(outcome)
    outcome = outcome.encode(qmap, teleportation.circuit())
    outcome.prnt_state(column=1)
    
    # Creating entangled qubit
    teleportation.add_photons(1, 2)
    
    teleportation.add_photons(1, 3)
    teleportation.add_photons(1, 4)
    teleportation.add_photons(0, 5)
    teleportation.add_photons(1, 6)
    
    teleportation.add_photons(1,7)
    teleportation.add_photons(0,8)
    teleportation.add_photons(1,9)
    teleportation.add_photons(0,10)
    
    # Alice and Bob share this state
    # 1/3 * 1/sqrt(2) (|00> + |11>)
    entangledState = getEntanglementGenerator()
    
    chlist = [2, 3, 4, 5, 6]
    teleportation.add_gate(chlist, entangledState, "Entangle")
   
    teleportation.detector(2)
  
    bellMeasurement = getMeasureGate()
    qmap=[[0, 3, 4], [1, 5, 6]]
    print("NEED WORK HERE!")
    print(SEPERATOR)
    print("s_2 (Before measuring Alice's two qubits)")
    outcome = simulator.run_st(teleportation.input(), teleportation.circuit())
    outcome = outcome.encode(qmap, teleportation.circuit())
    outcome.prnt_state(column=1)
    chlist = [0, 1, 3, 5]
    teleportation.add_gate(chlist, bellMeasurement, "measure") 

    # teleportation.detector(0)
    # teleportation.detector(1)
    # teleportation.detector(3)
    # teleportation.detector(5)
    
    qmap=[[0, 3, 4], [1, 5, 6]]
    print(SEPERATOR)
    print("Bob received measured into this state:")
    
    teleportation.add_gate([0, 1, 4, 6, 7, 8, 9, 10], controlZ(), 'CZ')
    teleportation.add_gate([4, 6], getRandomUnitaryGate(inverse=True), 'Ψ')
    outcome = simulator.run_st(teleportation.input(), teleportation.circuit())
    outcome=teleportation.apply_condition(outcome)
    
    qmap=[[0, 3, 4], [1, 5, 6]]
    outcome = outcome.encode(qmap, teleportation.circuit())
    outcome.normalize()
    outcome.prnt_state(column=1)
   
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
  

'''
Function which returns a quantum device which conducts a bell measurement
'''
def getMeasureGate():
    bellMeasurement = soqcs.qodev(4,4)
    
    bellMeasurement.beamsplitter(0, 3, 45.0, 0)
    bellMeasurement.beamsplitter(1, 2, 45.0, 0)
  
    bellMeasurement.detector(0)
    bellMeasurement.detector(1)
    bellMeasurement.detector(2)
    bellMeasurement.detector(3)
    
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
    teleport()

if __name__=="__main__":
    main()
   