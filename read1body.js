import requests
import json
import time
import random
import os
from datetime import datetime, timezone, timedelta

# def file_name(file_dir):
#     File_Name=[]
#     for files in os.listdir(file_dir):
#         if os.path.splitext(files)[1] == '.json':
#             File_Name.append(files)
#     return File_Name
path = 'youth_data/youth_xxm.json'
    
headers = {
    'request_time': '1615353817',
    'os-api': '26',
    'openudid': 'a4a7468e35d49626',
    'phone-sim': '1',
    'carrier': 'CHN-CT',
    'device-model': ' V1981A',
    'device-platform': 'android',
    'access': 'WIFI',
    'os-version': ' QP1A.190711.020+release-keys',
    'app-version': '2.8.8',
    'Host': 'kandian.youth.cn',
    'User-Agent': 'okhttp/3.12.2',
}


def get_standard_time():
    """
  获取utc时间和北京时间
  :return:
  """
    # <class 'datetime.datetime'>
    utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
    beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
    return beijing_datetime

def youth_read(path):
    with open(path,'r') as f:
        body_list = json.load(f)
        random.shuffle(body_list)
        for i, body in enumerate(body_list):
            response = requests.post('https://kandian.youth.cn/v5/article/complete.json', headers=headers, data=body)
            r = response.json()
            print(f'开始第{i+1}次阅读,本次阅读共{len(body_list)}次')
            print(r)
            t = random.randint(28,33)
            print(f'等待{t}秒后进行下一次阅读')
            time.sleep(t)
        print(f'阅读完成,本次阅读共阅读{len(body_list)}条目')

# filepaths = file_name('youth_data/')

# def run():
#     for i, path in enumerate(filepaths):
#     	new_path = 'youth_data/' + path
#     	print(f'账号{i+1}开始阅读')
#     	youth_read(new_path)
def run():
	youth_read(path)


if __name__ == '__main__':
    run()

