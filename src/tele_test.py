from main import getMeasureGate, getEntanglementGenerator, getMeasureGateV2, getRandomUnitaryGate
from pauli import pauliGate
import soqcs

# def entanglementTests():
    
#     sim = soqcs.simulator()
#     test = soqcs.qodev(4, 5)
#     test.add_photons(1, 0)
    
#     test.add_photons(1, 1)
#     test.add_photons(1, 2)
#     test.add_photons(0, 3)
#     test.add_photons(1, 4)
    
#     chlist = [0, 1, 2, 3, 4]
#     test.add_gate(chlist, getEntanglementGenerator(), 'ENTANGLE')
    
#     qmap = [[1, 2],[3, 4]]
#     outcome = sim.run_st(test.input(), test.circuit())
#     measurement = outcome.encode(qmap, test.circuit())
#     measurement.prnt_state(column=1)
    
# def randomUnitaryMatrixTest():
#     state = soqcs.qodev(1, 2)
#     simulator = soqcs.simulator()
#     state.add_photons(0, 0)
#     state.add_photons(1, 1)
#     state.beamsplitter(0, 1, -45.0,0.0)
    
#     print("Before:")
#     qmap =[[0], [1]]
#     outcome = simulator.run_st(state.input(), state.circuit())
#     outcome = outcome.encode(qmap, state.circuit())
#     outcome.prnt_state(column=1)
#     state.add_gate([0, 1], pauliGate('z'), 'U')
    
#     print("During:")
   
#     outcome = simulator.run_st(state.input(), state.circuit())
#     outcome = outcome.encode(qmap, state.circuit())
#     outcome.prnt_state(column=1)
    
#     state.add_gate([0, 1], pauliGate('z'), 'U')
    
#     print("After:")
#     outcome = simulator.run_st(state.input(), state.circuit())
#     outcome = outcome.encode(qmap, state.circuit())
#     outcome.prnt_state(column=1)
    


def measureGateTests():
    sim=soqcs.simulator()
    qmap=[[0, 2],
          [1, 3]]
    
    test = soqcs.qodev(2, 4)
    
    test.add_photons(0, 0)
    test.add_photons(1, 1)
    test.add_photons(0, 2)
    test.add_photons(1, 3)
    outcome = sim.run_st(test.input(), test.circuit())
    outcome=test.apply_condition(outcome)
    outcome = outcome.encode([[0], [1]], test.circuit())
    outcome.prnt_state(column=1)
    #test.add_gate([0, 1], getRandomUnitaryGate(False), "U")
    test.add_gate([0, 1, 2, 3], getMeasureGate(), "M")
    #test.add_gate([0, 1], getRandomUnitaryGate(True), "U")
    
    test.detector(0)
    test.detector(1)
    test.detector(2)
    test.detector(3)
  
    outcome = sim.run_st(test.input(), test.circuit())
    outcome=test.apply_condition(outcome)
    #outcome = outcome.encode([[0, 2], [1, 3]], test.circuit())
    outcome.prnt_state(column=1)
measureGateTests()