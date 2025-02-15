from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import webbrowser
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.button import MDIconButton
import cv2
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

class CustomIconButton(MDIconButton, MDTooltip):
    pass

KV = '''
ScreenManager:
    LoginScreen:
    MainScreen:
    GenerationScreen:
    CheckScreen:
    HelpScreen:
    ProfileScreen:

<LoginScreen>:
    name: "login"
    
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(40)
        spacing: dp(20)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: (0.8, 0.6)
        
        MDLabel:
            text: "Авторизация"
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H5"
            bold: True

        MDTextField:
            id: login_field
            hint_text: "Введите логин"
            icon_right: "account"
            size_hint_x: None
            width: dp(250)
            pos_hint: {"center_x": 0.5}

        MDTextField:
            id: password_field
            hint_text: "Введите пароль"
            password: True
            icon_right: "eye"
            size_hint_x: None
            width: dp(250)
            pos_hint: {"center_x": 0.5}

        MDRectangleFlatButton:
            text: "Войти"
            size_hint_x: None
            width: dp(200)
            pos_hint: {"center_x": 0.5}
            on_release: app.login()

<ProfileScreen>:
    name: "profile"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            md_bg_color: 0.678, 0.847, 0.902, 1
            specific_text_color: 0, 0, 0, 1
            elevation: 5

            MDFloatLayout:
                MDIconButton:
                    icon: "home"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(40), dp(40)
                    pos_hint: {"center_x": 0.03, "center_y": 0.95}
                    on_release: app.root.current = "main"

                MDRectangleFlatButton:
                    text: "Генерация\\nтестов"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.35, "center_y": 0.95}
                    on_release: root.open_generation_screen()

                MDIconButton:
                    icon: "account"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(50), dp(50)
                    pos_hint: {"center_x": 0.5, "center_y": 0.95}
                    on_release: app.go_to_profile()  
                    tooltip_text: "Перейти в личный кабинет"

                MDRectangleFlatButton:
                    text: "Проверка\\nтестов"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.65, "center_y": 0.95}
                    on_release: root.open_check_screen()

        MDLabel:
            text: "Личный кабинет"
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H5"
            bold: True

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(10)
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}

            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(10)

                MDLabel:
                    text: "Фамилия:"
                    size_hint_x: None
                    width: dp(100)
                    theme_text_color: "Primary"
                
                MDLabel:
                    text: "Иванов"
                    theme_text_color: "Primary"

            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(10)

                MDLabel:
                    text: "Имя:"
                    size_hint_x: None
                    width: dp(100)
                    theme_text_color: "Primary"
                
                MDLabel:
                    text: "Иван"
                    theme_text_color: "Primary"

            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(10)

                MDLabel:
                    text: "Email:"
                    size_hint_x: None
                    width: dp(100)
                    theme_text_color: "Primary"
                
                MDLabel:
                    text: "testemail@test.ru"
                    theme_text_color: "Primary"

            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(10)

                MDLabel:
                    text: "Ваш уровень доступа:"
                    size_hint_x: None
                    width: dp(200)
                    theme_text_color: "Primary"

                MDLabel:
                    text: "Администратор"
                    theme_text_color: "Custom"
                    text_color: 1, 0, 0, 1  # Красный цвет

<MainScreen>:
    name: "main"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            md_bg_color: 0.678, 0.847, 0.902, 1
            specific_text_color: 0, 0, 0, 1
            elevation: 5

            MDFloatLayout:
                MDIconButton:
                    icon: "home"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(40), dp(40)
                    pos_hint: {"center_x": 0.03, "center_y": 0.95}
                    on_release: app.root.current = "main"

                MDRectangleFlatButton:
                    text: "Генерация\\nтестов"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.35, "center_y": 0.95}
                    on_release: root.open_generation_screen()

                MDIconButton:
                    icon: "account"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(50), dp(50)
                    pos_hint: {"center_x": 0.5, "center_y": 0.95}
                    on_release: app.go_to_profile()  
                    tooltip_text: "Перейти в личный кабинет"

                MDRectangleFlatButton:
                    text: "Проверка\\nтестов"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.65, "center_y": 0.95}
                    on_release: root.open_check_screen()

        MDLabel:
            text: "Добро пожаловать в помощник учителя\\n\\nТут вы сможете создавать уникальные тесты для своего класса\\n\\nи автоматически проверять их."
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H5"
            bold: True
            size_hint_y: None  
            height: dp(200) 

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(20)

            MDRectangleFlatButton:
                text: "Личный кабинет"
                size_hint: 0.6, None
                height: dp(48)
                pos_hint: {"center_x": 0.5}
                on_release: app.go_to_profile()  

            MDRectangleFlatButton:
                text: "Генерация тестов"
                size_hint: 0.6, None
                height: dp(48)
                pos_hint: {"center_x": 0.5}
                on_release: root.open_generation_screen()

            MDRectangleFlatButton:
                text: "Проверка тестов"
                size_hint: 0.6, None
                height: dp(48)
                pos_hint: {"center_x": 0.5}
                on_release: root.open_check_screen()

<GenerationScreen>:
    name: "generation"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            md_bg_color: 0.678, 0.847, 0.902, 1
            specific_text_color: 0, 0, 0, 1
            elevation: 5

            MDFloatLayout:
                CustomIconButton:
                    icon: "home"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(40), dp(40)
                    pos_hint: {"center_x": 0.03, "center_y": 0.95}
                    on_release: app.root.current = "main"
                    tooltip_text: "Вернуться на главный экран"

                MDRectangleFlatButton:
                    text: "Генерация\\nтестов"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.35, "center_y": 0.95}
                    on_release: app.root.current = "generation"

                MDIconButton:
                    icon: "account"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(50), dp(50)
                    pos_hint: {"center_x": 0.5, "center_y": 0.95}
                    on_release: app.go_to_profile()  
                    tooltip_text: "Перейти в личный кабинет"

                MDRectangleFlatButton:
                    text: "Проверка\\nтесты"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.65, "center_y": 0.95}
                    on_release: root.open_check_screen()

                MDFloatLayout:
                    size_hint: None, None
                    size: dp(220), dp(50)
                    pos_hint: {"center_x": 0.85, "center_y": 0.95}

                    CustomIconButton:
                        icon: "help"
                        icon_size: "30sp"
                        theme_text_color: "Custom"
                        text_color: 0, 0.44, 0.8, 1
                        size_hint: None, None
                        size: dp(40), dp(40)
                        pos_hint: {"center_x": 0.4, "center_y": 0.5}
                        on_release: app.root.current = "help"
                        tooltip_text: "Открыть справку по генерации тестов"

                    MDRectangleFlatButton:
                        text: "Справка\\nПо генерации"
                        theme_text_color: "Custom"
                        text_color: 0, 0.44, 0.8, 1
                        line_color: 0, 0.44, 0.8, 1
                        size_hint: None, None
                        size: dp(160), dp(40)
                        pos_hint: {"center_x": 0.75, "center_y": 0.5}
                        on_release: app.root.current = "help"

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(10)
            padding: dp(10)

            MDCard:
                size_hint: (1, 0.6)
                padding: dp(10)
                md_bg_color: 1, 1, 1, 1

                ScrollView:
                    MDLabel:
                        id: text_label
                        text: "Здесь будет отображаться загруженный вами вариант"
                        size_hint_y: None
                        height: self.texture_size[1]
                        theme_text_color: "Primary"
                        halign: "left"
                        valign: "top"
                        padding: dp(10)

            MDRectangleFlatButton:
                text: "Загрузить файл с вариантом"
                size_hint_x: None
                width: dp(150)
                pos_hint: {"center_x": 0.5}
                on_release: root.load_file()
            
            MDTextField:
                id: text_input
                hint_text: "Введите кол-во нужных вариантов"
                size_hint_x: None
                width: dp(300)
                pos_hint: {"center_x": 0.5}
                input_filter: "int"

            MDRectangleFlatButton:
                text: "Создать варианты"
                size_hint_x: None
                width: dp(200)
                pos_hint: {"center_x": 0.5}
                on_release: root.create_variants()

            MDRectangleFlatButton:
                id: open_pdf_button
                text: "Посмотреть сгенерированные варианты"
                size_hint_x: None
                width: dp(250)
                pos_hint: {"center_x": 0.5}
                disabled: True
                on_release: root.open_pdf_in_browser()

            MDRectangleFlatButton:
                id: print_pdf_button
                text: "Печать сгенерированных вариантов"
                size_hint_x: None
                width: dp(250)
                pos_hint: {"center_x": 0.5}
                disabled: True
                on_release: root.print_pdf()

<HelpScreen>:
    name: "help"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            md_bg_color: 0.678, 0.847, 0.902, 1
            specific_text_color: 0, 0, 0, 1
            elevation: 5

            MDFloatLayout:
                CustomIconButton:
                    icon: "home"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(40), dp(40)
                    pos_hint: {"center_x": 0.03, "center_y": 0.95}
                    on_release: app.root.current = "main"
                    tooltip_text: "Вернуться на главный экран"

                MDRectangleFlatButton:
                    text: "Генерация\\nработ"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.35, "center_y": 0.95}
                    on_release: app.root.current = "generation"

                MDIconButton:
                    icon: "account"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(50), dp(50)
                    pos_hint: {"center_x": 0.5, "center_y": 0.95}
                    on_release: app.go_to_profile()  
                    tooltip_text: "Перейти в личный кабинет"

                MDRectangleFlatButton:
                    text: "Проверка\\nработ"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.65, "center_y": 0.95}
                    on_release: root.open_check_screen()

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(10)

            MDLabel:
                text: "Справка по использованию приложения"
                halign: "center"
                theme_text_color: "Primary"
                font_style: "H5"
                bold: True 

            MDLabel:
                text: "Здесь будет информация о том, как пользоваться приложением."
                halign: "center"
                theme_text_color: "Primary"
                font_style: "Body1"
                bold: True
<CheckScreen>:
    name: "check"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            md_bg_color: 0.678, 0.847, 0.902, 1
            specific_text_color: 0, 0, 0, 1
            elevation: 5

            MDFloatLayout:
                CustomIconButton:
                    icon: "home"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(40), dp(40)
                    pos_hint: {"center_x": 0.03, "center_y": 0.95}
                    on_release: app.root.current = "main"
                    tooltip_text: "Вернуться на главный экран"

                MDRectangleFlatButton:
                    text: "Генерация\\nработ"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.35, "center_y": 0.95}
                    on_release: app.root.current = "generation"

                MDIconButton:
                    icon: "account"
                    icon_size: "50sp"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    size_hint: None, None
                    size: dp(50), dp(50)
                    pos_hint: {"center_x": 0.5, "center_y": 0.95}
                    on_release: app.go_to_profile()  
                    tooltip_text: "Перейти в личный кабинет"

                MDRectangleFlatButton:
                    text: "Проверка\\nработ"
                    theme_text_color: "Custom"
                    text_color: 0, 0.44, 0.8, 1
                    line_color: 0, 0.44, 0.8, 1
                    size_hint: 0.15, None
                    size: dp(140), dp(50)
                    pos_hint: {"center_x": 0.65, "center_y": 0.95}
                    on_release: root.open_check_screen()

                MDFloatLayout:
                    size_hint: None, None
                    size: dp(220), dp(50)
                    pos_hint: {"center_x": 0.85, "center_y": 0.95}

                    CustomIconButton:
                        icon: "help"
                        icon_size: "30sp"
                        theme_text_color: "Custom"
                        text_color: 0, 0.44, 0.8, 1
                        size_hint: None, None
                        size: dp(40), dp(40)
                        pos_hint: {"center_x": 0.4, "center_y": 0.5}
                        on_release: app.root.current = "help"
                        tooltip_text: "Открыть справку по проверке вариантов"

                    MDRectangleFlatButton:
                        text: "Справка\\nПо тестов"
                        theme_text_color: "Custom"
                        text_color: 0, 0.44, 0.8, 1
                        line_color: 0, 0.44, 0.8, 1
                        size_hint: None, None
                        size: dp(160), dp(40)
                        pos_hint: {"center_x": 0.75, "center_y": 0.5}
                        on_release: app.root.current = "help"

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(10)
            spacing: dp(10)

            MDCard:
                size_hint: (1, 0.6)
                padding: dp(10)
                md_bg_color: 1, 1, 1, 1

                Image:
                    id: image_widget
                    allow_stretch: True
                    size_hint: (1, 1)

            MDRectangleFlatButton:
                id: scan_button
                text: "Сделать скан"
                size_hint_x: None
                width: dp(200)
                pos_hint: {"center_x": 0.5}
                on_release: root.toggle_video()

            MDTextField:
                id: input_field
                hint_text: "Введите номер варианта"
                size_hint_x: None
                width: dp(300)
                pos_hint: {"center_x": 0.5}
                input_filter: "int"

            MDRectangleFlatButton:
                text: "Выбрать вариант"
                size_hint_x: None
                width: dp(200)
                pos_hint: {"center_x": 0.5}
                on_release: root.save_number()

            MDRectangleFlatButton:
                text: "Проверить работу"
                size_hint_x: None
                width: dp(200)
                pos_hint: {"center_x": 0.5}
                on_release: root.add_text_widget()
'''

