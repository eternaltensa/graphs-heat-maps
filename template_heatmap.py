import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
import datetime
import time
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt_bar
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
import pandas as pd
import os
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
import telebot
import matplotlib


matplotlib.use('agg')
bot_token = 'bot token'
bot = telebot.TeleBot(bot_token)
chat_id= 'telegram chat id'



def daily():
    values = Counter()
    values2 = Counter()

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
    data1 = response.json()

    i = 0
    oneday = f'{(datetime.now() - relativedelta(hours=24)).isoformat()}Z'
    oneday_normal = (datetime.now() - relativedelta(hours=24))
    user_counts = {}

    # Анализ данных
    for item in data1["items"]:
        if item['created_at'] > oneday:
            country = item["country"]
            projects_data = item.get("projects")
            if projects_data is not None:
                project = item["projects"]["template_id"]
                if project is not None:

                    if (country, project) in user_counts:
                        user_counts[(country, project)] += 1
                    else:
                        user_counts[(country, project)] = 1

    # Вывод результатов
    countryname = country
    projectname = project
    sorted_dict = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True))
    print (sorted_dict)

    top_countries = [key[0] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    top_projects = [key[1] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    filtered_dict = {(country, project): value for (country, project), value in sorted_dict.items() if country in top_countries and project in top_projects}
    filtered_dict = {key_value: value for key_value, value in filtered_dict.items() if 'Uzbekistan' not in key_value and key_value[1] != ''}
    print (filtered_dict)

    countries = list(set(item[0] for item in filtered_dict.keys()))
    projects = list(set(item[1] for item in filtered_dict.keys()))
    print(f"len count  {len(countries)}")
    print(f"len proj {len(projects)}")
    data_matrix = np.zeros((len(countries), len(projects)))


    for key, value in filtered_dict.items():
        country_index = countries.index(key[0])
        project_index = projects.index(key[1])
        data_matrix[country_index][project_index] = value


    colors = [(0.0, '#BCC5F8'), (0.5,'#E0B5CE'),(1.0, '#F59E9E')]
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors)
    # HEATMAP BUILD
    plt.figure(figsize=(20, 15), dpi=200)
    plt.imshow(data_matrix, cmap=custom_cmap, aspect='auto', vmin=1)
    for i in range(len(countries)):
        for j in range(len(projects)):
            plt.text(j, i, str(data_matrix[i, j]), ha='center', va='center', color='black')
    plt.subplots_adjust(top=0.9, bottom=0.25, left=0.11, right=1.0)
    cbar = plt.colorbar()
    cbar.set_label('Legend', color='white')
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(axis='y', colors='white')
    plt.xticks(range(len(projects)), projects, color='white', fontsize=12)
    plt.yticks(range(len(countries)), countries, color='white', fontsize=12)
    for i in range(len(countries)):
        for j in range(len(projects)):
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, color='black', linewidth=1)
            plt.gca().add_patch(rect)
    plt.gcf().set_facecolor('black')

    plt.xlabel('Projects', color='white')
    plt.ylabel('Countries', color='white')
    plt.title(f'Country-template heatmap for {oneday_normal.strftime("%Y-%m-%d")} - {datetime.now().strftime("%Y-%m-%d")}',color='white',fontsize=25)
    plt.grid(visible=False)
    text = '1 - Dubai Hills\n 2 - Six Senses\n 3- Ava\n 4- Beachfront\n 5 - W\n 6- Elora\n 7 - Golf Grand\n 8 - Park Ridge\n 9 - Damac Bay\n 10 - Boutique\n 11 - The Community\n 12 - FB Shorts\n 13 - Phase 3\n 14 - Verona shorts\n 15 - Reeman Shorts\n 16 - Keturah Resort\n 17 - Cavali Couture'
    x_coord = 1.1
    y_coord = 0.02 - (0.25 / (0.9 - 0.25))  # OTSTUO SNIZU

    # LEGENDA SHABLONOV
    plt.text(x_coord, y_coord, text, transform=plt.gca().transAxes,
             fontsize=12, verticalalignment='bottom', horizontalalignment='right', color='white')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    file_name = "daily_template_heat.png"

    # SOHRANENIE V FILE
    with open(file_name, 'wb') as f:
        f.write(buf.getbuffer())
    buf.seek(0)
    bot.send_photo(chat_id, photo=buf)
    plt.clf()


