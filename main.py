import json
import requests
from tqdm import tqdm

with open('token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()


class VkUser:
    url = 'https://api.vk.com/method/photos.get'

    def __init__(self, user_id, vk_token):
        self.params = {'owner_id': user_id,
                       'album_id': 'profile',
                       'access_token': vk_token,
                       'v': '5.131',
                       'extended': '1',
                       'photo_sizes': '1',
                       'count': 3,
                       }

    def photos_get(self):
        name_photos = []
        urls = []
        res = requests.post(self.url, params=self.params)
        reply = res.json()
        for info in tqdm(reply['response']['items']):
            for form in info['sizes']:
                if form['type'] != 'z':
                    continue
                else:
                    url_photo = form['url']
                    size = form['type']
                    file_name = info['likes']['count']
                    name_dict = {'file_name': file_name, 'size': size}
                    name_photos.append(name_dict)
                    url_dict = {'url': url_photo, 'name': file_name}
                urls.append(url_dict)

        with open('photos.json', 'w') as file:
            json.dump(name_photos, file)
        return urls


class YaDiskUser:

    def __init__(self, ya_token: str, urls):
        self.ya_token = ya_token
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': f'OAuth {self.ya_token}'}
        self.urls = urls

    def create_folder(self):
        link_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
        name_folder = "vk_photo"
        requests.put(f'{link_folder}?path={name_folder}', headers=self.headers)

    def upload_photo(self):
        link_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for url in self.urls:
            file_path = (f'vk_photo/{url["name"]}')
            params = {'path': (file_path), 'url': url['url']}
            res = requests.post(link_upload, params=params, headers=self.headers)
        print(res.status_code)


if __name__ == '__main__':
    user_id = 1
    vk_client = VkUser(user_id, vk_token)
    ya_token = ""
    uploader = YaDiskUser(ya_token, vk_client.photos_get())
    uploader.create_folder()
    uploader.upload_photo()
