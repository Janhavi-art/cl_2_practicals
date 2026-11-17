"""
Assignment 4: Randomized Benchmarking

Randomized Benchmarking is used to estimate quantum gate errors.
It applies random quantum gates followed by their inverse gates.
Ideally, the qubit should return to its initial state |0>.
Due to noise, errors accumulate and the qubit may not return correctly.
We measure the survival probability for different sequence lengths
and plot an exponential fidelity decay curve.
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# Define gates used to construct random Clifford-like sequences.
# The complete single-qubit Clifford group contains 24 operations.
clifford_gates = ['h', 'x', 'y', 'z', 's', 'sdg']


# Randomly select a gate, apply it to the qubit and return its name.
def apply_random_clifford(qc, qubit, rng):
    gate = rng.choice(clifford_gates)
    getattr(qc, gate)(qubit)
    return gate


# Apply the inverse of a gate to cancel its previous operation.
# H, X, Y and Z are their own inverses.
# S and S-dagger are inverses of each other.
def inverse_gate(qc, qubit, gate):
    inverse_map = {'h': 'h', 'x': 'x', 'y': 'y', 'z': 'z', 's': 'sdg', 'sdg': 's'}
    getattr(qc, inverse_map[gate])(qubit)


# Create a depolarizing noise model to simulate errors during gate operations.
# A noise parameter of 0.01 is applied to each specified single-qubit gate.
noise_model = NoiseModel()
error_1q = depolarizing_error(0.01, 1)
noise_model.add_all_qubit_quantum_error(error_1q, clifford_gates)

# Create a simulator that executes quantum circuits with the specified noise.
simulator = AerSimulator(noise_model=noise_model)


# Set up the experiment.
rng = np.random.default_rng(42)  # Fixed seed for reproducible random sequences.
sequence_lengths = [1, 5, 10, 20, 30, 50, 75, 100]  # Number of random gates.
shots = 512  # Number of times each circuit is executed.
n_sequences = 20  # Number of random circuits tested for each length.

survival_probabilities = []  # Stores average survival probability for each length.


# Test different random sequence lengths.
for length in sequence_lengths:
    successes = 0

    # Generate multiple random sequences for the same length.
    for _ in range(n_sequences):
        qc = QuantumCircuit(1, 1)  # One qubit and one classical bit.
        applied_gates = []  # Stores the random gates for later reversal.

        # Apply the randomly selected gates to the qubit.
        for _ in range(length):
            g = apply_random_clifford(qc, 0, rng)
            applied_gates.append(g)

        # Apply inverse gates in reverse order to ideally restore |0>.
        for g in reversed(applied_gates):
            inverse_gate(qc, 0, g)

        # Measure the qubit and store the result in the classical bit.
        qc.measure(0, 0)

        # Execute the circuit 512 times using the noisy simulator.
        job = simulator.run(qc, shots=shots)
        counts = job.result().get_counts()

        # Count measurements of 0 as successful returns to the initial state.
        # Divide by shots to calculate survival probability for this sequence.
        successes += counts.get('0', 0) / shots

    # Average the survival probabilities of all 20 random sequences.
    survival_probabilities.append(successes / n_sequences)


# Display sequence lengths and their corresponding average survival probabilities.
print("Sequence lengths:", sequence_lengths)
print("Survival probabilities (fidelity):", [round(p, 4) for p in survival_probabilities])


# Define the exponential decay equation used to fit the measured data.
# A = amplitude, p = decay parameter, m = sequence length, B = baseline.
# A higher p indicates slower decay and generally lower gate error.
def exp_decay(m, A, p, B):
    return A * (p ** m) + B


from scipy.optimize import curve_fit

try:
    # Fit the exponential equation to estimate A, p and B.
    # p0 provides initial guesses for the fitting algorithm.
    popt, _ = curve_fit(exp_decay, sequence_lengths, survival_probabilities, p0=[0.5, 0.99, 0.5])
    A, p, B = popt

    # Estimate average single-qubit Clifford error using the RB formula.
    error_per_clifford = (1 - p) / 2

    print(f"\nFitted depolarizing parameter p = {p:.5f}")
    print(f"Estimated average error per Clifford gate = {error_per_clifford:.5f}")

except Exception as e:
    # Use default values if curve fitting fails.
    print("Curve fit failed:", e)
    A, p, B = 0.5, 0.99, 0.5


# Generate additional points to draw a smooth fitted decay curve.
m_fit = np.linspace(min(sequence_lengths), max(sequence_lengths), 200)

plt.figure(figsize=(8, 5))

# Blue points represent measured survival probabilities.
plt.scatter(sequence_lengths, survival_probabilities,
            color='blue', label='Measured survival probability')

# Red curve represents the fitted exponential decay.
plt.plot(m_fit, exp_decay(m_fit, A, p, B),
         color='red', label=f'Fit: F(m) = A·p^m + B (p={p:.4f})')

# Add graph labels, title, legend and grid.
plt.xlabel("Sequence length (m)")
plt.ylabel("Survival probability (fidelity)")
plt.title("Randomized Benchmarking: Fidelity Decay Curve")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# Save the graph as an image.
plt.savefig("assignment4_output.png", dpi=120)
print("\nFidelity decay plot saved as assignment4_output.png")

# ==================== THEORY AND CONCEPTS ====================
#
# 1. RANDOMIZED BENCHMARKING (RB)
# Randomized Benchmarking is a technique used to estimate the error
# rates of quantum gates in a quantum computer.
# It applies random quantum gates followed by their inverse operations.
# Ideally, the qubit should return to its initial state |0>.
# Due to noise and gate imperfections, the final state may differ.
# By measuring the probability of returning to |0> for different
# sequence lengths, we can study how quantum gate errors accumulate.
#
#
# 2. QUBIT
# A qubit (quantum bit) is the basic unit of quantum information.
# Unlike a classical bit, which is either 0 or 1, a qubit can exist
# in a superposition of both computational basis states.
#
# General state of a qubit:
# |ψ> = α|0> + β|1>
#
# Here, α and β are probability amplitudes.
# Probability of measuring 0 = |α|²
# Probability of measuring 1 = |β|²
# |α|² + |β|² = 1
#
# The initial state used in this practical is |0>.
#
#
# 3. QUANTUM GATES
# Quantum gates are operations that change the state of a qubit.
# The practical uses the following single-qubit gates:
#
# H (Hadamard): Creates superposition from |0>.
#               H|0> = (|0> + |1>) / √2
#
# X (Pauli-X): Flips the qubit state, like a classical NOT gate.
#              X|0> = |1>, X|1> = |0>
#
# Y (Pauli-Y): Flips the state and introduces a phase change.
#
# Z (Pauli-Z): Changes the phase of the |1> component.
#              Z|0> = |0>, Z|1> = -|1>
#
# S (Phase gate): Adds a phase factor of i to the |1> component.
#
# S-dagger (S†): Inverse of the S gate; removes the phase
#                introduced by the S gate.
#
#
# 4. CLIFFORD GROUP
# The Clifford group is a special group of quantum operations
# used in quantum computing and Randomized Benchmarking.
# It contains 24 distinct single-qubit Clifford operations
# when operations differing only by global phase are treated
# as equivalent.
# Clifford operations can be constructed using gates such as
# H and S, along with Pauli operations.
#
# This practical uses H, X, Y, Z, S and S-dagger as generators
# to construct simplified random Clifford-like sequences.
# It does not generate all 24 Clifford operations uniformly.
#
#
# 5. INVERSE QUANTUM GATES
# An inverse gate reverses the effect of a previously applied gate.
# Applying a gate followed by its inverse returns the qubit
# to its original state.
#
# H, X, Y and Z are their own inverses:
# H² = I, X² = I, Y² = I, Z² = I
#
# S and S-dagger are inverses of each other:
# S†S = I
#
# I represents the identity operation (no net change).
#
# The inverse sequence must be applied in REVERSE ORDER.
# For example:
# Original sequence: H -> X -> S
# Inverse sequence:  S† -> X -> H
#
# Ideally, the complete sequence returns the qubit to |0>.
# Mathematically: G⁻¹G = I
#
#
# 6. QUANTUM NOISE
# Quantum noise refers to unwanted changes in a quantum state
# caused by imperfections in quantum hardware and operations.
# Noise can prevent the qubit from returning to its initial state.
#
# DEPOLARIZING NOISE:
# It is a mathematical noise model that introduces random
# Pauli errors (X, Y or Z) into a quantum state.
# It represents imperfections in quantum gate operations.
#
# In this practical, a depolarizing noise parameter of 0.01
# is used for the specified single-qubit gates.
# Noise is simulated using Qiskit Aer rather than a real device.
#
#
# 7. QUANTUM MEASUREMENT
# Measurement converts the quantum state into a classical result.
# The qubit is measured in the computational basis, producing 0 or 1.
#
# The initial state is |0>, so measurement result 0 is considered
# a successful return to the expected initial-state outcome.
#
#
# 8. SHOTS
# A shot is one execution of a quantum circuit.
# Since quantum measurement is probabilistic, the circuit is
# executed multiple times to estimate measurement probabilities.
#
# In this practical, each circuit is executed 512 times.
# The measurement counts are used to calculate survival probability.
#
#
# 9. SEQUENCE LENGTH
# Sequence length (m) represents the number of random gates
# applied before applying their inverse operations.
#
# Different sequence lengths are tested to study the effect
# of increasing the number of quantum gate operations.
# Longer sequences provide more opportunities for errors to accumulate.
#
# The tested sequence lengths are:
# 1, 5, 10, 20, 30, 50, 75 and 100.
#
#
# 10. SURVIVAL PROBABILITY
# Survival probability is the probability that the final
# measurement produces the expected initial-state outcome (0).
#
# Formula:
# P(survival) = Number of measurements resulting in 0 / Total shots
#
# For example, if 460 out of 512 measurements produce 0:
# P(survival) = 460 / 512 = 0.8984
#
# This means the expected outcome is obtained in approximately
# 89.84% of the executions.
#
# Multiple random sequences are tested for each sequence length,
# and their survival probabilities are averaged to reduce
# fluctuations caused by individual random sequences.
#
#
# 11. EXPONENTIAL FIDELITY DECAY
# Randomized Benchmarking uses an exponential decay model
# to describe how survival probability changes with sequence length.
#
# Mathematical equation:
# F(m) = A * p^m + B
#
# Where:
# F(m) = Survival probability at sequence length m.
# A     = Amplitude of the decay.
# p     = Depolarizing decay parameter.
# m     = Number of random gates in the sequence.
# B     = Baseline or offset.
#
# A value of p close to 1 indicates slower decay and generally
# lower gate error.
# A smaller p indicates faster decay and generally higher gate error.
#
#
# 12. CURVE FITTING
# Curve fitting is a mathematical technique used to find the
# parameters of an equation that best match experimental data.
#
# In this practical, SciPy's curve_fit() function estimates
# A, p and B from the measured survival probabilities.
# These fitted parameters are used to draw the exponential
# fidelity decay curve.
#
#
# 13. ERROR PER CLIFFORD GATE
# The standard single-qubit depolarizing Randomized Benchmarking
# model estimates average error per Clifford using:
#
# r = (1 - p) / 2
#
# Where:
# r = Estimated average error per Clifford.
# p = Fitted depolarizing decay parameter.
#
# For example, if p = 0.99:
# r = (1 - 0.99) / 2 = 0.005
#
# Therefore, the estimated error is 0.5%.
#
# This formula assumes standard single-qubit Clifford RB.
# Since this practical uses simplified random gate sequences,
# the calculated value is only an illustrative estimate.
#
#
# 14. FIDELITY DECAY GRAPH
# The graph represents the relationship between sequence length
# and survival probability.
#
# X-axis: Number of random gates (sequence length).
# Y-axis: Measured survival probability.
#
# Blue points: Experimentally measured average survival probabilities.
# Red curve: Exponential curve fitted to the measured data.
#
# Generally, survival probability decreases as sequence length
# increases because more gate operations create more opportunities
# for noise and errors to accumulate.
#
# A slower decay indicates better preservation of the expected
# quantum state under the assumed benchmarking model.
#
#
# 15. OVERALL WORKING
# 1. Initialize a qubit in state |0>.
# 2. Generate and apply a random sequence of quantum gates.
# 3. Store the applied gates.
# 4. Apply their inverse gates in reverse order.
# 5. Measure the qubit and count the occurrences of 0 and 1.
# 6. Calculate survival probability using repeated shots.
# 7. Repeat the experiment for multiple random sequences.
# 8. Calculate average survival probability for each sequence length.
# 9. Fit an exponential decay equation to the measured data.
# 10. Estimate the decay parameter and error rate.
# 11. Plot the fidelity decay curve.
#
#
# CONCLUSION:
# Randomized Benchmarking demonstrates how quantum gate errors
# accumulate as the number of operations increases.
# It estimates gate performance by measuring survival probability
# after applying random gate sequences and their inverses.
# The exponential decay curve helps characterize the effect
# of noise on quantum operations.
#
# ==============================================================