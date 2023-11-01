import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Initialize your Telegram Bot
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telegram.Bot(token=bot_token)

# Define a function to handle /start command
def start(update, context):
    update.message.reply_text("Welcome to the File Renaming Bot. Send a file to rename it.")

# Define a function to handle file messages
def handle_file(update, context):
    # Check if a file is attached
    if update.message.document:
        file_id = update.message.document.file_id
        file_info = bot.get_file(file_id)
        file_extension = os.path.splitext(file_info.file_path)[-1]
        
        # Rename the file (You can implement your renaming logic here)
        new_file_name = "new_filename" + file_extension
        
        # Download the file and save it with the new name
        file_info.download(new_file_name)
        
        # Send the renamed file back to the user
        update.message.reply_document(document=open(new_file_name, 'rb'))
        
        # Clean up by deleting the downloaded file
        os.remove(new_file_name)

def main():
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
