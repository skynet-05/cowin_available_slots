import datetime
from telegram.ext import *
import config
import requests
import logging
from threading import Thread
import schedule
import time
from discord_webhook import DiscordWebhook

URL = "https://api.telegram.org/bot{}/".format(config.token)

now=datetime.datetime.now()

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def slots():
    global URL
    d_id = '294'
    date = now.strftime("%d-%m-%Y")
    cowin_url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={d_id}&date={date}'
    browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.3'}
    responsess = requests.get(cowin_url, headers=browser_header)
    data_slots=responsess.json()
    final_text = ''
    if len(data_slots['sessions'])==0:
        print("\nSlots Not Available\n")
    else:
        for slots in data_slots['sessions']:
            if slots['min_age_limit']==18 and slots['available_capacity_dose1']!=0:
                final_text = final_text + "\nName: "+str(slots['name']) +'\n'+ "Available Capacity: "+str(slots['available_capacity']) +'\n' + "Available Capacity for Dose1: "+str(slots['available_capacity_dose1']) +'\n' + "Available Capacity for Dose2: "+str(slots['available_capacity_dose2']) +'\n' + "Min Age Limit: "+str(slots['min_age_limit']) +'\n' + "Vaccine: "+str(slots['vaccine'])+ '\n'
                final_text = final_text + '----------------------------------------'
    
    URL = f"https://api.telegram.org/bot{config.token}/sendMessage?chat_id=@cowinbbmpslots&text={final_text}"
    get_url(URL)
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/844520658242109475/wwoStY69vUGMoJi1yOr4wirvVR0hDr6Mzqb0Y_BPo31NZPSKlxTQ_kuPPxJ5rVbChz25', content=final_text)
    response = webhook.execute()

# schedule.every(2).minutes.do(slots)
schedule.every(10).seconds.do(slots)

while True:
    schedule.run_pending()
    time.sleep(1)