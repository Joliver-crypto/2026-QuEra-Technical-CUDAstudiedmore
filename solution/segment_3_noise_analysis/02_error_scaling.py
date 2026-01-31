"""
Segment 3.2: Logical vs Physical Error Scaling
==============================================
Goal: Analyze logical error rate as a function of physical error rate

This demonstrates:
- Systematic sweep of physical error rates
- Logical error rate measurement
- Power law analysis
- Threshold behavior
- Pure Bloqade implementation (no external plotting libraries)
"""

from bloqade import squin
import bloqade.stim
from typing import List, Tuple


@squin.kernel
def steane_qec_round(data, physical_error: float = 0.01):
    """Single QEC round with physical errors"""
    # Physical errors on data qubits
    for i in range(7):
        squin.depolarize(physical_error, data[i])
    
    # Syndrome measurements (with noise on ancillas)
    # X-stabilizers
    anc_x1 = squin.qalloc(1)[0]
    squin.h(anc_x1)
    squin.depolarize(physical_error, anc_x1)
    squin.cx(anc_x1, data[0])
    squin.cx(anc_x1, data[1])
    squin.cx(anc_x1, data[2])
    squin.cx(anc_x1, data[3])
    squin.h(anc_x1)
    squin.measure(anc_x1)
    
    anc_x2 = squin.qalloc(1)[0]
    squin.h(anc_x2)
    squin.depolarize(physical_error, anc_x2)
    squin.cx(anc_x2, data[0])
    squin.cx(anc_x2, data[1])
    squin.cx(anc_x2, data[4])
    squin.cx(anc_x2, data[5])
    squin.h(anc_x2)
    squin.measure(anc_x2)
    
    anc_x3 = squin.qalloc(1)[0]
    squin.h(anc_x3)
    squin.depolarize(physical_error, anc_x3)
    squin.cx(anc_x3, data[0])
    squin.cx(anc_x3, data[2])
    squin.cx(anc_x3, data[4])
    squin.cx(anc_x3, data[6])
    squin.h(anc_x3)
    squin.measure(anc_x3)
    
    # Z-stabilizers
    anc_z1 = squin.qalloc(1)[0]
    squin.depolarize(physical_error, anc_z1)
    squin.cx(data[0], anc_z1)
    squin.cx(data[1], anc_z1)
    squin.cx(data[2], anc_z1)
    squin.cx(data[3], anc_z1)
    squin.measure(anc_z1)
    
    anc_z2 = squin.qalloc(1)[0]
    squin.depolarize(physical_error, anc_z2)
    squin.cx(data[0], anc_z2)
    squin.cx(data[1], anc_z2)
    squin.cx(data[4], anc_z2)
    squin.cx(data[5], anc_z2)
    squin.measure(anc_z2)
    
    anc_z3 = squin.qalloc(1)[0]
    squin.depolarize(physical_error, anc_z3)
    squin.cx(data[0], anc_z3)
    squin.cx(data[2], anc_z3)
    squin.cx(data[4], anc_z3)
    squin.cx(data[6], anc_z3)
    squin.measure(anc_z3)


@squin.kernel
def prepare_steane_zero():
    """Prepare Steane logical |0>"""
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
def memory_experiment(rounds: int = 3, physical_error: float = 0.01):
    """
    Memory experiment with multiple QEC rounds
    
    Args:
        rounds: Number of QEC cycles
        physical_error: Physical error rate
    """
    data = prepare_steane_zero()
    
    for _ in range(rounds):
        steane_qec_round(data, physical_error)
    
    # Final measurement
    for i in range(7):
        squin.measure(data[i])


def measure_logical_error_rate(physical_error: float, rounds: int = 3, shots: int = 5000) -> float:
    """
    Measure logical error rate for given physical error rate
    
    Returns:
        Logical error rate (fraction of incorrect logical outcomes)
    """
    @squin.kernel
    def mem_exp():
        return memory_experiment(rounds, physical_error)
    
    stim_circ = bloqade.stim.Circuit(mem_exp)
    sampler = stim_circ.compile_sampler()
    samples = sampler.sample(shots=shots)
    
    # Extract final measurements (last 7 measurements)
    syndromes_per_round = 6
    syndrome_offset = rounds * syndromes_per_round
    final_data = samples[:, syndrome_offset:]
    
    # Count valid Steane |0> codewords
    steane_zero_codewords = {
        '0000000', '1010101', '0110011', '1100110',
        '0001111', '1011010', '0111100', '1101001'
    }
    
    valid_count = 0
    for data in final_data:
        outcome = ''.join(map(str, data.astype(int)))
        if outcome in steane_zero_codewords:
            valid_count += 1
    
    logical_fidelity = valid_count / shots
    logical_error_rate = 1 - logical_fidelity
    
    return logical_error_rate


def sweep_physical_errors() -> Tuple[List[float], List[float]]:
    """
    Sweep physical error rates and measure logical error rates
    
    Returns:
        (physical_errors, logical_errors) tuple
    """
    print("\n" + "="*60)
    print("Sweeping Physical Error Rates")
    print("="*60)
    
    # Physical error rates to test
    physical_errors = [0.001, 0.002, 0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1]
    logical_errors = []
    
    rounds = 3
    shots = 3000
    
    for p_err in physical_errors:
        print(f"\nPhysical error: {p_err:.3f}")
        l_err = measure_logical_error_rate(p_err, rounds, shots)
        logical_errors.append(l_err)
        print(f"  Logical error: {l_err:.4f}")
        print(f"  Ratio (L/P): {l_err/p_err:.2f}")
    
    return physical_errors, logical_errors


