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
from telegram import InputFile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Image
pdf_file = "image.pdf"
document = SimpleDocTemplate(pdf_file, pagesize=letter)
kartinki = []
matplotlib.use('agg')

bot_token = 'token'
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


    for item in data1["items"]:
            if item['created_at'] > oneday:
                country = item["country"]
                project = item["project"]

          
                if (country, project) in user_counts:
                    user_counts[(country, project)] += 1
                else:
                    user_counts[(country, project)] = 1


    countryname = country
    projectname = project
    sorted_dict = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True))
    print (sorted_dict)

    top_countries = [key[0] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    top_projects = [key[1] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    filtered_dict = {(country, project): value for (country, project), value in sorted_dict.items() if country in top_countries and project in top_projects}
    filtered_dict = {key_value: value for key_value, value in filtered_dict.items() if 'Uzbekistan' not in key_value}
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
    colors = [(0.0, '#BCC5F8'), (0.5, '#E0B5CE'), (1.0, '#F59E9E')]
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors)
    plt.figure(figsize=(20, 15), dpi=100)
    plt.imshow(data_matrix, cmap=custom_cmap, aspect='auto', vmin=1)
    for i in range(len(countries)):
        for j in range(len(projects)):
            plt.text(j, i, str(data_matrix[i, j]), ha='center', va='center', color='black')
    plt.subplots_adjust(top=0.9, bottom=0.25, left=0.12, right=1.1)
    cbar = plt.colorbar()
    cbar.set_label('Legend', color='white')
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(axis='y', colors='white')
    plt.xticks(range(len(projects)), projects, rotation=90, color='white')
    plt.yticks(range(len(countries)), countries, color='white')

    for i in range(len(countries)):
        for j in range(len(projects)):
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, color='black', linewidth=1)
            plt.gca().add_patch(rect)
    plt.gcf().set_facecolor('black')


    plt.xlabel('Projects', color='white')
    plt.ylabel('Countries', color='white')
    plt.title(f'Country-project heatmap for {oneday_normal.strftime("%Y-%m-%d")} - {datetime.now().strftime("%Y-%m-%d")}', color='white', fontsize=25)
    plt.grid(visible=False)
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    file_name = "daily_project_heat.png"
    with open(file_name, 'wb') as f:
        f.write(buf.getbuffer())
    buf.seek(0)
    bot.send_photo(chat_id, photo=buf)
    image = Image(buf, height=612 ,width=1008)  # Укажите ширину и высоту по вашему усмотрению
    kartinki.append(image)
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
                project = item["project"]
                if (country, project) in user_counts:
                    user_counts[(country, project)] += 1
                else:
                    user_counts[(country, project)] = 1
    countryname = country
    projectname = project
    sorted_dict = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True))
    print (sorted_dict)

    top_countries = [key[0] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    top_projects = [key[1] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    filtered_dict = {(country, project): value for (country, project), value in sorted_dict.items() if
                     country in top_countries and project in top_projects}
    filtered_dict = {key_value: value for key_value, value in filtered_dict.items() if 'Uzbekistan' not in key_value}
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


    colors = [(0.0, '#BCC5F8'), (0.5, '#E0B5CE'), (1.0, '#F59E9E')]
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors)

    plt.figure(figsize=(20, 15), dpi=100)
    plt.imshow(data_matrix, cmap=custom_cmap, aspect='auto', vmin=1)
    for i in range(len(countries)):
        for j in range(len(projects)):
            plt.text(j, i, str(data_matrix[i, j]), ha='center', va='center', color='black')
    plt.subplots_adjust(top=0.9, bottom=0.25, left=0.12, right=1.1)
    cbar = plt.colorbar()
    cbar.set_label('Legend', color='white')
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(axis='y', colors='white')
    plt.xticks(range(len(projects)), projects, rotation=90, color='white')
    plt.yticks(range(len(countries)), countries, color='white')
    for i in range(len(countries)):
        for j in range(len(projects)):
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, color='black', linewidth=1)
            plt.gca().add_patch(rect)
    plt.gcf().set_facecolor('black')

    plt.xlabel('Projects',color='white')
    plt.ylabel('Countries', color='white')
    plt.title(f'Country-project heatmap for {oneday_normal.strftime("%Y-%m-%d")} - {datetime.now().strftime("%Y-%m-%d")}', color='white', fontsize=25)
    plt.grid(visible=False)


    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    file_name = "weekly_project_heat.png"
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
    for item in data1["items"]:
            if item['created_at'] > oneday:
                country = item["country"]
                project = item["project"]
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
            project = item["project"]
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
            country = item[""]
            project = item[""]
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
            project = item["project"]
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
            project = item["project"]
            if (country, project) in user_counts:
                user_counts[(country, project)] += 1
            else:
                user_counts[(country, project)] = 1
    countryname = country
    projectname = project
    sorted_dict = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True))
    print (sorted_dict)

    top_countries = [key[0] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    top_projects = [key[1] for key, value in sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True)[:50]]
    filtered_dict = {(country, project): value for (country, project), value in sorted_dict.items() if country in top_countries and project in top_projects}
    filtered_dict = {key_value: value for key_value, value in filtered_dict.items() if 'Uzbekistan' not in key_value}
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

    colors = [(0.0, '#BCC5F8'), (0.5, '#E0B5CE'), (1.0, '#F59E9E')]
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors)
    plt.figure(figsize=(20, 15), dpi=100)
    plt.imshow(data_matrix, cmap=custom_cmap, aspect='auto', vmin=1)
    for i in range(len(countries)):
        for j in range(len(projects)):
            plt.text(j, i, str(data_matrix[i, j]), ha='center', va='center', color='black')
    plt.subplots_adjust(top=0.9, bottom=0.25, left=0.12, right=1.1)
    cbar = plt.colorbar()
    cbar.set_label('Legend', color='white')
    cbar.ax.yaxis.label.set_color('white')
    cbar.ax.tick_params(axis='y', colors='white')
    plt.xticks(range(len(projects)), projects, rotation=90,color='white')
    plt.yticks(range(len(countries)), countries, color='white')

    for i in range(len(countries)):
        for j in range(len(projects)):
            rect = Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, color='black', linewidth=1)
            plt.gca().add_patch(rect)
    plt.gcf().set_facecolor('black')

    plt.xlabel('Projects',color='white')
    plt.ylabel('Countries', color='white')
    plt.title(f'Country-project heatmap for {oneday_normal.strftime("%Y-%m-%d")} - {datetime.now().strftime("%Y-%m-%d")}', color='white', fontsize=25)
    plt.grid(visible=False)


    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    file_name = "monthly_project_heat.png"

    with open(file_name, 'wb') as f:
        f.write(buf.getbuffer())
    buf.seek(0)
    bot.send_photo(chat_id, photo=buf)
    plt.clf()

daily()
weekly()
monthly()

