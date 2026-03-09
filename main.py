import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 1. إعداد نظام التسجيل (Logging) لمراقبة الأداء والأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. جلب التوكن (تأكد من ضبطه في متغيرات البيئة أو وضعه هنا مباشرة)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- الدالات الأساسية (Handlers) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الترحيب بالمستخدم عند إرسال /start"""
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"أهلاً {user}! 💻\n"
        "أنا بوت مساعد مبرمج بـ Python.\n"
        "جاهز لمساعدتك في مراقبة مهام الرندر الخاصة بك."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة الأوامر"""
    await update.message.reply_text(
        "قائمة الأوامر:\n"
        "/start - بدء التشغيل\n"
        "/render_status - فحص حالة الرندر الحالية\n"
        "/help - المساعدة"
    )

async def render_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مثال لمحاكاة فحص حالة الرندر"""
    # هنا يمكنك برمجياً فحص استهلاك المعالج أو وجود ملفات ناتجة
    await update.message.reply_text("⏳ جاري فحص الجهاز... الرندر مستمر بنسبة إنجاز تقريبية 75%.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على الرسائل العادية (Echo)"""
    text = update.message.text
    await update.message.reply_text(f"وصلتني رسالتك: {text}")

# --- تشغيل المحرك الرئيسي ---

def main():
    if not BOT_TOKEN:
        print("❌ خطأ: لم يتم العثور على BOT_TOKEN. تأكد من إعداده!")
        return

    # بناء تطبيق التليجرام
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # ربط الأوامر بالدالات الخاصة بها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("render_status", render_status))

    # ربط الرسائل العادية (تصفية الأوامر لتجنب التكرار)
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🚀 البوت يعمل الآن بنجاح...")
    application.run_polling()

if __name__ == '__main__':
    main()

