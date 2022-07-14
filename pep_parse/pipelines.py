# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from collections import defaultdict
import csv
import datetime as dt

# возвращает путь до директории с текущим файлом
# -   `Path(__file__)— абсолютный путь до текущего файла;
# -   `parent`— директория, в которой он лежит.
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    pep_status_count = defaultdict(int)
    total_pep_count = 0

    def open_spider(self, spider):
        """Формирование пути до директории results."""
        result_dir = BASE_DIR / 'results'
        # Создайте директорию.
        result_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        """Посчет количества статусов."""
        if item['status']:
            self.total_pep_count += 1
            self.pep_status_count[
                item['status']] = self.pep_status_count.get(
                item['status'], 0) + 1

        return item

    def close_spider(self, spider):
        """Запись результов в csv-файл."""
        results = [('Cтатус', 'Количество')]
        # results.extend([status for status in self.pep_status_count.items()])
        results.extend(self.pep_status_count.items())
        results.append(('Total: ', self.total_pep_count))

        file_format = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{file_format}.csv'
        file_path = BASE_DIR / 'results' / file_name
        # with open(file_name, mode='w', encoding='utf-8') as f:
        #     # Записываем строки в csv-файл. Колонки разделяются запятой, без пробелов.
        #     f.write('Статус,Количество\n')
        #     # Здесь цикл с записью данных в файл.
        #     result = [result for result in results]
        #     f.write(f'Total,{result}\n')
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(results)