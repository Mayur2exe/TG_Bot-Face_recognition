# A Telegram bot for face recognition
- This Bot is created by @Mayurrr2.
- It is used for face recognition.
- It uses Laptop's webcam to detect and recognise faces.
- If a face is unknown to system it takes a screenshot and save it.
- It can take screenshot of the live feed.
- It can also inform the current status from live feed.
- After Stopping Webcam, it collects all the data and send it to user.
- It can also detect and recognise faces using an Image.
- It can also detect and recognise faces using a Video.
- It can also add images to known faces.
- Type / to know about features.




### Steps Required to run this bot
#### Editing in Scripts
1. Enter API KEY  (Provided by BotFather)
>  Line - 17 main.py
2. Enter Path and Image (For eg. D:\Image\telegram_bot\1.jpg)
>  Line - 23 main2.py
3. Enter Email ID and Username of the bot created
>  Line - 13 mail.py - Sender's ID <br />
>  Line - 14 mail.py - Receiver's ID <br />
>  Line - 30 mail.py - username <br />
4. ##### *Important*
   If you do not have OpenCV Library built with CUDA Support
>  Comment with # Line- 7 & Line - 8 detector.py
5. Enter Path
>  Line - 13 & Line - 14 Path where images are stored (For eg. D:\Image\telegram_bot\images) <br />
>  Line - 16 & Line - 17 Path where both files are stored (For eg. D:\Image\telegram_bot\deploy.protoxt, D:\Image\telegram_bot\weights.caffemodel)
   