def weekly():
    values = Counter()
    values2 = Counter()

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
    data1 = response.json()

    i = 0
    oneday = f'{(datetime.now() - relativedelta(hours=168)).isoformat()}Z'
    oneday_normal = (datetime.now() - relativedelta(hours=168))
    user_counts = {}

    for item in data1["items"]:
        if item['created_at'] > oneday:
            country = item["country"]
            projects_data = item.get("projects")
            if projects_data is not None:
                project = item["projects"]["template_id"]
                if project is not None:
                    if (country, project) in user_counts:
                        user_counts[(country, project)] += 1
                    else:
                        user_counts[(country, project)] = 1



    countryname = country
    projectname = project
    sorted_dict = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True))
    print(sorted_dict)

    top_countries = [key[0] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    top_projects = [key[1] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    filtered_dict = {(country, project): value for (country, project), value in sorted_dict.items() if
                     country in top_countries and project in top_projects}
    filtered_dict = {key_value: value for key_value, value in filtered_dict.items() if 'Uzbekistan' not in key_value and key_value[1] != ''}
    print(filtered_dict)

    countries = list(set(item[0] for item in filtered_dict.keys()))
    projects = list(set(item[1] for item in filtered_dict.keys()))
    print(f"len count  {len(countries)}")
    print(f"len proj {len(projects)}")
    data_matrix = np.zeros((len(countries), len(projects)))


    for key, value in filtered_dict.items():
        country_index = countries.index(key[0])
        project_index = projects.index(key[1])
        data_matrix[country_index][project_index] = value


    colors = [(0.0, '#BCC5F8'), (0.5,'#E0B5CE'),(1.0, '#F59E9E')]
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors,N=50)

    plt.figure(figsize=(20, 15), dpi=200)
    plt.imshow(data_matrix, cmap=custom_cmap, aspect='auto', vmin=1)
    for i in range(len(countries)):
        for j in range(len(projects)):
            plt.text(j, i, str(data_matrix[i, j]), ha='center', va='center', color='black')
    plt.subplots_adjust(top=0.9, bottom=0.25, left=0.11, right=1.0)
    cbar = plt.colorbar()
    cbar.set_label('Legend', color='white')
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(axis='y', colors='white')
    plt.xticks(range(len(projects)), projects, color='white',fontsize=12)
    plt.yticks(range(len(countries)), countries, color='white',fontsize=12)
    for i in range(len(countries)):
        for j in range(len(projects)):
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, color='black', linewidth=1)
            plt.gca().add_patch(rect)
    plt.gcf().set_facecolor('black')


    plt.xlabel('Projects',color='white')
    plt.ylabel('Countries',color='white')
    plt.title(f'Country-template heatmap for {oneday_normal.strftime("%Y-%m-%d")} - {datetime.now().strftime("%Y-%m-%d")}',color='white',fontsize=25)
    plt.grid(visible=False)
    text = '1 - Dubai Hills\n 2 - Six Senses\n 3- Ava\n 4- Beachfront\n 5 - W\n 6- Elora\n 7 - Golf Grand\n 8 - Park Ridge\n 9 - Damac Bay\n 10 - Boutique\n 11 - The Community\n 12 - FB Shorts\n 13 - Phase 3\n 14 - Verona shorts\n 15 - Reeman Shorts\n 16 - Keturah Resort\n 17 - Cavali Couture'
    x_coord = 1.1
    y_coord = 0.02 - (0.25 / (0.9 - 0.25))  # Вычисляем новую координату y с учетом отступа снизу

    # Добавляем текст
    plt.text(x_coord, y_coord, text, transform=plt.gca().transAxes,
             fontsize=12, verticalalignment='bottom', horizontalalignment='right',color='white')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    file_name = "weekly_template_heat.png"

    # Записать содержимое буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf.getbuffer())
    buf.seek(0)
    bot.send_photo(chat_id, photo=buf)
    plt.clf()


