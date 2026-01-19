# استخدام نسخة بايثون خفيفة
FROM python:3.9-slim

# تحديد مجلد العمل داخل الدوكر
WORKDIR /app


# نسخ ملف المتطلبات وتثبيت المكاتب
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود + ملف credentials.json إلى داخل الحاوية
# (تأكد أن ملف credentials.json موجود بجانب هذا الملف)
COPY . .

# أمر التشغيل (اسم السكربت الخاص بك)
CMD ["python", "invoice_automation.py"]