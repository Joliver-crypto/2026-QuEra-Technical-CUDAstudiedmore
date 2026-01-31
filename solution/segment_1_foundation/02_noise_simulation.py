"""
Segment 1.2: Noise Simulation Basics
====================================
Goal: Add noise channels to Bloqade circuits and simulate with Stim

This script demonstrates:
- Depolarizing noise on single qubits
- Two-qubit depolarizing noise
- Manual noise insertion at specific points
- Effect of noise on measurement outcomes

Pure Bloqade implementation
"""

from bloqade import squin
from kirin.dialects.ilist import IList
import bloqade.stim
import bloqade.tsim


@squin.kernel
def bell_state_with_noise(p: float = 0.01):
    """
    Bell state with single-qubit depolarizing noise
    
    Args:
        p: Depolarizing noise probability (0 = no noise, 1 = maximum noise)
    """
    q = squin.qalloc(2)
    
    # Create Bell state
    squin.h(q[0])
    squin.cx(q[0], q[1])
    
    # Add depolarizing noise to both qubits
    squin.depolarize(p, q[0])
    squin.depolarize(p, q[1])
    
    # Measure
    squin.measure(q[0])
    squin.measure(q[1])


@squin.kernel
def bell_with_two_qubit_noise(p1: float = 0.01, p2: float = 0.02):
    """
    Bell state with both single-qubit and two-qubit noise
    
    Args:
        p1: Single-qubit noise probability
        p2: Two-qubit noise probability
    """
    q = squin.qalloc(2)
    
    # Add noise before state preparation
    squin.depolarize(p1, q[0])
    squin.depolarize(p1, q[1])
    
    # Create Bell state
    squin.h(q[0])
    
    # Noise on CNOT gate
    squin.cx(q[0], q[1])
    squin.depolarize2(p2, q[0], q[1])  # Two-qubit depolarizing noise
    
    # Final single-qubit noise
    squin.depolarize(p1, q[0])
    squin.depolarize(p1, q[1])
    
    # Measure
    squin.measure(q[0])
    squin.measure(q[1])


@squin.kernel
def broadcast_noise_demo(p: float = 0.05):
    """
    Demonstrate broadcast operations for parallel noise application
    
    Args:
        p: Noise probability
    """
    q = squin.qalloc(4)
    
    # Create GHZ state
    squin.h(q[0])
    squin.cx(q[0], q[1])
    squin.cx(q[1], q[2])
    squin.cx(q[2], q[3])
    
    # Apply noise to multiple qubits in parallel using broadcast
    squin.broadcast.depolarize(p, IList([q[0], q[1], q[2], q[3]]))
    
    # Measure all
    squin.broadcast.measure(IList([q[0], q[1], q[2], q[3]]))


@squin.kernel
def noise_at_different_locations(p: float = 0.1, location: int = 0):
    """
    Bell state with noise at different circuit locations
    
    Args:
        p: Noise probability
        location: 0=before H, 1=after H, 2=after CNOT
    """
    q = squin.qalloc(2)
    
    if location == 0:
        # Noise before state preparation
        squin.depolarize(p, q[0])
        squin.depolarize(p, q[1])
    
    squin.h(q[0])
    
    if location == 1:
        # Noise after Hadamard
        squin.depolarize(p, q[0])
    
    squin.cx(q[0], q[1])
    
    if location == 2:
        # Noise after CNOT
        squin.depolarize(p, q[0])
        squin.depolarize(p, q[1])
    
    squin.measure(q[0])
    squin.measure(q[1])


def analyze_noise_effect(samples, circuit_name: str, expected_ideal: dict = None):
    """
    Analyze the effect of noise on measurement outcomes
    Pure Bloqade implementation
    
    Args:
        samples: Measurement samples
        circuit_name: Name of the circuit
        expected_ideal: Expected ideal outcome probabilities
    """
    unique_outcomes = {}
    for sample in samples:
        outcome = ''.join(map(str, [int(x) for x in sample]))
        unique_outcomes[outcome] = unique_outcomes.get(outcome, 0) + 1
    
    print(f"\n{'='*60}")
    print(f"Noise Analysis: {circuit_name}")
    print(f"{'='*60}")
    print(f"Total shots: {len(samples)}")
    print(f"Unique outcomes: {len(unique_outcomes)}")
    
    print("\nOutcome probabilities:")
    sorted_outcomes = sorted(unique_outcomes.items(), key=lambda x: x[1], reverse=True)
    for outcome, count in sorted_outcomes:
        prob = count / len(samples)
        ideal_str = ""
        if expected_ideal and outcome in expected_ideal:
            ideal = expected_ideal[outcome]
            deviation = abs(prob - ideal)
            ideal_str = f" (ideal: {ideal:.3f}, deviation: {deviation:.3f})"
        print(f"  |{outcome}⟩: {count:4d} ({prob:.3f}){ideal_str}")
    
    # Calculate fidelity to ideal Bell state (for 2-qubit circuits)
    if len(samples[0]) == 2 and expected_ideal:
        ideal_fidelity = sum(unique_outcomes.get(k, 0) / len(samples) 
                            for k in expected_ideal.keys())
        print(f"\nFidelity to ideal state: {ideal_fidelity:.4f}")
        print(f"Error rate: {1 - ideal_fidelity:.4f}")


