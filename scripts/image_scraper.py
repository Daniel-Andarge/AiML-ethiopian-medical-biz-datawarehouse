import os
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos
from dotenv import load_dotenv
from datetime import datetime, timezone


# Load environment variables
load_dotenv()

# Configuration
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")



# Directory to save images
SAVE_DIR = 'telegram_images'

# Create save directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

# Connect to Telegram
client = TelegramClient(phone, api_id, api_hash)

# Function to download images
async def download_images(channel, start_date=None, end_date=None, max_images=None):
    image_count = 0
    async for message in client.iter_messages(channel, filter=InputMessagesFilterPhotos):
        message_date = message.date.replace(tzinfo=timezone.utc)  # Make message date timezone aware
        if (start_date and message_date < start_date) or (end_date and message_date > end_date):
            continue
        if max_images and image_count >= max_images:
            break
        # Download the photo
        await client.download_media(message.photo, file=os.path.join(SAVE_DIR, f'{message.id}.jpg'))
        image_count += 1
channel_name = 'lobelia4cosmetics'
# Start the client
with client:
    # Run the function to download images from the channel
    client.loop.run_until_complete(download_images(channel_name,start_date=datetime(2024, 4, 1, tzinfo=timezone.utc), end_date=datetime(2024, 6, 10, tzinfo=timezone.utc),max_images=100))

