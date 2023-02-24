from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailsenderApp(App):
    button_color = (0, 1, .8, .8)
    text_color = '#00FFCE'


    def build(self):
        Window.clearcolor = (.1, .1, .1, 1)
        self.sm = ScreenManager()
        screen1 = Screen(name="main")
        screen2 = Screen(name="settings")
        screen3 = Screen(name="done")
        screen4 = Screen(name="data")
        screen5 = Screen(name="set_error")
        screen6 = Screen(name="set_done")
        screen7 = Screen(name="send_error")

        bl_main = BoxLayout(orientation='vertical',
                            padding=[25, 20],
                            spacing=5)
        bl_main.add_widget(Label(text="Ввод показаний",
                                 font_size=40,
                                 color=self.text_color))

        gl1 = GridLayout(cols=2,
                         padding=[25, 20])
        gl1.add_widget(Label(text='Дата показаний',
                             font_size=20,
                             color=self.text_color))
        self.date = TextInput(multiline=False,
                              padding_y=(15, 15))
        gl1.add_widget(self.date)
        bl_main.add_widget(gl1)
        gl2 = GridLayout(cols=2,
                         padding=[25, 20])
        bl_main.add_widget(gl2)
        gl2.add_widget(Label(text='Горячая вода',
                             font_size=20,
                             color=self.text_color))
        self.cold_water = TextInput(multiline=False,
                              padding_y=(15, 15))
        gl2.add_widget(self.cold_water)
        gl3 = GridLayout(cols=2,
                         padding=[25, 20])
        gl3.add_widget(Label(text='Холодная вода',
                             font_size=20,
                             color=self.text_color))
        self.hot_water = TextInput(multiline=False,
                              padding_y=(10, 10),
                              size_hint=(1,.5))
        gl3.add_widget(self.hot_water)
        bl_main.add_widget(gl3)

        bl_main.add_widget(Button(text='Отправить сообщение',
                                  font_size=35,
                                  on_press=self.send_e_mail,
                                  background_color=self.button_color,
                                  bold=True))
        bl_main.add_widget(Button(text='Настройки',
                                  font_size=35,
                                  on_press=self.to_settings,
                                  background_color=self.button_color,
                                  bold=True))

        bl_settings = BoxLayout(orientation='vertical',
                                padding=[25, 20],
                                spacing=5)
        bl_settings.add_widget(Label(text='Настройки',
                                     font_size=40,
                                     color='#00FFCE'))
        gl1 = GridLayout(cols=2,
                         padding=[25, 20])
        gl1.add_widget(Label(text='Твой email',
                             font_size=20,
                             color=self.text_color))
        self.from_email = TextInput(multiline=False,
                              padding_y=(15, 15))
        gl1.add_widget(self.from_email)
        bl_settings.add_widget(gl1)
        gl2 = GridLayout(cols=2,
                         padding=[25, 20])
        gl2.add_widget(Label(text='Твой пароль',
                             font_size=20,
                             color=self.text_color))
        self.password = TextInput(password=True,
                                  multiline=False,
                                  padding_y=(15, 15))
        gl2.add_widget(self.password)
        bl_settings.add_widget(gl2)
        gl3 = GridLayout(cols=2,
                         padding=[25, 20])
        gl3.add_widget(Label(text='Email отправления',
                             font_size=20,
                             color=self.text_color))
        self.to_email = TextInput(multiline=False,
                              padding_y=(15, 15))
        gl3.add_widget(self.to_email)
        bl_settings.add_widget(gl3)
        gl4 = GridLayout(cols=2,
                         padding=[25, 20])
        gl4.add_widget(Label(text='Тема письма',
                             font_size=20,
                             color=self.text_color))
        self.subject = TextInput(multiline=False,
                              padding_y=(10, 10))
        gl4.add_widget(self.subject)
        bl_settings.add_widget(gl4)
        bl_settings.add_widget(Button(text='Сохранить',
                                      font_size=35,
                                      on_press=self.write_config,
                                      background_color=self.button_color,
                                      bold=True))
        bl_settings.add_widget(Button(text='Назад',
                                      font_size=35,
                                      on_press=self.to_main,
                                      background_color=self.button_color,
                                      bold=True))

        bl_done = BoxLayout(orientation='vertical')
        bl_done.add_widget(Label(text='Показания отправлены!',
                                 font_size=35,
                                 color=self.text_color))
        bl_done.add_widget(Button(text='ОК',
                                  font_size=35,
                                  on_press=self.to_main,
                                  background_color=self.button_color,
                                  bold=True))

        bl_data = BoxLayout(orientation='vertical')
        bl_data.add_widget(Label(text='Сначала введи\n'
                                      'показания приборов!',
                                 font_size=35,
                                 color=self.text_color))
        bl_data.add_widget(Button(text='ОК',
                                  font_size=35,
                                  on_press=self.to_main,
                                  background_color=self.button_color,
                                  bold=True))

        bl_set_error = BoxLayout(orientation='vertical')
        bl_set_error.add_widget(Label(text='Заполните поля!',
                                      font_size=35,
                                      color=self.text_color))
        bl_set_error.add_widget(Button(text='ОК',
                                       font_size=35,
                                       on_press=self.to_settings,
                                       background_color=self.button_color,
                                       bold=True))

        bl_set_done = BoxLayout(orientation='vertical')
        bl_set_done.add_widget(Label(text='Изменения сохранены!',
                                     font_size=35,
                                     color=self.text_color))
        bl_set_done.add_widget(Button(text='ОК',
                                      font_size=35,
                                      on_press=self.to_main,
                                      background_color=self.button_color,
                                      bold=True))

        bl_send_error = BoxLayout(orientation='vertical')
        bl_send_error.add_widget(Label(text='Ошибка отправления!\n\n'
                                            'Проверьте настройки!',
                                       font_size=35,
                                       color=self.text_color))
        bl_send_error.add_widget(Button(text='ОК',
                                        font_size=35,
                                        on_press=self.to_settings,
                                        background_color=self.button_color,
                                        bold=True))

        screen1.add_widget(bl_main)
        screen2.add_widget(bl_settings)
        screen3.add_widget(bl_done)
        screen4.add_widget(bl_data)
        screen5.add_widget(bl_set_error)
        screen6.add_widget(bl_set_done)
        screen7.add_widget(bl_send_error)

        self.sm.add_widget(screen1)
        self.sm.add_widget(screen2)
        self.sm.add_widget(screen3)
        self.sm.add_widget(screen4)
        self.sm.add_widget(screen5)
        self.sm.add_widget(screen6)
        self.sm.add_widget(screen7)
        self.sm.current = 'main'
        return self.sm

    def write_config(self, instance):
        if self.from_email.text and self.password.text and self.to_email.text and self.subject.text:
            with open("config.txt", "w", encoding="utf-8") as config:
                config.write(f"FROM_E_MAIL = {self.from_email.text}\n")
                config.write(f"PASS = {self.password.text}\n")
                config.write(f"TO_E_MAIL = {self.to_email.text}\n")
                config.write(f"SUBJECT = {self.subject.text}\n")
            self.to_set_done(instance)
        else:
            self.to_set_error(instance)

    def to_settings(self, instance):
        self.sm.current = 'settings'

    def to_main(self, instance):
        self.sm.current = 'main'

    def to_done(self, instance):
        self.sm.current = 'done'

    def to_data(self, instance):
        self.sm.current = 'data'

    def to_set_error(self, instance):
        self.sm.current = 'set_error'

    def to_set_done(self, instance):
        self.sm.current = 'set_done'

    def to_send_error(self, instance):
        self.sm.current = 'send_error'

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
                    mgs['To'] = TO_E_MAIL
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
                except:
                    self.to_send_error(instance)
            else:
                self.to_data(instance)
        else:
            self.to_set_error(instance)


if __name__ == "__main__":
    EmailsenderApp().run()