def compare_noise_levels():
    """Compare different noise levels on Bell state"""
    noise_levels = [0.0, 0.01, 0.05, 0.1, 0.2]
    shots = 10000
    
    print("\n" + "="*60)
    print("Comparing Noise Levels on Bell State")
    print("="*60)
    
    expected_ideal = {'00': 0.5, '11': 0.5}
    
    for p in noise_levels:
        @squin.kernel
        def bell_p():
            return bell_state_with_noise(p)
        
        stim_circ = bloqade.stim.Circuit(bell_p)
        sampler = stim_circ.compile_sampler()
        samples = sampler.sample(shots=shots)
        
        analyze_noise_effect(samples, f"p = {p}", expected_ideal)


def compare_noise_locations():
    """Compare effect of noise at different circuit locations"""
    p = 0.1
    shots = 10000
    locations = [
        (0, "Before state preparation"),
        (1, "After Hadamard"),
        (2, "After CNOT")
    ]
    
    print("\n" + "="*60)
    print("Comparing Noise Locations (p = 0.1)")
    print("="*60)
    
    expected_ideal = {'00': 0.5, '11': 0.5}
    
    for loc, desc in locations:
        @squin.kernel
        def bell_loc():
            return noise_at_different_locations(p, loc)
        
        stim_circ = bloqade.stim.Circuit(bell_loc)
        sampler = stim_circ.compile_sampler()
        samples = sampler.sample(shots=shots)
        
        analyze_noise_effect(samples, desc, expected_ideal)


def test_two_qubit_noise():
    """Test two-qubit depolarizing noise"""
    shots = 10000
    p1 = 0.01  # Single-qubit noise
    p2 = 0.05  # Two-qubit noise
    
    @squin.kernel
    def bell_2q():
        return bell_with_two_qubit_noise(p1, p2)
    
    stim_circ = bloqade.stim.Circuit(bell_2q)
    sampler = stim_circ.compile_sampler()
    samples = sampler.sample(shots=shots)
    
    expected_ideal = {'00': 0.5, '11': 0.5}
    analyze_noise_effect(
        samples, 
        f"Bell with 2-qubit noise (p1={p1}, p2={p2})", 
        expected_ideal
    )


def main():
    """Run all noise simulation examples"""
    print("="*60)
    print("Segment 1.2: Noise Simulation Basics")
    print("="*60)
    
    # Test 1: Compare noise levels
    compare_noise_levels()
    
    # Test 2: Compare noise locations
    compare_noise_locations()
    
    # Test 3: Two-qubit noise
    test_two_qubit_noise()
    
    # Test 4: Broadcast noise
    print("\n" + "="*60)
    print("Testing Broadcast Noise")
    print("="*60)
    
    @squin.kernel
    def ghz_broadcast():
        return broadcast_noise_demo(0.05)
    
    stim_circ = bloqade.stim.Circuit(ghz_broadcast)
    sampler = stim_circ.compile_sampler()
    samples = sampler.sample(shots=1000)
    
    print(f"\n4-qubit GHZ with broadcast noise (p=0.05)")
    print(f"First 10 samples:\n{samples[:10]}")
    
    # Count outcomes
    outcomes = {}
    for sample in samples:
        outcome = ''.join(map(str, sample.astype(int)))
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
    
    print(f"\nTop 5 outcomes:")
    for outcome, count in sorted(outcomes.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  |{outcome}⟩: {count:4d} ({count/1000:.3f})")
    
    print("\n" + "="*60)
    print("✓ Segment 1.2 Complete!")
    print("="*60)
    print("\nKey Takeaways:")
    print("1. squin.depolarize(p, q) adds single-qubit noise")
    print("2. squin.depolarize2(p, q1, q2) adds two-qubit noise")
    print("3. squin.broadcast operations apply noise in parallel")
    print("4. Noise location significantly affects outcome")
    print("5. Higher noise rates → more error outcomes")
    print("6. Stim efficiently simulates noisy Clifford circuits")


if __name__ == "__main__":
    main()
