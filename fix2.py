from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(
            text="Главный экран",
            size_hint=(1, 0.15),
            font_size='30sp'
        )
        layout.add_widget(label)

        button_generation = Button(
            text="Генерация вариантов",
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        button_generation.bind(on_press=self.open_generation_screen)
        layout.add_widget(button_generation)

        button_check = Button(
            text="Проверка вариантов",
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        button_check.bind(on_press=self.open_check_screen)
        layout.add_widget(button_check)

        self.add_widget(layout)

    def open_generation_screen(self, instance):
        self.manager.current = "generation"

    def open_check_screen(self, instance):
        self.manager.current = "check"


class GenerationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(main_layout)

        top_buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        # Кнопка назад
        back_button = Button(
            text="Назад",
            size_hint=(None, None),
            size=(60, 50)  
        )
        back_button.bind(on_press=self.go_back)
        top_buttons_layout.add_widget(back_button)

        # кнопка загрузки файлов
        load_button = Button(
            text="Загрузить файл",
            size_hint=(None, None),
            size=(150, 50)  
        )
        load_button.bind(on_press=self.load_file)
        top_buttons_layout.add_widget(load_button)

        main_layout.add_widget(top_buttons_layout)

        # Отображение загруженного текста
        self.scroll_view = ScrollView(size_hint=(1, 0.15)) 
        with self.scroll_view.canvas.before:
            Color(1, 1, 1, 1)  
            self.rect = Rectangle(size=self.scroll_view.size, pos=self.scroll_view.pos)

        self.scroll_view.bind(size=self.update_background, pos=self.update_background)

        self.text_label = Label(
            text="Здесь будет отображаться текст из файла",
            size_hint_y=None,
            height=0,  
            valign='top',
            halign='left',
            color=(0, 0, 0, 1)  
        )
        self.text_label.bind(size=self.update_text_size)
        self.scroll_view.add_widget(self.text_label)
        main_layout.add_widget(self.scroll_view)

        # Кнопка "Создать варианты"
        create_variants_button = Button(
            text="Создать варианты",
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        create_variants_button.bind(on_press=self.create_variants)
        main_layout.add_widget(create_variants_button)

        # Поле для отображения созданных вариантов 
        # НУЖНО СПРОСИТЬ У КОСТИ И ДОРАБОТАТЬ
        self.variants_scroll_view = ScrollView(size_hint=(1, 0.3))  
        with self.variants_scroll_view.canvas.before:
            Color(1, 1, 1, 1) 
            self.variants_rect = Rectangle(
                size=self.variants_scroll_view.size, pos=self.variants_scroll_view.pos
            )

        self.variants_scroll_view.bind(
            size=self.update_variants_background, pos=self.update_variants_background
        )

        self.variants_label = Label(
            text="",
            size_hint_y=None,
            height=0,  
            valign='top',
            halign='left',
            color=(0, 0, 0, 1) 
        )
        self.variants_label.bind(size=self.update_variants_size)
        self.variants_scroll_view.add_widget(self.variants_label)
        main_layout.add_widget(self.variants_scroll_view)

    def update_text_size(self, instance, value):
        self.text_label.text_size = (self.text_label.width, None)
        self.text_label.height = self.text_label.texture_size[1]

    def update_background(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def update_variants_size(self, instance, value):
        self.variants_label.text_size = (self.variants_label.width, None)
        self.variants_label.height = self.variants_label.texture_size[1]

    def update_variants_background(self, instance, value):
        self.variants_rect.size = instance.size
        self.variants_rect.pos = instance.pos

    def go_back(self, instance):
        self.manager.current = "main"

    def load_file(self, instance):
        # функция загрузки файлов
        Tk().withdraw() 
        file_path = askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_label.text = content
    # НУЖНО СПРОСИТЬ У КОСТИ И ДОРАБОТАТЬ #2
    def create_variants(self, instance):
        self.variants_label.text = (
            "Варианты созданы!"
        )  

class CheckScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.is_function_called = False
        self.main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.add_widget(self.main_layout)

        back_button = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        back_button.bind(on_press=self.go_back)
        self.main_layout.add_widget(back_button)

        self.image_widget = Image(size_hint=(1, 0.7))
        self.main_layout.add_widget(self.image_widget)

        self.scan_button = Button(
            text="Сделать скан", size_hint=(0.5, 0.1), pos_hint={"center_x": 0.5}
        )
        self.scan_button.bind(on_press=self.toggle_video)
        self.main_layout.add_widget(self.scan_button)

        check_button = Button(
            text="Проверить работу",
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        check_button.bind(on_press=self.add_text_widget)  
        self.main_layout.add_widget(check_button)

        self.capture = None
        self.frame = None
        self.event = None

    def toggle_video(self, instance=None):
        # Переключает состояние видеопотока: запуск/остановка
        if self.capture and self.capture.isOpened():
            self.stop_video()
        else:
            self.start_video()

    def start_video(self):
        # Запускает видеопоток
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
        if not self.event:
            self.event = Clock.schedule_interval(self.update_video, 1 / 30)

    def stop_video(self):
        # Останавливает видеопоток
        if self.event:
            Clock.unschedule(self.event)
            self.event = None
        if self.capture:
            self.capture.release()
            self.capture = None

    def update_video(self, *args):
        # Обновляет текстуру видеопотока 
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
                texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
                self.image_widget.texture = texture

    def on_enter(self):
        # Вызывается при входе на экран: запускает видеопоток
        self.start_video()

    def on_leave(self):
        # Вызывается при выходе с экрана: останавливает видеопоток
        self.stop_video()

    def capture_frame(self, instance):
        # Сохраняет последний кадр
        if self.capture and self.frame is not None:
            cv2.imwrite("captured_frame.jpg", self.frame)

    def go_back(self, instance):
        self.manager.current = "main"
    
    def add_text_widget(self, instance):
        if not self.is_function_called:
            self.is_function_called = True  
            new_label = Label(
                text="Тест",
                size_hint=(1, None),
                height=40,
                font_size='18sp',
            )
            self.main_layout.add_widget(new_label)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(GenerationScreen(name="generation"))
        sm.add_widget(CheckScreen(name="check"))
        return sm


if __name__ == "__main__":
    MyApp().run()
