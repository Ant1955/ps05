# 3. Необходимо спарсить цены на диваны с сайта divan.ru в csv файл,
# обработать данные, найти среднюю цену и вывести ее,
# а также сделать гистограмму цен на диваны
import scrapy
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

class DivannewparsSpider(scrapy.Spider):
   name = "divannewpars"
   allowed_domains = ["https://divan.ru"]
   start_urls = ["https://www.divan.ru/category/divany-i-kresla"]
   # start_urls = ["https://www.divan.ru/category/svet"]
   def parse(self, response):
   # Создаём переменную, в которую будет сохраняться информация
   # Пишем ту же команду, которую писали в терминале
       divans = response.css('div._Ud0k')
       # Настраиваем работу с каждым отдельным диваном в списке
       for divan in divans:
           yield {
               # Ссылки и теги получаем с помощью консоли на сайте
               # Создаём словарик названий, используем поиск по диву, а внутри дива — по тегу span
               'name': divan.css('div.lsooF span::text').get(),
               # Создаём словарик цен, используем поиск по диву, а внутри дива — по тегу span
               'price': divan.css('div.pY3d2 span::text').get(),
               # Создаём словарик ссылок, используем поиск по тегу "a", а внутри тега — по атрибуту
               # Атрибуты — это настройки тегов
               'url': divan.css('a').attrib['href']
           }

#  scrapy crawl divannewpars -o output.csv > output.log 2>&1
def run_scrapy_spider():
    command = ["scrapy", "crawl", "divannewpars", "-o", "output.csv"]
    # выполняем команду в терминале и получаем ее результат
    with open("output.log", "w") as logfile:
        # Передаем команду и поток для логирования
        process = subprocess.run(command, stdout=logfile, stderr=subprocess.STDOUT, text=True)

    # Проверяем, что команда завершилась успешно
    if process.returncode == 0:
        print("Scrapy spider ran successfully.")
    else:
        print(f"Scrapy spider failed with return code {process.returncode}")


if __name__ == "__main__":
    run_scrapy_spider()

    file_path = 'output.csv'
    data = pd.read_csv(file_path)
    df = pd.DataFrame(data)

    # Удаляем строки с пустыми значениями
    df = df.dropna()

    # Очищаем данные в столбце 'price'
    # Удаляем символы, не являющиеся частью числовых значений
    df['price'] = df['price'].str.replace(r'[^\d.]', '', regex=True)

    # Преобразуем текст в числовой формат
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # Удаляем строки, где 'price' не удалось преобразовать в число (NaN)
    df = df.dropna(subset=['price'])

    # Сбрасываем индексы после удаления строк
    df = df.reset_index(drop=True)
    # столбец с ценами называется 'price'
    print(f"Количество диванов - {len(df)}")
    print(f"Максимальная цена дивана - {df['price'].max()}")
    print(f"Минимальная цена дивана - {df['price'].min()}")
    print(f"Средняя цена дивана - {df['price'].mean()}")
    prices = df['price']

    # Построение гистограммы
    plt.hist(prices, bins=10, edgecolor='black')
    # Добавление заголовка и меток осей
    plt.title('Гистограмма цен')
    plt.xlabel('Цена')
    plt.ylabel('Частота')

    # Отображение гистограммы
    plt.show()