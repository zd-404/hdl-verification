\# HDL Verification Portfolio



مجموعة من الدوائر الرقمية (Verilog) مع إطار تحقق آلي (Automated Verification) مبني على \*\*cocotb\*\* و \*\*Python\*\*.



\## 📋 المشاريع الحالية



| المشروع | الوصف | الاختبارات |

|---------|-------|-----------|

| \*\*Counter\*\* | عداد 8-بت مع تصفير وكشف overflow | 3 ✅ |

| \*\*Vending Machine\*\* | آلة بيع FSM بحالات متعددة | 7 ✅ |



\## 🛠️ المتطلبات



\- Python 3.9+

\- Icarus Verilog

\- cocotb



\## 🚀 التثبيت



```bash

\\# 1. إنشاء بيئة افتراضية

python -m venv cocotb\\\_env



\\# 2. تفعيلها

\\# Windows:

cocotb\\\_env\\\\Scripts\\\\activate

\\# Linux/Mac:

source cocotb\\\_env/bin/activate



\\# 3. تثبيت المكتبات

pip install -r requirements.txt


\----------------------------------------------------------------------------------------- 



🏃 تشغيل الاختبارات



\# اختبار العدّاد

python runners/run\_counter.py



\# اختبار آلة البيع

python runners/run\_vending.py





\-----------------------------------------------------------------------------------------



📁 بنية المشروع

hdl-automation/

├── duts/              ← الدوائر (Design Under Test)

├── tests/             ← ملفات الاختبار

├── runners/           ← مشغلات الاختبار

├── requirements.txt

└── README.md



\-----------------------------------------------------------------------------------------



👤 المؤلف

Zeyad



\-----------------------------------------------------------------------------------------



المتوقع

cocotb\_env

duts

runners

tests

.gitignore

requirements.txt

README.md

