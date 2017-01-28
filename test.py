import requests
import json
import config
import re
from bs4 import BeautifulSoup


def test_turing():
    turing_key = config.turing_key
    turing_api = config.turing_api
    ask_info = {}
    content = "nihao"
    from_user = "123456"
    ask_info['key'] = turing_key
    ask_info['info'] = content
    ask_info['userid'] = from_user
    print(ask_info)
    r = requests.get(turing_api, params=ask_info)
    res = json.loads(r.text)
    print(res['text'])


def test_face():
    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    api_key = config.api_key
    api_secret = config.api_secret
    param = dict()
    param['api_key'] = api_key
    param['api_secret'] = api_secret
    param['image_url'] = "http://mmbiz.qpic.cn/mmbiz_jpg/WuEqBMro7GBDEBNg5gtzib7yupEiaicBxIGQSlFlrPZxRerUVRJyzdAzAZm1xCfhS9UbujBbibVOZAXUrJ7UydibCgQ/0.jpg"

    param['return_landmark'] = 1
    param['return_attributes'] = 'gender,age,smiling,glass,headpose,facequality,blur'
    res = requests.post(url=url, data=param)
    info = json.loads(res.content.decode('utf-8'))
    print(info['faces'][0]['attributes']['gender'])


def test_pic():
    url = "http://mmbiz.qpic.cn/mmbiz_jpg/WuEqBMro7GBDEBNg5gtzib7yupEiaicBxIGQSlFlrPZxRerUVRJyzdAzAZm1xCfhS9UbujBbibVOZAXUrJ7UydibCgQ/0"
    r = requests.get(url)
    file = open("./src_file/1.jpg", "wb")
    file.write(r.content)
    file.close()


def test_mov():
    content = "movie 驴得水"
    mov_url = "http://www.btkiki.com/s/"
    if re.findall("movie( +)(.+)", content):
        pattern = re.compile("movie( +)(.+)")
        group = pattern.match(content)
        # print(group.group(2))
        res = requests.get(mov_url+group.group(2)+'.html')
        html = res.content.decode('utf-8')
        res.close()
        soup = BeautifulSoup(html, 'lxml')
        try:
            movies = soup.findAll('div', {'class': 'g'})
            for i in range(min(len(movies), 3)):
                movie = movies[i]
                href = movie.findAll('a', {'target': '_blank'})
                if href:
                    href = href[0].attrs.get('href')
                    mov_res = requests.get(href)
                    mov_html = mov_res.content
                    mov_res.close()
                    mov_soup = BeautifulSoup(mov_html, 'lxml')
                    mov_info = mov_soup.findAll('div', {'id': 'result'})
                    if mov_info:
                        print(mov_info[0].findAll('h1')[0].get_text())
                        for mov_thing in mov_info[0].findAll('p'):
                            print(mov_thing.get_text())
                print("------------------")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # test_face()
    # test_pic()
    test_mov()
