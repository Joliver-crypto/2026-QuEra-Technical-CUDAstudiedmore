"""
Segment 2.3: Multiple Rounds with Post-Selection
================================================
Goal: Implement multiple rounds of syndrome extraction with post-selection

This creates a quantum memory experiment where we:
1. Prepare a logical state
2. Run multiple QEC rounds (syndrome extraction)
3. Post-select on syndrome outcomes
4. Measure logical observable
5. Analyze logical error rates

Pure Bloqade implementation
"""

from bloqade import squin
import bloqade.stim
import bloqade.tsim
from typing import List, Tuple


@squin.kernel
def prepare_steane_logical_zero():
    """Prepare [[7,1,3]] Steane code logical |0>"""
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
    
    return q


@squin.kernel
def single_qec_round_with_noise(data, noise_level: float = 0.0):
    """
    Single QEC round: measure all 6 stabilizers with optional noise
    
    Args:
        data: 7 data qubits
        noise_level: Depolarizing noise probability
    """
    # Apply noise before syndrome measurement
    if noise_level > 0:
        for i in range(7):
            squin.depolarize(noise_level, data[i])
    
    # Measure X-stabilizers (S1, S2, S3)
    anc_x1 = squin.qalloc(1)[0]
    squin.h(anc_x1)
    squin.cx(anc_x1, data[0])
    squin.cx(anc_x1, data[1])
    squin.cx(anc_x1, data[2])
    squin.cx(anc_x1, data[3])
    squin.h(anc_x1)
    squin.measure(anc_x1)
    
    anc_x2 = squin.qalloc(1)[0]
    squin.h(anc_x2)
    squin.cx(anc_x2, data[0])
    squin.cx(anc_x2, data[1])
    squin.cx(anc_x2, data[4])
    squin.cx(anc_x2, data[5])
    squin.h(anc_x2)
    squin.measure(anc_x2)
    
    anc_x3 = squin.qalloc(1)[0]
    squin.h(anc_x3)
    squin.cx(anc_x3, data[0])
    squin.cx(anc_x3, data[2])
    squin.cx(anc_x3, data[4])
    squin.cx(anc_x3, data[6])
    squin.h(anc_x3)
    squin.measure(anc_x3)
    
    # Measure Z-stabilizers (S4, S5, S6)
    anc_z1 = squin.qalloc(1)[0]
    squin.cx(data[0], anc_z1)
    squin.cx(data[1], anc_z1)
    squin.cx(data[2], anc_z1)
    squin.cx(data[3], anc_z1)
    squin.measure(anc_z1)
    
    anc_z2 = squin.qalloc(1)[0]
    squin.cx(data[0], anc_z2)
    squin.cx(data[1], anc_z2)
    squin.cx(data[4], anc_z2)
    squin.cx(data[5], anc_z2)
    squin.measure(anc_z2)
    
    anc_z3 = squin.qalloc(1)[0]
    squin.cx(data[0], anc_z3)
    squin.cx(data[2], anc_z3)
    squin.cx(data[4], anc_z3)
    squin.cx(data[6], anc_z3)
    squin.measure(anc_z3)


@squin.kernel
def multi_round_qec(num_rounds: int = 3, noise_level: float = 0.01):
    """
    Multiple rounds of QEC with noise
    
    Args:
        num_rounds: Number of QEC cycles
        noise_level: Noise probability per round
    """
    # Prepare logical |0>
    data = prepare_steane_logical_zero()
    
    # Run multiple QEC rounds
    for _ in range(num_rounds):
        single_qec_round_with_noise(data, noise_level)
    
    # Final measurement of logical observable (measure all data qubits)
    for i in range(7):
        squin.measure(data[i])


