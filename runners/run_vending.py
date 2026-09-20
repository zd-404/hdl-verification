import os
from pathlib import Path
from cocotb_tools.runner import get_runner


def vending_runner():
    sim = os.getenv("SIM", "icarus")

    # المشروع الجذر (hdl-automation)
    proj_root = Path(__file__).resolve().parent.parent

    # مسار ملف الدائرة (في duts/)
    sources = [proj_root / "duts" / "vending_machine.v"]

    # مسار مجلد الاختبارات (tests/)
    test_dir = proj_root / "tests"

    runner = get_runner(sim)

    runner.build(
        sources=sources,
        hdl_toplevel="vending_machine",
        always=True,
    )

    runner.test(
        hdl_toplevel="vending_machine",
        test_module="test_vending",
        test_dir=test_dir,
    )


if __name__ == "__main__":
    vending_runner()