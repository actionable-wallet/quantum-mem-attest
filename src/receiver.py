import subprocess
import soqcs, re, sys
from math import sqrt


output = subprocess.run(["python3", "main.py"], capture_output=True)
parsed = output.stdout.decode('utf-8').strip().split("\x1b[36m")
AMPLITUDE_INDEX = 7

# Usually make this 6 in order to account for 1/3 * 1/2 (entanglement generator AND measurement)
NORMALISATION_FACTOR = 6 * sqrt(2)

teleportedStateChannels = [0, 1]
senderChannels = [3, 5]
receiverChannels = [4, 6]

zRotation = [[1, 0, 1, 0], [0, 1, 0, 1]]
identityRotation = [[1, 1, 0, 0], [0, 0, 1, 1]]

# Not sure why soqcs uses this convention, usually |10>> = |0> and |01>> = |1>
ZERO_DUAL_RAIL = [0, 1]
ONE_DUAL_RAIL = [1, 0]

VALID_THETA = 0

def getRandomUnitaryGate(theta):
    state = soqcs.qodev(1, 2)
    # Keep real and ensure we assign it once only
    state.beamsplitter(0, 1, -theta, 0.0)
       
    return state


def parseOutput(output):
    circuitState = []
    for item in parsed:
        output = item.replace("|", " ")
        output = output.replace(">\x1b[0m:", ",")
        output = output.strip().split(",")
        circuitState.append(output)
    return circuitState

def sender():
    return 0
    
def verify(temp):
    sim=soqcs.simulator(mem=20000)
    # Note changing from (9, 11) did not change anything
    verify = soqcs.qodev(1, 2)
    
    global VALID_THETA
    print(VALID_THETA)
    verify.beamsplitter(0, 1, VALID_THETA, 0.0)

    inputst = soqcs.state(2, 1)
    # Initialize input state
    # Adding superposition state
    term=[[0,1], [0, 1]] # Occupations at channel 0,1
    inputst.add_term(temp[2][1], term ,verify.circuit())
   
    term=[[0,1], [1, 0]] # Occupations at channels 0,1
    inputst.add_term(temp[3][1], term, verify.circuit())
 
    outputst=sim.run_st(inputst, verify.circuit())

    outputst=verify.apply_condition(outputst)
    qmap = [[0], [1]]
    outputst = outputst.encode(qmap, verify.circuit())
    outputst.prnt_state(column=1)
    

def receiver():
    output = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    circuitState = parseOutput(output)
    circuitStates = []
    measuredQubits = []
    senderQubits = []
    receiverQubits = []
    
    zIndices = []
    iIndices = []
    for i, outputStrings in enumerate(circuitState):
        if i == 1 or i == 2:
            print(outputStrings)
            match = re.search(r"= [0-9]+.*", outputStrings[1])
            global VALID_THETA
            if match:
                VALID_THETA = float(match.group().split()[1])
        if i < 2:
            continue
        measuredQubit = []
        teleportedQubit = []
        senderQubit = []
        receiverQubit = []
        circuitStates.append(outputStrings)
        for channel, photons in enumerate(outputStrings):
            # Don't want the amplitude
            if channel == AMPLITUDE_INDEX or "=" in photons:
                continue
            numPhotons = int(photons.strip())
            # Filtering out each rail into their respective qubit encodings
            if channel in teleportedStateChannels:
                teleportedQubit.append(numPhotons)
                measuredQubit.append(numPhotons)
            elif channel in senderChannels:
                senderQubit.append(numPhotons)
                measuredQubit.append(numPhotons)
            elif channel in receiverChannels:
                receiverQubit.append(numPhotons)
        measuredQubits.append(measuredQubit)
        senderQubits.append(senderQubit)
        receiverQubits.append(receiverQubit)
    
    # Filter out relevant bell measurements namely ones which satisfy valid detector patterns
    for index, qubits in enumerate(measuredQubits):
        if qubits in zRotation:
            zIndices.append(index)
        elif qubits in identityRotation:
            iIndices.append(index)
    
    # Filter out outputs whereby there was a relevant bell measurement
    # Namely we filter out the channels regarding Bob's dual rail encoded qubit
    
    temp = []
    for index in zIndices:
        left = circuitStates[index][4].strip()
        right = circuitStates[index][6].strip()
        amp = circuitStates[index][AMPLITUDE_INDEX].strip().split()[0]
        amp = float(amp) * NORMALISATION_FACTOR
        
        # Place within simulator here!
        if left == '0' and right == '1':
            # print(f"Applying Z |0> : {amp} [{index}]")
            temp.append([[0, 1], amp])
        elif left == '1' and right == '0':
            # print(f"Applying Z  |1> : {amp * -1} [{index}]")
            temp.append([[1, 0], amp * -1])
    verify(temp)
        
    
    for index in iIndices:
        left = circuitStates[index][4].strip()
        right = circuitStates[index][6].strip()
        amp = circuitStates[index][AMPLITUDE_INDEX].strip().split()[0]
        amp = float(amp) * NORMALISATION_FACTOR
        if left == '0' and right == '1':
            # print(f"Apply I  |0> : {amp} [{index}]")
            temp.append([[0, 1], amp])
        elif left == '1' and right == '0':
            # print(f"Apply I  |1> : {amp} [{index}]")
            temp.append([[1, 0], amp])
    # n = len(circuitStates)
receiver()