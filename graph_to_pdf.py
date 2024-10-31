from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
import telebot
bot_token = 'token'
bot = telebot.TeleBot(bot_token)
chat_id= '-1001900597631'

def doc():
    pdf_file = "Monthly_report.pdf"
    page_width = 4000  # ширина страницы в пикселях
    page_height = 3900
    pagesize=(page_width, page_height)
    c = canvas.Canvas(pdf_file, pagesize=pagesize)

    #добавление изображения с черным фоном
    def add_image_with_black_background(c, image_path, x, y, width, height):
        c.setFillColorRGB(0, 0, 0)  
        c.rect(x, y, width, height, fill=1)  
        c.drawImage(image_path, x, y, width, height)

    #список изображений и их координат
    images = [
        {"path": "monthly_template_heat.png", "x": 0, "y": 2400, "width": 2000, "height": 1500},
        {"path": "monthly_project_heat.png", "x": 2000, "y": 2400, "width": 2000, "height": 1500},
        {"path": "monthly_country_bar.png", "x": 0, "y": 1200, "width": 2000, "height": 1200},
        {"path": "monthly_country_pie.png", "x": 2000, "y": 1200, "width": 2000, "height": 1200},
        {"path": "monthly_project_bar.png", "x": 0, "y": 0, "width": 2000, "height": 1200},
        {"path": "monthly_project_pie.png", "x": 2000, "y": 0, "width": 2000, "height": 1200},
    ]

    #изображения с черным фоном в документ
    for img_info in images:
        add_image_with_black_background(c, img_info["path"], img_info["x"], img_info["y"], img_info["width"], img_info["height"])

    #создание PDF-документа
    c.save()

    print(f"PDF-файл {pdf_file} создан успешно.")
    with open(pdf_file, 'rb') as pdf:  #
        bot.send_document(chat_id, pdf)


doc()
# scheduler = BlockingScheduler()
# # # # каждое первое число месяца в 00:40
# scheduler.add_job(doc, 'cron', day='1', hour='0', minute='40')
# scheduler.start()

