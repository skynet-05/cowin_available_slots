import datetime
from telegram.ext import *
import config
import requests
import logging

URL = "https://api.telegram.org/bot{}/".format(config.token)

now=datetime.datetime.now()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def start(update, context):
    update.message.reply_text('Hi!, This bot updates you on available vaccine slots. Type /slots to view current free slots')


def help(update, context):
    update.message.reply_text('Type /slots to view current free slots')

def update_slots(update, context):
    d_id = '294'
    date = now.strftime("%d-%m-%Y")
    cowin_url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={d_id}&date={date}'
    browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.3'}
    response = requests.get(cowin_url, headers=browser_header)
    data_slots=response.json()
    final_text = ''
    if len(data_slots['sessions'])==0:
        print("\nSlots Not Available\n")
        update.message.reply_text("Slots Not Available")
    else:
        for slots in data_slots['sessions']:
            final_text = final_text + "\nName: "+str(slots['name']) +'\n'+ "Available Capacity: "+str(slots['available_capacity']) +'\n' + "Available Capacity for Dose1: "+str(slots['available_capacity_dose1']) +'\n' + "Available Capacity for Dose2: "+str(slots['available_capacity_dose2']) +'\n' + "Min Age Limit: "+str(slots['min_age_limit']) +'\n' + "Vaccine: "+str(slots['vaccine'])+ '\n'
            final_text = final_text + '----------------------------------------'
    update.message.reply_text(final_text)

def slots():
    global URL
    d_id = '294'
    date = now.strftime("%d-%m-%Y")
    cowin_url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={d_id}&date={date}'
    browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.3'}
    response = requests.get(cowin_url, headers=browser_header)
    data_slots=response.json()
    final_text = ''
    if len(data_slots['sessions'])==0:
        print("\nSlots Not Available\n")
    else:
        for slots in data_slots['sessions']:
            final_text = final_text + "\nName: "+str(slots['name']) +'\n'+ "Available Capacity: "+str(slots['available_capacity']) +'\n' + "Available Capacity for Dose1: "+str(slots['available_capacity_dose1']) +'\n' + "Available Capacity for Dose2: "+str(slots['available_capacity_dose2']) +'\n' + "Min Age Limit: "+str(slots['min_age_limit']) +'\n' + "Vaccine: "+str(slots['vaccine'])+ '\n'
            final_text = final_text + '----------------------------------------'
    
    URL=URL+"sendMessage?chat_id=@cowinbbmpslots&text={}".format(final_text)
    get_url(URL)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(config.token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("slots", update_slots))
    slots()
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
