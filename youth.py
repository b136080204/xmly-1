#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可 YOUTH_WITHDRAWBODY
# 分享一篇文章，找到 put.json 的请求，拷贝请求体，放入对应参数 YOUTH_SHAREBODY
# 清除App后台，重新启动App，找到 start.json 的请求，拷贝请求体，放入对应参数 YOUTH_STARTBODY

cookies1 = {
    'YOUTH_HEADER': {
        'Host': 'kd.youth.cn',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 10; V1981A Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.181 Mobile Safari/537.36',
        'Referer':
        'https://kd.youth.cn/h5/20190527watchMoney/?access=WIFI&app-version=2.8.8&app_version=2.8.8&carrier=%E4%B8%AD%E5%9B%BD%E7%94%B5%E4%BF%A1&channel=c1007&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691rWaxzZuwhYyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3ibOEsqCYrrnEapqGcXY&cookie_id=259ba4816ad785a6166f78013fafae60&device_brand=vivo&device_id=50981406&device_model=V1981A&device_platform=android&device_type=android&inner_version=202102031654&mi=0&oaid=866d45665fb29c6818c9edf7107d2900b37ad95d8ee60c6078534a3a822e99f3&openudid=a4a7468e35d49626&os_api=29&os_version=QP1A.190711.020%20release-keys&request_time=1615339832&resolution=1080x2182&sim=1&sm_device_id=202103082057057dffa61ae6d218e4e617693968d9998e0135df905eee2c05&subv=1.2.2&szlm_ddid=DuYLmKCAGG%2BCJWSifFLyp2SQ7740E9Hkvx7b6yjb%2FEo4dEQ9S0R9PJ9oDcm0ItIWsJHFRrK30ky0P%2Bq%2Fth1rmiTg&uid=54286805&version_code=56&version_name=%E4%B8%AD%E9%9D%92%E7%9C%8B%E7%82%B9&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691rWaxzZuwhYyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3ibOEsqCYrrnEapqGcXY&zqkey_id=259ba4816ad785a6166f78013fafae60',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'cn.youth.news',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775': '1615208268',
        'sensorsdata2019jssdkcross':
        '%7B%22distinct_id%22%3A%2254286805%22%2C%22%24device_id%22%3A%2217811ea40e117-0f2f5df42c5493-145e2523-289080-17811ea40e2310%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217811ea40e117-0f2f5df42c5493-145e2523-289080-17811ea40e2310%22%7D',
        'Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775': '1615338262',
        'Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775': '1615208268',
    },
    'YOUTH_READBODY':
    'p=6XU6PBNNsHKc%3DVtos3hc8_wUBTxmMpX7gRTsRbt2tOBeb_H6PU_yToWetvDeYDFNzMlBBTfFB-4-JpdazE0FzToYC-45K9i6wCkXnmhBYwWQfJj9Ufvb9fok3_j-l4yo2cbyj81o4U0Ri8fskw8nmOoBJy9hGEGoWt_bls1HDw6eP1i2NclOn2gG7aRA6msyUjQywsaahqsSZEl-PtNSNo0ZF0tBNmKeO_SxhigHhXDPwpDwjMr9LsoLJ3VvgkxYc7NSUeNaueMnhIv6nVvT1sBlDYWnfbd3eATt4avXwKuSZNxqw8mw_ANO3_dYeT45XqrxeSOmWGojr2Dgu5U99tt0-lkubn_3GpXwSmMziPKLwW2B2Lh61vPKFxuSNSbyLDWyrLwm8-JN1ntmloNves3cpKhHoYOsPVTyjiLdC07qWls7i1tbzfQDriXQw75bvB6S3IdsH-yh2KNESeLr6opGkFBaUEislNOAxW79vVerfApabUecVCJraulYGksRK6XGP9h1lDEOB718ze_AV205q4Mwnf_YpxTvJCDwrgzIbuQNk-zoY21KJj7pwgRbZV2OV7ylkoCzqZdiD6nAeME5zbCfNEe6_rJmFU1m7xPTfn_0flHFGIlDBiEqlQrmrz-VhQ6x1VlB-bkqCkLSbM8QN2eHlwAo7MA6qPrSKYu2YUV0seZ51y3I9IyCjMi2NZj0q5g1VrDfrMs1TUCXg8cOsT6eK7vjUyNrpw4vI6eAVXwWVTdIMB3kU7SQ8D0IocmQWUiM_Z-dKHqjsqLt8-DtRU8McHObBauwT_yy68ZmGn_ujV-klaX4aJGN87teM9GKev436zZBikc9S3naWVpAg87Z8wpBUqbqcRehCKAO7K4vGmRJh0uHYIdvxFrQji67qe4Bu0u5akhqcEdmg3eubXX-zUs3EkA1m4uZVJn1loORoak0DRTlCbsfW0Kcbf0qDctS-xcQIr9na5HotFwraspO6r-FUyXaJsRG4EgfoMMSdwf-hkipILkfkUl1ZssF44-av9rRtp8RlUBVQXQMU8dDPrT3q2WTks0eq3dLVjrk9zArEowsP49PwfWdQjn60Mj0uXkJpnJapZVZ3dVFn3K_673xNyNAdoF_Tn9Pf5imaP5ysam4mLHuPMCuRnD3JKat0eUbhJXHYZy_dQvmrW2KJ8elWU9vkHmmsgS6nh3gqQIwXD-g9U3InQCEXU0WddXLdQXkEz5XUabI5hoX47x1ANkJu5Jh0oRszJb87W3nDXs9VMCAf8dLkMRS5i2Jml10JuhooK36_uGmxZSbhg0O017xTDFzHGQWxFigt9nNz-3ihgPTeQxrwRGjCAXS1Q3CF4_Ol556_Y3qbv1nEHyBkwkkOdVobxdavvqPuIhd9utCft_nNgYSMsjFSkK-LMgJXj74WDe97_jRf6bPy856ZBHpg3cqeNLcxH-fPF0pZ409oeLcYJhHSwUvrxm_A0J0qbYXk5II67ulwDCU1RmToDQ-fLw%3D%3DM',
    'YOUTH_REDBODY':
    '',
    'YOUTH_READTIMEBODY':
    'p=DYdVi_XPUOzA%3D7ioCfKCMWbKiTOV7MrS4KrU4G1etY2rmZ67wlFp7pqL0WZSTXl0YNULJpX6CMGJKuijjm1mOkAHIIeZEWH7HY07iOlHXqOuAiPO2i19HRI4uEHdCjJYC2USwNPSM8P4uSOJmrfGukQ1btaw836KysW-kaQ7CyKh1_iA5Ol3R6Wo4JFajLU5uC3ysXc6QNCKRUgUzl12FMcnlp8b3PeabgQ-0xjO-O5RgNhj4JXhjxEMI7GKBwxN7rO_QlIVk5UPe-53WkunbsKUn1532gE_wSlgIpn4-zGeuOOM3xsw85GZICRkpAJzNaP-oNMU-hVTDwqko0kqVjUnFEzE1_XdGps5GPxevd3GVOmVZ4mRqT9kHAXo5V6CIca1FCdlEN3252ZnoEa90sGwB3YzJAKX65kUik-flEfmeC7-NYnxX7Y34tZaa_dz0rmb2NkPbhOTvvl2u-YFHCG3dXqUzpRgZhCkVOBERVOA32u_aPnvG3gEJrJ6f7CD3K7RFJzNbVDGU7Fr-tE6nf3Hj30nt_DjKI1yzk7_E8H6U14o1anTSkqn3jQkKTIBiUxWTNX73yLmjxitLfQUjL1Ky1QdokbjXOjwKFU-taPQ5O9oBCLn_dAR2DzZnUImXDTL-bRA6NDEIwnmo4QtoVuBTzJ8R9GoFedXVxvZR3iA_leUpq9fYA8Q-boM6Zdv4jdTOc8Eh3wfhCleLiu6eyvxBplVrVJVmS2j5XZjQg7TW8VUf35SmF0Ny5KLu_kjj9Ev1PDHc6M-IAqTV9bErvhAIuYdG4Z_0204nUBWJcpz8kcv09kPcNQZ-HLoUPtijbMCU-YGtkhi8ERhJyAefmZIGaTXRIehIKyL--B04fplgiXiw5Mb7ViRdMQ-bL8tJjPkf5_n4xNUkCIDZ37nxyR3j7kI9e9DJJttjZUIBgxfxZ7tF2lKHNOwnt0oOsA0IV4eAdO_vbeAwjFKRdH9Q0faFnQNotVOLPTMo4Rn7z8M4yaje6HArH53XmGhXKyyJGI-Hwy5ERTonU69ODFt0NnzKTJFQB0hGzspXMwKR9j-ikblcMtINjOHbYmiqhutmWXmRazeclSeIy9b8XZ_XMZEIHapyCI2ncWmH5eKO5bpU5BLUijGGu_hgIM73HEKYMAQgwqLZ7TsMhr5Gzy82yjnw2Jt4Qr84QJMttpUQ9nq6dblX1vB103zwhzWTCvz4Yk-pdzwhNiv6GBBpo6G7uf90gmBMlEYiiQ8-GSSNLR5jrsiVqJkQkgbtE0gF5YpMTuZUMUz36IP_OsNxqxdh6FQsHLc4hdU_JPi4q5Fd_Hw1oe665VVkWXixGfbdq0Rr-mZg_LN5ubrLyqpVSC1aOQSTUyRK4U64GL7OpzZXiedaZuT2qVakVKrADF8HqojlzhTwiUroxDttN8n_qmByxBCeYCz-_FIOXXUg4yHBuvMIO6NpszJMOuqL1sv3U8t8MNkDd8Ujn3n3WRQABhghvOc%3DUT',
    'YOUTH_WITHDRAWBODY':
    "",
    'YOUTH_SHAREBODY':
    'access=WIFI&androidid=a4a7468e35d49626&app-version=2.8.8&app_name=zqkd_app&app_version=2.8.8&article_id=36743008&carrier=CHN-CT&channel=c1007&device_brand=vivo&device_id=50981406&device_model=V1981A&device_platform=android&device_type=android&dpi=480&fp=DuYLmKCAGG%2BCJWSifFLyp2SQ7740E9Hkvx7b6yjb%2FEo4dEQ9S0R9PJ9oDcm0ItIWsJHFRrK30ky0P%2Bq%2Fth1rmiTg&from=4&inner_version=202102031654&language=zh-CN&memory=11&mi=0&mobile_type=1&net_type=1&network_type=WIFI&oaid=866d45665fb29c6818c9edf7107d2900b37ad95d8ee60c6078534a3a822e99f3&openudid=a4a7468e35d49626&os_api=29&os_version=QP1A.190711.020%20release-keys&request_time=1615353843&resolution=1080x2182&rom_version=QP1A.190711.020%20release-keys&sim=1&sm_device_id=202103082057057dffa61ae6d218e4e617693968d9998e0135df905eee2c05&storage=108.89&stype=wx&subv=1.2.2&szlm_ddid=DuYLmKCAGG%2BCJWSifFLyp2SQ7740E9Hkvx7b6yjb%2FEo4dEQ9S0R9PJ9oDcm0ItIWsJHFRrK30ky0P%2Bq%2Fth1rmiTg&token=2a3785701822701772d1a8ea761a4a97&uid=54286805&version_code=56&zqkey=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualIejl691rWaxzZuwhYyp4LDPyGl9onqkj3ZqYJa8Y898najWsJupZLC3ibOFjIKYrs-uapqGcXY&zqkey_id=11f652d33ece80bb1a525c27e3f34da1'
}
cookies2 = {}

