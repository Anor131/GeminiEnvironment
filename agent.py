import subprocess

def analyze_intent(user_input):
    if "افتح" in user_input:
        return {"action": "open_app"}
    return {"action": "unknown"}

def plan(action):
    if action == "open_app":
        return ["open_app"]
    return []

def execute(step, user_input):
    if step == "open_app":
        if "كروم" in user_input:
            print("🔹 جاري فتح كروم...")
            subprocess.run("start chrome", shell=True)
            return True
    return False


# ===== تشغيل الإيجنت =====
user_input = input("أمرك: ")

intent = analyze_intent(user_input)
steps = plan(intent["action"])

print("الخطة:", steps)

success = True
for step in steps:
    if not execute(step, user_input):
        success = False

if success:
    print("✅ تم التنفيذ بنجاح، شنو الخطوة الجاية؟")
else:
    print("❌ ما قدرت أنفّذ الأمر")
