import cocotb
import random
from cocotb.triggers import Timer

from alu_coverage import sample_alu, export_coverage_xml, export_coverage_yaml

# ===== رموز العمليات (نفسها في Verilog) =====
ADD = 0b000
SUB = 0b001
AND = 0b010
OR  = 0b011
XOR = 0b100
NOT = 0b101
SHL = 0b110
SHR = 0b111


# ===== Reference Model (النموذج المرجعي) =====
# يحسب المتوقع بلغة Python — موثوق 100%
def reference_model(a, b, op):
    if op == ADD: return (a + b) & 0xFF
    if op == SUB: return (a - b) & 0xFF
    if op == AND: return a & b
    if op == OR:  return a | b
    if op == XOR: return a ^ b
    if op == NOT: return (~a) & 0xFF
    if op == SHL: return (a << 1) & 0xFF
    if op == SHR: return a >> 1
    return 0


# ===== Helper: تطبيق مدخلات وقراءة المخرجات =====
async def apply_and_check(dut, a, b, op, test_name=""):
    # 1. طبّق المدخلات
    dut.a.value = a
    dut.b.value = b
    dut.op.value = op

    # 2. انتظر قليلاً ليستقر المنطق التركيبي
    await Timer(1, unit="ns")

    # 3. اقرأ الناتج الفعلي من الدائرة
    actual = int(dut.result.value)

    # 4. احسب المتوقع من Reference Model
    expected = reference_model(a, b, op)

    # 5. ⬅️ سجّل العينة في نظام Coverage
    sample_alu(a, b, op, actual)

    # 6. قارن
    assert actual == expected, \
        f"{test_name}: a={a}, b={b}, op={op:03b}, expected={expected}, actual={actual}"

    dut._log.info(f"✅ {test_name}: a={a}, b={b}, op={op:03b} → {actual}")

# ===== الاختبارات =====
@cocotb.test()
async def test_add(dut):
    """اختبار الجمع"""
    await apply_and_check(dut, 5, 3, ADD, "ADD basic")
    await apply_and_check(dut, 100, 100, ADD, "ADD 100+100")
    await apply_and_check(dut, 255, 1, ADD, "ADD overflow")
    await apply_and_check(dut, 0, 0, ADD, "ADD zeros")


@cocotb.test()
async def test_sub(dut):
    """اختبار الطرح"""
    await apply_and_check(dut, 10, 3, SUB, "SUB basic")
    await apply_and_check(dut, 100, 50, SUB, "SUB 100-50")
    await apply_and_check(dut, 5, 10, SUB, "SUB underflow")
    await apply_and_check(dut, 0, 0, SUB, "SUB zeros")


@cocotb.test()
async def test_and(dut):
    """اختبار AND"""
    await apply_and_check(dut, 0b11110000, 0b10101010, AND, "AND")
    await apply_and_check(dut, 0xFF, 0xFF, AND, "AND all ones")
    await apply_and_check(dut, 0x00, 0xFF, AND, "AND with zero")


@cocotb.test()
async def test_or(dut):
    """اختبار OR"""
    await apply_and_check(dut, 0b11110000, 0b00001111, OR, "OR")
    await apply_and_check(dut, 0x00, 0x00, OR, "OR zeros")
    await apply_and_check(dut, 0xFF, 0x00, OR, "OR with FF")


@cocotb.test()
async def test_xor(dut):
    """اختبار XOR"""
    await apply_and_check(dut, 0xFF, 0xFF, XOR, "XOR same")
    await apply_and_check(dut, 0xFF, 0x00, XOR, "XOR with FF")
    await apply_and_check(dut, 0xAA, 0x55, XOR, "XOR alternating")


@cocotb.test()
async def test_not(dut):
    """اختبار NOT"""
    await apply_and_check(dut, 0x00, 0, NOT, "NOT zero")
    await apply_and_check(dut, 0xFF, 0, NOT, "NOT FF")
    await apply_and_check(dut, 0xAA, 0, NOT, "NOT AA")


@cocotb.test()
async def test_shl(dut):
    """اختبار الإزاحة لليسار"""
    await apply_and_check(dut, 0b00000001, 0, SHL, "SHL 1")
    await apply_and_check(dut, 0b10000000, 0, SHL, "SHL MSB")
    await apply_and_check(dut, 0x0F, 0, SHL, "SHL 0F")


@cocotb.test()
async def test_shr(dut):
    """اختبار الإزاحة لليمين"""
    await apply_and_check(dut, 0b10000000, 0, SHR, "SHR MSB")
    await apply_and_check(dut, 0xFF, 0, SHR, "SHR FF")
    await apply_and_check(dut, 0b00000010, 0, SHR, "SHR 2")


@cocotb.test()
async def test_zero_flag(dut):
    """اختبار علم الصفر"""
    # 5 - 5 = 0 → zero يجب أن يكون 1
    dut.a.value = 5
    dut.b.value = 5
    dut.op.value = SUB
    await Timer(1, unit="ns")
    assert int(dut.zero.value) == 1, "zero must be 1 when result is 0"
    dut._log.info("✅ zero flag = 1 when result = 0")

    # 10 - 5 = 5 → zero يجب أن يكون 0
    dut.a.value = 10
    dut.b.value = 5
    dut.op.value = SUB
    await Timer(1, unit="ns")
    assert int(dut.zero.value) == 0, "zero must be 0 when result != 0"
    dut._log.info("✅ zero flag = 0 when result != 0")


@cocotb.test()
async def test_random_100(dut):
    """اختبار عشوائي: 100 حالة لكل عملية"""
    ops = [ADD, SUB, AND, OR, XOR, NOT, SHL, SHR]

    for i in range(100):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        op = random.choice(ops)

        await apply_and_check(dut, a, b, op, f"random #{i+1}")

    dut._log.info("✅ 100 random tests passed")
@cocotb.test()
async def test_export_coverage(dut):
    """اختبار نهائي: تشغيل كل العمليات وتصدير تقرير التغطية"""
    test_cases = [
        (0, 0, ADD, "ADD zero"),
        (255, 1, ADD, "ADD overflow"),
        (100, 50, SUB, "SUB normal"),
        (5, 10, SUB, "SUB underflow"),
        (0xFF, 0xAA, AND, "AND full"),
        (0xAA, 0x55, OR, "OR alternating"),
        (0xFF, 0x00, XOR, "XOR full"),
        (0x00, 0, NOT, "NOT zero"),
        (0x01, 0, SHL, "SHL 1"),
        (0x80, 0, SHR, "SHR MSB"),
        (200, 100, ADD, "ADD high range"),
        (10, 200, SUB, "SUB b high"),
        # ⬇️ الحالات الجديدة لإغلاق فجوات التغطية
        (0, 0xFF, XOR, "XOR with a=0"),
        (0, 0xAA, SHL, "SHL with a=0"),
        (0, 0xFF, SHR, "SHR with a=0"),
    ]

    for a, b, op, name in test_cases:
        await apply_and_check(dut, a, b, op, name)

    # تصدير التقارير
    export_coverage_xml("coverage.xml")
    export_coverage_yaml("coverage.yml")
    dut._log.info("✅ تم تصدير تقرير التغطية")