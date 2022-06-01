import re

import requests


class AccountServices:
    cookies = {
        '__gpi': 'UID=000008034d31b8e2:T=1654114425:RT=1654114425:S=ALNI_MbGGGk5vuGhEqSSj-NudiRBeNsirg',
        'lang': 'en',
        '_freebie_sso_server': 's%3A8ZSkcLgKUot3ecG9z_nbATdiX122TP63.yeCVoQdLoptp3o9V%2BI6UiyxAHlTP9nYcyL5QqXUnvks',
        '_gcl_au': '1.1.1481375597.1654114440',
        'PAPVisitorId': 'Dz3QpSKEQaO3ckguZOGZyJvhjEQM2z8c',
        '_ga': 'GA1.2.1858651927.1654115052',
        '_gid': 'GA1.2.1059504016.1654115054',
        '_clck': '1jkgzhc|1|f1y|0',
        '__gads': 'ID=c65f420419145b8e-22dcfb3bf1d30017:T=1654114425:RT=1654115526:S=ALNI_MaBq48brYOS2QE2KGK8tAJnO6VSww',
        '_uetsid': 'cddfe880e1e811ec9e6c47063ee1fd2b',
        '_uetvid': 'cde0d690e1e811ec8e8f9917e232cb69',
        '_clsk': '116gsaj|1654115814949|5|1|h.clarity.ms/collect',
    }

    @staticmethod
    def get_download_link(download_authorization: str, data_id: int, extension='png') -> str:
        headers = {
            'authority': 'download.api.photo-ac.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
            'authorization': download_authorization,
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://en.ac-illust.com',
            'referer': 'https://en.ac-illust.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        }

        json_data = {
            'data_id': data_id,
            'data_size': extension.upper(),
            'data_type': extension.lower(),
            'service_type': 'illust_ac',
            'lang': 'en',
            'currency': 'USD',
            'paymentID': '',
            'payerID': '',
            'paymentToken': '',
            'language': 'en',
            'disp_language': 'en',
            'overseas': True,
            'site': 1,
        }

        response = requests.post('https://download.api.photo-ac.com/download', headers=headers, json=json_data)
        return response.json().get('link')

    @staticmethod
    def _get_token(sso_token: str):
        headers = {
            'authority': 'accounts.ac-illust.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
            'authorization': 'Bearer rxYsUahLKQ8LwvCzjwsMa4xvYW4',
            'origin': 'https://en.ac-illust.com',
            'referer': 'https://en.ac-illust.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        }

        params = {
            'ssoToken': sso_token,
        }

        response = requests.get('https://accounts.ac-illust.com/verifytoken', params=params, headers=headers)

        return response.json().get('token')

    @staticmethod
    def _extract_sso_token(redirect_url: str):
        return re.findall(r'ssoToken=(.+)', redirect_url)[0]

    def _get_redirect_sso_token(self, username: str, password: str, session: requests.Session) -> str:

        headers = {
            'authority': 'accounts.ac-illust.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://accounts.ac-illust.com',
            'referer': 'https://accounts.ac-illust.com/login?lang=en&serviceURL=https%3A%2F%2Fen.ac-illust.com%2F',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'lang': 'en',
            'serviceURL': 'https://en.ac-illust.com/',
        }

        data = {
            'email': username,
            'password': password,
            'remember_me': 'on',
        }

        response = session.post('https://accounts.ac-illust.com/login', params=params, cookies=self.cookies,
                                headers=headers, data=data)

        return response.json().get('redirect_to')
