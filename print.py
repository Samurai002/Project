import win32print
import win32api

def print_pdf(file_path):
    try:
        # Получение имени стандартного принтера
        printer_name = win32print.GetDefaultPrinter()
        print(f"Печать на принтере: {printer_name}")

        # Отправка команды на печать файла

        win32api.ShellExecute(0, "print", file_path, None, ".", 0)
        print("Документ отправлен на печать.")
    except Exception as e:
        print(f"Ошибка при печати: {e}")

if __name__ == "__main__":
    pdf_file_path = r"C:\Users\Gamer\Desktop\test.pdf"  # Замените на путь к вашему PDF-файлу
    print_pdf(pdf_file_path)
