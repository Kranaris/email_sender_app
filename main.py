from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailsenderApp(App):

    button_color = (0, 1, .8, 1)
    text_color = '#00FFCE'


    def build(self):
        self.sm = ScreenManager()
        screen1 = Screen(name="main")
        screen2 = Screen(name="settings")
        screen3 = Screen(name="done")
        screen4 = Screen(name="data")
        screen5 = Screen(name="set_error")
        screen6 = Screen(name="set_done")

        bl_main = BoxLayout(orientation='vertical',
                            padding=[25, 20],
                            spacing=5)
        bl_main.add_widget(Label(text="Ввод показаний",
                                 color=self.text_color))

        gl1 = GridLayout(cols=2,
                         padding=[25, 20])
        gl1.add_widget(Label(text='Дата показаний',
                                 color=self.text_color))
        self.date = TextInput(multiline=False)
        gl1.add_widget(self.date)
        bl_main.add_widget(gl1)
        gl2 = GridLayout(cols=2,
                         padding=[25, 20])
        bl_main.add_widget(gl2)
        gl2.add_widget(Label(text='Горячая вода',
                                 color=self.text_color))
        self.cold_water = TextInput(multiline=False)
        gl2.add_widget(self.cold_water)
        gl3 = GridLayout(cols=2,
                         padding=[25, 20])
        gl3.add_widget(Label(text='Холодная вода',
                                 color=self.text_color))
        self.hot_water = TextInput(multiline=False)
        gl3.add_widget(self.hot_water)
        bl_main.add_widget(gl3)

        bl_main.add_widget(Button(text='Отправить сообщение',
                                  on_press=self.send_e_mail,
                                  background_color =self.button_color,
                                  bold=True))
        bl_main.add_widget(Button(text='Настройки',
                                  on_press=self.to_settings,
                                  background_color =self.button_color,
                                  bold=True))

        bl_settings = BoxLayout(orientation='vertical',
                                padding=[25, 20],
                                spacing=5)
        bl_settings.add_widget(Label(text='Настройки',
                                     color='#00FFCE'))
        gl1 = GridLayout(cols=2,
                         padding=[25, 20])
        gl1.add_widget(Label(text='Твой email',
                                 color=self.text_color))
        self.from_email = (TextInput(multiline=False))
        gl1.add_widget(self.from_email)
        bl_settings.add_widget(gl1)
        gl2 = GridLayout(cols=2,
                         padding=[25, 20])
        gl2.add_widget(Label(text='Твой пароль',
                                 color=self.text_color))
        self.password = TextInput(multiline=False,
                                  password=True)
        gl2.add_widget(self.password)
        bl_settings.add_widget(gl2)
        gl3 = GridLayout(cols=2,
                         padding=[25, 20])
        gl3.add_widget(Label(text='Email для отправления',
                                 color=self.text_color))
        self.to_email = TextInput(multiline=False)
        gl3.add_widget(self.to_email)
        bl_settings.add_widget(gl3)
        gl4 = GridLayout(cols=2,
                         padding=[25, 20])
        gl4.add_widget(Label(text='Тема письма',
                                 color=self.text_color))
        self.subject = TextInput()
        gl4.add_widget(self.subject)
        bl_settings.add_widget(gl4)
        bl_settings.add_widget(Button(text='Сохранить',
                                      on_press=self.write_config,
                                      background_color =self.button_color,
                                      bold=True))
        bl_settings.add_widget(Button(text='Назад',
                                      on_press=self.to_main,
                                      background_color =self.button_color,
                                      bold=True))

        bl_done = BoxLayout(orientation='vertical')
        bl_done.add_widget(Label(text='Показания отправлены!',
                                 color=self.text_color))
        bl_done.add_widget(Button(text='ОК',
                                  on_press=self.to_main,
                                  background_color =self.button_color,
                                  bold=True))

        bl_data = BoxLayout(orientation='vertical')
        bl_data.add_widget(Label(text='Сначала введи показания приборов!',
                                 color=self.text_color))
        bl_data.add_widget(Button(text='ОК',
                                  on_press=self.to_main,
                                  background_color =self.button_color,
                                  bold=True))

        bl_set_error = BoxLayout(orientation='vertical')
        bl_set_error.add_widget(Label(text='Заполните поля!',
                                 color=self.text_color))
        bl_set_error.add_widget(Button(text='ОК',
                                       on_press=self.to_settings,
                                       background_color =self.button_color,
                                       bold=True))

        bl_set_done = BoxLayout(orientation='vertical')
        bl_set_done.add_widget(Label(text='Изменения сохранены!',
                                 color=self.text_color))
        bl_set_done.add_widget(Button(text='ОК',
                                      on_press=self.to_main,
                                      background_color =self.button_color,
                                      bold=True))

        screen1.add_widget(bl_main)
        screen2.add_widget(bl_settings)
        screen3.add_widget(bl_done)
        screen4.add_widget(bl_data)
        screen5.add_widget(bl_set_error)
        screen6.add_widget(bl_set_done)

        self.sm.add_widget(screen1)
        self.sm.add_widget(screen2)
        self.sm.add_widget(screen3)
        self.sm.add_widget(screen4)
        self.sm.add_widget(screen5)
        self.sm.add_widget(screen6)
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
                    self.to_data(instance)
            else:
                self.to_data(instance)
        else:
            self.to_set_error(instance)


if __name__ == "__main__":
    EmailsenderApp().run()
