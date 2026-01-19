import google.generativeai as genai
import sys
import os
import subprocess

# --- إعداداتك ---
# ضع مفتاحك هنا
os.environ["GOOGLE_API_KEY"] = 'YOUR_API_KEY_HERE'
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

def smart_execute(user_input):
    # هذا البرومبت هو "الدماغ" الذي يقرر نوع المهمة
    sys_prompt = f"""
    You are a CLI automation assistant. Analyze the following user input: "{user_input}"
    
    Determine the intent and strictly output in ONE of the following formats:
    
    1. IF SYSTEM COMMAND (e.g., open browser, run exe, list files, ping):
       Output: SYSTEM_CMD: <actual_windows_command>
       
    2. IF CODE GENERATION (e.g., write java code, python script for X):
       Output: WRITE_CODE: <filename> | <code>
       (Ensure code is plain text, no markdown backticks)
       
    3. IF GENERAL QUERY/PLAN (e.g., explain, plan a project, analyze):
       Output: ANSWER: <your_response>
       
    Do not add extra text. Just the formatted output.
    """
    
    try:
        response = model.generate_content(sys_prompt)
        result = response.text.strip()
        
        # --- معالجة الردود ---
        
        # 1. حالة تنفيذ أوامر النظام
        if result.startswith("SYSTEM_CMD:"):
            cmd = result.replace("SYSTEM_CMD:", "").strip()
            print(f"⚙️  جاري تنفيذ: {cmd}")
            # تنفيذ الأمر مباشرة
            os.system(cmd)
            
        # 2. حالة كتابة الكود
        elif result.startswith("WRITE_CODE:"):
            parts = result.replace("WRITE_CODE:", "").split("|", 1)
            if len(parts) == 2:
                filename = parts[0].strip()
                code_content = parts[1].strip()
                # تنظيف الكود من علامات الماركداون إذا بقيت
                code_content = code_content.replace("```", "")
                
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(code_content)
                print(f"💾 تم حفظ الملف بنجاح: {filename}")
                print(f"   (يمكنك تشغيله الآن)")
            else:
                print("❌ حدث خطأ في تنسيق الكود المستلم.")

        # 3. حالة الإجابة العامة
        elif result.startswith("ANSWER:"):
            print("\n🤖 Gemini:")
            print(result.replace("ANSWER:", "").strip())
            print("-" * 30)

        else:
            # في حال لم يلتزم النموذج بالتنسيق، اطبع الرد كما هو
            print(result)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # دمج كل الكلمات التي تكتبها في سطر الأوامر لتصبح جملة واحدة
    full_command = " ".join(sys.argv[1:])
    
    if not full_command:
        print("الرجاء كتابة أمر، مثال: g open notepad")
    else:
        smart_execute(full_command)