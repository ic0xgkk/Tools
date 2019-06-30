import requests
import time


def post(session):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Length": "9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "xg.zhbit.com",
        "Referer": "http://xg.zhbit.com/yxssfj!goYxss.action?action=1&gy05id=${gy05id%20}&pk=这里需要手动填入&param=&rnd=27",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
    }

    index_cookie = {
        "JSESSIONID": ""
    }
    login_data = {
        "pk": ""
    }

    while True:
        try:
            response = session.post(cookies=index_cookie, headers=headers,
                                    url="http://xg.zhbit.com/yxssfj!doYxss.action", timeout=5,
                                    data=login_data, allow_redirects=False)
            print(str(time.time()) + ", " + str(response.content, encoding='utf-8'))
            time.sleep(1)
        except requests.exceptions.Timeout as e:
            print("有问题" + str(e))


if __name__ == '__main__':
    session = requests.Session()
    post(session)