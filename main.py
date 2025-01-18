#!/usr/bin/python3

import soqcs

simulator = soqcs.simulator()
# Maximum number of photons = 2 (parameter 1)
# Creates two channels (parameter 2)
test = soqcs.qodev(2,2)
test.add_photons(0, 0) # adds a 0 state to channel 0
test.add_photons(1, 1) # adds a 1 state to channel 1
# Beam splitter applied to channels 0 and 1
# 45.0 is the 
# 50:50 beam splitter ?
test.beamsplitter(0, 1, 45.0, 90.0)

test.detector(0)
test.detector(1)

qmap = [[0], [1]]
outcome = simulator.run_st(test.input(), test.circuit())
qubit = outcome.encode(qmap, test.circuit())
qubit.prnt_state(column=1)