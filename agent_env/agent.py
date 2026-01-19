import subprocess

def analyze_intent(user_input):
    if "افتح" in user_input:
        return {"action": "open_app"}
    return {"action": "unknown"}

def plan(action):
    plans = {
        "open_app": ["open_app"]
    }
    return plans.get(action, [])

def execute(step, user_input):
    if step == "open_app":
        if "كروم" in user_input:
            subprocess.run("start chrome", shell=True)
            return True
    return False

# ===== تشغيل الإيجنت =====
user_input = input("كرما: ")

intent = analyze_intent(user_input)
steps = plan(intent["action"])

print("الخطة:", steps)

success = True
for step in steps:
    result = execute(step, user_input)
    if not result:
        success = False

if success:
    print("✅ تم التنفيذ بنجاح، شنو الخطوة الجاية؟")
else:
    print("❌ صار خطأ، أعيد المحاولة")
