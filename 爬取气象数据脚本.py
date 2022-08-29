import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime
import re
import csv

city_dict = {
    'chongqing': '重庆',
    'beijing': '北京'
}
regex = re.compile(r'\s+')

def get_content(target):
    req = requests.get(url = target)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    texts1 = bf.find('table',{"class":"b"})
    elements=texts1.find_all("tr")

    for element in elements[1:]:
        date_str = regex.sub('', element.find_all('a')[0].text.strip())
        # date_str = regex.sub('', element.find_all('td')[0].find_all('a')[0].text.strip())
        weather=regex.sub('', element.find_all('td')[1].text.strip())
        temperature = regex.sub('', element.find_all('td')[2].text.strip())
        wind = regex.sub('', element.find_all('td')[3].text.strip())
        weather_day, weather_night = re.split(r'\/', weather)
        temperature_day, temperature_night = re.split(r'\/', temperature)
        temperature_day = re.sub(r'[^0-9\-]+', '', temperature_day)
        temperature_night = re.sub(r'[^0-9\-]+', '', temperature_night)
        wind_day, wind_night = re.split(r'\/', wind)
        wind_day = re.sub(r'[^0-9]+', '', re.split(r'\-', wind_day)[-1])
        wind_night = re.sub(r'[^0-9]+', '', re.split(r'\-', wind_night)[-1])
        params = [
            city_dict[city],
            datetime.strptime(date_str, '%Y年%m月%d日'),
            weather_day,
            temperature_day,
            wind_day,
            weather_night,
            temperature_night,
            wind_night
        ]
        csv_writer.writerow(params)

    return "运行完成"

if __name__ == '__main__':
    for city in tqdm(list(city_dict.keys())):
        f = open(f'{city_dict[city]}日气温数据202208.csv', 'w', newline='', encoding='utf-8')  # 1. 创建文件对象
        csv_writer = csv.writer(f)  # 2. 基于文件对象构建 csv写入对象
        csv_writer.writerow(["城市", "日期", "白天天气", "白天气温", "白天风力", "夜晚天气", "夜晚气温", "夜晚风力"])  # 3. 构建列表头
        for year in [2022]:
            for month in range(1,3):
                if year == datetime.now().year and month >= (datetime.now().month+2):
                    continue
                month = str(month).zfill(2)
                target = f'http://www.tianqihoubao.com/lishi/{city}/month/{year}{month}.html'
                content = get_content(target)