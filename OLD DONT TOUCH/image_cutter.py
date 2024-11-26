import cv2
import numpy as np

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
