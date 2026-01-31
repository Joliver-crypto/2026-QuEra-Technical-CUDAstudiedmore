"""
MAIN SOLUTION RUNNER
====================
Run all implemented segments of the iQuHACK 2026 QuEra Challenge

This script provides an easy way to execute all segments and see results.
"""

import subprocess
import sys
from pathlib import Path

# Define all segments
SEGMENTS = {
    "Phase 1: Foundation": [
        ("1.1", "Basic Bloqade", "solution/segment_1_foundation/01_basic_bloqade.py"),
        ("1.2", "Noise Simulation", "solution/segment_1_foundation/02_noise_simulation.py"),
        ("1.3", "Parallelism", "solution/segment_1_foundation/03_parallelism.py"),
    ],
    "Phase 2: Core QEC": [
        ("2.1", "MSD Encoding", "solution/segment_2_core_qec/01_msd_encoding.py"),
        ("2.2", "Syndrome Extraction", "solution/segment_2_core_qec/02_syndrome_extraction.py"),
        ("2.3", "Multi-Round QEC", "solution/segment_2_core_qec/03_multi_round_qec.py"),
    ],
    "Phase 3: Noise Analysis": [
        ("3.1", "Heuristic Noise", "solution/segment_3_noise_analysis/01_heuristic_noise.py"),
        ("3.2", "Error Scaling", "solution/segment_3_noise_analysis/02_error_scaling.py"),
    ],
}


def run_segment(script_path: str, segment_id: str, segment_name: str):
    """Run a single segment script"""
    print("\n" + "="*70)
    print(f"RUNNING SEGMENT {segment_id}: {segment_name}")
    print("="*70)
    
    try:
        result = subprocess.run(
            ["uv", "run", "python", script_path],
            capture_output=False,
            text=True,
            check=True
        )
        print(f"\n✓ Segment {segment_id} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Segment {segment_id} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n✗ Segment {segment_id} failed: {e}")
        return False


def main():
    """Run all segments"""
    print("="*70)
    print("iQuHACK 2026 QuEra Challenge - Solution Runner")
    print("="*70)
    
    # Check we're in the right directory
    if not Path("solution").exists():
        print("Error: Must run from project root directory")
        sys.exit(1)
    
    all_results = {}
    
    for phase, segments in SEGMENTS.items():
        print(f"\n\n{'#'*70}")
        print(f"# {phase}")
        print(f"{'#'*70}")
        
        phase_results = []
        for segment_id, segment_name, script_path in segments:
            if not Path(script_path).exists():
                print(f"\n⚠ Segment {segment_id} not found: {script_path}")
                phase_results.append(False)
                continue
            
            success = run_segment(script_path, segment_id, segment_name)
            phase_results.append(success)
        
        all_results[phase] = phase_results
    
    # Summary
    print("\n\n" + "="*70)
    print("EXECUTION SUMMARY")
    print("="*70)
    
    total_segments = 0
    total_passed = 0
    
    for phase, segments in SEGMENTS.items():
        results = all_results[phase]
        passed = sum(results)
        total = len(results)
        total_segments += total
        total_passed += passed
        
        print(f"\n{phase}: {passed}/{total} passed")
        for (seg_id, seg_name, _), success in zip(segments, results):
            status = "✓" if success else "✗"
            print(f"  {status} Segment {seg_id}: {seg_name}")
    
    print(f"\n{'='*70}")
    print(f"OVERALL: {total_passed}/{total_segments} segments passed")
    print(f"{'='*70}")
    
    if total_passed == total_segments:
        print("\n🎉 All segments completed successfully!")
        return 0
    else:
        print(f"\n⚠ {total_segments - total_passed} segment(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
