import requests, json


def getBingImg():
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }
    url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
    html_text = requests.get(url, headers=header).text
    json_data = json.loads(html_text)
    bing_data = {
        "startdate": json_data['images'][0]['startdate'],
        "title": json_data['images'][0]['title'],
        "url": json_data['images'][0]['urlbase'],
        "copyright": json_data['images'][0]['copyright']
    }
    return bing_data


if __name__ == '__main__':
    bing_data = getBingImg()
    print(bing_data)
