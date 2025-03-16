# Quantum Methods for Memory Attestation

The following implementation aims to simulate quantum teleportation in order to deploy a memory attestation protocol using quantum methods. 

The current scheme utilises the `soqcs` library which simulates a quantum linear optics circuit. Using the library, we have implemented a variety of quantum gates, namely the `Pauli [X|Y|Z]` and rotation gates. 

Since we have simulated a quantum teleportation scheme by extension we have implemented a non-deterministic quantum entanglement generator with a success of generating a maximally entangled Bell State with probability $\frac{1}{9}$. We have also implemented a Bell State analyser (Bell state measurer) using linear optics.



## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Building](#building)
  - [Running](#running)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

Using the `soqcs` library we simulate quantum teleportation using a linear optics approach. Quantum teleportation is the process of "cutting and pasting" an arbitary quantum state from a sender to a receiver from a distance. 

### Quantum Teleportation Crash Course

Suppose we have a friend Proton who wants to quantumally teleport an arbitary quantum state to another friend Neutron who lives $\frac{1}{365}$ light years away. Proton and Neutron first generate a maximally entangled Bell State. In our example, we will use $\frac{1}{\sqrt{2}}(\ket{00} + \ket{11}).$ Proton and Neutron a half of the entangled state. Proton prepares the quantum state $\psi$ which he wants to 

## Getting Started

The following section will show what libraries are required in order to run the work. We personally used a virtual environment `venv`.

### Prerequisites

- `soqcs`
- 

### Building

```bash
    python3 receiver.py
```