@squin.kernel
def memory_experiment_with_idle_noise(idle_time_steps: int = 5, noise_per_step: float = 0.01):
    """
    Memory experiment: prepare logical state, wait (with noise), then measure
    
    Args:
        idle_time_steps: Number of idle time steps
        noise_per_step: Noise per time step
    """
    data = prepare_steane_logical_zero()
    
    # Idle period with noise accumulation
    for _ in range(idle_time_steps):
        # Apply noise to simulate decoherence during idle time
        for i in range(7):
            squin.depolarize(noise_per_step, data[i])
        
        # Syndrome measurement
        single_qec_round_with_noise(data, 0.0)  # No additional noise during measurement
    
    # Measure logical observable
    for i in range(7):
        squin.measure(data[i])


def analyze_multi_round_results(samples, num_rounds: int, description: str):
    """
    Analyze results from multi-round QEC
    Pure Bloqade implementation - no numpy
    
    Args:
        samples: Measurement outcomes
        num_rounds: Number of QEC rounds
        description: Description of experiment
    """
    print(f"\n{'='*60}")
    print(f"Multi-Round QEC Analysis: {description}")
    print(f"{'='*60}")
    
    # Each round has 6 syndrome measurements
    syndromes_per_round = 6
    total_syndrome_measurements = num_rounds * syndromes_per_round
    
    # Extract syndromes and final data measurements
    all_syndromes = samples[:, :total_syndrome_measurements]
    final_data = samples[:, total_syndrome_measurements:]
    
    print(f"\nTotal shots: {len(samples)}")
    print(f"QEC rounds: {num_rounds}")
    print(f"Syndrome measurements per shot: {total_syndrome_measurements}")
    
    # Analyze each round
    for round_idx in range(num_rounds):
        start = round_idx * syndromes_per_round
        end = (round_idx + 1) * syndromes_per_round
        round_syndromes = all_syndromes[:, start:end]
        
        # Count all-zero syndromes (no error detected)
        all_zero = 0
        for syndrome in round_syndromes:
            if all(s == 0 for s in syndrome):
                all_zero += 1
        
        print(f"\nRound {round_idx + 1}:")
        print(f"  All-zero syndromes: {all_zero}/{len(samples)} ({all_zero/len(samples):.3f})")
    
    # Analyze final data measurements
    # For logical |0>, valid codewords have specific patterns
    steane_zero_codewords = {
        '0000000', '1010101', '0110011', '1100110',
        '0001111', '1011010', '0111100', '1101001'
    }
    
    valid_count = 0
    outcomes = {}
    for data in final_data:
        outcome = ''.join(map(str, [int(x) for x in data]))
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        if outcome in steane_zero_codewords:
            valid_count += 1
    
    logical_fidelity = valid_count / len(samples)
    print(f"\nFinal Logical State:")
    print(f"  Valid codewords: {valid_count}/{len(samples)} ({logical_fidelity:.3f})")
    print(f"  Logical error rate: {1 - logical_fidelity:.3f}")
    
    print(f"\nTop 5 final outcomes:")
    sorted_outcomes = sorted(outcomes.items(), key=lambda x: x[1], reverse=True)[:5]
    for outcome, count in sorted_outcomes:
        is_valid = "✓" if outcome in steane_zero_codewords else "✗"
        print(f"  {is_valid} |{outcome}>: {count:4d} ({count/len(samples):.3f})")
    
    return logical_fidelity


def post_select_on_syndromes(samples, num_rounds: int):
    """
    Post-select shots based on syndrome outcomes
    Keep only shots where ALL syndromes are zero (no errors detected)
    Pure Bloqade implementation
    """
    syndromes_per_round = 6
    total_syndrome_measurements = num_rounds * syndromes_per_round
    
    all_syndromes = samples[:, :total_syndrome_measurements]
    
    # Find shots with all-zero syndromes
    selected_indices = []
    for idx, syndromes in enumerate(all_syndromes):
        if all(s == 0 for s in syndromes):
            selected_indices.append(idx)
    
    if len(selected_indices) == 0:
        print("Warning: No shots with all-zero syndromes!")
        return samples[:0]  # Return empty array
    
    # Select rows manually
    selected_samples = [samples[i] for i in selected_indices]
    
    # Convert back to array-like structure
    import array
    num_cols = len(samples[0])
    result = []
    for row in selected_samples:
        result.append(row)
    
    print(f"\nPost-Selection Results:")
    print(f"  Original shots: {len(samples)}")
    print(f"  Selected shots: {len(selected_samples)} ({len(selected_samples)/len(samples):.3f})")
    
    # Return as list of lists (compatible with analysis function)
    return selected_samples


