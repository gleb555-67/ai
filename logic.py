import requests
from config import API_KEY
from urllib.parse import quote


def generate_image(prompt, filename="cat", width=1024, height=1024, seed=42):
    """
    Генерирует изображение по текстовому промпту через Pollinations AI.

    :param prompt:   текст запроса (что нарисовать)
    :param filename: имя файла без расширения (по умолчанию "cat")
    :param width:    ширина изображения
    :param height:   высота изображения
    :param seed:     зерно (42 — повторяемый результат, -1 — случайный)
    :return:         имя сохранённого файла или None при ошибке
    """

    # Заголовки запроса (ключ передаётся как Bearer-токен)
    headers = {
        "authorization": "Bearer %s" % API_KEY
    }

    # URL для генерации: промпт передаётся прямо в адресе
    url = "https://gen.pollinations.ai/image/%s" % quote(prompt)

    # Параметры генерации
    params = {
        "model":  "google/gemini-nano-banana-2.1",  # модель по умолчанию
        "width":  width,   # ширина изображения
        "height": height,  # высота изображения
        "seed":   seed,    # для повторяемого результата (-1 = случайный)
    }

    # Отправляем GET-запрос: сервер сразу возвращает готовую картинку
    response = requests.get(url, params=params, headers=headers, timeout=120)
    print(response.status_code)

    if response.status_code == 200:
        # Расширение файла берём по типу ответа (jpeg / png / svg)
        content_type = response.headers.get("content-type", "")
        ext = {"image/png": "png", "image/svg+xml": "svg"}.get(content_type, "jpg")

        filepath = "%s.%s" % (filename, ext)
        with open(filepath, "wb") as f:
            f.write(response.content)

        print("Картинка сохранена в", filepath)
        return filepath

    else:
        # Текст ошибки: 401 — нет ключа, 402 — кончился баланс, 429 — слишком часто
        print(response.text)
        return None