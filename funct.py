from g4f.client import Client
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Функция генерации pdf
def genered_variants(t, v=1):
    client = Client()
    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": f"Тебе будет предложен один вариант контрольной работы по алгебре. Твоя задача - составить {v} новых вариантов с подобными задачами. Не используй никакого форматирования, просто текст. В качестве возведения в степень используй символ '^'. Вот пример контрольной работы: {t}"}],

        )
        if "В" in response.choices[0].message.content:
            print("Работает")
            break
        print("Ещё раз")
    text = response.choices[0].message.content.split("\n") + ['', 'Ответы:', '1 –', '2 – ', '3 – ']
    canvas = Canvas("test.pdf", pagesize=A4)
    text_ob = canvas.beginText(10, 800)
    text_ob.setFont("Times-New_Roman", 12)
    for line in text:
        text_ob.textLine(line)
    canvas.drawText(text_ob)
    canvas.save()


if __name__ == "__main__":
    with open(r"C:\Users\Kostya\Desktop\test.txt") as file:
        t = file.read()
    pdfmetrics.registerFont(TTFont('Times-New_Roman', 'times-new-roman-cyr.ttf'))
    genered_variants(t)
