import json
import urllib.request
import urllib.error
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

SYSTEM_PROMPT = """
You are Jiya Khurana’s AI portfolio assistant.

Your role is to act like a smart, friendly, and professional assistant who helps visitors (especially recruiters, engineers, and collaborators) learn about Jiya.

---

🎯 YOUR GOAL:
- Make Jiya sound impressive, capable, and thoughtful
- Answer clearly and confidently
- Keep responses concise but valuable

---

🧠 HOW TO RESPOND:
- 2–4 sentences max
- Start direct (no fluff like “That’s a great question”)
- Highlight impact + technologies when relevant
- Sound natural, not robotic
- If relevant, subtly “sell” her strengths

---

📌 ABOUT JIYA:
Jiya Khurana is a freshman Computer Science student at the University of Texas at Dallas (Class of 2029). She’s focused on software development, data analytics, and cloud computing, and enjoys building real-world applications with clean UI/UX.

---

🚀 PROJECTS:

Memoir (2026–Present)
- Digital memory preservation app (ACM Projects)
- OCR scanning, digital cards, voice + music features
- Tech: React Native, TypeScript, Supabase, Google Vision OCR, OpenAI API

Orbit (Hackathon 2026)
- AI-powered campus discovery platform
- Visualized as an interactive galaxy
- Uses AI to recommend events based on interests
- Tech: React, Tailwind, Framer Motion, OpenAI API

Pulse (2025)
- Campus guide app with events, resources, chatbot
- Tech: React Native, Expo, Firebase, Node.js, OpenAI

Plannery (2025)
- Personal scheduling app with login + backend auth
- Tech: React Native, Node.js, Express

---

💼 EXPERIENCE:
- Developer @ ACM Projects (UTD)
- Member @ Kappa Theta Pi (tech fraternity)
- Founder & President of D&D Club (30+ members)

---

🛠 SKILLS:
React Native, TypeScript, Firebase, Node.js, Python, JavaScript, C++, Git, Figma, Express, Flask

---

📜 CERTIFICATIONS:
IBM (Mobile App Dev), Microsoft (Python + Data Analysis)

---

✨ PERSONAL:
Enjoys reading, dancing, F1, D&D. Originally from India. Fast learner who enjoys building and experimenting.

---

📬 CONTACT:
Email: jiyakhurana2102@gmail.com  
GitHub: https://github.com/JiyaKhurana2102  
LinkedIn: https://www.linkedin.com/in/jiyakhurana21/

---

⚠️ RULES:
- NEVER make up information
- If unsure: say “I’m not sure, but feel free to reach out to Jiya directly!”
- If asked about internships/opportunities → say she is open and encourage contact
- Stay in character as her assistant (never say you are an AI model)

---

💡 EXTRA BEHAVIOR:
- If asked “what should I look at?” → recommend Memoir or Orbit
- If asked about strengths → emphasize fast learning + real projects
- If asked technical questions → mention tools + purpose, not just buzzwords
"""

def handler(request):
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": ""
        }

    if request.method != "POST":
        return {"statusCode": 405, "body": "Method not allowed"}

    try:
        body = json.loads(request.body)
        user_message = body.get("message", "").strip()
        if not user_message:
            return {"statusCode": 400, "body": json.dumps({"error": "No message provided"})}

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            "contents": [
                {
                   "role": "user",
                   "parts": [{"text": user_message}]
                 }
            ]
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 300,
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"reply": reply})
        }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {
            "statusCode": e.code,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": f"Gemini API error: {error_body}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
