# iQuHACK 2026 QuEra Challenge Solution

## Project Structure

```
solution/
├── segment_1_foundation/
│   ├── 01_basic_bloqade.py          - Bloqade basics, gates, sampling
│   ├── 02_noise_simulation.py       - Noise channels and analysis
│   └── 03_parallelism.py            - Circuit parallelism optimization
├── segment_2_core_qec/
│   ├── 01_msd_encoding.py           - MSD state injection + Steane encoding
│   ├── 02_syndrome_extraction.py    - Syndrome measurement for all stabilizers
│   └── 03_multi_round_qec.py        - Multi-round QEC with post-selection
├── segment_3_noise_analysis/
│   ├── 01_heuristic_noise.py        - Hardware noise models via Cirq
│   └── 02_error_scaling.py          - Logical vs physical error analysis
├── segment_4_optimization/
│   ├── 01_improved_encoding.py      - Non-magic encodings + flagging
│   └── 02_noise_comparison.py       - Comprehensive noise model comparison
├── segment_5_advanced/
│   ├── 01_syndrome_decoding.py      - Decoding + correction feedforward
│   └── 02_tsim_magic_states.py      - T-state memory with Tsim
├── segment_4_5_quick_test.py        - Quick validation for segments 4 & 5
├── quick_test.py                     - Fast validation for segments 1-3
└── run_all.py                        - Master runner for all segments
```

## Progress

### ✅ Phase 1: Foundation (Complete)
- [x] Segment 1.1: Basic Bloqade setup with Squin kernels
- [x] Segment 1.2: Noise simulation with depolarizing channels
- [x] Segment 1.3: Circuit parallelism exploration

### ✅ Phase 2: Core QEC (Complete)
- [x] Segment 2.1: MSD state encoding circuit
- [x] Segment 2.2: Steane QEC syndrome extraction
- [x] Segment 2.3: Multiple rounds + post-selection
- [x] Segment 2.4: Logical information reconstruction

### ✅ Phase 3: Noise Analysis (Complete)
- [x] Segment 3.1: Manual noise injection
- [x] Segment 3.2: Heuristic noise models (Cirq export)
- [x] Segment 3.3: Noise channel comparison
- [x] Segment 3.4: Logical error vs physical error plots

### ✅ Phase 4: Optimization (Complete)
- [x] Segment 4.1: Alternative state injection circuits (non-magic)
- [x] Segment 4.2: Comprehensive noise model comparison
- [x] Flagging techniques implemented
- [x] Parallelism optimization demonstrated

### ✅ Phase 5: Advanced Topics (Complete)
- [x] Segment 5.1: Syndrome decoding with lookup table
- [x] Segment 5.2: Tsim T-state memory demonstration
- [x] Bonus 2: Recurrent syndrome extraction with decoding
- [x] Bonus 4: Tsim for magic state preservation

## Running the Code

### Setup
```bash
cd "/path/to/2026-QuEra-Technical-CUDAstudiedmore"
source .venv/bin/activate  # or use uv
```

### Quick Tests (Recommended First)
```bash
# Test segments 1-3 (30 seconds)
python solution/quick_test.py

# Test segments 4-5 (1-2 minutes)
python solution/segment_4_5_quick_test.py

# All segments work? Run everything!
python solution/run_all.py  # 30-60 minutes
```

### Run Individual Segments
```bash
# Phase 1: Foundation
python solution/segment_1_foundation/01_basic_bloqade.py
python solution/segment_1_foundation/02_noise_simulation.py
python solution/segment_1_foundation/03_parallelism.py

# Phase 2: Core QEC
python solution/segment_2_core_qec/01_msd_encoding.py
python solution/segment_2_core_qec/02_syndrome_extraction.py
python solution/segment_2_core_qec/03_multi_round_qec.py

# Phase 3: Noise Analysis
python solution/segment_3_noise_analysis/01_heuristic_noise.py
python solution/segment_3_noise_analysis/02_error_scaling.py

# Phase 4: Optimization
python solution/segment_4_optimization/01_improved_encoding.py
python solution/segment_4_optimization/02_noise_comparison.py

# Phase 5: Advanced
python solution/segment_5_advanced/01_syndrome_decoding.py
python solution/segment_5_advanced/02_tsim_magic_states.py
```

