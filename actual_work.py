import cv2
from PIL import Image
import pytesseract
import os

def analys():
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract\tesseract.exe'  # Укажите правильный путь
    image_path = 'image.png'

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

if __name__ == "__main__":
    scanner()
    analys()