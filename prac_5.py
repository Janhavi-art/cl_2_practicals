
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a 5-qubit quantum circuit
n = 5
qc = QuantumCircuit(n, n)

# Initial state is |00000>
# All qubits are initially 0

# Apply Quantum Fourier Transform
def qft(qc, n):

    # Apply Hadamard gates to all qubits
    for j in range(n - 1, -1, -1):
        qc.h(j)

        # Apply controlled phase rotation gates
        for k in range(j - 1, -1, -1):
            angle = np.pi / (2 ** (j - k))
            qc.cp(angle, k, j)

    # Reverse the qubit order using SWAP gates
    for j in range(n // 2):
        qc.swap(j, n - j - 1)


# Perform QFT
qft(qc, n)

# Measure all qubits
qc.measure(range(n), range(n))

# Display the quantum circuit
print(qc.draw(output='text', fold=120))

# Create quantum simulator
simulator = AerSimulator()

# Execute circuit for 2048 shots
result = simulator.run(qc, shots=2048).result()

# Get measurement counts
counts = result.get_counts()

print("\nMeasurement counts:")
print(counts)

# Plot histogram
fig = plot_histogram(
    counts,
    title="5-Qubit Quantum Fourier Transform Output"
)

# Save and display histogram
fig.savefig(
    "assignment5_output.png",
    dpi=120,
    bbox_inches="tight"
)

plt.show()

print("\nHistogram saved as assignment5_output.png")



# ================= THEORY AND CONCEPTS =================

# 1. Fourier Transform (FT):
# Fourier Transform is a mathematical technique that converts
# information into a frequency-based representation.
# It is used in audio, image and signal processing.

# 2. Quantum Fourier Transform (QFT):
# QFT is the quantum equivalent of the Discrete Fourier Transform.
# It transforms a quantum state from the computational basis
# into the Fourier basis by changing its amplitudes and phases.
# It is used in quantum algorithms to extract periodicity
# and phase information.

# 3. Qubits:
# A qubit is the basic unit of quantum information.
# Unlike a classical bit, which is either 0 or 1, a qubit
# can exist in a superposition of both states.

# 4. Computational Basis States:
# These are the possible combinations of 0s and 1s.
# For 5 qubits, there are 2^5 = 32 possible states,
# ranging from |00000> to |11111>.

# 5. Initial State:
# The circuit starts in |00000>, meaning all five qubits
# are initially in state 0.

# 6. Superposition:
# Superposition means a quantum state can be a combination
# of multiple basis states.
# It allows a quantum circuit to represent multiple
# possible states simultaneously.

# 7. Hadamard Gate (H):
# The Hadamard gate creates superposition.
# When applied to |0>, it produces an equal combination
# of |0> and |1>.
# Applying H to all five qubits creates an equal
# superposition of 32 basis states.

# 8. Controlled Phase Gate (CP):
# It is a two-qubit gate that introduces a phase rotation
# when both control and target qubits are in state 1.
# Different rotation angles create different phase relationships.
# These rotations are essential for implementing QFT.

# 9. Phase:
# Phase is a property of a quantum probability amplitude.
# It affects how quantum states interfere with each other.
# QFT uses controlled phase rotations to introduce
# specific phase relationships.

# 10. SWAP Gate:
# The SWAP gate exchanges the states of two qubits.
# It is used at the end of QFT to reverse the qubit order
# and obtain the correct output ordering.

# 11. Measurement:
# Measurement converts quantum information into classical bits.
# It produces a 5-bit binary output representing one
# of the 32 possible measurement outcomes.

# 12. Quantum Simulator:
# AerSimulator simulates the execution of a quantum circuit
# without requiring an actual quantum computer.

# 13. Shots:
# Shots represent the number of times the circuit is executed
# and measured.
# In this practical, 2048 shots are used.

# 14. Measurement Histogram:
# A histogram displays how frequently each measurement
# outcome occurs.
# It helps visualize and verify the output probability distribution.
# For the input |00000>, all 32 outcomes have equal probability.
# Therefore, each is expected to appear approximately
# 2048/32 = 64 times.

# 15. Applications of QFT:
# - Shor's Algorithm: Helps find periodicity for integer factorisation.
# - Quantum Phase Estimation: Helps estimate phase values.
# - Quantum Chemistry: Used in algorithms for estimating molecular energies.

# ==================== CONCLUSION ====================

# Thus, a 5-qubit Quantum Fourier Transform was implemented
# using Hadamard, Controlled Phase and SWAP gates.
# The circuit was simulated and measured, and the output
# probability distribution was visualized using a histogram.

# ==========================================================
