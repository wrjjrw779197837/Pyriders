import requests
import hashlib
import json
JSESSION = ""
kxzmc = [
    "大类基础课程",
    "公共基础课程",
    "公共选修课程",
    "通识选修课程",
    "新生研讨课程",
    "专业选修课程",
    "专业必修课程",
    "其他课程"
]


def md5(pw):
    m = hashlib.md5()
    m.update(pw.encode())
    return m.hexdigest()


class AFF(object):
    def __init__(self, xh=None, password=None):
        self.cookies = None
        if xh is None:
            self.xh = input()
        else :
            self.xh = xh
        if password is None:
            self.password = input()
        else:
            self.password = password
        self.pre()

    def login(self):
        # get cookie
        request_url = 'http://ids1.suda.edu.cn/amserver/UI/Login?goto=http%3a%2f%2fmyauth.suda.edu.cn%2fdefault.aspx' \
                      '%3fapp%3dsswsswzx2%26jumpto%3d&welcome=%e5%b8%88%e7%94%9f%e7%bd%91%e4%b8%8a%e4%ba%8b%e5%8a%a1' \
                      '%e4%b8%ad%e5%bf%83&linkName=%e5%a6%82%e6%9e%9c%e6%97%a0%e6%b3%95%e4%bd%bf%e7%94%a8%e7%bb%9f%e4' \
                      '%b8%80%e8%ba%ab%e4%bb%bd%e7%99%bb%e5%bd%95%ef%bc%8c%e8%af%b7%e7%82%b9%e5%87%bb%e8%bf%99%e9%87' \
                      '%8c&linkUrl=http://aff.suda.edu.cn/_web/ucenter/login.jsp&gx_charset=UTF-8'

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
        self.cookies = r.cookies
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
            'Content-Length': '186',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://eos.suda.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'Referer': 'http://ids1.suda.edu.cn/amserver/UI/Login?goto=http%3a%2f%2fmyauth.suda.edu.cn%2fdefault.aspx' \
                      '%3fapp%3dsswsswzx2%26jumpto%3d&welcome=%e5%b8%88%e7%94%9f%e7%bd%91%e4%b8%8a%e4%ba%8b%e5%8a%a1' \
                      '%e4%b8%ad%e5%bf%83&linkName=%e5%a6%82%e6%9e%9c%e6%97%a0%e6%b3%95%e4%bd%bf%e7%94%a8%e7%bb%9f%e4' \
                      '%b8%80%e8%ba%ab%e4%bb%bd%e7%99%bb%e5%bd%95%ef%bc%8c%e8%af%b7%e7%82%b9%e5%87%bb%e8%bf%99%e9%87' \
                      '%8c&linkUrl=http://aff.suda.edu.cn/_web/ucenter/login.jsp&gx_charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.cookies['JSESSIONID'] = '1D142E0A93F9B18D90C23C10F1F81CF0.sudaItemCenter'
        r = requests.post(url=get_score_url, data=json.dumps(payload), cookies=self.cookies, headers=headers)
        data = json.loads(r.text)['data']
        return data

    def pre(self):
        url_login_redirect = 'http://eos.suda.edu.cn/default/index/loginRedirect.jsp'
        r = requests.get(url_login_redirect, cookies=self.cookies)
        JSESSION = r.cookies['JSESSIONID']
        self.cookies = r.cookies
        self.cookies['ASP.NET_SessionId'] = 'a1jjl2aq1l3ty2mol4l1cgdw'
        url = "http://myauth.suda.edu.cn/default.aspx?app=sswsswzx2"
        r = requests.get(url, cookies=self.cookies)
        self.cookies = r.cookies
        self.login()

        # url = "http://aff.suda.edu.cn/mobile/getSchoolUrlListByStatic.mo?timeStamp=1547031303272"
        # r = requests.post(url, cookies=self.cookies)
        #
        # url = 'http://eos.suda.edu.cn/default/base/workflow/ajaxDone.jsp?iportal.uid=38362&iportal.uxid=1627406066&iportal.ualias=1627406066&iportal.uname=%E7%8E%8B%E4%BB%81%E6%9D%B0&iportal.timestamp=1547031302166&iportal.nonce=4908&iportal.group=4%2CAnyUser%2CInternalUsers&iportal.signature=da3a6d0cd10f54c39fee6ba6b45f7dd986ed7170&iportal.ip=10.20.8.122&timeStamp=1547031303283&callback=jQuery2140017983163611926978_1547031303058&begin=0&length=6&isCount=true&_=1547031303059'
        # r = requests.get(url, cookies=self.cookies)
        # print(r.content)
        # print(r.cookies)
        # self.cookies = r.cookies


    def print_all(self):
        data = []
        try:
            for i in kxzmc:
                data += self.get_one_zmc_score(i)
        except KeyError as e:
            self.pre()
            for i in kxzmc:
                data += aff.get_one_zmc_score(i)
            print("Error about Cookie ! ")
        finally:
            for i in data:
                print(i['coursename'], i['MAXCJ'])

    def get_other_score(self, xh=None):
        if xh is None:
            xh = self.xh



if __name__ == "__main__":
    aff = AFF()
    print(aff.get_one_zmc_score(kxzmc[0]))
    # aff.print_all()