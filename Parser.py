from bs4 import BeautifulSoup
import abc
import requests
import pandas as pd
import lxml


class TechnicalAnalysisParser:
    def __init__(self):
        self.data_summary = {}
        self.data = {}
        self.response = None

    @abc.abstractmethod
    def refresh_data(self):
        pass

    @abc.abstractmethod
    def system_loop(self):
        pass

    def start(self):
        self.system_loop()


class InvestComParser(TechnicalAnalysisParser):
    def refresh_data(self):
        url = "https://www.investing.com/portfolio/gettabdata?portfolio_id=9996712&tab=technical&action=technical&filter=false"

        payload = {}
        headers = {
            'Host': 'www.investing.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Sec-Fetch-Dest': 'empty',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.investing.com/portfolio/?portfolioID=ZWllP24xN21mN2tmZzY%3D',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'G_AUTHUSER_H=0; portfolioStateundefined=; portfolioStatecdc2af03901c7ee6e6a1f4bc9d20d905=9996712:open; adBlockerNewUserDomains=1585497092; _hjid=2b2d5daa-5005-4794-b7a2-5776f3f4b2b6; __gads=ID=a7acaf5d4f694515:T=1585497093:S=ALNI_MZ7CAbZcx6hKIGqwXAR-z7grvE1VQ; _ga=GA1.2.199549310.1585497094; G_ENABLED_IDPS=google; _fbp=fb.1.1585497097101.473260139; r_p_s_n=1; PHPSESSID=21ube18jss9rclictip1l2fbk5; comment_notification_211113320=1; geoC=DE; prebid_page=0; prebid_session=0; gtmFired=OK; StickySession=id.26715798474.394_www.investing.com; _gid=GA1.2.769838797.1585810371; notice_behavior=expressed,eu; notice_preferences=2:; TAconsentID=0e98cdc8-404a-4df0-8411-827662345788; notice_gdpr_prefs=0,1,2:; SKpbjs-unifiedid=%7B%22TDID%22%3A%2242f323e0-2ff0-49be-bd40-a05ddc0df8c7%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222020-03-02T06%3A52%3A57%22%7D; SKpbjs-unifiedid_last=Thu%2C%2002%20Apr%202020%2006%3A52%3A58%20GMT; SKpbjs-id5id=%7B%22ID5ID%22%3A%22ID5-ZHMO6IcC5_MUg0lE9YYCexUOUrZqNA_J4TKkj3O5Zw%22%2C%22ID5ID_CREATED_AT%22%3A%222020-01-07T14%3A49%3A51.896Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Afalse%2C%22ID5ID_LOOKUP%22%3Atrue%2C%223PIDS%22%3A%5B%5D%7D; SKpbjs-id5id_last=Thu%2C%2002%20Apr%202020%2006%3A52%3A58%20GMT; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A7%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A3%3A%22172%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Findices%2Fgermany-30%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228826%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A27%3A%22%2Findices%2Fgermany-30-futures%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A962987%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A29%3A%22%2Fequities%2Fmlp-exch%3Fcid%3D962987%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A962814%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A42%3A%22%2Fequities%2Fcewe-color-holding-ag%3Fcid%3D962814%22%3B%7Di%3A4%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A3%3A%22652%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A23%3A%22%2Fequities%2Fbay-mot-werke%22%3B%7Di%3A5%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A29486%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A33%3A%22%2Fequities%2Fbay-mot-werke%3Fcid%3D29486%22%3B%7Di%3A6%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A3%3A%22656%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A20%3A%22%2Fequities%2Fdt-telekom%22%3B%7D%7D%7D%7D; GED_PLAYLIST_ACTIVITY=W3sidSI6ImFYd1oiLCJ0c2wiOjE1ODU4MTQ3MjUsIm52IjoxLCJ1cHQiOjE1ODU4MTQ3MDUsImx0IjoxNTg1ODE0NzI0fSx7InUiOiI1SWpkIiwidHNsIjoxNTg1ODE0MTUzLCJudiI6MSwidXB0IjoxNTg1ODEzODc2LCJsdCI6MTU4NTgxNDE1Mn1d; _gat_allSitesTracker=1; _gat=1; nyxDorf=Z2tjNWUtMGU1Yz4sM2EwOzJhZSAwMWdg; ses_id=ZSs0dWFuNDwxdWBmZzY0NzVlMmgyNGdmPD5hYDE2YnQ0IDU7YDdjJTE%2BbCIyMTklZ2E1NTUxOm9lMjU5YWxlNWVkNDRhMTRrMWRgbGcyNDc1ZzJpMj1nNDxoYTAxNGI7NDM1a2BnY2YxYWxjMmo5MGd1NSk1cTorZTc1ZWEgZSJlajR1YTI0PTFvYGlnPTRjNTIyYDIxZzM8aGEwMWBiejR%2F'
        }

        self.response = requests.request("GET", url, headers=headers, data=payload)
        self.data = pd.read_html(self.response.text,match="")[0]
        print(self.data.head(5))


class BoerseDeParser(TechnicalAnalysisParser):
    def refresh_data(self):
        url = "https://www.boerse.de/insider-trades/"

        payload = {}
        headers = {}

        self.response = requests.request("GET", url, headers=headers, data=payload)
        self.data = pd.read_html(self.response.text, match="")[3]
        self.data.columns = self.data.tail(1).values[0]
        print(self.data.head(5))



#InvestComParser().refresh_data()
BoerseDeParser().refresh_data()
