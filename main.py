from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sqlite


class EmailsenderApp(App):
    button_color = (0, 1, .8, .8)
    text_color = '#00FFCE'
    font_size = 50

    set_error = 'Заполни все поля!'
    set_done = 'Изменения сохранены!'
    send_error = 'Ошибка отправления!\n\n' \
                 'Проверьте настройки!'

    def show_popup(self, message):
        popup = Popup(title="ОШИБКА",
                      title_size=self.font_size,
                      title_color=self.text_color,
                      separator_color=self.text_color,
                      title_align='center',
                      size_hint=(.8, .8),
                      auto_dismiss=False)

        layout = BoxLayout(orientation='vertical')

        label = Label(text=message,
                      font_size=self.font_size,
                      color=self.text_color
                      )
        layout.add_widget(label)

        def dismiss_popup(instance):
            popup.dismiss()

        ok_button = Button(text="ОК",
                           background_color=self.button_color,
                           font_size=self.font_size,
                           size_hint=(1, 0.3),
                           on_release=dismiss_popup)

        layout.add_widget(ok_button)
        popup.content = layout

        popup.open()

    def build(self):
        sqlite.db_connect()

        Window.clearcolor = (.1, .1, .1, 1)

        self.sm = ScreenManager()

        now = datetime.datetime.now()
        date = now.strftime("%d.%m.%Y")

        screen1 = Screen(name="main")
        screen2 = Screen(name="settings")
        screen3 = Screen(name="done")
        screen4 = Screen(name="data")
        screen5 = Screen(name="history")

        bl_main = BoxLayout(orientation='vertical',
                            padding=[50, 10],
                            spacing=50)
        bl_main.add_widget(Label(text="Ввод показаний",
                                 font_size=80,
                                 color=self.text_color))

        gl1 = GridLayout(cols=2,
                         padding=[50, 100])
        gl1.add_widget(Label(text='Дата показаний',
                             font_size=self.font_size,
                             color=self.text_color))
        self.date = TextInput(multiline=False,
                              text=f'{date}',
                              font_size=self.font_size,
                              halign="center")
        gl1.add_widget(self.date)
        bl_main.add_widget(gl1)
        gl2 = GridLayout(cols=4,
                         padding=[50, 100])
        bl_main.add_widget(gl2)
        gl2.add_widget(Label(text='ХВС',
                             font_size=self.font_size,
                             color=self.text_color))

        gl2.add_widget(Button(text='-',
                              background_color=self.button_color,
                              font_size=self.font_size,
                              size_hint=[.2, 1],
                              on_press=self.cw_min))

        self.cold_water = TextInput(multiline=False,
                                    text=str(self.get_data_history()[-2]),
                                    font_size=self.font_size,
                                    halign="center",
                                    size_hint=[.3, 1])
        gl2.add_widget(self.cold_water)

        gl2.add_widget(Button(text='+',
                              background_color=self.button_color,
                              font_size=self.font_size,
                              size_hint=[.2, 1],
                              on_press=self.cw_plus))

        gl3 = GridLayout(cols=4,
                         padding=[50, 100])
        gl3.add_widget(Label(text='ГВС',
                             font_size=self.font_size,
                             color=self.text_color))
        gl3.add_widget(Button(text='-',
                              background_color=self.button_color,
                              font_size=self.font_size,
                              size_hint=[.2, 1],
                              on_press=self.hw_min))
        self.hot_water = TextInput(multiline=False,
                                   text=str(self.get_data_history()[-1]),
                                   font_size=self.font_size,
                                   halign="center",
                                   size_hint=[.3, 1])
        gl3.add_widget(self.hot_water)
        gl3.add_widget(Button(text='+',
                              background_color=self.button_color,
                              font_size=self.font_size,
                              size_hint=[.2, 1],
                              on_press=self.hw_plus))
        bl_main.add_widget(gl3)

        bl_main.add_widget(Button(text='Отправить сообщение',
                                  font_size=self.font_size,
                                  on_press=self.send_e_mail,
                                  background_color=self.button_color,
                                  bold=True))

        bl_main.add_widget(Button(text='История отправлений',
                                  font_size=self.font_size,
                                  on_press=self.to_history,
                                  background_color=self.button_color,
                                  bold=True))

        bl_main.add_widget(Button(text='Настройки',
                                  font_size=self.font_size,
                                  on_press=self.to_settings,
                                  background_color=self.button_color,
                                  bold=True))

        bl_settings = BoxLayout(orientation='vertical',
                                padding=[30, 20],
                                spacing=20)
        bl_settings.add_widget(Label(text='Настройки',
                                     font_size=80,
                                     color='#00FFCE'))

        gl1 = GridLayout(cols=2,
                         padding=[30, 80])
        gl1.add_widget(Label(text='Твой email',
                             font_size=self.font_size,
                             color=self.text_color))
        self.from_email = TextInput(multiline=False,
                                    font_size=self.font_size)
        gl1.add_widget(self.from_email)
        bl_settings.add_widget(gl1)
        gl2 = GridLayout(cols=2,
                         padding=[30, 80])
        gl2.add_widget(Label(text='Твой пароль',
                             font_size=self.font_size,
                             color=self.text_color))
        self.password = TextInput(password=True,
                                  multiline=False,
                                  font_size=self.font_size)
        gl2.add_widget(self.password)
        bl_settings.add_widget(gl2)
        gl3 = GridLayout(cols=2,
                         padding=[30, 80])
        gl3.add_widget(Label(text='Email получателя',
                             font_size=self.font_size,
                             color=self.text_color))
        self.to_email = TextInput(multiline=False,
                                  font_size=self.font_size)
        gl3.add_widget(self.to_email)
        bl_settings.add_widget(gl3)
        gl4 = GridLayout(cols=2,
                         padding=[30, 80])
        gl4.add_widget(Label(text='Тема письма',
                             font_size=self.font_size,
                             color=self.text_color,
                             ))
        self.subject = TextInput(multiline=False,
                                 font_size=self.font_size)
        gl4.add_widget(self.subject)
        bl_settings.add_widget(gl4)
        bl_settings.add_widget(Button(text='Сохранить',
                                      font_size=self.font_size,
                                      on_press=self.write_config,
                                      background_color=self.button_color,
                                      bold=True))
        bl_settings.add_widget(Button(text='Назад',
                                      font_size=self.font_size,
                                      on_press=self.to_main,
                                      background_color=self.button_color,
                                      bold=True))

        bl_done = BoxLayout(orientation='vertical')
        bl_done.add_widget(Label(text='Показания отправлены!',
                                 font_size=self.font_size,
                                 color=self.text_color))
        bl_done.add_widget(Button(text='ОК',
                                  font_size=self.font_size,
                                  on_press=self.to_main,
                                  background_color=self.button_color,
                                  bold=True))

        bl_data = BoxLayout(orientation='vertical')
        bl_data.add_widget(Label(text='Сначала введи\n'
                                      'показания приборов!',
                                 halign="center",
                                 font_size=self.font_size,
                                 color=self.text_color))
        bl_data.add_widget(Button(text='ОК',
                                  font_size=self.font_size,
                                  on_press=self.to_main,
                                  background_color=self.button_color,
                                  bold=True))

        bl_history = BoxLayout(orientation='vertical',
                               padding=[30, 20],
                               spacing=20)
        gl_hostory = GridLayout(cols=3, spacing=50, size_hint_y=None)

        gl_hostory.add_widget(Label(text='Дата',
                                    font_size=self.font_size,
                                    color=self.text_color))
        gl_hostory.add_widget(Label(text='ХВС',
                                    font_size=self.font_size,
                                    color=self.text_color))
        gl_hostory.add_widget(Label(text='ГВС',
                                    font_size=self.font_size,
                                    color=self.text_color))
        bl_history.add_widget(gl_hostory)

        self.history_grid = GridLayout(cols=3, spacing=50, size_hint_y=None)
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))
        for i in sqlite.get_all_data():
            self.label_history_data = Label(text=str(i[1]),
                                            font_size=self.font_size,
                                            color=self.text_color)
            self.history_grid.add_widget(self.label_history_data)

            self.label_history_cw = Label(text=str(i[2]),
                                          font_size=self.font_size,
                                          color=self.text_color)
            self.history_grid.add_widget(self.label_history_cw)

            self.label_history_hw = Label(text=str(i[3]),
                                          font_size=self.font_size,
                                          color=self.text_color)
            self.history_grid.add_widget(self.label_history_hw)

        sv_history = ScrollView()
        sv_history.add_widget(self.history_grid)
        bl_history.add_widget(sv_history)
        bl_history.add_widget(Button(text='Назад',
                                     font_size=self.font_size,
                                     on_press=self.to_main,
                                     background_color=self.button_color,
                                     bold=True,
                                     size_hint=[1, .2]))

        screen1.add_widget(bl_main)
        screen2.add_widget(bl_settings)
        screen3.add_widget(bl_done)
        screen4.add_widget(bl_data)
        screen5.add_widget(bl_history)

        self.sm.add_widget(screen1)
        self.sm.add_widget(screen2)
        self.sm.add_widget(screen3)
        self.sm.add_widget(screen4)
        self.sm.add_widget(screen5)
        self.sm.current = 'main'
        return self.sm

    def get_data_history(self):
        data = sqlite.get_all_data()
        if data:
            return data[-1]
        return [0, 0]

    def write_config(self, instance):
        if self.from_email.text and self.password.text and self.to_email.text and self.subject.text:
            try:
                with open("config.txt", "w", encoding="utf-8") as config:
                    config.write(f"FROM_E_MAIL = {self.from_email.text}\n")
                    config.write(f"PASS = {self.password.text}\n")
                    config.write(f"TO_E_MAIL = {self.to_email.text}\n")
                    config.write(f"SUBJECT = {self.subject.text}\n")
                self.show_popup(self.set_done)
            except:
                self.show_popup(self.set_error)
        else:
            self.show_popup(self.set_error)

    def cw_min(self, instance):
        self.cold_water.text = str(int(self.cold_water.text) - 1)

    def cw_plus(self, instance):
        self.cold_water.text = str(int(self.cold_water.text) + 1)

    def hw_min(self, instance):
        self.hot_water.text = str(int(self.hot_water.text) - 1)

    def hw_plus(self, instance):
        self.hot_water.text = str(int(self.hot_water.text) + 1)

    def to_settings(self, instance):
        self.sm.current = 'settings'

    def to_main(self, instance):
        self.sm.current = 'main'

    def to_done(self, instance):
        self.sm.current = 'done'

    def to_data(self, instance):
        self.sm.current = 'data'

    def to_history(self, instance):
        self.sm.current = 'history'

    def send_e_mail(self, instance):
        try:
            with open("config.txt", "r", encoding="utf-8") as config:
                config = config.readlines()
                FROM_E_MAIL = config[0][14:]
                PASS = config[1][7:]
                TO_E_MAIL = config[2][12:]
                SUBJECT = config[3][10:]
        except:
            FROM_E_MAIL = None
            PASS = None
            TO_E_MAIL = None
            SUBJECT = None

        if FROM_E_MAIL and TO_E_MAIL and PASS and SUBJECT:
            if self.date.text and self.hot_water.text and self.cold_water.text:
                try:
                    mgs = MIMEMultipart()
                    mgs['From'] = FROM_E_MAIL
                    mgs['To'] = TO_E_MAIL, FROM_E_MAIL
                    mgs['Subject'] = SUBJECT
                    body = f'Добрый день!\n' \
                           f'\n' \
                           f'Показания приборов учета на {self.date.text}\n' \
                           f'ХВС: {self.cold_water.text}\n' \
                           f'ГВС: {self.hot_water.text}'
                    mgs.attach(MIMEText(body, 'plain'))
                    smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
                    smtpObj.starttls()
                    smtpObj.login(FROM_E_MAIL, PASS)
                    smtpObj.send_message(mgs)
                    smtpObj.quit()
                    self.to_done(instance)
                    sqlite.create_new_data(self.date.text, self.cold_water.text, self.hot_water.text)
                except:
                    self.show_popup(self.send_error)
            else:
                self.to_data(instance)
        else:
            self.show_popup(self.set_error)


if __name__ == "__main__":
    EmailsenderApp().run()
