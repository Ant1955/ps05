import scrapy
import subprocess
import logging
from scrapy.utils.log import configure_logging

class DivannewparsSpider(scrapy.Spider):
   name = "divannewpars"
   allowed_domains = ["https://divan.ru"]
 #  start_urls = ["https://www.divan.ru/category/divany-i-kresla"]
   start_urls = ["https://www.divan.ru/category/svet"]
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

    with open("output.log", "w") as logfile:
        # Redirect stdout and stderr to the log file
        process = subprocess.run(command, stdout=logfile, stderr=subprocess.STDOUT, text=True)

    # Check if the process completed successfully
    if process.returncode == 0:
        print("Scrapy spider ran successfully.")
    else:
        print(f"Scrapy spider failed with return code {process.returncode}")


if __name__ == "__main__":
    run_scrapy_spider()

