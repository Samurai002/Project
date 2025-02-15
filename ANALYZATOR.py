import cv2
from PIL import Image, ImageDraw
import easyocr
import numpy as np
from PIL import ImageFont

class MathExpressionRecognizer:
    def __init__(self):
        # Initialize EasyOCR with English language
        self.reader = easyocr.Reader(['en'])
        
        # Define mathematical symbols for detection
        self.math_symbols = {
            'V': '√',
            '÷': '/',
            '×': '*',
            '+': '+',
            '-': '-',
            '=': '='
        }

    def preprocess_image(self, image):
        """Preprocess the image for better OCR results"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
            
        # Apply bilateral filter to preserve edges while removing noise
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Adaptive thresholding to handle different lighting conditions
        binary = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )
        
        # Dilate to connect components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(binary, kernel, iterations=1)
        
        return dilated

    def normalize_math_symbols(self, text):
        """Normalize detected mathematical symbols"""
        for symbol, replacement in self.math_symbols.items():
            text = text.replace(symbol, replacement)
        return text

    def recognize(self, image_path):
        """Main recognition function"""
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
            
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Get results from EasyOCR
        easy_ocr_result = self.reader.readtext(processed_image)
        
        # Sort results by y-coordinate (top to bottom)
        easy_ocr_result.sort(key=lambda x: x[0][0][1])
        
        # Extract and normalize text
        recognized_texts = [self.normalize_math_symbols(detection[1].replace(" ", "")) for detection in easy_ocr_result]
        
        return recognized_texts

def scanner():
    # Задаём размер окна, похожий на вертикальный лист A4
    WIDTH = 600  # Ширина
    HEIGHT = 600 # Высота

    # Открываем видеопоток с веб-камеры
    cap = cv2.VideoCapture(0)

    # Проверка на успешное подключение к камере
    if not cap.isOpened():
        print("Не удалось подключиться к веб-камере.")
        return

    # Устанавливаем разрешение видеопотока (если камера поддерживает)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    while True:
        # Считываем текущий кадр
        ret, frame = cap.read()

        # Проверяем, что кадр был получен
        if not ret:
            print("Не удалось получить кадр с веб-камеры.")
            break

        # Изменяем размер кадра для отображения в окне с пропорциями A4
        frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))

        # Отображаем изображение в реальном времени
        cv2.imshow('A4 Sized Window (Vertical)', frame_resized)

        # Ждем нажатия клавиши
        key = cv2.waitKey(1)

        # Если нажата клавиша 'f', сохраняем изображение
        if key == ord('f'):
            cv2.imwrite('image.png', frame_resized)
            print('Фото сохранено!')

        # Если нажата клавиша 'q', закрываем приложение
        if key == ord('q'):
            break

    # Освобождаем ресурсы и закрываем окна
    cap.release()
    cv2.destroyAllWindows()

def image_cutter():
    # Функция для нахождения наибольшего контура
    def find_largest_contour(image, contours):
        largest_area = 0
        largest_contour = None
        
        for contour in contours:
            # Вычисляем площадь контура
            area = cv2.contourArea(contour)
            
            # Если площадь текущего контура больше, чем предыдущего наибольшего
            if area > largest_area:
                largest_area = area
                largest_contour = contour
        
        return largest_contour

    # Загружаем изображение
    image = cv2.imread('image.png')

    if image is None:
        print("Ошибка: изображение не загружено!")
        return

    # Преобразуем изображение в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяем адаптивную бинаризацию для улучшения качества при разных условиях освещения
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    #cv2.imwrite('thresh_debug.png', thresh)  # Сохраняем для отладки

    # Находим контуры
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("Контуры не найдены!")
        return

    # Визуализируем все найденные контуры для отладки
    contour_img = image.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
    #cv2.imwrite('contours_debug.png', contour_img)  # Сохраняем изображение с контурами для отладки

    # Находим наибольший контур
    largest_contour = find_largest_contour(image, contours)

    # Если нашли наибольший контур
    if largest_contour is not None:
        # Получаем ограничивающий прямоугольник
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Вырезаем наибольший прямоугольник
        rect_img = image[y:y+h, x:x+w]
        
        # Сохраняем вырезанный прямоугольник в файл obrez.png
        cv2.imwrite('obrez.png', rect_img)
        print("Вырезанное изображение сохранено как obrez.png")

        # Отображаем вырезанный прямоугольник для проверки
        #cv2.imshow("Вырезанный прямоугольник", rect_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("Прямоугольник не найден.")

def crop_image(cm_to_crop=1.3):
    # Загрузить изображение
    image = cv2.imread("obrez.png")
    if image is None:
        print("Ошибка: изображение не найдено!")
        return False

    # Получаем размеры изображения
    height, width, _ = image.shape

    # Рассчитаем смещение в пикселях на основе 2 см. 1 см ≈ 37.8 пикселей (при 96 DPI)
    cm_to_pixels = 37.8
    offset = int(cm_to_crop * cm_to_pixels)  # Преобразуем сантиметры в пиксели

    # Обрезаем изображение, оставляя только правую часть (где находятся ответы)
    cropped_image = image[0:height, offset:width]

    # Сохраняем обрезанное изображение
    cv2.imwrite("obrez_cropped.png", cropped_image)
    print(f"Обрезанное изображение сохранено как obrez_cropped.png")

def analys(correct_answers, result_image_path='result.png'):
    recognizer = MathExpressionRecognizer()

    # Загрузка и предобработка изображения
    image_cv = cv2.imread("obrez_cropped.png")
    if image_cv is None:
        print("Ошибка: изображение не найдено!")
        return

    # Преобразования изображения
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(gray)
    median_filtered = cv2.medianBlur(enhanced_img, 3)
    inverted_img = cv2.bitwise_not(median_filtered)

    try:
        # Распознавание текста
        easy_ocr_result = recognizer.reader.readtext(inverted_img)
        
        # Создание основного изображения
        image = Image.open("obrez_cropped.png").convert("RGBA")
        base_image = image.copy()
        
        # Слои для элементов
        answers_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
        table_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))

        # Параметры подсчета
        correct_count = 0
        incorrect_count = 0
        correct_indices = []
        incorrect_indices = []

        # Отрисовка ответов
        answers_draw = ImageDraw.Draw(answers_layer)
        for i, detection in enumerate(easy_ocr_result):
            text = detection[1].strip().strip(".")
            if text.isdigit():
                # Координаты bounding box
                (tl, tr, br, bl) = detection[0]
                x_min = int(min(tl[0], bl[0]))
                y_min = int(min(tl[1], tr[1]))
                x_max = int(max(tr[0], br[0]))
                y_max = int(max(bl[1], br[1]))

                # Определение цвета
                idx = len(correct_indices) + len(incorrect_indices)
                if idx < len(correct_answers):
                    if text == correct_answers[idx]:
                        color = (0, 255, 0, 128)
                        correct_count += 1
                        correct_indices.append(idx+1)
                    else:
                        color = (255, 0, 0, 128)
                        incorrect_count += 1
                        incorrect_indices.append(idx+1)

                    # Рисуем прямоугольник
                    answers_draw.rectangle([(x_min, y_min), (x_max, y_max)], fill=color)

        # Отрисовка таблички
        table_draw = ImageDraw.Draw(table_layer)
        try:
            font = ImageFont.truetype("ARIALBD.ttf", 40)
        except:
            font = ImageFont.load_default().font_variant(size=40)

        # Текст таблички
        result_text = [
            f"✓ Правильных: {correct_count} ({', '.join(map(str, correct_indices))})",
            f"✗ Ошибок: {incorrect_count} ({', '.join(map(str, incorrect_indices))})"
        ]

        # Расчет размеров
        text_sizes = [table_draw.textlength(line, font=font) for line in result_text]
        max_width = max(text_sizes)
        line_height = 50
        padding = 20
        
        # Позиционирование
        table_width = max_width + 2*padding
        table_height = len(result_text)*line_height + padding
        table_x = image.width - table_width - 50
        table_y = image.height - table_height - 50

        # Фон таблички
        table_draw.rounded_rectangle(
            [(table_x-10, table_y-10), (table_x+table_width+10, table_y+table_height+10)],
            fill=(0, 0, 0, 200),
            radius=15,
            outline=(255, 255, 0),
            width=3
        )

        # Текст таблички
        for i, line in enumerate(result_text):
            y_pos = table_y + padding + i*line_height
            table_draw.text(
                (table_x + padding, y_pos),
                line,
                font=font,
                fill=(255, 255, 255))
        
        # Собираем финальное изображение
        image = Image.alpha_composite(base_image, answers_layer)
        image = Image.alpha_composite(image, table_layer)

        # Сохранение
        image.save(result_image_path)
        print(f"Результат сохранен: {result_image_path}")

    except Exception as e:
        print(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    correct_answers = ['200', '100', '789', '497', '367']
    scanner()
    image_cutter()
    crop_image(cm_to_crop=2.7)
    analys(correct_answers)