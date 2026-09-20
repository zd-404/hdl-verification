import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


@cocotb.test()
async def test_reset(dut):
    """اختبار 1: عند تفعيل rst، يجب أن يكون العداد 0"""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    assert dut.count.value == 0, f"Expected 0, got {dut.count.value}"
    dut._log.info("✅ اختبار rst نجح")


@cocotb.test()
async def test_increment(dut):
    """اختبار 2: بعد rst، كل نبضة تزيد العداد 1"""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    # 1. صفّر العداد
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    # 2. اختبر 5 نبضات
    for expected in range(1, 6):
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")  # انتظر قليلاً ليستقر العداد بعد الحافة
        got = int(dut.count.value)
        dut._log.info(f"Expected={expected}, Got={got}")
        assert got == expected, f"Expected {expected}, got {got}"

    dut._log.info("✅ اختبار الزيادة نجح")




@cocotb.test()
async def test_overflow(dut):
    """اختبار 3: العداد يعود لـ 0 بعد 255"""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    # صفّر العداد
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    # اختبر 256 نبضة (من 0 إلى 255 ثم يرجع لـ 0)
    for i in range(256):
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")

    # بعد 256 نبضة، العداد يجب أن يعود لـ 0
    got = int(dut.count.value)
    dut._log.info(f"بعد 256 نبضة، العداد = {got}")
    assert got == 0, f"Expected 0 after overflow, got {got}"

    dut._log.info("✅ اختبار overflow نجح")