from whatsapp_chatbot_python import GreenAPIBot, Notification

bot = GreenAPIBot(
    "7105440419",
    "77b88741bcc44531b820423138b142ddae420073cea843ea87"
)

WEB_OWNER = "923462831053@c.us"
VOIP_OWNER = "18639901187@c.us"
HR_NUMBER = "923462831053@c.us"

user_session = {}

# ---------------- HELPERS ----------------
def get_text(n):
    return (
        getattr(n, "message_text", None)
        or getattr(n, "text", None)
        or getattr(n, "body", None)
    )

def is_valid_name(name):
    return name.replace(" ", "").isalpha() and len(name.strip()) >= 3

def start_bot(chatId):
    user_session[chatId] = {"step": "main"}

    # -------- COMPANY LOGO --------
    bot.api.sending.sendFileByUrl(
        chatId=chatId,
        urlFile="https://i.ibb.co/21mBhZTS/Group-81.png",
        fileName="company_logo.png",
        caption=
        "👋 *Welcome to Tritechtitan  Company*🏢\n\n"
        "🌐 Website: https://tritechtitan.com/\n\n"
        "Tritechtitan Company provides professional *IT services* and *job opportunities* "
        "to help individuals and businesses grow through technology.\n\n"
        "Please reply only with:\n"
        "1️⃣ Services  ➜  Reply 1\n"
        "2️⃣ Jobs      ➜  Reply 2"

    )

# ---------------- MAIN HANDLER ----------------
@bot.router.message()
def handler(notification: Notification):
    chatId = notification.sender
    text = get_text(notification)

    if not text and not hasattr(notification, "file_url"):
        return

    text = text.strip() if text else ""
    low = text.lower()

    # -------- SESSION NOT FOUND → FRESH START --------
    if chatId not in user_session:
        start_bot(chatId)
        return

    s = user_session[chatId]

    # -------- BACK --------
    if text == "0" and s["step"] != "main":
        start_bot(chatId)
        return

    # ================= MAIN MENU =================
    if s["step"] == "main":

        if text == "1":
            s["step"] = "services"
            bot.api.sending.sendMessage(
                chatId,
                "🛠 *Our Services*\n\n"
                "_Please reply with 1, 2 or 0_\n"
                "1️⃣ Web Development ➜ Reply 1\n"
                "2️⃣ VoIP Solutions ➜ Reply 2\n"
                "0️⃣ Back"

            )
            return

        if text == "2":
            s["step"] = "jobs"
            bot.api.sending.sendMessage(
                chatId,
                "💼 *We Are Hiring!*\n\n"
                "We are looking for talented and passionate professionals to join our growing team.\n\n"
                "📌 *Open Positions:*\n"
                "✔ Web Developer\n"
                "✔ Network Security Engineer\n"
                "✔ UI/UX Designer\n\n"
                "📎 *How to Apply:*\n"
                "Please send your updated CV / Resume here on WhatsApp.\n\n"
                "⏰ Working Hours: 6:00 PM – 2:00 AM\n"
                "📅 Saturday & Sunday Off\n\n"
                "ℹ️ After sharing your CV, our HR team will review it and contact you if shortlisted.\n\n"
                "0️⃣ Back"
            )
            return

        start_bot(chatId)
        return

    # ================= JOB FLOW =================
    if s["step"] == "jobs":

        if hasattr(notification, "file_url"):
            bot.api.sending.sendFileByUrl(
                HR_NUMBER,
                notification.file_url,
                "CV",
                caption=f"📄 *New CV Received*\nWhatsApp: {chatId}"
            )

            bot.api.sending.sendMessage(
                chatId,
                "✅ Your CV has been successfully forwarded to HR.\nThank you for applying!"
            )

            user_session.pop(chatId)
            return

        bot.api.sending.sendMessage(
            chatId,
            "📎 Please send your CV file to apply.\n\n0️⃣ Back"
        )
        return

    # ================= SERVICES =================
    if s["step"] == "services":

        if text == "1":
            s["service"] = "Web Development"
            s["step"] = "package"
            bot.api.sending.sendMessage(
                chatId,
                "🌐 *Web Development* (Select one)\n\n"
                "_Please reply with 1, 2 or 0_\n"
                "1️⃣ Business Websites ➜ Reply 1\n"
                "2️⃣ E-Commerce / Web Applications ➜ Reply 2\n"
                "0️⃣ Back"

            )
            return

        if text == "2":
            s["service"] = "VoIP"
            s["step"] = "package"
            bot.api.sending.sendMessage(
                chatId,
                "☎️ *VoIP Solutions* (Select one)\n\n"
                "_Please reply with 1, 2 or 0_\n"
                "1️⃣ Small Business Setup ➜ Reply 1\n"
                "2️⃣ Enterprise Call Center ➜ Reply 2\n"
                "0️⃣ Back"

            )
            return

        return

    # ================= PACKAGE =================
    if s["step"] == "package":

        if text not in ["1", "2"]:
            bot.api.sending.sendMessage(
                chatId,
                "❌ Invalid option.\nReply with 1 or 2.\n\n0️⃣ Back"
            )
            return

        s["package"] = text
        s["user"] = {}
        s["step"] = "name"

        bot.api.sending.sendMessage(
            chatId,
            "✍️ Enter your *full name*\n"
            "(Alphabets only, minimum 3 characters)"
        )
        return

    # ================= NAME =================
    if s["step"] == "name":

        if not is_valid_name(text):
            bot.api.sending.sendMessage(
                chatId,
                "❌ Invalid name.\n"
                "Please enter a valid name (alphabets only, min 3 characters)."
            )
            return

        s["user"]["name"] = text
        s["step"] = "phone"
        bot.api.sending.sendMessage(chatId, "📱 Enter your contact number:")
        return

    if s["step"] == "phone":
        s["user"]["phone"] = text
        s["step"] = "email"
        bot.api.sending.sendMessage(chatId, "📧 Enter your email address:")
        return

    if s["step"] == "email":
        s["user"]["email"] = text
        s["step"] = "confirm"

        bot.api.sending.sendMessage(
            chatId,
            "✅ *Please confirm your request*\n\n"
            "1️⃣ YES – Confirm\n"
            "2️⃣ NO – Cancel\n"
            "0️⃣ Back"
        )
        return

    # ================= CONFIRM =================
    if s["step"] == "confirm":

        if text == "1" or low == "yes":
            owner = WEB_OWNER if s["service"] == "Web Development" else VOIP_OWNER

            bot.api.sending.sendMessage(
                owner,
                f"🧾 *New Service Request*\n\n"
                f"Service: {s['service']}\n"
                f"Option: {s['package']}\n"
                f"Name: {s['user']['name']}\n"
                f"Phone: {s['user']['phone']}\n"
                f"Email: {s['user']['email']}"
            )

            bot.api.sending.sendMessage(
                chatId,
                "✅ *Order Confirmed!*\n\n"
                "📞 Please contact our owner:\n"
                "If you need more guide contect us\n"
                "📱 *0346-2831053*\n\n"
                "Reliable & scalable solutions guaranteed ✅"
            )

            user_session.pop(chatId)
            return

        if text == "2" or low == "no":
            start_bot(chatId)
            return

        start_bot(chatId)
        return


bot.run_forever()



