import re
import requests
import os

# name = input('输入文件夹名称:')
robot = ".\\datasets\\train\\ink_painting\\trainB\\"
search_word = "风景"

kv = {'user-agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)'}


# (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36

# 获取url对应的源码页面
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


# 解析url源码页面
def parserHTML(html):
    # 正则表达式为获取ObjURL
    pattern = r'"ObjURL":"(.*?)"'
    reg = re.compile(pattern)
    urls = re.findall(reg, html)
    return urls


# 下载图片
def download(List):
    for url in List:
        try:
            path = robot + url.split('/')[-1]
            url = url.replace('\\', '')
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            if not os.path.exists(robot):
                os.makedirs(robot)
            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print(path + ' 文件保存成功')
            else:
                print('文件已经存在')
        except:
            continue


# 通过Requests URL请求到更多的url源码页面
def getmoreurl(num, word):
    ur = []
    url = r'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={word}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn={pn}&rn=30'
    for x in range(1, num + 1):
        # word为搜索关键词，num为想获取的页面数量
        u = url.format(word=word, pn=30 * x)
        ur.append(u)
    return ur


def main():
    n = int(input('输入想下载多少张图片(n*30)：'))
    word = search_word
    # 初始页面url
    url = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1499773676062_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word={word}'.format(
        word=word)
    html = getHTMLText(url)
    urls = parserHTML(html)
    download(urls)
    # 下面操作获取的更多页面图片
    url1 = getmoreurl(n, word)
    for i in range(n):
        html1 = getHTMLText(url1[i])
        urls1 = parserHTML(html1)
        download(urls1)


main()
