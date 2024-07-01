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
configure_logging(install_root_handler=False)
logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.WARNING  # Устанавливаем уровень логирования на WARNING, чтобы подавить Info и Debug
)

# Выполнение команды scrapy crawl divannewpars
# process = subprocess.run(['scrapy', 'crawl', 'divannewpars','--set', 'LOG_STDOUT=True', '--set', 'LOG_FILE='],
# stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# Read the output line by line
# for line in process.stdout:
#    print(line.strip())

# To capture the complete output
# output, errors = process.communicate()

# print("Output:", output)
# print("Errors:", errors)