def plot_error_scaling(physical_errors: List[float], logical_errors: List[float]):
    """
    Analyze and display logical vs physical error rates
    Pure Bloqade implementation - results printed to console
    """
    print("\n" + "="*60)
    print("Error Scaling Analysis")
    print("="*60)
    
    # Display data table
    print("\n{:<15} {:<15} {:<15}".format("Physical (P)", "Logical (L)", "Ratio (L/P)"))
    print("-" * 60)
    for p, l in zip(physical_errors, logical_errors):
        ratio = l / p if p > 0 else 0
        print("{:<15.4f} {:<15.4f} {:<15.2f}".format(p, l, ratio))
    
    # Power law fit using log-linear regression
    # L = a * P^b  =>  log(L) = log(a) + b*log(P)
    log_p = [_log(p) for p in physical_errors]
    log_l = [_log(l) for l in logical_errors]
    
    # Simple linear regression: y = mx + c
    n = len(log_p)
    mean_x = sum(log_p) / n
    mean_y = sum(log_l) / n
    
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_p, log_l))
    denominator = sum((x - mean_x) ** 2 for x in log_p)
    
    power = numerator / denominator if denominator != 0 else 1.0
    log_a = mean_y - power * mean_x
    a = _exp(log_a)
    
    print("\n" + "="*60)
    print("Power Law Analysis")
    print("="*60)
    print("Fitted model: L = {:.4f} * P^{:.3f}".format(a, power))
    
    print("\nInterpretation:")
    if power < 1:
        print("  • Power < 1: QEC provides benefit (suppresses errors)")
        print("  • Error suppression factor: P^{:.2f} < P".format(power))
    elif power == 1:
        print("  • Power = 1: No QEC benefit (L = aP)")
    else:
        print("  • Power > 1: QEC amplifies errors (not working)")
    
    # Threshold analysis
    print("\n" + "="*60)
    print("Threshold Analysis")
    print("="*60)
    print("Points where L < P (QEC helps):")
    for p, l in zip(physical_errors, logical_errors):
        if l < p:
            ratio = l / p
            print("  P={:.3f}: L={:.4f}, ratio={:.3f} ✓".format(p, l, ratio))
    
    print("\nPoints where L > P (QEC hurts):")
    for p, l in zip(physical_errors, logical_errors):
        if l > p:
            ratio = l / p
            print("  P={:.3f}: L={:.4f}, ratio={:.3f} ✗".format(p, l, ratio))
    
    print("\n" + "="*60)
    print("Results Summary")
    print("="*60)
    print("Power law exponent (β): {:.3f}".format(power))
    print("Coefficient (a): {:.4f}".format(a))
    
    below_threshold = sum(1 for p, l in zip(physical_errors, logical_errors) if l < p)
    print("Points below threshold: {}/{}".format(below_threshold, len(physical_errors)))


def _log(x):
    """Natural logarithm (pure Python)"""
    import math
    return math.log(x)


def _exp(x):
    """Exponential function (pure Python)"""
    import math
    return math.exp(x)


def compare_different_rounds():
    """Compare error scaling for different numbers of QEC rounds"""
    print("\n" + "="*60)
    print("Comparing Different QEC Round Counts")
    print("="*60)
    
    physical_errors = [0.005, 0.01, 0.02, 0.05]
    round_counts = [1, 3, 5]
    shots = 2000
    
    results = {}
    
    for rounds in round_counts:
        print(f"\n--- {rounds} QEC rounds ---")
        logical_errors = []
        for p_err in physical_errors:
            l_err = measure_logical_error_rate(p_err, rounds, shots)
            logical_errors.append(l_err)
            print(f"P={p_err:.3f}: L={l_err:.4f}")
        results[rounds] = logical_errors
    
    # Create comparison table
    print("\n" + "="*60)
    print("Comparison Table: Logical Error vs Physical Error")
    print("="*60)
    print("\n{:<12} {}".format("Physical", " | ".join([f"{r} rounds" for r in round_counts])))
    print("-" * 60)
    for i, p_err in enumerate(physical_errors):
        values = " | ".join([f"{results[r][i]:.4f}" for r in round_counts])
        print(f"{p_err:<12.3f} {values}")
    
    print("\nObservation: More rounds typically means more opportunities for errors")
    print("to accumulate, leading to higher logical error rates in this regime.")


def main():
    """Run all error scaling experiments"""
    print("="*60)
    print("Segment 3.2: Logical vs Physical Error Scaling")
    print("="*60)
    
    # Main experiment: sweep physical errors
    physical_errors, logical_errors = sweep_physical_errors()
    
    # Create plots and analysis
    plot_error_scaling(physical_errors, logical_errors)
    
    # Compare different round counts
    compare_different_rounds()
    
    print("\n" + "="*60)
    print("✓ Segment 3.2 Complete!")
    print("="*60)
    print("\nKey Achievements:")
    print("  ✓ Systematic error rate sweep")
    print("  ✓ Power law analysis (pure Bloqade)")
    print("  ✓ Threshold identification")
    print("  ✓ Console-based visualization")
    print("  ✓ Comparison across QEC rounds")
    print("\nResults displayed in console (no external plotting libraries)")


if __name__ == "__main__":
    main()