class MainScreen(MDScreen):
    def open_generation_screen(self):
        self.manager.current = "generation"

    def open_check_screen(self):
        self.manager.current = "check"

class GenerationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_content = ""

    def go_back(self):
        self.manager.current = "main"

    def load_file(self):
        Tk().withdraw()
        file_path = askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.ids.text_label.text = content
            self.file_content = content

    def create_variants(self):
        if self.file_content and self.ids.text_input.text.strip():
            print(f"Создание вариантов: {self.file_content}")

        pdf_path = "test.pdf"
        if os.path.exists(pdf_path):
            self.ids.open_pdf_button.disabled = False  
            self.ids.print_pdf_button.disabled = False  

    def open_pdf_in_browser(self):
        pdf_path = "test.pdf"
        if os.path.exists(pdf_path):
            webbrowser.open_new_tab(f"file://{os.path.abspath(pdf_path)}")

    def print_pdf(self):
        print("Печать PDF: test.pdf")

    def open_check_screen(self):
        self.manager.current = "check"  

class HelpScreen(MDScreen):
    def open_generation_screen(self):
        self.manager.current = "generation"

    def open_check_screen(self):
        self.manager.current = "check"

class CheckScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_function_called = False
        self.capture = None  
        self.frame = None
        self.event = None
        self.video_running = False 

    def toggle_video(self):
        if self.video_running:
            self.stop_video()
            self.capture_frame()  
            self.ids.scan_button.text = "Сделать скан повторно"
        else:
            self.start_video()
            self.ids.scan_button.text = "Сделать скан"
        self.video_running = not self.video_running

    def start_video(self):
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
        if not self.event:
            self.event = Clock.schedule_interval(self.update_video, 1 / 30)

    def stop_video(self):
        if self.event:
            Clock.unschedule(self.event)
            self.event = None
        if self.capture:
            self.capture.release()
            self.capture = None

    def update_video(self, *args):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
                texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
                self.ids.image_widget.texture = texture

    def capture_frame(self):
        if self.frame is not None:
            cv2.imwrite("image.png", self.frame)
            self.ids.image_widget.source = "image.png"
            self.ids.image_widget.reload()

    def on_enter(self):
        self.start_video()

    def on_leave(self):
        self.stop_video()

    def go_back(self):
        self.manager.current = "main"

    def add_text_widget(self):
        if not self.is_function_called:
            correct_answers = ['44', '56', '71', '17', '98']
            self.is_function_called = True  

            result = Image(
                source='result.png',  
                size_hint=(1, None),
                height=280,  
                allow_stretch=True 
            )
            self.ids.image_widget.texture = result.texture  
            os.remove("obrez_cropped.png")
            os.remove("obrez.png")
            os.remove("final_thresh_image.png")

    def save_number(self):
        try:
            self.saved_number = int(self.ids.input_field.text)
            print(f"Сохраненное число: {self.saved_number}")
        except ValueError:
            print("Введите корректное число!")

class LoginScreen(MDScreen):
    pass

class ProfileScreen(MDScreen):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        sm = self.root = Builder.load_string(KV)
        sm.current = "login"  
        return sm

    def login(self):
        self.root.current = "main"

    def go_to_profile(self):
        self.root.current = "profile"

    def go_to_main(self):
        self.root.current = "main"

if __name__ == "__main__":
    MyApp().run()