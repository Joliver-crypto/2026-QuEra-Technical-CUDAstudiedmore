#!/usr/bin/env python3
"""
Quick Test Script
=================
Quickly verify all segments are working
"""

from bloqade import squin
import bloqade.stim
import sys

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    try:
        import bloqade
        import bloqade.stim
        import bloqade.tsim
        from bloqade.cirq_utils import noise
        import numpy as np
        import matplotlib.pyplot as plt
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_basic_circuit():
    """Test basic Bloqade circuit"""
    print("\nTesting basic circuit...")
    try:
        @squin.kernel
        def test():
            q = squin.qalloc(2)
            squin.h(q[0])
            squin.cx(q[0], q[1])
            squin.measure(q[0])
            squin.measure(q[1])
        
        stim_circ = bloqade.stim.Circuit(test)
        sampler = stim_circ.compile_sampler()
        samples = sampler.sample(shots=100)
        
        if len(samples) == 100 and samples.shape[1] == 2:
            print("✓ Basic circuit working")
            return True
        else:
            print("✗ Unexpected sample shape")
            return False
    except Exception as e:
        print(f"✗ Circuit test failed: {e}")
        return False


def test_noise():
    """Test noise simulation"""
    print("\nTesting noise simulation...")
    try:
        @squin.kernel
        def test_noisy():
            q = squin.qalloc(1)
            squin.h(q[0])
            squin.depolarize(0.1, q[0])
            squin.measure(q[0])
        
        stim_circ = bloqade.stim.Circuit(test_noisy)
        sampler = stim_circ.compile_sampler()
        samples = sampler.sample(shots=100)
        
        print("✓ Noise simulation working")
        return True
    except Exception as e:
        print(f"✗ Noise test failed: {e}")
        return False


def test_steane_encoding():
    """Test Steane encoding"""
    print("\nTesting Steane encoding...")
    try:
        @squin.kernel
        def steane():
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
        
        stim_circ = bloqade.stim.Circuit(steane)
        sampler = stim_circ.compile_sampler()
        samples = sampler.sample(shots=100)
        
        if samples.shape[1] == 7:
            print("✓ Steane encoding working")
            return True
        else:
            print("✗ Unexpected sample shape")
            return False
    except Exception as e:
        print(f"✗ Steane test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("iQuHACK 2026 QuEra Challenge - Quick Test")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Basic Circuit", test_basic_circuit),
        ("Noise Simulation", test_noise),
        ("Steane Encoding", test_steane_encoding),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to run full solution.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Check your environment.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
