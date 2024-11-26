import cv2
from PIL import Image
import pytesseract
import os
import numpy as np


def analys():
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract\tesseract.exe'  # Укажите правильный путь
    image_path = 'obrez.png'

    # Загрузить изображение и проверить его
    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка: изображение не найдено!")
        exit(1)

    preprocess = "thresh"

    # Преобразовать в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применить пороговое значение для предварительной обработки изображения
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    #Сохранить временный файл для OCR
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    print(f"Сохранен временный файл: {filename}")

    # Применить OCR с ограничением только на цифры
    try:
        config = "--psm 6 -c tessedit_char_whitelist=0123456789.,-"  # Режим страницы 6: распознавание блока текста
        text = pytesseract.image_to_string(Image.open(filename), config=config)
        print(f"{text}")
        
        # Записать результат в файл result.txt
        with open("result.txt", "w") as file:
            file.write(text)
            print("Распознанный текст сохранен в файл result.txt")
    except Exception as e:
        print(f"Ошибка при применении OCR: {e}")

    # Удалить временный файл
    os.remove(filename)

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


if __name__ == "__main__":
    scanner()
    image_cutter()
    analys()