"""
Assignment 2: Tackle Noise with Error Correction 3-Qubit Bit-Flip Error Correction Code
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. Define bit-flip noise with probability 0.3
p_error = 0.3

# X represents a bit-flip error; I represents no error
bit_flip = pauli_error([
    ('X', p_error),
    ('I', 1 - p_error)
])

# Apply noise only to the ID gate
noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(bit_flip, ['id'])

# 2. Create circuit: 3 data qubits and 2 syndrome qubits
# Q0, Q1, Q2 = data qubits; Q3, Q4 = syndrome qubits
qc = QuantumCircuit(5, 3)

# 3. Encode logical |1> as |111>
# Initially all qubits are |0>
qc.x(0)
qc.cx(0, 1)
qc.cx(0, 2)

# 4. Introduce bit-flip noise on qubit 1 (Q1)
qc.id(1)

# 5. Detect errors using syndrome qubits
# Q3 stores Q0 XOR Q1; Q4 stores Q1 XOR Q2
qc.cx(0, 3)
qc.cx(1, 3)
qc.cx(1, 4)
qc.cx(2, 4)

# 6. Measure the syndrome qubits and store result in classical bits
qc.measure(3, 0)
qc.measure(4, 1)

# 7. Correct errors based on syndrome

# Syndrome 10: Error in Q0
with qc.if_test((qc.clbits[0], 1)):
    with qc.if_test((qc.clbits[1], 0)):
        qc.x(0)

# Syndrome 11: Error in Q1
with qc.if_test((qc.clbits[0], 1)):
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(1)

# Syndrome 01: Error in Q2
with qc.if_test((qc.clbits[0], 0)):
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(2)

# 8. Measure Q0 after correction to verify the logical state
qc.measure(0, 2)

# 9. Display the circuit
print("Quantum Circuit:")
print(qc.draw(output='text', fold=120))

# 10. Run the noisy simulation
simulator = AerSimulator(noise_model=noise_model)
result = simulator.run(qc, shots=1024).result()

counts = result.get_counts()

# 11. Display measurement counts
print("\nMeasurement Counts:")
print(counts)

# 12. Plot and save the histogram

# Rename measurement outcomes for clear identification in the histogram
counts = {'No Error (100)': counts.get('100', 0),
          'Error Corrected (111)': counts.get('111', 0)}

fig = plot_histogram(
    counts,
    title="3-Qubit Bit-Flip Error Correction"
)

fig.savefig(
    "assignment2_output.png",
    dpi=120,
    bbox_inches="tight"
)

plt.show()

print("\nHistogram saved as assignment2_output.png")

# THEORY CONCEPTS:

# 1. Qubit:
# A qubit is the basic unit of quantum information.
# It can exist in a superposition of |0> and |1> states.

# 2. Quantum Gates:
# Quantum gates perform operations on qubits.
# X gate flips a qubit, while CNOT flips the target
# qubit only when the control qubit is 1.

# 3. Bit-Flip Error:
# A bit-flip error changes |0> to |1> or |1> to |0>.
# It is represented by the Pauli-X gate.

# 4. Quantum Noise:
# Noise represents unwanted changes in qubits.
# Here, bit-flip noise is introduced with 30% probability
# and no error occurs with 70% probability.

# 5. 3-Qubit Bit-Flip Error Correction:
# One logical qubit is encoded using three physical qubits.
# |0> is encoded as |000> and |1> as |111>.
# This redundancy helps detect and correct a single bit-flip error.

# 6. Syndrome Measurement:
# Syndrome measurement identifies the location of an error
# without directly measuring the encoded logical information.
# Two syndrome qubits compare adjacent data qubits using XOR.

# 7. Error Correction:
# Conditional X gates are applied based on the syndrome.
# This restores the affected qubit to its original state.

# 8. Quantum Simulation:
# AerSimulator executes the quantum circuit on a classical computer.
# Multiple shots are used to observe measurement statistics.

# 9. Measurement Histogram:
# The histogram displays the frequency of measurement outcomes.
# It helps verify error detection and correction.
# Qiskit displays classical bits in reverse order (c2 c1 c0).