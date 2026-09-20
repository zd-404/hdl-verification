import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def setup(dut):
    """تهيئة الساعة وإعادة الضبط"""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst.value = 1
    dut.coin5.value = 0
    dut.coin10.value = 0
    dut.cancel.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")


async def insert_coin(dut, coin_type):
    """إدخال عملة، وترجّع حالة المخارج بعد الانتقال مباشرة"""
    if coin_type == 5:
        dut.coin5.value = 1
    else:
        dut.coin10.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    # ⬅️ نلتقط المخارج هنا (الحالة انتقلت للتو)
    result = {
        'dispense': int(dut.dispense.value) == 1,
        'change5': int(dut.change5.value) == 1,
        'change10': int(dut.change10.value) == 1,
    }
    dut.coin5.value = 0
    dut.coin10.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    return result


async def press_cancel(dut):
    """ضغط الإلغاء، وترجّع حالة مخارج الباقي بعد الانتقال"""
    dut.cancel.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    result = {
        'change5': int(dut.change5.value) == 1,
        'change10': int(dut.change10.value) == 1,
    }
    dut.cancel.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    return result


@cocotb.test()
async def test_initial_state(dut):
    """اختبار 1: في البداية، لا صرف ولا باقي"""
    await setup(dut)
    assert int(dut.dispense.value) == 0, "لا يجب صرف مشروب في البداية"
    assert int(dut.change5.value) == 0
    assert int(dut.change10.value) == 0
    dut._log.info("✅ الحالة الابتدائية صحيحة")


@cocotb.test()
async def test_buy_with_5_and_5_and_5(dut):
    """اختبار 2: 5+5+5 = مشروب بدون باقي"""
    await setup(dut)
    await insert_coin(dut, 5)
    await insert_coin(dut, 5)
    result = await insert_coin(dut, 5)
    assert result['dispense'], "يجب صرف المشروب بعد 15 ريال"
    assert not result['change5'], "لا يجب إرجاع باقي"
    dut._log.info("✅ شراء بـ 5+5+5 نجح")


@cocotb.test()
async def test_buy_with_10_and_5(dut):
    """اختبار 3: 10+5 = مشروب بدون باقي"""
    await setup(dut)
    await insert_coin(dut, 10)
    result = await insert_coin(dut, 5)
    assert result['dispense'], "يجب صرف المشروب"
    assert not result['change5']
    dut._log.info("✅ شراء بـ 10+5 نجح")


@cocotb.test()
async def test_buy_with_10_and_10_with_change(dut):
    """اختبار 4: 10+10 = مشروب + باقي 5"""
    await setup(dut)
    await insert_coin(dut, 10)
    result = await insert_coin(dut, 10)
    assert result['dispense'], "يجب صرف المشروب"
    assert result['change5'], "يجب إرجاع 5 ريال باقي"
    dut._log.info("✅ شراء بـ 10+10 مع باقي نجح")


@cocotb.test()
async def test_cancel_from_5(dut):
    """اختبار 5: إلغاء بعد إدخال 5 → إرجاع 5"""
    await setup(dut)
    await insert_coin(dut, 5)
    result = await press_cancel(dut)
    assert result['change5'], "يجب إرجاع 5 ريال"
    assert not result['change10']
    dut._log.info("✅ الإلغاء من حالة 5 نجح")


@cocotb.test()
async def test_cancel_from_10(dut):
    """اختبار 6: إلغاء بعد إدخال 10 → إرجاع 10"""
    await setup(dut)
    await insert_coin(dut, 10)
    result = await press_cancel(dut)
    assert result['change10'], "يجب إرجاع 10 ريال"
    assert not result['change5']
    dut._log.info("✅ الإلغاء من حالة 10 نجح")


@cocotb.test()
async def test_reset_behavior(dut):
    """اختبار 7: إعادة الضبط ترجع كل شيء لـ 0"""
    await setup(dut)
    await insert_coin(dut, 10)
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert int(dut.dispense.value) == 0
    assert int(dut.change5.value) == 0
    assert int(dut.change10.value) == 0
    dut._log.info("✅ إعادة الضبط نجحت")