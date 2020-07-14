import re
import requests
from datetime import datetime
import json
from namedlist import namedtuple


class BAIDUPAN(object):
    def __init__(self):
        self.Result = namedtuple('Result', ['status', 'access_url', 'access_code'])

    def getPid(self, url: str) -> str:
        # 获取PID
        matches = re.match("https?:\/\/pan\.baidu\.com\/s\/1([a-zA-Z0-9_\-]{5,22})", url)
        return matches[1] if matches else None

    def Meet(self, pid):
        uuid = f"BDY-{pid}"
        headers = {
            "type": "GET",
            "data": '',
            "dataType": "json"
        }
        accessKey = "4fxNbkKKJX2pAm3b8AEu2zT5d2MbqGbD"
        clientVersion = "web-client"
        url = f"http://ypsuperkey.meek.com.cn/api/items/{uuid}?access_key={accessKey}&client_version={clientVersion}&{datetime.utcnow()}"
        return requests.get(url, headers=headers)

    def doGet(self, url):
        pid = self.getPid(url)
        req = self.Meet(pid)
        code = req.status_code
        if code == 200:
            data = json.loads(req.text)
            accessCode = data.get("access_code", None)
            if accessCode:
                results = self.Result(*['success', url, accessCode])
                return results
        results = self.Result(*['error', url, '没找到提取密码，o(╥﹏╥)o'])
        return results

    def getkey(self, url):
        results = self.doGet(url)
        return results._asdict()


if __name__ == '__main__':
    baidupan = BAIDUPAN()
    print(baidupan.getkey('https://pan.baidu.com/s/1gsaf5iNes5aXmqwNrekaEA'))
