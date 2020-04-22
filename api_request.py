import json, requests


class ApiRequest:
    @classmethod
    def make_api_get_request(cls, uri='', params={}, timeout=10):
        try:
            req = requests.get(uri, params=params, timeout=timeout)
            # print(req.url)
            return req.json()
        except Exception as e:
            return {'API get request error': str(e)}

    @classmethod
    def make_api_post_request(cls, uri='', data={}, verify=True, timeout=10):
        try:
            req = requests.post(uri, data=data, verify=verify, timeout=timeout)
            # print(req.url)
            return req.json()
        except Exception as e:
            return {'API post request error': str(e)}