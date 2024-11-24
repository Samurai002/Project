from PIL import Image
import pytesseract
import cv2
import os

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

# Показать оригинальное и обработанное изображения
cv2.imshow("Original Image", image)
cv2.imshow("Processed Image", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
