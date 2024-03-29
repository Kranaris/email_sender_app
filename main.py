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
    data_error = 'Сначала введи\n' \
                 'показания приборов!'

    profile = 1

    def show_popup(self, message, go_to=None):
        popup = Popup(title="ВНИМАНИЕ",
                      title_size=self.font_size,
                      title_color=self.text_color,
                      separator_color=self.text_color,
                      title_align='center',
                      size_hint=(.8, .5),
                      auto_dismiss=False)

        layout = BoxLayout(orientation='vertical')

        label = Label(text=message,
                      font_size=self.font_size,
                      color=self.text_color
                      )
        layout.add_widget(label)

        def dismiss_popup(instance):
            popup.dismiss()
            if go_to:
                go_to(instance)

        ok_button = Button(text="ОК",
                           background_color=self.button_color,
                           font_size=self.font_size,
                           size_hint=(1, 0.3),
                           on_release=dismiss_popup)

        layout.add_widget(ok_button)
        popup.content = layout

        popup.open()

    def set_profile_1(self, instance):
        self.profile = 1
        self.update_profile_buttons()

    def set_profile_2(self, instance):
        self.profile = 2
        self.update_profile_buttons()

    def update_profile_buttons(self):
        if self.profile == 1:
            self.btn_profile1.background_color = [0.2, 0.8, 0.2, 1]
            self.btn_profile1.text = self.get_title(1)
            self.btn_profile2.background_color = self.button_color
            self.hot_water.text = str(self.get_data_history(1)[-1])
            self.cold_water.text = str(self.get_data_history(1)[-2])
        elif self.profile == 2:
            self.btn_profile1.background_color = self.button_color
            self.btn_profile2.text = self.get_title(2)
            self.btn_profile2.background_color = [0.2, 0.8, 0.2, 1]
            self.hot_water.text = str(self.get_data_history(2)[-1])
            self.cold_water.text = str(self.get_data_history(2)[-2])

    def get_title(self, profile):
        data = sqlite.get_profile(profile)
        if data:
            title = data[1]
        else:
            title = f"P{profile}"
        return title

    def build(self):
        sqlite.db_connect()

        Window.clearcolor = (.1, .1, .1, 1)

        self.sm = ScreenManager()

        now = datetime.datetime.now()
        date = now.strftime("%d.%m.%Y")

        screen1 = Screen(name="main")
        screen2 = Screen(name="settings")
        screen3 = Screen(name="done")
        self.screen4 = Screen(name="history")

        bl_main = BoxLayout(orientation='vertical',
                            padding=[10, 10],
                            spacing=10)

        bl_profiles = BoxLayout(orientation='horizontal',
                                padding=[10, 10],
                                spacing=10)

        self.btn_profile1 = Button(text=self.get_title(1),
                                   background_color=self.button_color,
                                   font_size=self.font_size,
                                   size_hint=[.1, 1],
                                   on_press=self.set_profile_1)

        self.btn_profile2 = Button(text=self.get_title(2),
                                   background_color=self.button_color,
                                   font_size=self.font_size,
                                   size_hint=[.1, 1],
                                   on_press=self.set_profile_2)

        bl_profiles.add_widget(self.btn_profile1)
        bl_profiles.add_widget(self.btn_profile2)

        bl_main.add_widget(bl_profiles)

        bl_main.add_widget(Label(text="Ввод показаний",
                                 font_size=60,
                                 color=self.text_color))

        gl1 = GridLayout(cols=2,
                         padding=[50,80])
        gl1.add_widget(Label(text='Дата показаний',
                             font_size=self.font_size,
                             color=self.text_color))
        self.date = TextInput(multiline=False,
                              text=f'{date}',
                              font_size=self.font_size,
                              halign="center",
                              pos_hint={"center_x": .5, "center_y": .5},
                              )
        gl1.add_widget(self.date)
        bl_main.add_widget(gl1)
        gl2 = GridLayout(cols=4,
                         padding=[50, 80])
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
                                    text=str(self.get_data_history(self.profile)[-2]),
                                    font_size=self.font_size,
                                    halign="center",
                                    pos_hint={"center_x": .5, "center_y": .5},
                                    size_hint=[.3, 1])
        gl2.add_widget(self.cold_water)

        gl2.add_widget(Button(text='+',
                              background_color=self.button_color,
                              font_size=self.font_size,
                              size_hint=[.2, 1],
                              on_press=self.cw_plus))

        gl3 = GridLayout(cols=4,
                         padding=[50, 80])
        gl3.add_widget(Label(text='ГВС',
                             font_size=self.font_size,
                             color=self.text_color))
        gl3.add_widget(Button(text='-',
                              background_color=self.button_color,
                              font_size=self.font_size,
                              size_hint=[.2, 1],
                              on_press=self.hw_min))
        self.hot_water = TextInput(multiline=False,
                                   text=str(self.get_data_history(self.profile)[-1]),
                                   font_size=self.font_size,
                                   halign="center",
                                   pos_hint={"center_x": .5, "center_y": .5},
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

        gl05 = GridLayout(cols=2,
                          padding=[30, 80])
        gl05.add_widget(Label(text='Имя профиля',
                              font_size=self.font_size,
                              color=self.text_color))
        self.profile_name = TextInput(multiline=False,
                                      font_size=self.font_size)
        gl05.add_widget(self.profile_name)
        bl_settings.add_widget(gl05)

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
        sv_history = ScrollView()
        sv_history.add_widget(self.refresh_history(instance=None))
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
        self.screen4.add_widget(bl_history)

        self.sm.add_widget(screen1)
        self.sm.add_widget(screen2)
        self.sm.add_widget(screen3)
        self.sm.add_widget(self.screen4)
        self.sm.current = 'main'
        return self.sm

    def get_data_history(self, profile):
        data = sqlite.get_all_data(profile)
        if data:
            return data[-1]
        return [0, 0]

    def update_history_screen(self):
        self.screen4.clear_widgets()

        history_grid = self.refresh_history(None)
        sv_history = ScrollView()
        sv_history.add_widget(history_grid)
        bl_history = BoxLayout(orientation='vertical')

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
        bl_history.add_widget(sv_history)
        bl_history.add_widget(Button(text='Назад',
                                     font_size=self.font_size,
                                     on_press=self.to_main,
                                     background_color=self.button_color,
                                     bold=True,
                                     size_hint=[1, .2]))

        self.screen4.add_widget(bl_history)

    def refresh_history(self, instance):
        history_grid = GridLayout(cols=3, spacing=50, size_hint_y=None)
        history_grid.bind(minimum_height=history_grid.setter('height'))
        for i in sqlite.get_all_data(self.profile):
            label_history_data = Label(text=str(i[1]),
                                       font_size=self.font_size,
                                       color=self.text_color)
            history_grid.add_widget(label_history_data)

            label_history_cw = Label(text=str(i[2]),
                                     font_size=self.font_size,
                                     color=self.text_color)
            history_grid.add_widget(label_history_cw)

            label_history_hw = Label(text=str(i[3]),
                                     font_size=self.font_size,
                                     color=self.text_color)
            history_grid.add_widget(label_history_hw)
        return history_grid
    def write_config(self, instance):
        if self.profile_name.text and self.from_email.text and self.password.text and self.to_email.text and self.subject.text:
            sqlite.create_new_profile(self.profile,
                                      self.profile_name.text,
                                      self.from_email.text,
                                      self.password.text,
                                      self.to_email.text,
                                      self.subject.text)
            self.show_popup(self.set_done)
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
        self.update_profile_buttons()
        self.sm.current = 'main'


    def to_done(self, instance):
        self.sm.current = 'done'

    def to_history(self, instance):
        self.update_history_screen()
        self.sm.current = 'history'

    def send_e_mail(self, instance):
        profile = sqlite.get_profile(self.profile)
        if profile:
            FROM_E_MAIL = profile[2]
            PASS = profile[3]
            TO_E_MAIL = profile[4]
            SUBJECT = profile[5]

            if self.date.text and self.hot_water.text and self.cold_water.text:
                try:
                    mgs = MIMEMultipart()
                    mgs['From'] = FROM_E_MAIL
                    mgs['To'] = ', '.join([TO_E_MAIL, FROM_E_MAIL])
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
                    sqlite.create_new_data(self.profile, self.date.text, self.cold_water.text, self.hot_water.text)
                except:
                    self.show_popup(self.send_error)
            else:
                self.show_popup(self.data_error)
        else:
            self.show_popup(self.send_error, self.to_settings)


if __name__ == "__main__":
    EmailsenderApp().run()
