import soqcs, sys
from math import sqrt, acos, pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


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

    qmap = [
    [1, 4], 
    [3, 5],  
    ]

    qubit = outcome.encode(qmap, entangle_v1.circuit())

    # Final simulation
    outcome = simulator.run(entangle_v1)
    qubit.prnt_state(column=1)
def main():
    entanglementGenV1()
    #entanglementGenV2()
 

if __name__=="__main__":
    main()
   