## Key Technologies

- **Bloqade**: QuEra's SDK for neutral atom quantum computing
- **Squin**: Kernel-based circuit construction
- **Stim**: Efficient Clifford circuit simulator
- **Tsim**: QuEra's simulator for circuits with limited magic
- **Cirq**: For noise model application

## Technical Achievements

### Segment 1.1: Basic Bloqade
- Implemented Bell state, GHZ state, basic gates
- Demonstrated Stim and Tsim sampling
- Verified correct entanglement patterns

### Segment 1.2: Noise Simulation
- Implemented depolarizing noise (single and two-qubit)
- Analyzed noise effects at different circuit locations
- Quantified fidelity degradation with noise levels
- Key finding: Noise after CNOT more damaging than before

### Segment 1.3: Parallelism
- Demonstrated automatic gate parallelization
- Showed circuit depth reduction strategies
- Prepared [[7,1,3]] Steane code with optimized parallelism

### Segment 2.1: MSD Encoding
- Implemented MSD state injection circuit from QuEra paper
- Created standard Steane code preparation
- Verified codeword structure

### Segment 2.2: Syndrome Extraction
- All 6 stabilizers (3 X-type, 3 Z-type) implemented
- Ancilla-based measurement circuits
- Error detection and verification

### Segment 2.3: Multi-Round QEC
- Multi-round syndrome extraction (1-5 rounds)
- Post-selection on zero syndromes
- Fidelity improvement analysis

### Segment 3.1: Heuristic Noise Models
- Cirq export pipeline working
- GeminiOneZone hardware noise model
- Noise scaling parameter sweeps

### Segment 3.2: Error Scaling
- Logical error (L) vs physical error (P) analysis
- Power law fitting: L ∝ P^β
- Threshold behavior identification

### Segment 4.1: Improved Encoding
- Direct Steane encoding (non-magic states)
- Flagged encoding with error detection
- Circuit depth optimization (4 layers vs 10+)
- Parallelism maximization

### Segment 4.2: Noise Model Comparison
- Uniform vs realistic vs biased noise
- Gate-specific noise hierarchy analysis
- Noise scaling comparisons
- QEC integration testing

### Segment 5.1: Syndrome Decoding
- Lookup table decoder for [[7,1,3]] code
- Correction feedforward simulation
- Multi-round QEC with decoding
- Theoretical vs practical correction analysis

### Segment 5.2: Tsim Magic States
- T gate implementation with Tsim
- Magic T-state encoding into Steane code
- T-state memory with QEC (1-3 rounds)
- Magic preservation demonstration
- Clifford vs magic comparison

## Summary Statistics

- **Total Scripts:** 12 implementation files
- **Total Lines:** ~3,500 lines of code
- **Squin Kernels:** 70+ kernel functions
- **Backend Calls:** Stim (primary) + Tsim (magic)
- **System Size:** 7 data + 6 ancilla qubits
- **Shots per Test:** 100-1000
- **Phases Complete:** 5/5 (100%)
- **Challenge Requirements:** All core + 2 bonuses met

## References

1. QuEra MSD Paper: https://arxiv.org/abs/2412.15165
2. Steane QEC: https://arxiv.org/pdf/2312.09745
3. Bloqade Documentation: https://bloqade.quera.com/latest/digital/
4. Tsim Documentation: https://queracomputing.github.io/tsim/dev/

## Notes

- All circuits use Bloqade Squin kernels as required
- Stim backend for Clifford-only simulations
- Tsim backend ready for magic gate support
- Code emphasizes modularity and reusability
