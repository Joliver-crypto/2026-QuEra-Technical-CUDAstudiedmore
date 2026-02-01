import os
import subprocess
import importlib.util
from pathlib import Path

from bloqade import squin
import bloqade.tsim


BASE = Path(__file__).resolve().parent
OUTPUT_DIR = BASE / "circuit_pngs"
MPLCONFIGDIR = BASE / ".mplconfig"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def svg_only(diagram_svg_html: str) -> str:
    start = diagram_svg_html.find("<svg")
    end = diagram_svg_html.rfind("</svg>")
    if start == -1 or end == -1:
        raise ValueError("SVG tag not found in diagram output")
    return diagram_svg_html[start : end + len("</svg>")]


def render_kernel(name: str, kernel):
    circ = bloqade.tsim.Circuit(kernel)
    diag = circ.diagram(height=400)
    svg = svg_only(diag._svg)
    svg_path = OUTPUT_DIR / f"{name}.svg"
    png_path = OUTPUT_DIR / f"{name}.png"
    svg_path.write_text(svg)
    subprocess.run(
        ["/opt/homebrew/bin/rsvg-convert", "-o", str(png_path), str(svg_path)],
        check=True,
    )
    return png_path


def main():
    os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)

    mod1 = load_module("seg1_1", BASE / "01_basic_bloqade.py")
    mod2 = load_module("seg1_2", BASE / "02_noise_simulation.py")
    mod3 = load_module("seg1_3", BASE / "03_parallelism.py")

    @squin.kernel
    def seg1_1_ghz_3_demo():
        return mod1.ghz_state(3)

    @squin.kernel
    def seg1_2_bell_state_with_noise_demo():
        return mod2.bell_state_with_noise(0.01)

    @squin.kernel
    def seg1_2_bell_with_two_qubit_noise_demo():
        return mod2.bell_with_two_qubit_noise(0.01, 0.02)

    @squin.kernel
    def seg1_2_broadcast_noise_demo():
        return mod2.broadcast_noise_demo(0.05)

    @squin.kernel
    def seg1_2_noise_at_locations_demo():
        return mod2.noise_at_different_locations(0.1, 2)

    render_list = [
        ("seg1_1_basic_bell_state", mod1.basic_bell_state),
        ("seg1_1_basic_gates_demo", mod1.basic_gates_demo),
        ("seg1_1_ghz_state_3", seg1_1_ghz_3_demo),
        ("seg1_2_bell_state_with_noise", seg1_2_bell_state_with_noise_demo),
        ("seg1_2_bell_with_two_qubit_noise", seg1_2_bell_with_two_qubit_noise_demo),
        ("seg1_2_broadcast_noise_demo", seg1_2_broadcast_noise_demo),
        ("seg1_2_noise_at_locations", seg1_2_noise_at_locations_demo),
        ("seg1_3_parallel_single_qubit_gates", mod3.parallel_single_qubit_gates),
        ("seg1_3_sequential_dependent_gates", mod3.sequential_dependent_gates),
        ("seg1_3_mixed_parallel_sequential", mod3.mixed_parallel_sequential),
        ("seg1_3_optimized_steane_preparation", mod3.optimized_steane_preparation),
        ("seg1_3_broadcast_parallel_ops", mod3.broadcast_parallel_ops),
    ]

    created = []
    failed = []
    for name, kernel in render_list:
        try:
            created.append(render_kernel(name, kernel))
        except Exception as exc:
            failed.append((name, str(exc)))

    print("Created PNGs:")
    for path in created:
        print(path)

    if failed:
        print("\nFailed renders:")
        for name, err in failed:
            print(f"{name}: {err}")


if __name__ == "__main__":
    main()
