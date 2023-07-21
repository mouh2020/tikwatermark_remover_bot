import telebot
from config import bot_token
from utils import get_valid_link,download_video
from loguru import logger


logger.add("watermark_bot.log",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function} | {message}",colorize=False,enqueue=True,mode="w")

bot = telebot.TeleBot(bot_token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\n
Hi there, I'am Watermark Remover Bot.
I'am here to remove watermark from TikTok videos. Just send the link and i will send you the video to downlaod without watermark !\n
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    link = message.text
    message_id = bot.reply_to(message,"Wait until checking URL's validity.").id
    if "https://" in message.text and "tiktok.com" in message.text : 
        bot.edit_message_text('Converting the link ...')
        tiktok_video_link : str = get_valid_link(tiktok_link=message.text)
        if tiktok_video_link :
            bot.edit_message_text(f"Removing watermark ...",
                                chat_id=message.from_user.id,
                                message_id=message_id) 
            video_link = download_video(tiktok_video_link)
            if video_link :
                bot.edit_message_text(f"Watermark was removed successfully 👌",
                                        chat_id=message.from_user.id,
                                        message_id=message_id)
                bot.send_video(message.from_user.id,
                               video_link)
                return
            
            bot.edit_message_text(f"Unable to remove watermark ❌",
                             chat_id=message.from_user.id,
                             message_id=message_id) 
            return
        bot.edit_message_text("Unable to convert the link.")
        return
    bot.edit_message_text("Please enter a valid TikTok link.")
            
        
                   




        


    bot.send_message(message.from_user.id,
                     )
bot.infinity_polling()