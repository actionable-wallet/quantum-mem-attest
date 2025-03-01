import subprocess
import pprint
import re
from math import sqrt


output = subprocess.run(["python3", "main.py"], capture_output=True)
parsed = output.stdout.decode('utf-8').strip().split("\x1b[36m")
amplitudeIndex = 7

# Usually make this 6 in order to account for 1/3 * 1/2 (entanglement generator AND measurement)
normalisationFactor = 6


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
            if channel == amplitudeIndex or "=" in photons:
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
        bobQubits.append(bobQubit)
        measuredQubits.append(measuredQubit)
        aliceQubits.append(aliceQubit)
    
    for index, qubits in enumerate(measuredQubits):
        if qubits in zRotation:
            zIndices.append(index)
        elif qubits in identityRotation:
            iIndices.append(index)
    
    for index in zIndices:
        left = rawOutputs[index][4].strip()
        right = rawOutputs[index][6].strip()
        amp = rawOutputs[index][amplitudeIndex].strip().split()[0]
        amp = float(amp) * normalisationFactor
        if left == '0' and right == '1':
            print(f"Apply Z |0> : {amp} [{index}]")
        elif left == '1' and right == '0':
            print(f"Apply Z  |1> : {amp} [{index}]")
    
    for index in iIndices:
        left = rawOutputs[index][4].strip()
        right = rawOutputs[index][6].strip()
        amp = rawOutputs[index][amplitudeIndex].strip().split()[0]
        amp = float(amp) * normalisationFactor
        if left == '0' and right == '1':
            print(f"Apply I  |0> : {amp} [{index}]")
        elif left == '1' and right == '0':
            print(f"Apply I  |1> : {amp} [{index}]")

bob()