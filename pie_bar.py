import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
import datetime
import time
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt_bar
import matplotlib.pyplot as plt_map
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt2_bar
import numpy as np
from matplotlib import rc
from datetime import datetime
import telebot
from io import BytesIO
import telegram
import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
matplotlib.use('agg')
explode = (0.05, 0.0, 0.0, 0.0, 0.0)
now = datetime.now()

bot_token = 'token'
bot = telebot.TeleBot(bot_token)
chat_id= '-1001900597631'

values = Counter()
values2 = Counter()


font = {'family': 'Verdana',
        'weight': 'normal',
        'size'  : 8}
rc('font', **font)


def monthly():
    token = ""

    payload_token = json.dumps({
        "username": "",
        "password": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response_token = requests.request("POST", token, headers=headers, data=payload_token)

    jtoken = response_token.json()
    access = jtoken['access_token']
    print(access)

    url = ""

    payload = {}
    headers = {
        'Authorization': f'Bearer {access}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    i = 0
    onemonth = f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z'
    print(f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z')
    while i < len(data['items']) and data['items'][i]['created_at'] > onemonth:
        strana = json.dumps(data['items'][i]['country'], indent=4)
        proekt = json.dumps(data['items'][i]['project'], indent=4)
        vremya = json.dumps(data['items'][i]['created_at'], indent=4)
        if strana.lower() != "uzbekistan":
            values[strana] += 1
            values2[proekt] += 1
            print(f"{proekt}  {strana} {vremya}")
            i += 1

    url_2 = ""

    payload = {}
    headers = {
        'Authorization': f'Bearer {access}'
    }
    response = requests.request("GET", url_2, headers=headers, data=payload)
    data = response.json()

    i = 0
    onemonth = f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z'
    print(f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z')
    while i < len(data['items']) and data['items'][i]['created_at'] > onemonth:
        strana = json.dumps(data['items'][i]['country'], indent=4)
        proekt = json.dumps(data['items'][i]['project'], indent=4)
        vremya = json.dumps(data['items'][i]['created_at'], indent=4)
        if strana.lower() != "uzbekistan":
            values[strana] += 1
            values2[proekt] += 1
            print(f"{proekt}  {strana} {vremya}")
            i += 1

    url_3 = ""

    payload = {}
    headers = {
        'Authorization': f'Bearer {access}'
    }
    response = requests.request("GET", url_3, headers=headers, data=payload)
    data = response.json()

    i = 0
    onemonth = f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z'
    print(f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z')
    while i < len(data['items']) and data['items'][i]['created_at'] > onemonth:
        strana = json.dumps(data['items'][i]['country'], indent=4)
        proekt = json.dumps(data['items'][i]['project'], indent=4)
        vremya = json.dumps(data['items'][i]['created_at'], indent=4)
        if strana.lower() != "uzbekistan":
            values[strana] += 1
            values2[proekt] += 1
            print(f"{proekt}  {strana} {vremya}")
            i += 1


    bot.send_message(chat_id, text=f"Monthly report ({onemonth} - {datetime.now().isoformat()})")
    del values['"Uzbekistan"']
    print(values)
    top_results = values.most_common(5)
    labels = [str(value) for value, count in top_results]
    sizes = [count for value, count in top_results]

    # BAR COUNTRIES
    plt_bar.style.use('dark_background')
    bar_colors = ['#D95B5B', '#DF73AD', '#DAAEE5', '#877FE4', '#68B9E6']
    fig, ax = plt_bar.subplots(facecolor='black')
    plt_bar.figure(figsize=(15, 9), dpi=100, facecolor='black')
    # plt.subplots_adjust(top=0.9, bottom=0.25, left=0.11, right=0.9)
    plt_bar.bar(labels, sizes, color=bar_colors )  # создаем столбчатую диаграмму
    plt_bar.xlabel('Countries', color='white')
    plt2_bar.xticks(color='white')
    plt_bar.ylabel('Forms', color='white')
    plt_bar.yticks(color='white')
    plt_bar.title(f'Monthly countries bar chart',fontsize=25, color="white")
    plt.gcf().set_facecolor('black')
    buf_bar = BytesIO()
    ax.set_facecolor('black')
    plt_bar.savefig(buf_bar, format='png',dpi=100)
    file_name = "monthly_country_bar.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf_bar.getbuffer())
    buf_bar.seek(0)
    bot.send_photo(chat_id, photo=buf_bar)
    plt_bar.clf()

    # PIE COUNTRIES
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=bar_colors,textprops={'color': 'white'}, explode = explode)
    plt.title(f'Monthly countries pie chart',fontsize=25, color='white')
    plt.axis('equal')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    file_name = "monthly_country_pie.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf.getbuffer())
    buf.seek(0)
    bot.send_photo(chat_id, photo=buf)
    plt.clf()

    print(values2)

    top_results_project = values2.most_common(5)
    labels_project = [str(value2) for value2, count in top_results_project]
    sizes_project = [count for value2, count in top_results_project]

    # BAR PROJECTS
    plt2_bar.bar(labels_project, sizes_project, color=bar_colors)
    plt2_bar.xlabel('Projects')
    plt2_bar.ylabel('Forms')
    plt2_bar.title(f'Monthly projects bar chart ',fontsize=25, color='white')
    buf2_bar = BytesIO()
    plt2_bar.savefig(buf2_bar, format='png')
    file_name = "monthly_project_bar.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf2_bar.getbuffer())
    buf2_bar.seek(0)
    bot.send_photo(chat_id, photo=buf2_bar)
    plt2_bar.clf()

    # PIE PROJECTS
    plt2.pie(sizes_project, labels=labels_project, autopct='%1.1f%%',colors=bar_colors, explode = explode)
    plt2.title(f'Monthly projects pie chart ',fontsize=25,color='white')
    plt2.axis('equal')
    buf2 = BytesIO()
    plt2.savefig(buf2, format='png')
    file_name = "monthly_project_pie.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf2.getbuffer())
    buf2.seek(0)
    bot.send_photo(chat_id, photo=buf2)
    plt2.clf()


def daily():
    token = "https://form.sales-inquiries.ae/api/users/login/"

    payload_token = json.dumps({
        "username": "enver",
        "password": "J3d5689kw2"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response_token = requests.request("POST", token, headers=headers, data=payload_token)

    jtoken = response_token.json()
    access = jtoken['access_token']
    print(access)

    url = ""

    payload = {}
    headers = {
        'Authorization': f'Bearer {access}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    i = 0
    oneday = f'{(datetime.now() - relativedelta(hours=24)).isoformat()}Z'
    print(f'{(datetime.now() - relativedelta(hours=24)).isoformat()}Z')
    while i < len(data['items']) and data['items'][i]['created_at'] > oneday:
        strana = json.dumps(data['items'][i]['country'], indent=4)
        proekt = json.dumps(data['items'][i]['project'], indent=4)
        vremya = json.dumps(data['items'][i]['created_at'], indent=4)
        values[strana] += 1
        values2[proekt] += 1
        print(f"{proekt}  {strana} {vremya}")
        i += 1

    bot.send_message(chat_id, text=f"Daily report ({oneday} - {datetime.now().isoformat()})")
    del values['"Uzbekistan"']
    print(values)
    top_results = values.most_common(5)
    labels = [str(value) for value, count in top_results]
    sizes = [count for value, count in top_results]
    border_colors = ['black', 'black', 'black', 'black', 'black']
    # BAR COUNTRIES

    plt_bar.style.use('dark_background')
    bar_colors = ['#D95B5B', '#DF73AD', '#DAAEE5', '#877FE4', '#68B9E6']
    fig, ax = plt_bar.subplots(facecolor='black')
    plt_bar.figure(figsize=(15, 9), dpi=100, facecolor='black')
    # plt.subplots_adjust(top=0.9, bottom=0.25, left=0.11, right=0.9)
    plt_bar.bar(labels, sizes, color=bar_colors)  # создаем столбчатую диаграмму
    plt_bar.xlabel('Countries', color='white')
    plt2_bar.xticks(color='white')
    plt_bar.ylabel('Forms', color='white')
    plt_bar.yticks(color='white')
    plt_bar.title(f'Daily countries bar chart',fontsize=25, color="white")
    plt.gcf().set_facecolor('black')
    buf_bar = BytesIO()
    ax.set_facecolor('black')
    plt_bar.savefig(buf_bar, format='png', dpi=100)
    file_name = "daily_country_bar.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf_bar.getbuffer())
    buf_bar.seek(0)
    bot.send_photo(chat_id, photo=buf_bar)
    plt_bar.clf()

    # PIE COUNTRIES
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=bar_colors, textprops={'color': 'white'}, explode = explode)
    plt.axis('equal')
    plt.title(f'Daily countries pie chart', fontsize=25, color="white")
    buf = BytesIO()
    plt.savefig(buf, format='png',dpi=100)
    file_name = "daily_country_pie.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf.getbuffer())
    buf.seek(0)
    bot.send_photo(chat_id, photo=buf)
    plt.clf()

    print(values2)

    top_results_project = values2.most_common(5)
    labels_project = [str(value2) for value2, count in top_results_project]
    sizes_project = [count for value2, count in top_results_project]

    # BAR PROJECTS
    plt2_bar.bar(labels_project, sizes_project, color=bar_colors)
    plt2_bar.xlabel('Projects')
    plt2_bar.ylabel('Forms')
    plt2_bar.title(f'Daily projects bar chart',fontsize=25, color="white")
    buf2_bar = BytesIO()
    plt2_bar.savefig(buf2_bar, format='png')
    file_name = "daily_project_bar.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf2_bar.getbuffer())
    buf2_bar.seek(0)
    bot.send_photo(chat_id, photo=buf2_bar)
    plt2_bar.clf()

    # PIE PROJECTS
    plt2.pie(sizes_project, labels=labels_project, autopct='%1.1f%%', colors=bar_colors, explode = explode)
    plt2.axis('equal')
    plt2.title(f'Daily projects pie chart', fontsize=25, color="white")
    buf2 = BytesIO()
    plt2.savefig(buf2, format='png')
    file_name = "daily_project_pie.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf2.getbuffer())
    buf2.seek(0)
    bot.send_photo(chat_id, photo=buf2)
    plt2.clf()

def weekly():
    token = ""

    payload_token = json.dumps({
        "username": "",
        "password": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response_token = requests.request("POST", token, headers=headers, data=payload_token)

    jtoken = response_token.json()
    access = jtoken['access_token']
    print(access)

    url = ""

    payload = {}
    headers = {
        'Authorization': f'Bearer {access}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    i = 0
    oneweek = f'{(datetime.now() - relativedelta(hours=168)).isoformat()}Z'
    print(f'{(datetime.now() - relativedelta(hours=168)).isoformat()}Z')
    while i < len(data['items']) and data['items'][i]['created_at'] > oneweek:
        strana = json.dumps(data['items'][i]['country'] , indent=4)
        proekt = json.dumps(data['items'][i]['project'], indent=4)
        vremya = json.dumps(data['items'][i]['created_at'], indent=4)
        values[strana] += 1
        values2[proekt] += 1
        print (f"{proekt}  {strana} {vremya}")
        i += 1

    bot.send_message(chat_id, text=f"Weekly report ({oneweek} - {datetime.now().isoformat()})")
    del values['"Uzbekistan"']
    print(values)
    top_results = values.most_common(5)
    labels = [str(value) for value, count in top_results]
    sizes = [count for value, count in top_results]

    # BAR COUNTRIES
    plt_bar.style.use('dark_background')
    bar_colors = ['#D95B5B', '#DF73AD', '#DAAEE5', '#877FE4', '#68B9E6']
    fig, ax = plt_bar.subplots(facecolor='black')
    plt_bar.figure(figsize=(15, 9), dpi=100, facecolor='black')
    # plt.subplots_adjust(top=0.9, bottom=0.25, left=0.11, right=0.9)
    plt_bar.bar(labels, sizes, color=bar_colors)  # создаем столбчатую диаграмму
    plt_bar.xlabel('Countries', color='white')
    plt_bar.xticks(color='white')
    plt_bar.ylabel('Forms', color='white')
    plt_bar.yticks(color='white')
    plt_bar.title(f'Weekly countries bar chart',fontsize=25, color="white")
    plt.gcf().set_facecolor('black')
    buf_bar = BytesIO()
    ax.set_facecolor('black')
    plt_bar.savefig(buf_bar, format='png', dpi=100)
    file_name = "weekly_country_bar.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf_bar.getbuffer())
    buf_bar.seek(0)
    bot.send_photo(chat_id, photo=buf_bar)
    plt_bar.clf()

    # PIE COUNTRIES
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=bar_colors, textprops={'color': 'white'}, explode = explode)
    plt.axis('equal')
    plt.title(f'Weekly countries pie chart', fontsize=25, color="white")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    file_name = "weekly_country_pie.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf.getbuffer())
    buf.seek(0)
    bot.send_photo(chat_id, photo=buf)
    plt.clf()

    print(values2)

    top_results_project = values2.most_common(5)
    labels_project = [str(value2) for value2, count in top_results_project]
    sizes_project = [count for value2, count in top_results_project]

    # BAR PROJECTS
    plt2_bar.bar(labels_project, sizes_project, color=bar_colors)
    plt2_bar.xlabel('Projects')
    plt2_bar.ylabel('Forms')
    plt2_bar.title(f'Weekly projects bar chart',fontsize=25, color="white")
    buf2_bar = BytesIO()
    plt2_bar.savefig(buf2_bar, format='png')
    file_name = "weekly_project_bar.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf2_bar.getbuffer())
    buf2_bar.seek(0)
    bot.send_photo(chat_id, photo=buf2_bar)
    plt2_bar.clf()

    # PIE PROJECT
    plt2.pie(sizes_project, labels=labels_project, autopct='%1.1f%%', colors=bar_colors, explode = explode)
    plt2.axis('equal')
    plt2.title(f'Weekly projects pie chart',fontsize=25, color="white")
    buf2 = BytesIO()
    plt2.savefig(buf2, format='png')
    file_name = "weekly_project_pie.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf2.getbuffer())
    buf2.seek(0)
    bot.send_photo(chat_id, photo=buf2)
    plt2.clf()


daily()
weekly()
monthly()

# scheduler = BlockingScheduler()
# #EVERY MINUTE
# scheduler.add_job(daily, 'cron', day_of_week='*', hour='*', minute='*')

# # Каждый день в 00:01
# scheduler.add_job(daily, 'cron', day_of_week='*', hour='0', minute='1')
#
# # Каждый понедельник в 00:10
# scheduler.add_job(weekly, 'cron', day_of_week='mon', hour='0', minute='10')
#
# # Каждое первое число месяца в 00:20
# scheduler.add_job(monthly, 'cron', day='1', hour='0', minute='20')

# scheduler.start()


