import random
import soqcs, sys
import subprocess
from pauli import pauliGate
from random import randrange
from math import sqrt, acos, pi

def teleport():
    sim=soqcs.simulator(mem=20000)
   
    teleportation = soqcs.qodev(9, 11)
    
    teleportation.add_photons(0, 0)
    teleportation.add_photons(1, 1)
    #qmap=[[0], [1]]
    
    
    #teleportation.add_gate([0, 1], getRandomUnitaryGate(inverse=False), 'Ψ')
    print(SEPERATOR)
    print("s_1 (Teleported state)")
    qmap =[[0], [1]]
    printState(teleportation, qmap)
    
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
    # 1/3 * 1/sqrt(2) (|0_A 0_B> + |1_A 1_B>)
    entangledState = getEntanglementGenerator()
    
    chlist = [2, 3, 4, 5, 6]
    teleportation.add_gate(chlist, entangledState, "Entangle")
   
    teleportation.detector(2)
  
    bellMeasurement = getMeasureGate()
   
    #outcome.prnt_state(column=1)
    # PROBLEM -----------------------------------------------------------------
    chlist = [0, 1, 3, 5]
    # qmap=[[0, 3, 4], [1, 5, 6]]
    teleportation.add_gate(chlist, bellMeasurement, "measure") 
    # print("Alice measures:")
    # outcome = simulator.run_st(teleportation.input(), teleportation.circuit())
    # outcome.prnt_state(column=1)
    # # teleportation.detector(0)
    # # teleportation.detector(1)
    # # teleportation.detector(3)
    # # teleportation.detector(5)

    
    print(SEPERATOR)
    print("Bob received measured into this state:")
    #teleportation.add_gate([0, 1, 4, 6, 7, 8, 9, 10], controlZ(), 'CZ')
    #teleportation.add_gate([4, 6], getRandomUnitaryGate(inverse=True), 'Ψ')

    qmap=[[0, 3, 4], [1, 5, 6]]
    state = soqcs.state(teleportation.circuit().num_levels())
    state = state.encode(qmap, teleportation.circuit())
    prob_bins = sim.run(teleportation)
    prob_bins = prob_bins.translate(qmap, teleportation)
    prob_bins.prnt_bins()
    print("The number of levels")
    print(prob_bins.num_levels())
   