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
│   ├── 02_syndrome_extraction.py    - (In progress)
│   └── 03_post_selection.py         - (In progress)
├── segment_3_noise_analysis/
│   └── (To be implemented)
├── segment_4_optimization/
│   └── (To be implemented)
└── segment_5_bonuses/
    └── (To be implemented)
```

## Progress

### ✅ Phase 1: Foundation (Complete)
- [x] Segment 1.1: Basic Bloqade setup with Squin kernels
- [x] Segment 1.2: Noise simulation with depolarizing channels
- [x] Segment 1.3: Circuit parallelism exploration

### 🔄 Phase 2: Core QEC (In Progress)
- [x] Segment 2.1: MSD state encoding circuit
- [ ] Segment 2.2: Steane QEC syndrome extraction
- [ ] Segment 2.3: Multiple rounds + post-selection
- [ ] Segment 2.4: Logical information reconstruction

### ⏳ Phase 3: Noise Analysis (Pending)
- [ ] Segment 3.1: Manual noise injection
- [ ] Segment 3.2: Heuristic noise models (Cirq export)
- [ ] Segment 3.3: Noise channel comparison
- [ ] Segment 3.4: Logical error vs physical error plots

### ⏳ Phase 4: Optimization (Pending)
- [ ] Segment 4.1: Alternative state injection circuits
- [ ] Segment 4.2: Flagging techniques
- [ ] Segment 4.3: Parallelism optimization

### ⏳ Phase 5: Bonuses (Pending)
- [ ] Bonus 1: Distance 5 color code
- [ ] Bonus 2: Recurrent syndrome extraction with decoding
- [ ] Bonus 3: Custom layout + bespoke noise model
- [ ] Bonus 4: Tsim T-state memory at distance 5

## Running the Code

### Setup
```bash
cd "/path/to/2026-QuEra-Technical-CUDAstudiedmore"
export PATH="$HOME/.local/bin:$PATH"
source .venv/bin/activate
```

### Run Individual Segments
```bash
# Foundation segments
uv run python solution/segment_1_foundation/01_basic_bloqade.py
uv run python solution/segment_1_foundation/02_noise_simulation.py
uv run python solution/segment_1_foundation/03_parallelism.py

# QEC segments
uv run python solution/segment_2_core_qec/01_msd_encoding.py
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
