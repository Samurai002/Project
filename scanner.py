import cv2

# Задаём размер окна, похожий на вертикальный лист A4
WIDTH = 350 * 2  # Ширина
HEIGHT = 495 * 2 # Высота

# Открываем видеопоток с веб-камеры
cap = cv2.VideoCapture(0)

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
        cv2.imwrite('result.png', frame_resized)
        print('Фото сохранено!')

    # Если нажата клавиша 'q', закрываем приложение
    if key == ord('q'):
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
