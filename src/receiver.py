import subprocess
import pprint
import re
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
    for index in zIndices:
        left = circuitStates[index][4].strip()
        right = circuitStates[index][6].strip()
        amp = circuitStates[index][AMPLITUDE_INDEX].strip().split()[0]
        amp = float(amp) * NORMALISATION_FACTOR
        
        # Place within simulator here!
        if left == '0' and right == '1':
            print(f"Applying Z |0> : {amp} [{index}]")
        elif left == '1' and right == '0':
            print(f"Applying Z  |1> : {amp * -1} [{index}]")
    
    for index in iIndices:
        left = circuitStates[index][4].strip()
        right = circuitStates[index][6].strip()
        amp = circuitStates[index][AMPLITUDE_INDEX].strip().split()[0]
        amp = float(amp) * NORMALISATION_FACTOR
        if left == '0' and right == '1':
            print(f"Apply I  |0> : {amp} [{index}]")
        elif left == '1' and right == '0':
            print(f"Apply I  |1> : {amp} [{index}]")

receiver()