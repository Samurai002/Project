#import cv2
#import pytesseract

#def analys():
 #   pytesseract.pytesseract.tesseract_cmd = 'Tesseract\\tesseract.exe'

 #   # Подключение фото
  #  img = cv2.imread('image.png')
 #   img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#    # Будет выведен весь текст с картинки
 #   config = r'--oem 3 --psm 6'
#    text = pytesseract.image_to_string(img, lang='eng+rus', config=config)

    # Запись результата в файл result.txt
#    with open('result.txt', 'w', encoding='utf-8') as file:
#        file.write(text)

#    print("Результат сохранен в файл result.txt")

#if __name__ == "__main__":
#    analys()