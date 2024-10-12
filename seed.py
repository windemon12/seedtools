# -*- coding: utf-8 -*-
# @Author   :
# @Time     : 2024/10/10 20:00
# @File     : seed.py
# @Project  : 11.py
import time

import requests
import jsonpath



def get_laohen_Data(starttime,endtime,cookie):
   """查询烙痕池数据"""
   url = "https://comm.ams.game.qq.com/ide/"

   payload=f'iChartId=323691&iSubChartId=323691&sIdeToken=Q4rDBY&e_code=0&g_code=0&eas_url=http%253A%252F%252Fseed.qq.com%252Fact%252Fa20240905record%252F&eas_refer=http%253A%252F%252Fseed.qq.com%252Fact%252Fa20220931yuyue%252F%253Freqid%253De646b16e-4b72-4fb7-822c-23f0c68b49af%2526version%253D27&sMiloTag=AMS-bjhl-1010195813-LXLqGO-666158-1067627&startTime={starttime}&endTime={endtime}&isPreengage=1&needGopenid=1'
   headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'zh-CN,zh;q=0.9',
      'origin': 'https://seed.qq.com',
      'priority': 'u=1, i',
      'referer': 'https://seed.qq.com/',
      'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
      'Cookie': cookie,
      'content-type': 'application/x-www-form-urlencoded',
      'Host': 'comm.ams.game.qq.com',
      'Connection': 'keep-alive'
   }

   response = requests.request("POST", url, headers=headers, data=payload).json()

   laohenData=response
   tids=laohenData["jData"]["data"]
   tidData=jsonpath.jsonpath(tids,'$..[?(@.poolId!="100")].tid')
   return tidData

def get_juese_Data(starttime,endtime,cookie):
   '''查询角色池数据'''
   url = "https://comm.ams.game.qq.com/ide/"

   payload = f'iChartId=323543&iSubChartId=323543&sIdeToken=mhi97c&e_code=0&g_code=0&eas_url=http%253A%252F%252Fseed.qq.com%252Fact%252Fa20240905record%252F&eas_refer=http%253A%252F%252Fseed.qq.com%252Fact%252Fa20220931yuyue%252F%253Freqid%253D62bfa423-a949-4772-8c64-930dafe616eb%2526version%253D27&sMiloTag=AMS-bjhl-1010230334-TFwGjd-666158-1067503&startTime={starttime}&endTime={endtime}&isPreengage=1&needGopenid=1'
   headers = {
      'Cookie': cookie,
      'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
      'Accept': '*/*',
      'Host': 'comm.ams.game.qq.com',
      'Connection': 'keep-alive',
      'Content-Type': 'application/x-www-form-urlencoded'
   }

   response = requests.request("POST", url, headers=headers, data=payload).json()
   userData = response
   tids = userData["jData"]["data"]
   tidData = jsonpath.jsonpath(tids, '$..tid')
   return tidData



def six_count(cookie):
   '''从1月1日到10月31日，分10次查询所有数据，统计并计算'''
   startTime="1704988800"
   seconds_in_30_days = 29 * 24 * 60 * 60
   tidAllList=[]
   tidAllLaohenList=[]
   for i in range(0,10):
      endTime = str(int(startTime) + seconds_in_30_days)
      tidData=get_juese_Data(startTime,endTime,cookie)
      tidAllList.extend(tidData)
      tid_laohen_data=get_laohen_Data(startTime,endTime,cookie)
      tidAllLaohenList.extend(tid_laohen_data)
      time.sleep(2)
      startTime=endTime
   # 计算角色数据
   six=0
   for i in tidAllList:
      if int(i) > 600:
         six+=1
   six_pro=(six/len(tidAllList))
   all_times=len(tidAllList)
   print(f"您总共获得了{six}个六星角色，总共抽取{all_times}次，六星概率为{six_pro},平均{all_times/six}抽出一个六星角色")
   # 计算烙痕数据
   six_laohen = 0
   for j in tidAllLaohenList:
      if int(j) > 2000:
         six_laohen += 1
   six_laohen_pro = (six_laohen / len(tidAllLaohenList))
   all_times = len(tidAllLaohenList)
   print(f"您总共获得了{six_laohen}张六星烙痕，总共抽取{all_times}次，六星概率为{six_laohen_pro},平均{all_times / six_laohen}抽出一个六星烙痕")

if __name__ == '__main__':
   six_count("在这里填上你的cookie，引号是必要的")