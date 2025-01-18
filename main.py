#!/usr/bin/python3

import soqcs

test = soqcs.qodev(2,2)

test.empty_channel(0)
test.add_photons(2,1)
test.separator()
test.beamsplitter(0,1,45.0,0.0)
test.separator()
test.detector(0)
test.detector(1)

test.show(depth=7,sizexy=70)

simulator=soqcs.simulator()
outcome=simulator.run(test)

outcome.prnt_bins()