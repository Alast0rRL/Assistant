import time
from plyer import notification
from datetime import datetime
import flet

def main(page: flet.Page):
    page.title = "Assistent"
    page.theme_mode = "dark"
    page.vertical_alignment = flet.MainAxisAlignment.CENTER

    page.add(flet.Row([flet.IconButton(flet.icons.MAIL_LOCK_OUTLINED),]))

# while True:
#     now = datetime.now()
#     formatted_time = now.strftime("%H:%M")

#     def muing():
#         notification.notify(
#             title='Напоминание',
#             message='Мьюинг',
#             app_name='Assistent',
#             # app_icon=r'C:\Users\Maksim\GIT\Assistant\sample.jpg',
#         )

#     muing()
#     time.sleep(3600)
    

flet.app(target=main)


