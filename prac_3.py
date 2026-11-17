"""
Assignment 3: Implement Quantum Teleportation Algorithm in Python
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

# 1. Create 3-qubit circuit and 3 classical bits
qc = QuantumCircuit(3, 3)

# 2. Prepare Alice's quantum state
qc.ry(np.pi / 3, 0)
qc.rz(np.pi / 4, 0)

# 3. Create Bell pair shared by Alice and Bob
qc.h(1)
qc.cx(1, 2)

# 4. Alice performs Bell measurement
qc.cx(0, 1)
qc.h(0)

qc.measure(0, 0)
qc.measure(1, 1)

# 5. Bob applies conditional corrections
# Apply X if Alice's second measurement is 1
with qc.if_test((qc.clbits[1], 1)):
    qc.x(2)

# Apply Z if Alice's first measurement is 1
with qc.if_test((qc.clbits[0], 1)):
    qc.z(2)

# 6. Measure Bob's qubit
qc.measure(2, 2)

# 7. Display the circuit
print("Quantum Teleportation Circuit:")
print(qc.draw(output="text", fold=120))

# 8. Run the simulation
simulator = AerSimulator()
result = simulator.run(qc, shots=1024).result()

# 9. Display measurement results
counts = result.get_counts()
print("\nMeasurement Counts:")
print(counts)

# 10. Plot and save histogram
fig = plot_histogram(
    counts,
    title="Quantum Teleportation Results"
)

fig.savefig(
    "assignment3_output.png",
    dpi=120,
    bbox_inches="tight"
)

plt.show()

print("\nHistogram saved as assignment3_output.png")

# Meaning of measurement results (Qiskit displays bits as c2 c1 c0):
# c2 = Bob's measurement result
# c1 = Alice's second measurement (controls X gate)
# c0 = Alice's first measurement (controls Z gate)

# 000: Alice gets 00, Bob measures 0. No correction required.
# 001: Alice gets 10, Bob measures 0. Apply Z gate.
# 010: Alice gets 01, Bob measures 0. Apply X gate.
# 011: Alice gets 11, Bob measures 0. Apply both X and Z gates.

# The number beside each bitstring represents how many times
# that measurement result occurred in 1024 executions.


# QUANTUM TELEPORTATION:
# Quantum teleportation is a technique used to transfer an unknown
# quantum state from a sender (Alice) to a receiver (Bob).
# It uses quantum entanglement, Bell measurement and classical communication.
# The physical qubit is not transferred; only its quantum state is transferred.


# 1. QUBIT:
# A qubit is the basic unit of quantum information.
# Unlike a classical bit, which is either 0 or 1, a qubit can exist
# in a superposition of both states.
# General quantum state:
# |ψ> = α|0> + β|1>
# where α and β are probability amplitudes and
# |α|² + |β|² = 1.


# 2. SUPERPOSITION:
# Superposition means a qubit can exist as a combination of
# |0> and |1> states before measurement.
# Measurement gives either 0 or 1.
# The probability of each outcome depends on its probability amplitude.


# 3. QUANTUM GATES:
# Quantum gates are operations used to change or manipulate qubit states.
# H (Hadamard): Creates superposition.
# X (Pauli-X): Flips the qubit, changing |0> to |1> and vice versa.
# Z (Pauli-Z): Changes the phase of the |1> component.
# CNOT: A two-qubit gate that flips the target if the control is 1.
# RY and RZ: Rotate a qubit around the Y-axis and Z-axis.


# 4. BELL PAIR / QUANTUM ENTANGLEMENT:
# Entanglement is a special quantum connection between two qubits.
# The state of one qubit is correlated with the other.
# A Bell pair is a maximally entangled pair of two qubits.
# It is created using a Hadamard gate followed by a CNOT gate.
# Bell state:
# |Φ+> = (|00> + |11>) / √2
# In this practical, q1 belongs to Alice and q2 belongs to Bob.
# The entangled pair acts as the quantum resource for teleportation.


# 5. THREE QUBITS USED IN TELEPORTATION:
# q0: Alice's original quantum state that she wants to teleport.
# q1: Alice's half of the entangled Bell pair.
# q2: Bob's half of the entangled Bell pair.
# q0 and q1 are used by Alice for Bell measurement.
# q2 is the destination qubit that receives the original state.


# 6. BELL-STATE MEASUREMENT:
# Alice performs Bell measurement on her two qubits (q0 and q1).
# CNOT and Hadamard gates are applied before measurement.
# Measurement converts the quantum information into two classical bits.
# The original state on q0 is destroyed during this process.
# Alice's measurement results determine which corrections Bob must apply.


# 7. CLASSICAL COMMUNICATION:
# Alice sends her two measurement results (c0 and c1) to Bob.
# Each classical bit can have a value of 0 or 1.
# Therefore, four possible combinations are obtained:
# 00, 01, 10 and 11.
# These results tell Bob which correction gates are required.


# 8. CONDITIONAL QUANTUM CORRECTIONS:
# Bob applies correction gates to his qubit q2 based on Alice's results.
# c1 controls the X gate (bit-flip correction).
# c0 controls the Z gate (phase-flip correction).
#
# Measurement result 00: No correction required.
# Measurement result 01: Apply X gate.
# Measurement result 10: Apply Z gate.
# Measurement result 11: Apply both X and Z gates.
#
# Both conditions are checked independently.
# After correction, Bob's qubit contains Alice's original quantum state,
# up to an irrelevant global phase.


# 9. QUANTUM MEASUREMENT:
# Measurement converts a quantum state into a classical result (0 or 1).
# In this practical, Alice measures q0 and q1 to obtain classical bits.
# Bob measures q2 to obtain his final measurement result.
# Measuring a qubit generally destroys its superposition.


# 10. QUANTUM SIMULATION:
# A quantum simulator imitates the execution of a quantum circuit
# on a classical computer.
# It allows us to test quantum algorithms without a physical quantum computer.
# AerSimulator is used to execute the circuit.


# 11. SHOTS:
# Shots represent the number of times a quantum circuit is executed.
# For example, 1024 shots means the circuit is executed 1024 times.
# Repeated executions help us observe the statistical distribution
# of different measurement outcomes because quantum measurement is probabilistic.


# 12. MEASUREMENT COUNTS:
# Measurement counts represent the frequency of each measurement outcome.
# For example, {'000': 250} means the outcome 000 occurred 250 times.
# Qiskit displays classical bits in reverse order: c2 c1 c0.
# c2 represents Bob's measurement.
# c1 represents Alice's second measurement.
# c0 represents Alice's first measurement.


# 13. HISTOGRAM:
# A histogram is a graphical representation of measurement counts.
# X-axis represents different measurement outcomes (bitstrings).
# Y-axis represents the number of times each outcome occurred.
# It helps visualize the distribution of measurement results.
# It does not independently prove successful quantum teleportation.


# 14. NO-CLONING THEOREM:
# The no-cloning theorem states that an unknown quantum state
# cannot be copied perfectly.
# Quantum teleportation does not create a duplicate of the original state.
# Alice's original state is destroyed during measurement,
# while Bob obtains the same state on his qubit.

