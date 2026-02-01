"""
Color code state injection circuit (Fig. 1a from QuEra MSD paper)
Recreated from assets/colorcode.png using bloqade.squin.

Qubits 0-5: |0⟩, Qubit 6: |Ψ(θ,φ)⟩ (for Clifford sim, all start |0⟩)

Structure (6 columns):
  Column 1: √Y† on qubits 0-5
  Column 2: CNOT(0,1), CNOT(0,2), CNOT(3,4), CNOT(3,5), CNOT(6,4)
  Column 3: CNOT(0,3), CNOT(1,2), CNOT(4,5), CNOT(6,5)
  Column 4: √Y on qubits 1,2,3,4,5,6
  Column 5: CNOT(0,1), CNOT(2,3), CNOT(4,5), CNOT(6,3)
  Column 6: √Y on qubits 2,4,5,6
"""

from bloqade import squin
import bloqade.stim
import bloqade.tsim


@squin.kernel
def sqrt_y(q):
    """√Y = (I + iY)/√2. Clifford approx: S · H · S† (S† = S³)."""
    squin.s(q)
    squin.h(q)
    squin.s(q)
    squin.s(q)
    squin.s(q)


@squin.kernel
def sqrt_y_dagger(q):
    """√Y† = (I - iY)/√2. Clifford approx: S† · H · S (S† = S³)."""
    squin.s(q)
    squin.s(q)
    squin.s(q)  # S† = S³
    squin.h(q)
    squin.s(q)


@squin.kernel
def colorcode_state_injection():
    """
    Color code state injection circuit (exact match to Fig. 1a).

    Column 1: √Y† on qubits 0-5
    Column 2: CNOT(0,1), CNOT(0,2), CNOT(3,4), CNOT(3,5), CNOT(6,4)
    Column 3: CNOT(0,3), CNOT(1,2), CNOT(4,5), CNOT(6,5)
    Column 4: √Y on qubits 1,2,3,4,5,6
    Column 5: CNOT(0,1), CNOT(2,3), CNOT(4,5), CNOT(6,3)
    Column 6: √Y on qubits 2,4,5,6
    """
    q = squin.qalloc(7)
    # Qubit 6 holds |Ψ(θ,φ)⟩; for Clifford sim all start |0⟩

    # Column 1: √Y† on qubits 0-5
    for i in range(6):
        sqrt_y_dagger(q[i])

    # Column 2: CNOTs
    squin.cx(q[0], q[1])
    squin.cx(q[0], q[2])
    squin.cx(q[3], q[4])
    squin.cx(q[3], q[5])
    squin.cx(q[6], q[4])

    # Column 3: CNOTs
    squin.cx(q[0], q[3])
    squin.cx(q[1], q[2])
    squin.cx(q[4], q[5])
    squin.cx(q[6], q[5])

    # Column 4: √Y on qubits 1,2,3,4,5,6
    for i in range(1, 7):
        sqrt_y(q[i])

    # Column 5: CNOTs
    squin.cx(q[0], q[1])
    squin.cx(q[2], q[3])
    squin.cx(q[4], q[5])
    squin.cx(q[6], q[3])

    # Column 6: √Y on qubits 2,4,5,6
    sqrt_y(q[2])
    sqrt_y(q[4])
    sqrt_y(q[5])
    sqrt_y(q[6])

    for i in range(7):
        squin.measure(q[i])


if __name__ == "__main__":
    # Visualize
    tsim_circ = bloqade.tsim.Circuit(colorcode_state_injection)
    diagram = tsim_circ.diagram(height=400)
    print("Circuit diagram (view in notebook):", diagram)

    # Sample
    stim_circ = bloqade.stim.Circuit(colorcode_state_injection)
    sampler = stim_circ.compile_sampler()
    samples = sampler.sample(shots=1000)
    print(f"Samples shape: {samples.shape}")
    print("First 5 outcomes:", [''.join(map(str, s.astype(int))) for s in samples[:5]])
