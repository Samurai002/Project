import cv2
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import os
import numpy as np


def analys(correct_answers, image_path='obrez.png', result_image_path='result.png'):
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract\tesseract.exe'  # Укажите правильный путь

    # Открываем исходное изображение через OpenCV
    image_cv = cv2.imread(image_path)

    if image_cv is None:
        print("Ошибка: изображение для анализа не найдено!")
        return

    # Преобразуем в оттенки серого
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray_image.png', gray)  # Сохраним для отладки

    # Попробуем использовать обычную бинаризацию без инверсии
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('thresh_image.png', thresh)  # Сохраним для отладки

    # Сохраняем промежуточное изображение, чтобы видеть результаты OpenCV
    intermediate_path = "intermediate_image.png"
    cv2.imwrite(intermediate_path, thresh)

    # Применить OCR
    try:
        config = "--psm 6 -c tessedit_char_whitelist=0123456789"  # Режим страницы 6: распознавание блока текста
        data = pytesseract.image_to_data(thresh, config=config, output_type=pytesseract.Output.DICT)

        # Проверка распознанного текста
        print(f"Распознанный текст: {data['text']}")

        # Открыть изображение с помощью Pillow для разметки
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Проходим по данным OCR и отмечаем ответы
        answers = []
        for i, word in enumerate(data['text']):
            word = word.strip().strip(".")  # Убираем любые точки и лишние пробелы
            if word.isdigit() and word != "":
                answers.append(word)
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                # Определяем, правильный или неправильный ответ
                idx = len(answers) - 1  # Индекс ответа
                if idx < len(correct_answers):
                    if word == correct_answers[idx]:
                        draw.rectangle([(x, y), (x + w, y + h)], outline="green", width=3)
                    else:
                        draw.rectangle([(x, y), (x + w, y + h)], outline="red", width=3)

        # Проверка списка распознанных ответов
        if not answers:
            print("Ответы не были распознаны. Проверьте качество изображения и настройки OCR.")
            return

        print(f"Распознанные ответы: {answers}")

        # Сохраняем результат с разметкой
        image.save(result_image_path)
        print(f"Изображение с пометками сохранено как {result_image_path}")

    except Exception as e:
        print(f"Ошибка при применении OCR: {e}")
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
    # Функция для нахождения наибольшего прямоугольника
    def find_largest_rectangle(image, contours):
        largest_area = 0
        largest_rect = None
        
        for contour in contours:
            # Аппроксимация контура
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Если контур имеет 4 угла (предполагаем прямоугольник)
            if len(approx) == 4:
                # Вычисляем площадь
                area = cv2.contourArea(contour)
                
                # Если площадь текущего контура больше, чем предыдущего наибольшего
                if area > largest_area:
                    largest_area = area
                    largest_rect = approx
        
        return largest_rect

    # Загружаем изображение
    image = cv2.imread('image.png')

    # Преобразуем изображение в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяем пороговое значение
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Находим контуры
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Находим наибольший прямоугольник
    largest_rect = find_largest_rectangle(image, contours)

    # Если нашли наибольший прямоугольник
    if largest_rect is not None:
        # Получаем координаты ограничивающего прямоугольника
        x, y, w, h = cv2.boundingRect(largest_rect)
        
        # Вырезаем наибольший прямоугольник
        rect_img = image[y:y+h, x:x+w]
        
        # Сохраняем вырезанный прямоугольник в файл otvet.png
        cv2.imwrite('obrez.png', rect_img)
        
        # Ожидаем нажатие клавиши для закрытия окна
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("Прямоугольник не найден.")

def crop_image(image_path, output_path, cm_to_crop=2):
    # Загрузить изображение
    image = cv2.imread(image_path)
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
    cv2.imwrite(output_path, cropped_image)
    print(f"Обрезанное изображение сохранено как {output_path}")
    return True
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
    cv2.imwrite("output.png", cropped_image)
    print(f"Обрезанное изображение сохранено как output.png")
    return True

if __name__ == "__main__":
    correct_answers = ['25', '61', '74', '98', '81']
    #scanner()
    image_cutter()
    crop_image('obrez.png', 'obrez_cropped.png', cm_to_crop=2)
    analys(correct_answers, image_path='obrez_cropped.png')