from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv
from os import getenv
import re
import asyncio

from rest import rest
from hyper_image import generate_image

load_dotenv()

user_data = {}

def is_bearer_token(token):
    pattern = r"^Bearer\s+[a-zA-Z0-9\-_\.]+(\.[a-zA-Z0-9\-_\.]+){2}$"
    return bool(re.match(pattern, token))

def models():
    keyboard = [
        [
            InlineKeyboardButton("FLUX.1-dev", callback_data="FLUX.1-dev"),
            InlineKeyboardButton("SDXL1.0-base", callback_data="SDXL1.0-base")
        ],
        [
            InlineKeyboardButton("SD1.5", callback_data="SD1.5"),
            InlineKeyboardButton("SSD", callback_data="SSD")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def auto_manual():
    keyboard = [
        [
            InlineKeyboardButton("Auto mode", callback_data="auto"),
            InlineKeyboardButton("Manual mode", callback_data="manual")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def send_image_loop(message, context: ContextTypes.DEFAULT_TYPE, user_id, stop_event):
    while not stop_event.is_set():
        try:
            await send_image(message, context, user_id)
            await asyncio.sleep(0.1)  
            rest()
        except Exception as e:
            await message.reply_text(f"Error in loop: {e}")
            break

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer() 
    
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {"model": None, "mode": None, "running": False, "stop_event": asyncio.Event()}
    
    if query.data in  ["FLUX.1-dev","SDXL1.0-base","SD1.5","SSD"]:
        if query.data == "FLUX.1-dev":
            user_data[user_id]["model"] = 0
            await query.message.reply_text("Run Model FLUX.1-dev in auto or manual mode?",reply_markup=auto_manual())
        elif query.data == "SDXL1.0-base":
            user_data[user_id]["model"] = 1
            await query.message.reply_text("Run Model SDXL1.0-base in auto or manual mode?",reply_markup=auto_manual())
        elif query.data == "SD1.5":
            user_data[user_id]["model"] = 2
            await query.message.reply_text("Run Model SD1.5 in auto or manual mode?",reply_markup=auto_manual())
        elif query.data == "SSD":
            user_data[user_id]["model"] = 3
            await query.message.reply_text("Run Model SSD in auto or manual mode?",reply_markup=auto_manual())
    elif query.data in ["auto", "manual"]:
        user_data[user_id]["mode"] = query.data
        if query.data == "auto":
            await query.message.reply_text("Starting in auto mode.... Please wait")
            user_data[user_id]["stop_event"].clear()  
            asyncio.create_task(send_image_loop(query.message, context, user_id, user_data[user_id]["stop_event"]))
        elif query.data == "manual":
            if "stop_event" in user_data[user_id]:
                user_data[user_id]["stop_event"].set()  

async def send_image(message, context: ContextTypes.DEFAULT_TYPE, user_id):
    try:
        model = user_data[user_id]["model"]
        token = user_data[user_id]["token"]
        image = generate_image(model, token)
        image_buffer = image[1]
        
        await message.reply_text(image[0])

        if image_buffer:
            try:
                await context.bot.send_photo(chat_id=message.chat.id, photo=image_buffer, filename="imagine.png")
                image_buffer.close()
            except Exception as e:
                await message.reply_text(f"Error sending image: {e}")
        else:
            await message.reply_text("Failed to decode the image.")
    except Exception as e:
        await message.reply_text(f"Error generating image: {e}\n\nPlease click /start to restart")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {"model": None, "mode": None, "token": None, "stop_event": asyncio.Event()}
        if not user_data[user_id].get("token"):
            await update.message.reply_text("Please run /settoken first")
    else:
        if "stop_event" not in user_data[user_id]:
            user_data[user_id]["stop_event"] = asyncio.Event()
        await update.message.reply_text("Hello! Which Image model do you want to run?",reply_markup=models())

async def set_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please enter your token:")
    context.user_data["awaiting_token"] = True

async def help_setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Use /start to start the bot\n\nUse /settoken to set your API")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if update.message.text == "/stop":
        if user_id in user_data and "stop_event" in user_data[user_id]:
            user_data[user_id]["stop_event"].set()  
            await update.message.reply_text("Auto mode stopped.")
        else:
            await update.message.reply_text("No auto mode running.")
    if context.user_data.get("awaiting_token", False):
        token = update.message.text
        if is_bearer_token(token):
            user_id = update.effective_user.id
            if user_id not in user_data:
                user_data[user_id] = {"model": None, "mode": None, "token": None, "stop_event": asyncio.Event()}
            user_data[user_id]["token"] = token
            await update.message.reply_text("Token set successfully!. Run /start")
            context.user_data["awaiting_token"] = False
        else:
            await update.message.reply_text("Invalid token. Please try again.")
    else:
        await update.message.reply_text("Unknown command. Use /start to begin.")

def main():
    application = ApplicationBuilder().token(getenv("TG_token")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_setup))
    application.add_handler(CommandHandler("settoken", set_token))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.run_polling()

if __name__ == "__main__":
    main()
