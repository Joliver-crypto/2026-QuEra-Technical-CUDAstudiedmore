"""
Segment 3.1: Heuristic Noise Models with Cirq
=============================================
Goal: Export Squin circuits to Cirq and apply QuEra's heuristic noise models

This demonstrates:
- Squin to Cirq conversion
- GeminiOneZone noise model
- Comparison of different noise channels (moves, gates, etc.)
- Effect of noise model parameters
"""

from bloqade import squin
from bloqade.cirq_utils import noise
from bloqade.cirq_utils.emit import emit_circuit
from bloqade.cirq_utils import load_circuit
import bloqade.stim
import bloqade.tsim
import numpy as np


@squin.kernel
def simple_bell_state():
    """Simple Bell state for noise analysis"""
    q = squin.qalloc(2)
    squin.h(q[0])
    squin.cx(q[0], q[1])
    squin.measure(q[0])
    squin.measure(q[1])


@squin.kernel
def steane_logical_zero_for_noise():
    """Steane logical |0> for noise analysis"""
    q = squin.qalloc(7)
    squin.h(q[0])
    squin.h(q[1])
    squin.h(q[2])
    
    squin.cx(q[0], q[3])
    squin.cx(q[1], q[3])
    squin.cx(q[0], q[4])
    squin.cx(q[2], q[4])
    squin.cx(q[1], q[5])
    squin.cx(q[2], q[5])
    squin.cx(q[0], q[6])
    squin.cx(q[1], q[6])
    squin.cx(q[2], q[6])
    
    for i in range(7):
        squin.measure(q[i])


def apply_heuristic_noise(kernel_func, noise_scale: float = 1.0):
    """
    Apply QuEra's heuristic noise model to a circuit
    
    Args:
        kernel_func: Squin kernel function
        noise_scale: Scaling factor for all noise parameters
    
    Returns:
        Noisy Squin circuit
    """
    # Convert to Cirq
    cirq_circuit = emit_circuit(kernel_func)
    
    # Define noise model (GeminiOneZone is QuEra's default architecture)
    noise_model = noise.GeminiOneZoneNoiseModel(scaling_factor=noise_scale)
    
    # Apply noise to circuit
    noisy_cirq = noise.transform_circuit(cirq_circuit, model=noise_model)
    
    # Convert back to Squin
    noisy_squin = load_circuit(noisy_cirq)
    
    return noisy_squin


def compare_noise_models():
    """Compare different noise model configurations"""
    print("\n" + "="*60)
    print("Comparing Noise Model Configurations")
    print("="*60)
    
    scaling_factors = [0.5, 1.0, 2.0, 5.0]
    shots = 5000
    
    results = []
    
    for scale in scaling_factors:
        print(f"\n--- Noise scaling factor: {scale} ---")
        
        # Apply heuristic noise
        noisy_circuit = apply_heuristic_noise(simple_bell_state, scale)
        
        # Simulate with Stim
        stim_circ = bloqade.stim.Circuit(noisy_circuit)
        sampler = stim_circ.compile_sampler()
        samples = sampler.sample(shots=shots)
        
        # Analyze Bell state fidelity
        outcomes = {}
        for sample in samples:
            outcome = ''.join(map(str, sample.astype(int)))
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
        
        # Bell state should have |00> and |11>
        ideal_count = outcomes.get('00', 0) + outcomes.get('11', 0)
        fidelity = ideal_count / shots
        
        print(f"Outcomes:")
        for outcome, count in sorted(outcomes.items(), key=lambda x: x[1], reverse=True)[:4]:
            print(f"  |{outcome}>: {count:4d} ({count/shots:.3f})")
        
        print(f"Bell state fidelity: {fidelity:.3f}")
        results.append((scale, fidelity))
    
    # Summary
    print("\n" + "="*60)
    print("Summary: Fidelity vs Noise Scaling")
    print("="*60)
    for scale, fidelity in results:
        print(f"  Scale {scale:.1f}: Fidelity {fidelity:.3f}")
    
    return results


def analyze_steane_with_heuristic_noise():
    """Analyze Steane code with heuristic noise"""
    print("\n" + "="*60)
    print("Steane Code with Heuristic Noise")
    print("="*60)
    
    scaling_factors = [0.5, 1.0, 2.0]
    shots = 5000
    
    steane_zero_codewords = {
        '0000000', '1010101', '0110011', '1100110',
        '0001111', '1011010', '0111100', '1101001'
    }
    
    results = []
    
    for scale in scaling_factors:
        print(f"\n--- Noise scaling: {scale} ---")
        
        noisy_circuit = apply_heuristic_noise(steane_logical_zero_for_noise, scale)
        
        stim_circ = bloqade.stim.Circuit(noisy_circuit)
        sampler = stim_circ.compile_sampler()
        samples = sampler.sample(shots=shots)
        
        # Count valid codewords
        valid_count = 0
        outcomes = {}
        for sample in samples:
            outcome = ''.join(map(str, sample.astype(int)))
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
            if outcome in steane_zero_codewords:
                valid_count += 1
        
        fidelity = valid_count / shots
        
        print(f"Valid codewords: {valid_count}/{shots} ({fidelity:.3f})")
        print(f"Top 5 outcomes:")
        for outcome, count in sorted(outcomes.items(), key=lambda x: x[1], reverse=True)[:5]:
            is_valid = "✓" if outcome in steane_zero_codewords else "✗"
            print(f"  {is_valid} |{outcome}>: {count:4d} ({count/shots:.3f})")
        
        results.append((scale, fidelity))
    
    print("\n" + "="*60)
    print("Summary: Steane Fidelity vs Noise")
    print("="*60)
    for scale, fidelity in results:
        print(f"  Scale {scale:.1f}: Fidelity {fidelity:.3f}")
    
    return results


