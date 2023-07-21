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
Hi there, I'am TikTok Watermark Remover Bot.
I'am here to remove watermarks from TikTok videos.\nJust send the link and i will send you the video to downlaod without watermark !\n
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    link = message.text
    message_id = bot.reply_to(message,"Wait until checking URL's validity.").id
    logger.info(f'message from : {str(message.from_user.id)} link : {str(message.text)}')
    if "https://" in message.text and "tiktok.com" in message.text : 
        bot.edit_message_text(chat_id=message.from_user.id,
                              text='Converting the link ...',
                              message_id=message_id)
        
        tiktok_video_link  = get_valid_link(tiktok_link=message.text)
        logger.info(f'convert link to : {str(tiktok_video_link)}')
        if tiktok_video_link :
            bot.edit_message_text(text="Removing watermark ...",
                                  chat_id=message.from_user.id,
                                  message_id=message_id) 
            video_link = download_video(tiktok_video_link)
            if video_link :
                bot.edit_message_text(text=f"Watermark was removed successfully 👌",
                                      chat_id=message.from_user.id,
                                      message_id=message_id)
                bot.send_video(message.from_user.id,
                               video_link)
                return
            
            bot.edit_message_text(text="Unable to remove watermark ❌",
                                  chat_id=message.from_user.id,
                                  message_id=message_id) 
            return
        bot.edit_message_text(chat_id= message.from_user.id,
                              text="Unable to convert the link.",
                              message_id=message_id)
        return
    bot.edit_message_text(chat_id= message.from_user.id,
                          text="Please enter a valid TikTok link.",
                          message_id=message_id)
            
        
                   




        


    bot.send_message(message.from_user.id,
                     )
bot.infinity_polling()