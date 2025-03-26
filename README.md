# Quantum Methods for Memory Attestation

The following implementation aims to simulate quantum teleportation in order to deploy a memory attestation protocol using quantum methods. The methods used ensure that a remote device's memory is in a secure state. A key aspect of the scheme is to authenticate the prover without the requirement for trusted hardware. In the real-world relying on trusted hardware presents challenges within the supply chain and insider threats.

The current scheme utilises the `soqcs` library which simulates a quantum linear optics circuit. Using the library, we have implemented a variety of quantum gates, namely the `Pauli [X|Y|Z]` and rotation gates. 

Since we have simulated a quantum teleportation scheme by extension we have implemented a non-deterministic quantum entanglement generator with a success of generating a maximally entangled Bell State with probability $\frac{1}{9}$. We have also implemented a Bell State analyser (Bell state measurer) using linear optics.



## Table of Contents
- [Protocol](#protocol)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Building](#building)
  - [Running](#running)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Protocol

1. Verifier and Prover begin a game brrrrr. Verifier uniformly samples a challenge $c \leftarrow \{0, 1\}^*$. 

2. Prover has the memory state as $s_0$ and calculates Attest $(s_0, c) = \theta'$. Prover prepares the state $\sin(\frac{\theta'}{2})\ket{0} + \cos(\frac{\theta'}{2})\ket{1}$
to teleport.
3. 

## Features

Using the `soqcs` library we simulate quantum teleportation using a linear optics approach. Quantum teleportation is the process of "cutting and pasting" an arbitary quantum state from a sender to a receiver from a distance. 

![alt text](image.png)
> Example circuit

### Quantum Teleportation Crash Course

Suppose we have a friend Proton who wants to quantumally teleport an arbitary quantum state to another friend Neutron who lives $\frac{1}{365}$ light years away. Proton and Neutron first generate a maximally entangled Bell State. In our example, we will use $\frac{1}{\sqrt{2}}(\ket{0_P0_N} + \ket{1_P1_N}).$ Proton and Neutron a half of the entangled state denoted by the subscript $P$ and $N$. Proton prepares the quantum state $\psi_P$ which he wants to teleport to Neutron. Now the entire system can be denoted as $\psi_P \otimes\frac{1}{\sqrt{2}}(\ket{0_P0_N} + \ket{1_P1_N}.$

## Getting Started

The following section will show what libraries are required in order to run the work. We personally used a virtual environment `venv`. We have two files, `main.py` and `receiver.py`. Within the context of the memory attestation protocol, `main.py` represents the prover and `receiver.py` is the verifier.

### Prerequisites

- `soqcs`
- 

### Building

```bash
    python3 receiver.py
```