import asyncio
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import Database

class FileStoreBot:
    def __init__(self):
        self.app = Client(
            "FileStoreBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN
        )
        self.db = Database()

    async def start(self):
        await self.app.start()
        print("Bot started...")
        await self.app.idle()

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.start())

    async def setup_handlers(self):
        @self.app.on_message(filters.command("start"))
        async def start_command(client, message):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Help", callback_data="help"),
                 InlineKeyboardButton("About", callback_data="about")],
                [InlineKeyboardButton("CREATE MY OWN CLONE", callback_data="clone")],
                [InlineKeyboardButton("Update Channel", url="https://t.me/your_channel")]
            ])

            await message.reply_text(
                "🚀 Build Your Own File Store Bot with @juststoreitbot\n\n"
                "No coding needed! Get a powerful, feature-packed bot to store, "
                "share, and manage your files with ease...",
                reply_markup=keyboard
            )

        @self.app.on_callback_query(filters.regex("help"))
        async def help_callback(client, callback_query):
            help_text = (
                "✨ Help Menu\n\n"
                "I am a permanent file store bot...\n\n"
                "📚 Available Commands:\n"
                "➛ /start - check i am alive.\n"
                "➛ /genlink - To store a single message or file.\n"
                "➛ /batch - To store multiple messages from a channel.\n"
                # ... rest of help text
            )
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data="start")
            ]])
            await callback_query.message.edit_text(help_text, reply_markup=keyboard)

        @self.app.on_message(filters.command("genlink"))
        async def generate_link(client, message):
            if not message.reply_to_message:
                await message.reply_text("Please reply to a file to generate link.")
                return

            file_message = await message.reply_to_message.forward(Config.DATABASE_CHANNEL)
            share_link = f"https://t.me/{(await client.get_me()).username}?start=file_{file_message.id}"
            await message.reply_text(f"Here's your file link:\n{share_link}")

        # Add more handlers for batch, clone, etc.

if __name__ == "__main__":
    bot = FileStoreBot()
    bot.run()