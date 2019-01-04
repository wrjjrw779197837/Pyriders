import requests
from PIL import Image
import hashlib
import json

def md5(pw):
    m = hashlib.md5()
    m.update(pw.encode())
    return m.hexdigest()

class AFF(object):
    def __init__(self, xh, password):
        self.cookies = None
        self.xh = xh
        self.password = password

    def login(self):
        # get cookie
        request_url = 'http://ids1.suda.edu.cn/amserver/UI/Login?goto=http%3a%2f%2fmyauth.suda.edu.cn%2fdefault.aspx' \
                      '%3fapp%3dsswsswzx2%26jumpto%3d&welcome=%e5%b8%88%e7%94%9f%e7%bd%91%e4%b8%8a%e4%ba%8b%e5%8a%a1' \
                      '%e4%b8%ad%e5%bf%83&linkName=%e5%a6%82%e6%9e%9c%e6%97%a0%e6%b3%95%e4%bd%bf%e7%94%a8%e7%bb%9f%e4' \
                      '%b8%80%e8%ba%ab%e4%bb%bd%e7%99%bb%e5%bd%95%ef%bc%8c%e8%af%b7%e7%82%b9%e5%87%bb%e8%bf%99%e9%87' \
                      '%8c&linkUrl=http://aff.suda.edu.cn/_web/ucenter/login.jsp&gx_charset=UTF-8'
        r = requests.get(request_url)
        self.cookies = r.cookies

        data = {
            'IDButton': 'Submit',
            'encoded': 'false',
            'goto': '',
            'gx_charset': 'UTF - 8',
            'IDToken0': '',
            'IDToken1': str(self.xh),
            'IDToken9': self.password,
            'IDToken2': md5(self.password)  # md5 加密
        }

        headers = {
            'Host': 'ids1.suda.edu.cn',
            'Connection': 'keep-alive',
            'Content-Length': '187',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://ids1.suda.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        r = requests.post(request_url, data=data, headers=headers, cookies=self.cookies)
        return r

    def get_one_zmc_score(self, zmc, xh=None):
        if xh is None:
            xh = self.xh
        get_score_url = 'http://eos.suda.edu.cn/default/businessplatfrom/processform/stuCustomReport/cn.edu.suda.' \
                        'itemscenter.businessplatfrom.apply2.customReport.getCJB.biz.ext'
        payload = {
            "xh": str(xh),
            "kcxz": str(zmc),
            "pageIndex": '0',
            "pageSize": '10',
            "sortField": "",
            "sortOrder": "",
            "page": {"begin": 0, "length": 10}
        }

        headers = {
            'POST': 'http://eos.suda.edu.cn/default/businessplatfrom/processform/stuCustomReport/'
                    'cn.edu.suda.itemscenter.businessplatfrom.apply2.customReport.getCJB.biz.ext HTTP/1.1',
            'Host': 'eos.suda.edu.cn',
            'Proxy-Connection': 'keep-alive',
            'Content-Length': '136',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://eos.suda.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'Referer': 'http://eos.suda.edu.cn/default/businessplatfrom/'
                       'processform/stuCustomReport/customReportApply.jsp?',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        tmp_cookies = self.cookies
        tmp_dict = tmp_cookies.get_dict()
        tmp_dict['JSESSIONID'] = 'C8863A96EAAABF46B44EF448455B15CE.sudaItemCenter'
        tmp_cookies = requests.cookies.cookiejar_from_dict(tmp_dict)

        r = requests.post(url=get_score_url, data=json.dumps(payload), cookies=tmp_cookies, headers=headers)
        print(r.text)
        data = json.loads(r.text)['data']
        return data


if __name__ == '__main__':
    aff = AFF(input(), input())
    tmp = aff.login()
    print(tmp.session)
    try:
        aff.get_one_zmc_score("大类基础课程")
    except KeyError as e:

        print("Error about Cookie ! ")
    finally:
        aff.get_one_zmc_score("大类基础课程")
        pass
