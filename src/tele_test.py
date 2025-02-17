from main import getMeasureGate, getEntanglementGenerator, getRandomUnitaryGate
import soqcs

def entanglementTests():
    
    sim = soqcs.simulator()
    test = soqcs.qodev(4, 5)
    test.add_photons(1, 0)
    
    test.add_photons(1, 1)
    test.add_photons(1, 2)
    test.add_photons(0, 3)
    test.add_photons(1, 4)
    
    chlist = [0, 1, 2, 3, 4]
    test.add_gate(chlist, getEntanglementGenerator(), 'ENTANGLE')
    
    qmap = [[1, 2],[3, 4]]
    outcome = sim.run_st(test.input(), test.circuit())
    measurement = outcome.encode(qmap, test.circuit())
    measurement.prnt_state(column=1)
    
def randomUnitaryMatrixTest():
    state = soqcs.qodev(1, 2)
    simulator = soqcs.simulator()
    state.add_photons(0, 0)
    state.add_photons(1, 1)
    
    print("Before:")
    qmap =[[0], [1]]
    outcome = simulator.run_st(state.input(), state.circuit())
    outcome = outcome.encode(qmap, state.circuit())
    outcome.prnt_state(column=1)
    
    state.add_gate([0, 1], getRandomUnitaryGate(inverse=False), 'U')
    
    print("During:")
   
    outcome = simulator.run_st(state.input(), state.circuit())
    outcome = outcome.encode(qmap, state.circuit())
    outcome.prnt_state(column=1)
    
    state.add_gate([0, 1], getRandomUnitaryGate(inverse=True), 'U')
    
    print("After:")
    outcome = simulator.run_st(state.input(), state.circuit())
    outcome = outcome.encode(qmap, state.circuit())
    outcome.prnt_state(column=1)
    


def measureGateTests(case):
    sim=soqcs.simulator()
    qmap=[[0, 2],
         [1, 3]]
    
    test = soqcs.qodev(4,4)
    if case == 0:
        test.add_photons(0, 0)
        test.add_photons(1, 1)
        test.add_photons(0, 2)
        test.add_photons(1, 3)
    elif case == 1:
        test.add_photons(1, 0)
        test.add_photons(1, 1)
        test.add_photons(0, 2)
        test.add_photons(0, 3)
    elif case == 2:
        test.add_photons(2, 0)
        test.add_photons(0, 1)
        test.add_photons(0, 2)
        test.add_photons(0, 3)
    elif case == 3:
        test.add_photons(0, 0)
        test.add_photons(2, 1)
        test.add_photons(0, 2)
        test.add_photons(0, 3)
    test.separator()
    
    chlist = [0, 1, 2, 3]
    measurement = getMeasureGate()
    test.add_gate(chlist, measurement, "M")
    
    outcome = sim.run_st(test.input(), test.circuit())
    measurement = outcome.encode(qmap, test.circuit())
    measurement.prnt_state(column=1)

# randomUnitaryMatrixTest()