from g4f.client import Client
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Загрузка файла - пример для AI
path = r"ПУТЬ ДО ФАЙЛА С ПРИМЕРОМ"
with open(path) as f:
    obraz = f.read()

# Функция генерации тестов
def genered_variants(t):
    client = Client()
    while True:
        print("Загрузка...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": f"Тебе будет предложен один вариант контрольной работы по алгебре для учеников 7 класса. Твоя задача - составить 1 новый вариант с пятью подобными задачами. Не используй никакого форматирования, просто текст. В качестве возведения в степень используй символ '^'. Вот пример контрольной работы: {t}"}],

        )
        if "В" in response.choices[0].message.content:
            break
        else:
            print("Повторим ещё раз")

    return response.choices[0].message.content


text = genered_variants(obraz).split("\n") + ['', 'Ответы:', '1 –', '2 – ', '3 – ', '4 – ', '5 –', '']

pdf_path = r"ПУТЬ ГДЕ БУДЕТ СОЗДАНА PDF-КА"
canvas = Canvas(pdf_path, pagesize=A4)
pdfmetrics.registerFont(TTFont('Times-New_Roman', 'times-new-roman-cyr.ttf'))

text_ob = canvas.beginText(10, 800)

text_ob.setFont("Times-New_Roman", 12)
for line in text:
    text_ob.textLine(line)
canvas.drawText(text_ob)

canvas.save()
