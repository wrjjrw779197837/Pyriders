import requests
from PIL import Image


class XK:
    cookies = None
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

    def __init__(self):
        r = requests.post('http://xk.suda.edu.cn/default_szdx.aspx')
        self.cookies = r.cookies

    def get_image(self, url='http://xk.suda.edu.cn/CheckCode.aspx'):
        r = requests.get(url=url, cookies=self.cookies)
        with open("YZM.jpg", 'wb') as f:
            f.write(r.content)
        img = Image.open("YZM.jpg")
        return img

    @staticmethod
    def img_to_digit(img):
        img.show()
        return input()

    def login_xk_web(self, digit, xh, passwd, url='http://xk.suda.edu.cn/default_szdx.aspx'):
        data = {
            '__VIEWSTATE': 'dDwtMTE5ODQzMDQ1NDt0PDtsPGk8MT47PjtsPHQ8O2w8aTw0PjtpPDc+O2k8OT47PjtsPHQ8cDw7cDxsPHZhbHVlO'
                           'z47bDxcZTs+Pj47Oz47dDxwPDtwPGw8b25jbGljazs+O2w8d2luZG93LmNsb3NlKClcOzs+Pj47Oz47dDx0PDs7bDxp'
                           'PDI+Oz4+Ozs+Oz4+Oz4+Oz5527rVtbyXbkyZdrm5O4U8rQ4EHA==',
            'TextBox1': str(xh),
            'TextBox2': str(passwd),
            'TextBox3': str(digit),
            'Button1': ''
        }
        r = requests.post(url, data=data, cookies=self.cookies)
        return r

    def get_class_plan(self, url='http://xk.suda.edu.cn/xskbcx.aspx?xh=1627406066&xm=%cd%f5%c8%ca%bd%dc&gnmkdm=N121603'):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'xk.suda.edu.cn',
            'Referer': 'http://xk.suda.edu.cn/xs_main.aspx?xh=1627406066',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/71.0.3578.98 Safari/537.36'
        }
        r = requests.get(url, headers=headers, cookies=self.cookies)
        print(r.text)

    @staticmethod
    def test(funcs):
        if type(funcs) != type([]):
            funcs = list(funcs)
        for func in funcs:
            func()

    def run(self):
        img = self.get_image()
        digit = self.img_to_digit(img)
        self.login_xk_web(digit, input(), input())
        self.get_class_plan()


if __name__ == '__main__':
    xk = XK()
    xk.run()

