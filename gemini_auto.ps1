# ==== Gemini CLI Full Auto Setup ====

# 1️⃣ حدد مسار .env
$envPath = "D:\GeminiEnvironment\.env"

# 2️⃣ محتوى .env (غير USERNAME و PASSWORD إذا تحب)
$envContent = @"
USERNAME=demo_user
PASSWORD=demo_pass
"@

# 3️⃣ احفظ .env
$envContent | Out-File -Encoding UTF8 $envPath
Write-Host "[✔] .env file configured"

# 4️⃣ روح لمجلد GeminiEnvironment
cd D:\GeminiEnvironment

# 5️⃣ أغلق أي حاويات Docker شغالة
Write-Host "[⏳] Shutting down existing containers..."
docker-compose down

# 6️⃣ شغّل كل الحاويات بالخلفية
Write-Host "[⏳] Starting containers in background..."
docker-compose up -d

# 7️⃣ تحقق من حالة الحاويات
Write-Host "[✔] Containers status:"
docker-compose ps

Write-Host "[🎉] Gemini CLI is now running fully automated!"
