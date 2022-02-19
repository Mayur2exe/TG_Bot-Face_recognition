import os.path
from urllib.request import urlretrieve
import cv2
import Respones as r
import loader
from telegram.ext import *
import time
import xlsxwriter
from datetime import datetime, date
import calendar
import main2
import recognizer
from main2 import name_box
from threading import Timer
import mail

API_KEY = 'API_KEY'
print("Bot Started")
encodings, names, models = loader.usepkl()
on_off = True
book = xlsxwriter.Workbook('Data.xlsx')
sheet = book.add_worksheet()
now = datetime.now()
curr_date = date.today()
ss_offset = 0
mail_offset = 0


def start_command(update, context):
    def reply():
        update.message.reply_text("Webcam Started")

    t = Timer(5, reply)
    t.start()
    row = 0
    img_counter = 0
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    global on_off
    on_off = True
    global ss_offset
    ss_offset = 0
    while cam.isOpened():
        while on_off:
            _, frame = cam.read()
            st = time.time()
            n_name, box_faces, _ = recognizer.compare_faces(frame, encodings, names, models)
            for item in n_name:
                sheet.write(row, 0, item)
                current_time = now.strftime("%H:%M:%S")
                sheet.write(row, 1, current_time)
                sheet.write(row, 2, calendar.day_name[curr_date.weekday()])
                row += 1
                if item == "Mayur":
                    update.message.reply_text("Alert Mayur (Thief) Detected")
                    global mail_offset
                    mail_offset = 1
                    ss_offset = 1
            frame = name_box(frame, box_faces, n_name)
            end_time = time.time() - st
            FPS = 1 / end_time
            cv2.putText(frame, f"Fps {round(FPS, 3)}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Face Recognition", frame)
            if ss_offset == 1:
                path = "Path where ss should be stored"
                img_name = "frame_{}.png".format(img_counter)
                cv2.imwrite(os.path.join(path, img_name), frame)
                img_counter += 1
                ss_offset = 0
            if cv2.waitKey(1) & on_off == False:
                cv2.destroyAllWindows()
                cam.release()
                update.message.reply_text("Webcam Stopped")
                break
    else:
        update.message.reply_text("Camera Disconnected")


def help_command(update, context):
    update.message.reply_text(
        "This Bot is created by @Mayurrr2."
        "\nThis bot is basically for face recognition."
        "\nThis bot uses Laptop's webcam to detect and recognise faces."
        "\nIt can take screenshot of the live feed."
        "\nAfter Stopping Webcam, it collects all the data and send it to user."
        "\nIt can also detect and recognise faces using an Image."
        "\nType / to know about features"
        "\n\n------------         Commands         ------------\n"
        "\n/update - To update database"
        "\n/start - To start webcam"
        "\n/screenshot - To take screenshot"
        "\n/stop - To stop webcam"
        "\n\n------             More INFO             ------\n"
        "\nType Image to recognize using image."
        "\nType ss after taking Screenshot to download it."
        "\nAn excel file is generated for each frame whenever faces are detected."
        "\nType email to receive an excel sheet on mails"
        "\nNOTE:Names displayed with accuracy less than 90-92% are usually incorrect(Depending on occlusion)")


def ss_command(update, context):
    global ss_offset
    ss_offset = 1
    update.message.reply_text("Screenshot Taken")


def stop_command(update, context):
    book.close()
    global on_off
    on_off = False
    if mail_offset == 1:
        mail.mail()


def handle_message(update, context):
    text = str(update.message.text).lower()
    respone = r.give_responses(text)

    update.message.reply_text(respone)
    if text == "ss":
        context.bot.send_photo(update.message.chat_id, photo=open("Path and image where ss is stored".format(0), 'rb'))


def receive_image(update, context):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    url = file['file_path']
    urlretrieve(url, "1.jpg")
    names, acc = main2.main1()

    def listToString(names, acc):
        s = ""
        for i in range(0, len(names)):
            s = s + str(names[i]) + " - " + str(acc[i]) + "\n"
        return s

    st = listToString(names, acc)

    if st == "":
        update.message.reply_text("Sorry! No face is detected")
    else:
        update.message.reply_text("Faces Recognized by bot:\nNames - Accuracy\n{}".format(st))
        context.bot.send_photo(update.message.chat_id, photo=open("Path where image is sent by user", 'rb'))


def update_db(update, context):
    update.message.reply_text("Updating database...")
    _, _, _, k, l, m, name = loader.load_images_to_db()
    update.message.reply_text("Database Updated")
    update.message.reply_text("Total Files:{}"
                              "\nTotal Images:{}"
                              "\nTotal Images with faces{}"
                              "\nNames ={}".format(k, l, m, str(name)))


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("update", update_db))
    dp.add_handler(CommandHandler("start", start_command, run_async=True))
    dp.add_handler(CommandHandler("stop", stop_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("screenshot", ss_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.photo, receive_image))
    dp.add_error_handler(error)
    updater.start_polling(0)
    updater.idle()


main()