def manual_vs_heuristic_noise():
    """
    Compare manual noise insertion vs heuristic noise model
    """
    print("\n" + "="*60)
    print("Manual vs Heuristic Noise Comparison")
    print("="*60)
    
    shots = 5000
    
    # Test 1: Manual depolarizing noise
    print("\n--- Manual Depolarizing Noise (p=0.01) ---")
    
    @squin.kernel
    def bell_manual_noise():
        q = squin.qalloc(2)
        squin.h(q[0])
        squin.depolarize(0.01, q[0])
        squin.cx(q[0], q[1])
        squin.depolarize2(0.02, q[0], q[1])
        squin.depolarize(0.01, q[0])
        squin.depolarize(0.01, q[1])
        squin.measure(q[0])
        squin.measure(q[1])
    
    stim_circ = bloqade.stim.Circuit(bell_manual_noise)
    sampler = stim_circ.compile_sampler()
    samples = sampler.sample(shots=shots)
    
    outcomes_manual = {}
    for sample in samples:
        outcome = ''.join(map(str, sample.astype(int)))
        outcomes_manual[outcome] = outcomes_manual.get(outcome, 0) + 1
    
    fidelity_manual = (outcomes_manual.get('00', 0) + outcomes_manual.get('11', 0)) / shots
    print(f"Bell fidelity (manual): {fidelity_manual:.3f}")
    
    # Test 2: Heuristic noise model
    print("\n--- Heuristic Noise Model (scale=1.0) ---")
    
    noisy_heuristic = apply_heuristic_noise(simple_bell_state, 1.0)
    stim_circ = bloqade.stim.Circuit(noisy_heuristic)
    sampler = stim_circ.compile_sampler()
    samples = sampler.sample(shots=shots)
    
    outcomes_heuristic = {}
    for sample in samples:
        outcome = ''.join(map(str, sample.astype(int)))
        outcomes_heuristic[outcome] = outcomes_heuristic.get(outcome, 0) + 1
    
    fidelity_heuristic = (outcomes_heuristic.get('00', 0) + outcomes_heuristic.get('11', 0)) / shots
    print(f"Bell fidelity (heuristic): {fidelity_heuristic:.3f}")
    
    print("\n" + "="*60)
    print("Comparison Summary")
    print("="*60)
    print(f"  Manual noise:     {fidelity_manual:.3f}")
    print(f"  Heuristic noise:  {fidelity_heuristic:.3f}")
    print(f"  Difference:       {abs(fidelity_manual - fidelity_heuristic):.3f}")


def create_noise_analysis_summary():
    """Create summary of noise channel effects"""
    print("\n" + "="*60)
    print("Noise Channel Effects Summary")
    print("="*60)
    
    print("\nQuEra's GeminiOneZone Noise Model includes:")
    print("  1. Single-qubit gate errors")
    print("  2. Two-qubit gate errors (typically higher)")
    print("  3. Measurement errors")
    print("  4. Idle/decoherence errors")
    print("  5. Atom shuttling errors (for moves)")
    
    print("\nKey insights from experiments:")
    print("  • Higher noise scaling → lower fidelity")
    print("  • Two-qubit gates more sensitive to noise")
    print("  • Heuristic models capture hardware-specific effects")
    print("  • Can tune noise model with scaling_factor parameter")
    
    print("\nNoise hierarchy (typical):")
    print("  Lowest:  Single-qubit Clifford gates")
    print("  Medium:  Measurements")
    print("  High:    Two-qubit gates")
    print("  Highest: Long-distance atom shuttling")


def main():
    """Run all heuristic noise model experiments"""
    print("="*60)
    print("Segment 3.1: Heuristic Noise Models with Cirq")
    print("="*60)
    
    # Test 1: Compare noise scaling factors
    bell_results = compare_noise_models()
    
    # Test 2: Steane code with heuristic noise
    steane_results = analyze_steane_with_heuristic_noise()
    
    # Test 3: Manual vs heuristic comparison
    manual_vs_heuristic_noise()
    
    # Summary
    create_noise_analysis_summary()
    
    print("\n" + "="*60)
    print("✓ Segment 3.1 Complete!")
    print("="*60)
    print("\nKey Achievements:")
    print("  ✓ Squin → Cirq → Squin conversion pipeline")
    print("  ✓ GeminiOneZone heuristic noise model")
    print("  ✓ Noise scaling analysis")
    print("  ✓ Comparison with manual noise insertion")
    print("\nNext: Segment 3.2 - Logical vs Physical Error Scaling")


if __name__ == "__main__":
    main()
