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

from config import load_config, write_config


class EmailsenderApp(App):

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
        bl_main.add_widget(Label(text="Ввод показаний"))

        gl1 = GridLayout(cols=2,
                         padding=[25, 20])
        gl1.add_widget(Label(text='Дата показаний'))
        self.date = TextInput()
        gl1.add_widget(self.date)
        bl_main.add_widget(gl1)
        gl2 = GridLayout(cols=2,
                         padding=[25, 20])
        bl_main.add_widget(gl2)
        gl2.add_widget(Label(text='Горячая вода'))
        self.cold_water = TextInput()
        gl2.add_widget(self.cold_water)
        gl3 = GridLayout(cols=2,
                         padding=[25, 20])
        gl3.add_widget(Label(text='Холодная вода'))
        self.hot_water = TextInput()
        gl3.add_widget(self.hot_water)
        bl_main.add_widget(gl3)

        bl_main.add_widget(Button(text='Отправить сообщение',
                                  on_press=self.send_e_mail))
        bl_main.add_widget(Button(text='Настройки',
                                  on_press=self.to_settings))

        bl_settings = BoxLayout(orientation='vertical',
                                padding=[25, 20],
                                spacing=5)
        bl_settings.add_widget(Label(text='Настройки'))
        gl1 = GridLayout(cols=2,
                         padding=[25, 20])
        gl1.add_widget(Label(text='Твой email'))
        self.from_email = (TextInput())
        gl1.add_widget(self.from_email)
        bl_settings.add_widget(gl1)
        gl2 = GridLayout(cols=2,
                         padding=[25, 20])
        gl2.add_widget(Label(text='Твой пароль'))
        self.password = TextInput(password=True)
        gl2.add_widget(self.password)
        bl_settings.add_widget(gl2)
        gl3 = GridLayout(cols=2,
                         padding=[25, 20])
        gl3.add_widget(Label(text='Email для отправления'))
        self.to_email = TextInput()
        gl3.add_widget(self.to_email)
        bl_settings.add_widget(gl3)
        gl4 = GridLayout(cols=2,
                         padding=[25, 20])
        gl4.add_widget(Label(text='Тема письма'))
        self.subject = TextInput()
        gl4.add_widget(self.subject)
        bl_settings.add_widget(gl4)
        bl_settings.add_widget(Button(text='Сохранить',
                                      on_press=self.write_config))
        bl_settings.add_widget(Button(text='Назад',
                                      on_press=self.to_main))

        bl_done = BoxLayout(orientation='vertical')
        bl_done.add_widget(Label(text='Показания отправлены!'))
        bl_done.add_widget(Button(text='ОК',
                                  on_press=self.to_main))

        bl_data = BoxLayout(orientation='vertical')
        bl_data.add_widget(Label(text='Сначала введи показания приборов!'))
        bl_data.add_widget(Button(text='ОК',
                                  on_press=self.to_main))

        bl_set_error = BoxLayout(orientation='vertical')
        bl_set_error.add_widget(Label(text='Сначала заполните контактные данные в меню "настройки"!'))
        bl_set_error.add_widget(Button(text='ОК',
                                       on_press=self.to_settings))

        bl_set_done = BoxLayout(orientation='vertical')
        bl_set_done.add_widget(Label(text='Изменения сохранены. Перезагрузи приложение!'))
        bl_set_done.add_widget(Button(text='ОК',
                                      on_press=self.to_main))

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
            write_config(self.from_email.text, self.password.text, self.to_email.text, self.subject.text)
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

        config = load_config('.env')
        FROM_E_MAIL = config.profile.FROM_E_MAIL
        PASS = config.profile.PASS
        TO_E_MAIL = config.profile.TO_E_MAIL
        SUBJECT = config.profile.SUBJECT

        if FROM_E_MAIL and TO_E_MAIL and PASS and SUBJECT:
            if self.date.text and self.hot_water and self.cold_water:
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
            else:
                self.to_data(instance)
        else:
            self.to_set_error(instance)


if __name__ == "__main__":
    EmailsenderApp().run()
