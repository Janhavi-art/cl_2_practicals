"""
Assignment 1: Implementation of 16-Qubit Random Number Generator
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Initialize number of qubits
n = 16

# Create a quantum circuit with 16 qubits and 16 classical bits
qc = QuantumCircuit(n, n)



# Apply hadamard gate to all qubits to create superposition
qc.h(range(n)) 

# Measure all qubits and store results in classical bits
qc.measure(range(n), range(n))

# Display quantum circuit
print(qc.draw(output='text'))

# Create a quantum circuit simulator
simulator = AerSimulator()

# Execute circuit once to generate one random 16-bit number
result = simulator.run(qc, shots=1).result()

# Retrieve measurement results
counts = result.get_counts()

# Extract generated binary string
bitstring = list(counts)[0]

# Convert binary to decimal
number = int(bitstring, 2)

print("\nRandom 16-bit string:", bitstring)
print("Random number (decimal):", number)

# Generate multiple results
result = simulator.run(qc, shots=1024).result()
counts = result.get_counts()

# Show only top 10 outcomes in histogram
top_counts = dict(
    sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
)
print("\nTop 10 measurement results:")
print(top_counts)

# Save histogram
fig = plot_histogram(
    top_counts,
    title="16-Qubit Random Number Generator"
)
fig.savefig(
    "assignment1_output.png",
    dpi=120,
    bbox_inches="tight"
)
plt.show()
print("\nHistogram saved as assignment1_output.png")

# ==================== CONCEPTS USED ====================

# 1. Quantum Computing:
# Quantum computing is a type of computing based on the principles
# of quantum mechanics. Classical computers use bits (0 or 1),
# whereas quantum computers use qubits.

# 2. Qubit (Quantum Bit):
# A qubit is the basic unit of quantum information.
# Unlike a classical bit, a qubit can exist in a superposition
# of 0 and 1 states. When measured, it produces either 0 or 1.

# 3. Superposition:
# Superposition is a quantum phenomenon in which a qubit exists
# in a combination of multiple possible states.
# In equal superposition, the probability of measuring 0 is 50%
# and the probability of measuring 1 is also 50%.
#
# Mathematically:
# |ψ⟩ = (|0⟩ + |1⟩) / √2

# 4. Hadamard Gate (H Gate):
# The Hadamard gate is a single-qubit quantum gate used to create
# equal superposition.
# It converts the initial state |0⟩ into a combination of |0⟩
# and |1⟩ with equal probability.
#
# H|0⟩ = (|0⟩ + |1⟩) / √2

# 5. Quantum Measurement:
# Measurement is the process of observing a qubit to obtain
# a classical result (0 or 1).
# It converts the quantum state into a classical bit.
# Measuring all 16 qubits produces a 16-bit binary string.

# 6. Quantum Circuit:
# A quantum circuit is a graphical representation of quantum
# operations performed on qubits.
# It consists of quantum wires, quantum gates and measurement
# operations.

# 7. Classical Register:
# A classical register stores the results obtained after
# measuring quantum bits.
# In this practical, 16 classical bits store the measurement
# results of 16 qubits.

# 8. Quantum Simulator:
# A quantum simulator executes quantum circuits on a classical
# computer without requiring actual quantum hardware.
# AerSimulator is used for this purpose.

# 9. Shots:
# A shot represents one execution of a quantum circuit.
# Each shot produces one measurement outcome.
# For example, 1024 shots generate 1024 measurement outcomes.

# 10. Measurement Counts:
# Measurement counts represent the frequency of each
# measurement outcome.
# They are stored as dictionary key-value pairs, where the
# binary string is the key and its frequency is the value.

# 11. Binary to Decimal Conversion:
# Binary is a number system with base 2, whereas decimal
# is a number system with base 10.
# The generated 16-bit binary string is converted into
# its equivalent decimal number.

# 12. Histogram:
# A histogram is a graphical representation of frequency
# distribution.
# The X-axis represents different measurement outcomes,
# while the Y-axis represents their corresponding frequencies.

# 13. Random Number Generation:
# Quantum random number generation uses the probabilistic
# nature of quantum measurement to produce random bits.
# Since each of the 16 qubits can produce 0 or 1,
# the total possible outcomes are 2^16 = 65536.

# 14. Quantum Random Number Generator (QRNG):
# A QRNG generates random numbers using quantum phenomena
# such as superposition and measurement.
# Unlike algorithm-based pseudo-random number generation,
# quantum randomness originates from probabilistic
# quantum measurement.