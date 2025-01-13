#!/usr/bin/python3

import soqcs

N      =  10000  # Number of outputs to calculate the density matrix
prntn  =   1000  # Print a message each 1000

# Initialize variables
V=0.0;
sim = soqcs.simulator()
apd = soqcs.dmatrix()

# Main loop
print("Start run of: ",N)
for i in range(0,N,1):
    if(i%prntn==0):
        print("Running:", i)

    example = soqcs.qodev(nph  = 4,  # Number of photons
                          nch  = 3,  # Number of channels
                          nm   = 2,  # number of polarization modes
                          ns   = 4,  # Number of packets
                          clock= 1,  # Detectors have a clock
                          ckind='E') # Exponential wavepackets
    # First QD cascade
    example.add_QD(0, 1,
                   t1 =  0.0,  # Time of bi-exciton XX photon
                   f1 =  1.0,  # Frequency of bi-exciton XX photons
                   w1 =  1.0,  # Characteristic decay time of bi-exciton XX photon
                   t2 =46.71,  # Time of exciton X photon
                   f2 =  1.0,  # Frequency of bi-exciton X photons
                   w2 =  1.0,  # Characteristic decay time of bi-exciton X photon
                   S  =  1.0,  # Fine Structure Splitting
                   k  =  0.8,  # Ratio of photons that are not due to noise
                   tss=  1.0,  # Characteristic coherence time.
                   thv=  1.0)  # Characteristic cross-dephasing time.
    example.add_QD(0, 2,
                   t1 = 16.0,  # Time of bi-exciton XX photon
                   f1 =  1.0,  # Frequency of bi-exciton XX photons
                   w1 =  1.0,  # Characteristic decay time of bi-exciton XX photon
                   t2 = 46.5,  # Time of exciton X photon
                   f2 =  1.0,  # Frequency of bi-exciton X photons
                   w2 =  1.0,  # Characteristic decay time of bi-exciton X photon
                   S  =  1.0,  # Fine Structure Splitting
                   k  =  0.8,  # Ratio of photons that are not due to noise
                   tss=  1.0,  # Characteristic coherence time.
                   thv=  1.0)  # Characteristic cross-dephasing time.
    # Circuit
    example.beamsplitter(1,2,45.0,0.0);
    # Detectors
    example.detector(0)
    example.detector(1,1)
    example.detector(2,1)

    # Run simulation
    inputst=example.input()               # Obtain input stste
    circuit=example.circuit()             # Obtain circuit
    outputst=sim.run_st(inputst,circuit)  # Run the simulation

    # Add state to the density matrix
    apd.add_state(outputst,example)

    # Calculate average photon overlapping
    V=V+example.emitted_vis(1,3)
    
    
print("V: ",V/N,"\n")

apd.normalize();                    # Normalize
partial=apd.calc_measure(example);  # Calculate post-selection
partial.prnt_mtx(3,0.01,example);   # Print the matrix