def monthly():
    values = Counter()
    values2 = Counter()

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
    data1 = response.json()

    i = 0
    oneday = f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z'
    oneday_normal = (datetime.now() - relativedelta(hours=730))
    user_counts = {}

    # Анализ данных page 1
    for item in data1["items"]:
            if item['created_at'] > oneday:
                country = item["country"]
                projects_data = item.get("projects")
                if projects_data is not None:
                    project = item["projects"]["template_id"]
                    if project is not None:
                    
                        if (country, project) in user_counts:
                            user_counts[(country, project)] += 1
                        else:
                            user_counts[(country, project)] = 1


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
    data1 = response.json()

    i = 0
    oneday = f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z'
    oneday_normal = (datetime.now() - relativedelta(hours=730))

    # Анализ данных page 1
    for item in data1["items"]:
            if item['created_at'] > oneday:
                country = item["country"]
                projects_data = item.get("projects")
                if projects_data is not None:
                    project = item["projects"]["template_id"]
                    if project is not None:

                        if (country, project) in user_counts:
                            user_counts[(country, project)] += 1
                        else:
                            user_counts[(country, project)] = 1



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
    data1 = response.json()

    i = 0
    oneday = f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z'
    oneday_normal = (datetime.now() - relativedelta(hours=730))

    # Анализ данных page 1
    for item in data1["items"]:
            if item['created_at'] > oneday:
                country = item["country"]
                projects_data = item.get("projects")
                if projects_data is not None:
                    project = item["projects"]["template_id"]
                    if project is not None:

                        if (country, project) in user_counts:
                            user_counts[(country, project)] += 1
                        else:
                            user_counts[(country, project)] = 1



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
    data1 = response.json()

    i = 0
    oneday = f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z'
    oneday_normal = (datetime.now() - relativedelta(hours=730))

    # Анализ данных page 1
    for item in data1["items"]:
            if item['created_at'] > oneday:
                country = item["country"]
                projects_data = item.get("projects")
                if projects_data is not None:
                    project = item["projects"]["template_id"]
                    if project is not None:

                        if (country, project) in user_counts:
                            user_counts[(country, project)] += 1
                        else:
                            user_counts[(country, project)] = 1


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
    data1 = response.json()

    i = 0
    oneday = f'{(datetime.now() - relativedelta(hours=730)).isoformat()}Z'
    oneday_normal = (datetime.now() - relativedelta(hours=730))


    for item in data1["items"]:
            if item['created_at'] > oneday:
                country = item["country"]
                projects_data = item.get("projects")
                if projects_data is not None:
                    project = item["projects"]["template_id"]
                    if project is not None:
                    # CHECK IF PROJECT ALREADY EXISTS
                        if (country, project) in user_counts:
                            user_counts[(country, project)] += 1
                        else:
                            user_counts[(country, project)] = 1



    countryname = country
    projectname = project
    sorted_dict = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True))
    print (sorted_dict)

    top_countries = [key[0] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:60]]
    top_projects = [key[1] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:60]]
    filtered_dict = {(country, project): value for (country, project), value in sorted_dict.items() if country in top_countries and project in top_projects}
    filtered_dict = {key_value: value for key_value, value in filtered_dict.items() if 'Uzbekistan' not in key_value and key_value[1] != ''}


    print (filtered_dict)

    countries = list(set(item[0] for item in filtered_dict.keys()))
    projects = list(set(item[1] for item in filtered_dict.keys()))
    print(f"len count  {len(countries)}")
    print(f"len proj {len(projects)}")
    data_matrix = np.zeros((len(countries), len(projects)))


    for key, value in filtered_dict.items():
        country_index = countries.index(key[0])
        project_index = projects.index(key[1])
        data_matrix[country_index][project_index] = value


    # colors = [(0.0, '#FFE86D'), (0.25, '#F0CC68'), (0.5, '#E6B865'), (0.75, '#DCA661'), (1.0, '#CD8B5C')]
    colors = [(0.0, '#BCC5F8'), (0.5, '#E0B5CE'), (1.0, '#F59E9E')]
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors)
    # Создайте тепловую карту
    plt.figure(figsize=(20, 15), dpi=100)
    plt.imshow(data_matrix, cmap=custom_cmap, aspect='auto', vmin=1)
    for i in range(len(countries)):
        for j in range(len(projects)):
            plt.text(j, i, str(data_matrix[i, j]), ha='center', va='center', color='black')
    plt.subplots_adjust(top=0.9, bottom=0.25, left=0.11, right=1.0)
    # plt.colorbar(label='Legend',labelcolor='white')
    cbar = plt.colorbar()
    cbar.set_label('Legend', color='white')
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(axis='y', colors='white')
    plt.xticks(range(len(projects)), projects, color='white', fontsize=12)
    plt.yticks(range(len(countries)), countries, color='white', fontsize=12)
    for i in range(len(countries)):
        for j in range(len(projects)):
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, color='black', linewidth=1)
            plt.gca().add_patch(rect)
    plt.gcf().set_facecolor('black')

    plt.xlabel('Projects', color='white')
    plt.ylabel('Countries', color='white')
    plt.title(f'Country-template heatmap for {oneday_normal.strftime("%Y-%m-%d")} - {datetime.now().strftime("%Y-%m-%d")}',color='white',fontsize=25)
    plt.grid(visible=False)
    text = '1 - Dubai Hills\n 2 - Six Senses\n 3- Ava\n 4- Beachfront\n 5 - W\n 6- Elora\n 7 - Golf Grand\n 8 - Park Ridge\n 9 - Damac Bay\n 10 - Boutique\n 11 - The Community\n 12 - FB Shorts\n 13 - Phase 3\n 14 - Verona shorts\n 15 - Reeman Shorts\n 16 - Keturah Resort\n 17 - Cavali Couture'
    x_coord = 1.1
    y_coord = 0.02 - (0.25 / (0.9 - 0.25))

    plt.text(x_coord, y_coord, text, transform=plt.gca().transAxes,
             fontsize=12, verticalalignment='bottom', horizontalalignment='right', color='white')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    file_name = "monthly_template_heat.png"

    # из буфера в файл
    with open(file_name, 'wb') as f:
        f.write(buf.getbuffer())
    buf.seek(0)
    bot.send_photo(chat_id, photo=buf)
    plt.clf()

daily()
weekly()
monthly()
# scheduler = BlockingScheduler()
# #EVERY MINUTE
# scheduler.add_job(monthly, 'cron', day_of_week='*', hour='*', minute='*')
#
# # # Каждый день в 00:01
# # scheduler.add_job(daily, 'cron', day_of_week='*', hour='0', minute='2')
# #
# # # Каждый понедельник в 00:10
# # scheduler.add_job(weekly, 'cron', day_of_week='mon', hour='0', minute='11')
# #
# # # Каждое первое число месяца в 00:20
# # scheduler.add_job(monthly, 'cron', day='1', hour='0', minute='21')
#
# scheduler.start()
