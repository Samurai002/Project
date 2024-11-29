import cv2
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import os
import numpy as np


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
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract\tesseract.exe'  # Укажите правильный путь

    # Открываем исходное изображение через OpenCV
    image_cv = cv2.imread("obrez_cropped.png")

    if image_cv is None:
        print("Ошибка: изображение для анализа не найдено!")
        return

    # Преобразуем в оттенки серого
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    
    # Применим CLAHE для улучшения контраста изображения
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(gray)
    #cv2.imwrite('enhanced_image.png', enhanced_img)  # Сохраним для отладки

    # Применим медианный фильтр для удаления шума
    median_filtered = cv2.medianBlur(enhanced_img, 3)
    #cv2.imwrite('median_filtered.png', median_filtered)

    # Инвертируем изображение (если текст черный на белом фоне)
    inverted_img = cv2.bitwise_not(median_filtered)
    #cv2.imwrite('inverted_image.png', inverted_img)

    # Применяем пороговую бинаризацию
    _, thresh = cv2.threshold(inverted_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite('final_thresh_image.png', thresh)
   
    # Применить OCR   
    try:
        config = "--psm 6 -c tessedit_char_whitelist=0123456789"  # Режим страницы 6: распознавание блока текста
        data = pytesseract.image_to_data(thresh, config=config, output_type=pytesseract.Output.DICT)

        # Проверка распознанного текста
        print(f"Распознанный текст: {data['text']}")

        # Открыть изображение с помощью Pillow для разметки
        image = Image.open("obrez_cropped.png")
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


if __name__ == "__main__":
    correct_answers = ['44', '55', '17', '17', '98']
    #scanner()
    image_cutter()
    crop_image(cm_to_crop=1.3)
    analys(correct_answers)