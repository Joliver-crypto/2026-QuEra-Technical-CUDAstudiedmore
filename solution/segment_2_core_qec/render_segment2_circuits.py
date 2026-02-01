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

    mod1 = load_module("seg2_1", BASE / "01_msd_encoding.py")
    mod2 = load_module("seg2_2", BASE / "02_syndrome_extraction.py")
    mod3 = load_module("seg2_3", BASE / "03_multi_round_qec.py")

    @squin.kernel
    def seg2_1_sqrt_y_demo():
        q = squin.qalloc(1)
        mod1.sqrt_y_gate(q[0])
        squin.measure(q[0])

    @squin.kernel
    def seg2_2_measure_x_s1_demo():
        data = mod2.prepare_steane_logical_zero()
        mod2.measure_x_syndrome_s1(data)
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_2_measure_x_s2_demo():
        data = mod2.prepare_steane_logical_zero()
        mod2.measure_x_syndrome_s2(data)
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_2_measure_x_s3_demo():
        data = mod2.prepare_steane_logical_zero()
        mod2.measure_x_syndrome_s3(data)
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_2_measure_z_s4_demo():
        data = mod2.prepare_steane_logical_zero()
        mod2.measure_z_syndrome_s4(data)
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_2_measure_z_s5_demo():
        data = mod2.prepare_steane_logical_zero()
        mod2.measure_z_syndrome_s5(data)
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_2_measure_z_s6_demo():
        data = mod2.prepare_steane_logical_zero()
        mod2.measure_z_syndrome_s6(data)
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_3_single_qec_round_demo():
        data = mod3.prepare_steane_logical_zero()
        mod3.single_qec_round_with_noise(data, 0.01)
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_2_prepare_steane_logical_zero_demo():
        data = mod2.prepare_steane_logical_zero()
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_2_syndrome_extraction_with_error_demo():
        mod2.syndrome_extraction_with_error(0, "X")

    @squin.kernel
    def seg2_3_prepare_steane_logical_zero_demo():
        data = mod3.prepare_steane_logical_zero()
        for i in range(7):
            squin.measure(data[i])

    @squin.kernel
    def seg2_3_multi_round_qec_demo():
        mod3.multi_round_qec(3, 0.01)

    @squin.kernel
    def seg2_3_memory_experiment_with_idle_noise_demo():
        mod3.memory_experiment_with_idle_noise(5, 0.01)

    render_list = [
        ("seg2_1_sqrt_y_gate", seg2_1_sqrt_y_demo),
        ("seg2_1_msd_state_injection_logical_zero", mod1.msd_state_injection_logical_zero),
        ("seg2_1_steane_logical_zero", mod1.steane_logical_zero),
        ("seg2_1_steane_logical_one", mod1.steane_logical_one),
        ("seg2_2_prepare_steane_logical_zero", seg2_2_prepare_steane_logical_zero_demo),
        ("seg2_2_measure_x_s1", seg2_2_measure_x_s1_demo),
        ("seg2_2_measure_x_s2", seg2_2_measure_x_s2_demo),
        ("seg2_2_measure_x_s3", seg2_2_measure_x_s3_demo),
        ("seg2_2_measure_z_s4", seg2_2_measure_z_s4_demo),
        ("seg2_2_measure_z_s5", seg2_2_measure_z_s5_demo),
        ("seg2_2_measure_z_s6", seg2_2_measure_z_s6_demo),
        ("seg2_2_full_syndrome_extraction", mod2.full_syndrome_extraction),
        ("seg2_2_syndrome_extraction_with_error_default", seg2_2_syndrome_extraction_with_error_demo),
        ("seg2_3_prepare_steane_logical_zero", seg2_3_prepare_steane_logical_zero_demo),
        ("seg2_3_single_qec_round_with_noise", seg2_3_single_qec_round_demo),
        ("seg2_3_multi_round_qec", seg2_3_multi_round_qec_demo),
        ("seg2_3_memory_experiment_with_idle_noise", seg2_3_memory_experiment_with_idle_noise_demo),
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