COOKIELIST = [cookies1,]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = f'YOUTH_HEADER{str(i+1)}'
    readBodyVar = f'YOUTH_READBODY{str(i+1)}'
    readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
    withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
    shareBodyVar = f'YOUTH_SHAREBODY{str(i+1)}'
    startBodyVar = f'YOUTH_STARTBODY{str(i+1)}'
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_SHAREBODY"] = os.environ[shareBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_STARTBODY"] = os.environ[startBodyVar]
      COOKIELIST.append(globals()['cookies'+str(i + 1)])
  print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"

def get_standard_time():
  """
  获取utc时间和北京时间
  :return:
  """
  # <class 'datetime.datetime'>
  utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
  beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
  return beijing_datetime

def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
  """
  签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/sign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def signInfo(headers):
  """
  签到详情
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/getSign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到详情')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def punchCard(headers):
  """
  打卡报名
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/signUp'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('打卡报名')
    print(response)
    if response['code'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doCard(headers):
  """
  早起打卡
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/doCard'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('早起打卡')
    print(response)
    if response['code'] == 1:
      shareCard(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareCard(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
  endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
  try:
    response = requests_session().post(url=startUrl, headers=headers, timeout=30).json()
    print('打卡分享')
    print(response)
    if response['code'] == 1:
      time.sleep(0.3)
      responseEnd = requests_session().post(url=endUrl, headers=headers, timeout=30).json()
      if responseEnd['code'] == 1:
        return responseEnd
    else:
      return
  except:
    print(traceback.format_exc())
    return

def luckDraw(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/luckdraw'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('七日签到')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def timePacket(headers):
  """
  计时红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}TimePacket/getReward'
  try:
    response = requests_session().post(url=url, data=f'{headers["Referer"].split("?")[1]}', headers=headers, timeout=30).json()
    print('计时红包')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def watchWelfareVideo(headers):
  """
  观看福利视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/recordNum?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('观看福利视频')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers, body):
  """
  分享文章
  :param headers:
  :return:
  """
  url = 'https://ios.baertt.com/v2/article/share/put.json'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('分享文章')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def threeShare(headers, action):
  """
  三餐分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareNew/execExtractTask'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  body = f'{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('三餐分享')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def openBox(headers):
  """
  开启宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/openHourRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('开启宝箱')
    print(response)
    if response['code'] == 1:
      share_box_res = shareBox(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareBox(headers):
  """
  宝箱分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/shareEnd'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('宝箱分享')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendList(headers):
  """
  好友列表
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友列表')
    print(response)
    if response['error_code'] == '0':
      if len(response['data']['active_list']) > 0:
        for friend in response['data']['active_list']:
          if friend['button'] == 1:
            time.sleep(1)
            friendSign(headers=headers, uid=friend['uid'])
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendSign(headers, uid):
  """
  好友签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友签到')
    print(response)
    if response['error_code'] == '0':
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def sendTwentyScore(headers, action):
  """
  每日任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print(f'每日任务 {action}')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchAdVideo(headers):
  """
  看广告视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data="type=taskCenter", headers=headers, timeout=30).json()
    print('看广告视频')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchGameVideo(body):
  """
  激励视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
  headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('激励视频')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def visitReward(body):
  """
  回访奖励
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/mission/msgRed.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('回访奖励')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def articleRed(body):
  """
  惊喜红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/article/red_packet.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('惊喜红包')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def readTime(body):
  """
  阅读时长
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/user/stay.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('阅读时长')
    print(response)
    if response['error_code'] == '0':
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def rotary(headers, body):
  """
  转盘任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘任务')
    print(response)
    return response
  except:
    print(traceback.format_exc())
    return

def rotaryChestReward(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘宝箱')
    print(response)
    if response['status'] == 1:
      i = 0
      while (i <= 3):
        chest = response['data']['chestOpen'][i]
        if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
          time.sleep(1)
          runRotary(headers=headers, body=f'{body}&num={i+1}')
        i += 1
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def runRotary(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('领取宝箱')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doubleRotary(headers, body):
  """
  转盘双倍
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘双倍')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def incomeStat(headers):
  """
  收益统计
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=50).json()
    print('收益统计')
    print(response)
    if response['status'] == 0:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def withdraw(body):
  """
  自动提现
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('自动提现')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def bereadRed(headers):
  """
  时段红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}Task/receiveBereadRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('时段红包')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def startApp(headers, body):
  """
  启动App
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v6/count/start.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('启动App')
    print(response)
    if response['success'] == True:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = f'📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account.get('YOUTH_HEADER')
    readBody = account.get('YOUTH_READBODY')
    readTimeBody = account.get('YOUTH_READTIMEBODY')
    withdrawBody = account.get('YOUTH_WITHDRAWBODY')
    shareBody = account.get('YOUTH_SHAREBODY')
    startBody = account.get('YOUTH_STARTBODY')
    rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'

    if startBody:
      startApp(headers=headers, body=startBody)
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += f'\n【账号】：{sign_info["user"]["nickname"]}'
      content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
      result += f'【账号】: {sign_info["user"]["nickname"]}'
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
    if shareBody:
      shareArticle(headers=headers, body=shareBody)
      for action in ['beread_extra_reward_one', 'beread_extra_reward_two', 'beread_extra_reward_three']:
        time.sleep(5)
        threeShare(headers=headers, action=action)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

    rotaryChestReward(headers=headers, body=rotaryBody)
    for i in range(5):
      watchWelfareVideo(headers=headers)
    timePacket(headers=headers)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward', 'first_share_article']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += f'\n【{group["name"]}】：+{group["money"]}青豆'
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 300000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += f'\n【自动提现】：发起提现30元成功'
          content += f'\n【自动提现】：发起提现30元成功'
          send(title=title, content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

      result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
      content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

  print(content)

  # 每天 23:00 发送消息推送
  if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 5:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 23:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
