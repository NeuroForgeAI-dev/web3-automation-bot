"""Telegram bot with AI-powered responses."""
import os
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from services.ai_chat import AIChat
from services.database import Database

db = Database()
ai = AIChat()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Book Appointment", callback_data="book")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("📞 Contact Us", callback_data="contact")],
    ]
    await update.message.reply_text(
        "👋 Welcome to NeuroForge AI!\n\n"
        "I can help you with:\n"
        "• 📅 Booking appointments\n"
        "• ❓ Answering questions\n"
        "• 📞 Connecting with our team\n\n"
        "Choose an option below or ask me anything!",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Main menu\n"
        "/book - Schedule appointment\n"
        "/faq - Frequently asked questions\n"
        "/contact - Get in touch\n"
        "/help - This message"
    )


async def book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 To book an appointment, please provide:\n"
        "1. Your name\n"
        "2. Preferred date (YYYY-MM-DD)\n"
        "3. Service needed\n\n"
        "Example: John, 2026-03-15, AI Avatar Creation"
    )
    context.user_data["awaiting_booking"] = True


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faqs = [
        "**Q: What services do you offer?**\nA: AI avatars, smart contract audits, web development, automation bots.",
        "**Q: How much does it cost?**\nA: Starting from $300 for basic projects. Contact us for a quote.",
        "**Q: How long does delivery take?**\nA: 1-5 business days depending on complexity.",
    ]
    await update.message.reply_text("\n\n".join(faqs), parse_mode="Markdown")


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Contact NeuroForge AI:\n\n"
        "🌐 GitHub: github.com/NeuroForgeAI-dev\n"
        "📧 Email: neuroforge2026@gmail.com\n"
        "💬 Discord: neuroforgeai"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_booking"):
        db.create_booking(update.effective_user.id, update.message.text)
        context.user_data["awaiting_booking"] = False
        await update.message.reply_text("✅ Booking created! We will confirm shortly.")
        return

    # AI-powered response
    response = ai.chat(update.message.text)
    await update.message.reply_text(response)

    # Log as lead
    db.save_lead(update.effective_user.id, update.effective_user.username, update.message.text)


def run_telegram():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("book", book))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
