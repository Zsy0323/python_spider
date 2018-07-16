import urllib.request
import urllib.parse
from lxml import html


# 定义生成url函数
def get_url(base,page):

    url = base + str(page) +'/'
    return url


# 发送请求获取数据
def getResponse(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Referer': 'https://www.kuaidaili.com/free/inha/2/',

    }
    proxies = {'http':'66.119.180.103:80'}
    handler = urllib.request.ProxyHandler(proxies=proxies)
    opener = urllib.request.build_opener(handler)
    myRequest = urllib.request.Request(url,headers=headers)
    res = opener.open(myRequest)
    return res.read().decode('utf-8')


# 提取有效数据
def xpathData(res):
    xpathObj = html.etree.HTML(res)
    ips = xpathObj.xpath("//tbody/tr/td[@data-title='IP']")
    ports = xpathObj.xpath("//tbody/tr/td[@data-title='PORT']")
    ipTypes = xpathObj.xpath("//tbody/tr/td[@data-title='类型']")
    ipList = []

    for i in range(len(ips)):
        dic = {}
        dic[ipTypes[i].text] = ips[i].text + ':' + ports[i].text
        ipList.append(dic)

    return ipList


# 保存数据
def save(filename,data):
    data = str(data)
    with open(filename,'w',encoding='utf-8') as fp:
        fp.write(data)



# 定义主函数
def main():
    base_url = 'https://www.kuaidaili.com/free/inha/'
    start_page = int(input('请输入想爬取的开始页面'))
    end_page = int(input('请输入想爬取的结束页面'))
    for page in range(start_page,end_page+1):
        url = get_url(base_url,page)
        # 下载
        res = getResponse(url)
        # print(res)
        # 提取数据
        data = xpathData(res)

        # 保存数据
        filename = './快代免费代理IP/'+str(page)+'.txt'
        save(filename,data)


if __name__ == '__main__':
    main()





