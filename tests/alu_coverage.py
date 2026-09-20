"""
ALU Functional Coverage Model
================================
يحدد نقاط التغطية (CoverPoints) التي نريد قياسها في ALU.
"""

from pathlib import Path
from cocotb_coverage.coverage import (
    CoverPoint,
    CoverCross,
    coverage_db,
)


# المسار الجذر للمشروع
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# دالة مساعدة: تصنيف قيمة إلى نطاق
# ============================================================
def range_bin(value):
    """يصنّف القيمة إلى: zero / low / high"""
    if value == 0:
        return "zero"
    elif value < 128:
        return "low"
    else:
        return "high"


# ============================================================
# CoverPoint 1: جميع العمليات الثمانية
# ============================================================
@CoverPoint(
    "alu.op",
    xf=lambda a, b, op, result: op,
    bins=list(range(8)),
)
# ============================================================
# CoverPoint 2: نطاق قيم a
# ============================================================
@CoverPoint(
    "alu.a_range",
    xf=lambda a, b, op, result: range_bin(a),
    bins=["zero", "low", "high"],
)
# ============================================================
# CoverPoint 3: نطاق قيم b
# ============================================================
@CoverPoint(
    "alu.b_range",
    xf=lambda a, b, op, result: range_bin(b),
    bins=["zero", "low", "high"],
)
# ============================================================
# CoverPoint 4: هل النتيجة صفر؟
# ============================================================
@CoverPoint(
    "alu.result_zero",
    xf=lambda a, b, op, result: (result == 0),
    bins=[True, False],
)
# ============================================================
# CoverCross: تقاطع العملية مع نطاق a
# ============================================================
@CoverCross(
    "alu.op_x_a",
    items=["alu.op", "alu.a_range"],
)
def sample_alu(a, b, op, result):
    """تسجيل عينة تغطية جديدة"""
    pass


# ============================================================
# دوال تصدير التقارير
# ============================================================
def export_coverage_xml(filename="coverage.xml"):
    filepath = PROJECT_ROOT / filename
    coverage_db.export_to_xml(filename=str(filepath))
    print(f"✅ XML saved to: {filepath}")


def export_coverage_yaml(filename="coverage.yml"):
    filepath = PROJECT_ROOT / filename
    coverage_db.export_to_yaml(filename=str(filepath))
    print(f"✅ YAML saved to: {filepath}")