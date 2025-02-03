# quantum-mem-attest

The current scheme utilises the `soqcs` library which simulates a quantum linear optics circuit. Using the library, we have implemented a variety of quantum gates, namely the `Pauli [X|Y|Z]` and rotation gates. We have also simulated a non-deterministic quantum entanglement generator with a success of generating a maximally entangled Bell State with probability $\frac{1}{9}$. 

In the next few weeks we expect to simulate quantum teleportation by introducing a Bell State measurement device. Once all the primitives are in place, we shall introduce noise into the system and reveal the viability of our scheme.