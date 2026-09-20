import os
from pathlib import Path
from cocotb_tools.runner import get_runner


def alu_runner():
    sim = os.getenv("SIM", "icarus")

    # المجلد الجذر
    proj_root = Path(__file__).resolve().parent.parent

    # ملف الدائرة
    sources = [proj_root / "duts" / "alu.v"]

    # مجلد الاختبارات
    test_dir = proj_root / "tests"

    runner = get_runner(sim)

    runner.build(
        sources=sources,
        hdl_toplevel="alu",
        always=True,
    )

    runner.test(
        hdl_toplevel="alu",
        test_module="test_alu",
        test_dir=test_dir,
    )


if __name__ == "__main__":
    alu_runner()