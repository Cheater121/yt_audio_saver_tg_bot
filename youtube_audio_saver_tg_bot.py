import os
import logging
import youtube_dl
import telebot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def send_audio(bot, chat_id, audio):
    bot.send_audio(chat_id, audio)

def get_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        audio_file = f"{info_dict['id']}.mp3"

    return open(audio_file, 'rb')

def on_message(message):
    chat_id = message.chat.id
    text = message.text
    if text.startswith("https://www.youtube.com") or text.startswith("https://m.youtube.com"):
        try:
            audio = get_audio(text)
            send_audio(bot, chat_id, audio)
        except Exception as e:
            bot.send_message(chat_id, "Sorry, something went wrong. Please try again.")
            logger.error(e)

if __name__ == '__main__':
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Hi, send me a YouTube video link and I'll send you the audio as an MP3 file.")

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        on_message(message)

    bot.polling()
