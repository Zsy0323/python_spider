import json

import requests
from bs4 import BeautifulSoup

# 定义类
class Job:
    def __init__(self,url,addr,page,job_name):
        self.url = url
        self.addr = addr
        self.page = page
        self.job_name = job_name

    # 获取url
    def getUrl(self):
        url = self.url + self.addr + '&kw=' + self.job_name + '&p=' + str(self.page)
        return url

    # 下载页面html
    def getHtml(self,url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        }
        res = requests.get(url,headers=headers)

        return res.text

    # 提取数据
    def getJson(self,html):
        soup = BeautifulSoup(html,'lxml')
        # print(soup)
        # 职位信息table_list
        table_list = soup.select('.newlist')
        # print(table_list)
        # 定义存放数据的列表
        data_list = []
        for table in table_list[1:]:
            dic = {}
            dic['zwmc'] = table.select('.zwmc > div > a')[0].get_text()
            dic['gsmc'] = table.select('.gsmc > a')[0].string
            dic['zwyx'] = table.select('.zwyx')[0].string
            dic['gzdd'] = table.select('.gzdd')[0].string
            data_list.append(dic)
        # print(data_list)

        jsonStr = json.dumps(data_list,ensure_ascii=False)
        # print(jsonStr)
        # 保存到文件
        with open('./智联职位/job.json','w',encoding='utf-8') as f:
            f.write(jsonStr)

# 定义入口函数
def main():
    # 基础url
    base_url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl='
    # 爬取页码
    start = int(input('请输入要爬取的起始页'))
    end = int(input('请输入要爬取的结束页'))
    # start= 1
    # end = 1
    # 爬取职位
    job_name = input('请输入要爬取的职位')
    # job_name = 'python'

    # 所在地址
    addr = input('请输入工作地址')
    # addr = '深圳'
    for page in range(start,end+1):
        # 创建对象
        job= Job(base_url,addr,page,job_name)

        # 获取url
        url = job.getUrl()

        # 下载html
        html = job.getHtml(url)
        # print(html)

        # 提取数据
        jsonData = job.getJson(html)


    print('完成爬取')


if __name__ == '__main__':
    main()










