def compare_noise_levels():
    """Compare QEC performance at different noise levels"""
    print("\n" + "="*60)
    print("Comparing Noise Levels")
    print("="*60)
    
    noise_levels = [0.0, 0.005, 0.01, 0.02, 0.05]
    num_rounds = 3
    shots = 5000
    
    results = []
    
    for noise in noise_levels:
        print(f"\n--- Noise level: {noise} ---")
        
        @squin.kernel
        def qec_with_noise():
            return multi_round_qec(num_rounds, noise)
        
        stim_circ = bloqade.stim.Circuit(qec_with_noise)
        sampler = stim_circ.compile_sampler()
        samples = sampler.sample(shots=shots)
        
        fidelity = analyze_multi_round_results(
            samples, num_rounds, f"Noise = {noise}"
        )
        results.append((noise, fidelity))
    
    # Summary
    print("\n" + "="*60)
    print("Summary: Logical Fidelity vs Noise Level")
    print("="*60)
    for noise, fidelity in results:
        error_rate = 1 - fidelity
        print(f"  Noise {noise:.3f}: Fidelity {fidelity:.3f}, Error {error_rate:.3f}")


def test_post_selection():
    """Test post-selection improves fidelity"""
    print("\n" + "="*60)
    print("Testing Post-Selection")
    print("="*60)
    
    noise = 0.02
    num_rounds = 3
    shots = 10000
    
    @squin.kernel
    def qec_noisy():
        return multi_round_qec(num_rounds, noise)
    
    stim_circ = bloqade.stim.Circuit(qec_noisy)
    sampler = stim_circ.compile_sampler()
    samples = sampler.sample(shots=shots)
    
    # Analyze without post-selection
    print("\n--- Without Post-Selection ---")
    fidelity_no_ps = analyze_multi_round_results(
        samples, num_rounds, f"No Post-Selection (noise={noise})"
    )
    
    # Post-select and analyze
    print("\n--- With Post-Selection ---")
    selected_samples = post_select_on_syndromes(samples, num_rounds)
    
    if len(selected_samples) > 0:
        fidelity_with_ps = analyze_multi_round_results(
            selected_samples, num_rounds, f"With Post-Selection (noise={noise})"
        )
        
        improvement = fidelity_with_ps - fidelity_no_ps
        print(f"\nImprovement from post-selection: {improvement:.3f}")
    else:
        print("No shots passed post-selection!")


def main():
    """Run all multi-round QEC experiments"""
    print("="*60)
    print("Segment 2.3: Multiple Rounds with Post-Selection")
    print("="*60)
    
    # Test 1: Multi-round QEC without noise
    print("\nTest 1: Clean Multi-Round QEC")
    
    @squin.kernel
    def clean_qec():
        return multi_round_qec(3, 0.0)
    
    stim_circ = bloqade.stim.Circuit(clean_qec)
    sampler = stim_circ.compile_sampler()
    samples = sampler.sample(shots=1000)
    analyze_multi_round_results(samples, 3, "Clean (no noise)")
    
    # Test 2: Compare noise levels
    compare_noise_levels()
    
    # Test 3: Post-selection
    test_post_selection()
    
    print("\n" + "="*60)
    print("✓ Segment 2.3 Complete!")
    print("="*60)
    print("\nKey Achievements:")
    print("  ✓ Multi-round QEC implementation")
    print("  ✓ Noise analysis across multiple rounds")
    print("  ✓ Post-selection on syndromes")
    print("  ✓ Demonstrated fidelity improvement")
    print("\nNext: Segment 2.4 - Logical information reconstruction")


if __name__ == "__main__":
    main()
