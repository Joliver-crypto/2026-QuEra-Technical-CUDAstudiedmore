"""
Segment 1.1: Basic Bloqade Setup
================================
Goal: Create a simple Bloqade Squin kernel with basic gates

This script demonstrates:
- Qubit allocation
- Basic quantum gates (H, CNOT, X, Y, Z)
- Circuit visualization
- Sampling with Stim and Tsim backends
"""

from bloqade import squin
import bloqade.stim
import bloqade.tsim


@squin.kernel
def basic_bell_state():
    """Create a Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2"""
    # Allocate 2 qubits
    q = squin.qalloc(2)
    
    # Apply Hadamard to first qubit
    squin.h(q[0])
    
    # Apply CNOT with q[0] as control and q[1] as target
    squin.cx(q[0], q[1])
    
    # Measure both qubits
    squin.measure(q[0])
    squin.measure(q[1])


@squin.kernel
def basic_gates_demo():
    """Demonstrate various basic gates"""
    q = squin.qalloc(3)
    
    # Single-qubit gates
    squin.x(q[0])  # Pauli X (bit flip)
    squin.y(q[1])  # Pauli Y
    squin.z(q[2])  # Pauli Z (phase flip)
    
    squin.h(q[0])  # Hadamard
    squin.s(q[1])  # S gate (phase)
    
    # Two-qubit gates
    squin.cx(q[0], q[1])  # CNOT
    squin.cz(q[1], q[2])  # Controlled-Z
    
    # Measurements
    squin.measure(q[0])
    squin.measure(q[1])
    squin.measure(q[2])


@squin.kernel
def ghz_state(n: int = 3):
    """Create a GHZ state: |GHZ⟩ = (|000...0⟩ + |111...1⟩)/√2"""
    q = squin.qalloc(n)
    
    # Apply Hadamard to first qubit
    squin.h(q[0])
    
    # Apply CNOT cascade
    for i in range(n - 1):
        squin.cx(q[i], q[i + 1])
    
    # Measure all qubits
    for i in range(n):
        squin.measure(q[i])


def visualize_and_sample(kernel_func, kernel_name: str, shots: int = 1000):
    """
    Visualize circuit and run sampling with both Stim and Tsim
    
    Args:
        kernel_func: Squin kernel function
        kernel_name: Name for display
        shots: Number of samples
    """
    print(f"\n{'='*60}")
    print(f"Circuit: {kernel_name}")
    print(f"{'='*60}\n")
    
    # Convert to Tsim for visualization
    print("Converting to Tsim circuit...")
    tsim_circ = bloqade.tsim.Circuit(kernel_func)
    
    print("Circuit diagram:")
    try:
        # Display circuit diagram (works in notebooks, saves to file otherwise)
        diagram = tsim_circ.diagram(height=400)
        print("  [Circuit diagram generated - view in Jupyter notebook]")
    except Exception as e:
        print(f"  [Diagram generation skipped: {e}]")
    
    # Sample with Stim (faster for Clifford circuits)
    print(f"\nSampling with Stim ({shots} shots)...")
    stim_circ = bloqade.stim.Circuit(kernel_func)
    stim_sampler = stim_circ.compile_sampler()
    stim_samples = stim_sampler.sample(shots=shots)
    
    print(f"Stim samples shape: {stim_samples.shape}")
    print(f"First 10 samples:\n{stim_samples[:10]}")
    
    # Analyze results
    analyze_samples(stim_samples, kernel_name)
    
    # Sample with Tsim
    print(f"\nSampling with Tsim ({shots} shots)...")
    tsim_sampler = tsim_circ.compile_sampler()
    tsim_samples = tsim_sampler.sample(shots=shots)
    
    print(f"Tsim samples shape: {tsim_samples.shape}")
    print(f"First 10 samples:\n{tsim_samples[:10]}")


def analyze_samples(samples, circuit_name: str):
    """Analyze measurement outcomes"""
    import numpy as np
    
    # Count unique outcomes
    unique_outcomes = {}
    for sample in samples:
        outcome = ''.join(map(str, sample.astype(int)))
        unique_outcomes[outcome] = unique_outcomes.get(outcome, 0) + 1
    
    print(f"\nOutcome statistics for {circuit_name}:")
    print(f"Total shots: {len(samples)}")
    print(f"Unique outcomes: {len(unique_outcomes)}")
    print("\nTop outcomes:")
    for outcome, count in sorted(unique_outcomes.items(), key=lambda x: x[1], reverse=True)[:5]:
        prob = count / len(samples)
        print(f"  |{outcome}⟩: {count:4d} ({prob:.3f})")


def main():
    """Run all basic examples"""
    print("="*60)
    print("Segment 1.1: Basic Bloqade Setup")
    print("="*60)
    
    # Example 1: Bell state
    visualize_and_sample(basic_bell_state, "Bell State", shots=1000)
    
    # Example 2: Basic gates demo
    visualize_and_sample(basic_gates_demo, "Basic Gates Demo", shots=1000)
    
    # Example 3: GHZ state
    @squin.kernel
    def ghz_3():
        return ghz_state(3)
    
    visualize_and_sample(ghz_3, "3-Qubit GHZ State", shots=1000)
    
    print("\n" + "="*60)
    print("✓ Segment 1.1 Complete!")
    print("="*60)
    print("\nKey Takeaways:")
    print("1. Bloqade Squin kernels use @squin.kernel decorator")
    print("2. qalloc() allocates qubits")
    print("3. Gates: h, x, y, z, s, cx, cz, etc.")
    print("4. Both Stim and Tsim can sample Clifford circuits")
    print("5. Circuit visualization available via Tsim")


if __name__ == "__main__":
    main()
