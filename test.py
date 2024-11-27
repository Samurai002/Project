from g4f.client import Client

with open("test.txt") as file:
    t = file.read()

client = Client()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user",
         "content": f"Тебе будет предложен один вариант контрольной работы по алгебре. Твоя задача - составить 2 новых вариантов с подобными задачами. Не используй никакого форматирования, просто текст. Отдельно выведи ответы (без решения). Ответ для задания сравнения - знак >, < или = В качестве возведения в степень используй символ '^'. Вот пример контрольной работы: {t}"}],
    )

text = response.choices[0].message.content

print(text)
print("______________________________")
print(text.split("Ответы:")[1])