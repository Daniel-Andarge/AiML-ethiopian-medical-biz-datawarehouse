import os
import logging
import asyncio
import csv
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    filename='data_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Telegram API credentials from environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')

# Telegram channel URLs to scrape
channel_urls = [
    'https://t.me/DoctorsET',
    'https://t.me/lobelia4cosmetics',
    'https://t.me/yetenaweg',
    'https://t.me/EAHCI'
]

# Directory to save CSV files
csv_directory = os.getenv('CSV_DIRECTORY', '../data/raw')

async def start_telegram_client():
    """Start the Telegram client and handle authentication."""
    client = TelegramClient(phone_number, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            await client.sign_in(phone_number, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Enter your password: '))
        except PhoneCodeInvalidError:
            logging.error('Invalid code. Please try again.')
            return None
    return client

async def extract_telegram_data(client):
    """Extract data from Telegram channels."""
    for channel_url in channel_urls:
        try:
            channel = await client.get_entity(channel_url)
            messages = await client.get_messages(channel, limit=100)
            data = [{
                'channel': channel.title,
                'message_id': message.id,
                'content': message.message,
                'timestamp': message.date,
                'views': message.views,
                'message_link': f'https://t.me/{channel.username}/{message.id}' if channel.username else None
            } for message in messages]
            df = pd.DataFrame(data)
            save_to_csv(df, channel.title)
        except Exception as e:
            logging.error(f'Error extracting data from {channel_url}: {e}')


def save_to_csv(df, channel_title):
    """Save DataFrame to a CSV file."""
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)
    csv_file_path = os.path.join(csv_directory, f'{channel_title}.csv')
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(df.columns)
            # Write data rows
            for index, row in df.iterrows():
                writer.writerow(row)
        logging.info(f'Saved data to CSV file: {csv_file_path}')
    except Exception as e:
        logging.error(f'Error saving data to CSV file: {e}')


async def main():
    """Main function to orchestrate the data pipeline."""
    client = await start_telegram_client()
    if client:
        await extract_telegram_data(client)
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
