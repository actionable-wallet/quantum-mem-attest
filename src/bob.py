import subprocess
import pprint
import re

# Recall Alice has channels [0, 1], [3, 5] (0, 1 is the teleported state) (3, 5 her entangled pair)
# Bob has channels [4, 6] (his entangled pair)
# output = subprocess.run(["python3", "main.py"], text=True, capture_output=True)
output = subprocess.run(["python3", "main.py"], capture_output=True)
parsed = output.stdout.decode('utf-8').strip().split("\x1b[36m")

amplitudeIndex = 11


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
    
    

def bob():
    output = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    circuitState = parseOutput(output)
    
    rawOutputs = []
    measuredQubits = []
    teleportedQubits = []
    aliceQubits = []
    bobQubits = []
    
    zIndices = []
    iIndices = []
    for i, outputStrings in enumerate(circuitState):
        # if (0, 1) and (3, 5) alternate then apply Z gate
        # if (0)
        if i == 1:
            print(outputStrings)
        if i < 2:
            continue
        measuredQubit = []
        teleportedQubit = []
        aliceQubit = []
        bobQubit = []
        
        rawOutputs.append(outputStrings)
        for channel, photons in enumerate(outputStrings):
            # Don't want the amplitude
            if channel == amplitudeIndex:
                continue
            numPhotons = int(photons.strip())
            
            if channel == 0 or channel == 1:
                teleportedQubit.append(numPhotons)
                measuredQubit.append(numPhotons)
            elif channel == 3 or channel == 5:
                aliceQubit.append(numPhotons)
                measuredQubit.append(numPhotons)
            elif channel == 4 or channel == 6:
                bobQubit.append(numPhotons)
        # teleportedQubits.append(teleportedQubit)
        # aliceQubits.append(aliceQubit)
        bobQubits.append(bobQubit)
        measuredQubits.append(measuredQubit)
    for index, qubits in enumerate(measuredQubits):
        if qubits in zRotation:
            print(f"Rotate Z: {qubits} Index: {index}")
            zIndices.append(index)
        elif qubits in identityRotation:
            print(f"Rotate I: {qubits} Index: {index}")
            iIndices.append(index)
    for index in zIndices:
        left = rawOutputs[index][4].strip()
        right = rawOutputs[index][6].strip()
        amp = rawOutputs[index][11].strip()
        print(f"Bob's Qubit Before Z rotation |{left}{right}> : {amp}")
    for index in iIndices:
        left = rawOutputs[index][4].strip()
        right = rawOutputs[index][6].strip()
        amp = rawOutputs[index][11].strip()
        print(f"Bob's Qubit |{left}{right}> : {amp}")
    

bob()