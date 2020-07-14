import json
import urllib.request
import execjs
from namedlist import namedtuple
import requests


class TTK():

    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


class TRANSLATE2(object):
    def __init__(self):
        self.Result = namedtuple('Result', ['type', 'text', 'result'])

    def run(self, connect):
        '''
        # 获取翻译结果
        :param name:
        :return:
        '''
        result = self.translate(connect)
        if result:
            results = self.Result(*['Google', connect, result])
            return results._asdict()

    def open_url(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req, timeout=3)
        data = response.read().decode('utf-8')
        return data

    def translate(self, content):
        if len(content) > 4891:
            print("翻译文本超过限制！")
            return
        tk = TTK().getTk(content)
        content = urllib.parse.quote(content)
        url = "http://translate.google.cn/translate_a/single?client=t" \
              "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
              "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
              "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)
        result = self.open_url(url)
        end = result.find("\",")
        if end > 4:
            return result[4:end]


class TRANSLATE(object):
    def __init__(self):
        self.Result = namedtuple('Result', ['type', 'text', 'result'])

    def run(self, connect):
        header = {
            'authority': 'translate.google.cn',
            'method': 'GET',
            'path': '',
            'scheme': 'https',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'x-client-data': 'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='
        }
        res = requests.get(
            'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=zh-CN&dt=t&q=' + connect, header)
        a = json.loads(res.text)
        if a:
            results = self.Result(*['Google', connect, a[0][0][0]])
            return results._asdict()


if __name__ == '__main__':
    truncate = TRANSLATE()
    print(truncate.run('hello world'))
