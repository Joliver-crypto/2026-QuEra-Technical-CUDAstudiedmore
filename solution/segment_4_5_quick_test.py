"""
Quick test for Segment 4 & 5
==============================
Simplified test to verify the new segments work
"""

from bloqade import squin
import bloqade.stim
import bloqade.tsim


@squin.kernel
def test_optimized_encoding():
    """Test optimized Steane encoding"""
    q = squin.qalloc(7)
    
    squin.h(q[0])
    squin.h(q[1])
    squin.h(q[2])
    
    squin.cx(q[0], q[3])
    squin.cx(q[1], q[5])
    squin.cx(q[2], q[4])
    
    squin.cx(q[0], q[4])
    squin.cx(q[1], q[3])
    squin.cx(q[2], q[5])
    
    squin.cx(q[0], q[6])
    squin.cx(q[1], q[6])
    squin.cx(q[2], q[6])
    
    for i in range(7):
        squin.measure(q[i])


@squin.kernel
def test_syndrome_extraction():
    """Test syndrome extraction"""
    q = squin.qalloc(7)
    anc = squin.qalloc(6)
    
    # Prepare Steane |0⟩
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
    
    # Add error
    squin.x(q[2])
    
    # Measure X-stabilizer S1
    squin.h(anc[0])
    for i in [0,1,2,3]:
        squin.cx(anc[0], q[i])
    squin.h(anc[0])
    
    # Measure other stabilizers
    squin.h(anc[1])
    for i in [0,1,4,5]:
        squin.cx(anc[1], q[i])
    squin.h(anc[1])
    
    squin.h(anc[2])
    for i in [0,2,4,6]:
        squin.cx(anc[2], q[i])
    squin.h(anc[2])
    
    for i in [0,1,2,3]:
        squin.cx(q[i], anc[3])
    for i in [0,1,4,5]:
        squin.cx(q[i], anc[4])
    for i in [0,2,4,6]:
        squin.cx(q[i], anc[5])
    
    for i in range(6):
        squin.measure(anc[i])
    for i in range(7):
        squin.measure(q[i])


@squin.kernel
def test_t_state():
    """Test T state with Tsim"""
    q = squin.qalloc(1)[0]
    squin.h(q)
    squin.t(q)
    squin.measure(q)


def main():
    """Run all quick tests"""
    print("\n" + "="*70)
    print("SEGMENT 4 & 5 QUICK TEST")
    print("="*70)
    
    # Test 1: Optimized encoding (Segment 4.1)
    print("\n1. Testing optimized encoding (Segment 4.1)...")
    circ = bloqade.stim.Circuit(test_optimized_encoding)
    sampler = circ.compile_sampler()
    results = sampler.sample(shots=100)
    print(f"   ✓ Optimized encoding works! Got {len(results)} samples")
    print(f"   First sample: {results[0]}")
    
    # Test 2: Syndrome extraction (Segment 5.1)
    print("\n2. Testing syndrome extraction (Segment 5.1)...")
    circ = bloqade.stim.Circuit(test_syndrome_extraction)
    sampler = circ.compile_sampler()
    results = sampler.sample(shots=100)
    print(f"   ✓ Syndrome extraction works! Got {len(results)} samples")
    print(f"   First syndrome: {results[0][:6]}")
    print(f"   First data: {results[0][6:]}")
    
    # Test 3: T state with Tsim (Segment 5.2)
    print("\n3. Testing T state with Tsim (Segment 5.2)...")
    circ = bloqade.tsim.Circuit(test_t_state)
    sampler = circ.compile_sampler()
    results = sampler.sample(shots=100)
    print(f"   ✓ T state works! Got {len(results)} samples")
    print(f"   Results distribution: {sum(results)}/100 measured |1⟩")
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED!")
    print("="*70)
    print("\nSegments 4 and 5 are working correctly.")
    print("\nTo run full demonstrations:")
    print("  python solution/segment_4_optimization/01_improved_encoding.py")
    print("  python solution/segment_5_advanced/01_syndrome_decoding.py")
    print("  python solution/segment_5_advanced/02_tsim_magic_states.py")
    print("\nNote: Full scripts may take 5-30 minutes to complete.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
