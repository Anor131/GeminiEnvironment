import imaplib
import email
import json
import time
import requests  # For making API calls to the AI model
import gspread  # For interacting with Google Sheets
from email.header import decode_header
import os

# --- الخطوة 1: إعداد البيئة والاتصال ---
# (هذا الجزء من الكود هو نتاج الـ Prompt الأول)

# --- إعدادات المستخدم (يجب ملؤها) ---
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASS = os.getenv('GMAIL_PASS')
GMAIL_IMAP_SERVER = 'imap.gmail.com'
AI_API_KEY = os.getenv('AI_API_KEY')
AI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent' # مثال لـ Gemini

# --- دوال التعامل مع Gmail ---
def connect_to_gmail():
    """الاتصال بسيرفر IMAP الخاص بـ Gmail."""
    mail = imaplib.IMAP4_SSL(GMAIL_IMAP_SERVER)
    mail.login(GMAIL_USER, GMAIL_PASS)
    return mail

def fetch_unread_emails(mail):
    """جلب قائمة بالإيميلات غير المقروءة."""
    mail.select('inbox')
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    
    emails = []
    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                emails.append({'id': email_id, 'message': msg})
    return emails

def get_email_body(msg):
    """استخراج محتوى النص من رسالة الإيميل."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if "text/plain" in content_type:
                try:
                    return part.get_payload(decode=True).decode()
                except:
                    return ""
    else:
        try:
            return msg.get_payload(decode=True).decode()
        except:
            return ""
    return ""

def mark_email_as_read(mail, email_id):
    """تعليم الإيميل كـ 'مقروء'."""
    mail.store(email_id, '+FLAGS', '\Seen')

# --- دوال التعامل مع Google Sheets ---
def connect_to_sheet():
    """الاتصال بجدول البيانات باستخدام gspread."""
    # تأكد من وجود ملف credentials.json في نفس المجلد
    sa = gspread.service_account(filename="/app/creds/credentials.json")
    sheet = sa.open("Invoices").sheet1 # افتح جدول بيانات باسم "Invoices"
    return sheet

def append_to_sheet(sheet, data):
    """إضافة صف جديد من البيانات إلى الجدول."""
    # يجب أن يكون ترتيب البيانات متوافقًا مع أعمدة الجدول
    row = [data.get('vendor_name'), data.get('invoice_number'), data.get('amount_due'), data.get('due_date')]
    sheet.append_row(row)
    print(f"تم تسجيل فاتورة من: {data.get('vendor_name')}")

# --- الخطوة 2: دمج الذكاء الاصطناعي ---
# (هذا الجزء من الكود هو نتاج الـ Prompt الثاني)

PROMPT_IS_INVOICE = "Is this email an invoice? Answer only with a single JSON object: {\"is_invoice\": true} or {\"is_invoice\": false}."
PROMPT_EXTRACT_DATA = "From the text of the invoice email provided, extract the following entities: 'invoice_number', 'vendor_name', 'amount_due', and 'due_date'. If a field is not found, return null. Provide the output as a clean JSON object only."

def call_ai_model(prompt, email_content):
    """إرسال الطلب إلى نموذج الذكاء الاصطناعي والحصول على الرد."""
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": f"{prompt}\n\nEmail Content:\n{email_content}"}]}]
    }
    response = requests.post(f"{AI_API_URL}?key={AI_API_KEY}", headers=headers, json=payload)
    if response.status_code == 200:
        # ملاحظة: طريقة استخراج الرد قد تختلف قليلاً بين Gemini و OpenAI
        response_json = response.json()
        text_content = response_json['candidates'][0]['content']['parts'][0]['text']
        return json.loads(text_content.strip())
    else:
        print(f"Error calling AI model: {response.text}")
        return None

def is_invoice(content):
    """يحدد ما إذا كان الإيميل فاتورة باستخدام الذكاء الاصطناعي."""
    response = call_ai_model(PROMPT_IS_INVOICE, content)
    return response and response.get('is_invoice', False)

def extract_invoice_data(content):
    """يستخرج بيانات الفاتورة باستخدام الذكاء الاصطناعي."""
    return call_ai_model(PROMPT_EXTRACT_DATA, content)


# --- الخطوة 3: تجميع المنطق الرئيسي (الـ Agent) ---
# (هذا الجزء من الكود هو نتاج الـ Prompt الثالث)

def main():
    """الدالة الرئيسية لتشغيل الـ Agent."""
    print("Agent الأتمتة قيد التشغيل... اضغط Ctrl+C للإيقاف.")

    required_env_vars = ['GMAIL_USER', 'GMAIL_PASS', 'AI_API_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"خطأ: المتغيرات البيئية التالية غير موجودة: {', '.join(missing_vars)}")
        print("يرجى إعداد هذه المتغيرات قبل تشغيل الـ Agent.")
        return


    
    try:
        mail = connect_to_gmail()
        sheet = connect_to_sheet()
        
        while True:
            print("البحث عن إيميلات جديدة...")
            unread_emails = fetch_unread_emails(mail)
            
            if not unread_emails:
                print("لا توجد إيميلات جديدة. الانتظار لمدة 5 دقائق.")
            else:
                print(f"تم العثور على {len(unread_emails)} إيميل جديد.")
                for email_data in unread_emails:
                    email_body = get_email_body(email_data['message'])
                    if not email_body:
                        continue
                        
                    if is_invoice(email_body):
                        print(f"تم اكتشاف فاتورة في الإيميل رقم: {email_data['id'].decode()}")
                        invoice_data = extract_invoice_data(email_body)
                        if invoice_data:
                            append_to_sheet(sheet, invoice_data)
                        mark_email_as_read(mail, email_data['id'])
                    else:
                        # اختياري: يمكن تعليم الإيميلات غير المهمة كمقروءة أيضًا
                        # mark_email_as_read(mail, email_data['id'])
                        print(f"الإيميل رقم {email_data['id'].decode()} ليس فاتورة.")

            time.sleep(300) # الانتظار لمدة 5 دقائق
            
    except Exception as e:
        print(f"حدث خطأ غير متوقع: {e}")
    finally:
        if 'mail' in locals() and mail.state == 'SELECTED':
            mail.logout()
        print("تم إيقاف الـ Agent.")


if __name__ == "__main__":
    main()