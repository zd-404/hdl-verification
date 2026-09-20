import os
from pathlib import Path
from cocotb_tools.runner import get_runner


def test_counter_runner():
    sim = os.getenv("SIM", "icarus")

    # المشروع الجذر (hdl-automation)
    proj_root = Path(__file__).resolve().parent.parent

    # مسار ملف الدائرة (في duts/)
    sources = [proj_root / "duts" / "counter.v"]

    # مسار مجلد الاختبارات (tests/)
    test_dir = proj_root / "tests"

    runner = get_runner(sim)

    runner.build(
        sources=sources,
        hdl_toplevel="counter",
        always=True,
    )

    runner.test(
        hdl_toplevel="counter",
        test_module="test_counter",
        test_dir=test_dir,
    )


if __name__ == "__main__":
    test_counter_runner()