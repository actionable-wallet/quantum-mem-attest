#!/usr/bin/python3

import soqcs

# maybe consider using add_Bell function
sim = soqcs.simulator()
# initialising a quantum optical device
# max number of photons = 4
# number of channels = 3
# number of modes = 2
# number of periods = 3
# number of packets = 3
# length of periods = 100
# clock - period
# ckind: exponential
test = soqcs.qodev(4,3)

# adding photons via quantum dot
test.add_QD(2, 1)
test.add_QD(2, 0)
# makes plot clearer
test.separator()
# adds beam splitter to channel 0 and 1
test.beamsplitter(0,1,45.0,0.0)
# polarisation filter added to channel ch
test.pol_filter(0,1)
test.rotator(0,45.0,0.0)
test.delay(1)
test.beamsplitter(0,1,45.0,0.0)

test.separator()

# measure state in each channel
test.detector(0,1,0,mpi=1,mpo=1)
test.detector(1,1,1,mpi=1,mpo=1)
test.detector(2, mpi=0,mpo=0)
test.show(sizexy=80,depth=13)

    
    
