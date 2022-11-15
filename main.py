import time
import json
import requests
from pprint import pprint
import time
from tqdm import tqdm
from itertools import chain


def main(user_ids, ya_token):
    with open('token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()

    def photos_get():
        url = 'https://api.vk.com/method/photos.getProfile'
        params = {'extended': '1',
                  'count': '3',
                  'rev': '1',
                  'photo_sizes': '1',
                  'user_ids': user_ids,
                  'access_token': vk_token,
                  'v': '5.131'
                  }
        res = requests.post(url, params=params)
        photos = []
        name_photos = []
        name_files = []
        a = res.json()
        for i in tqdm(a['response']['items']):
            for p in i['sizes']:
                if p['type'] != 'z':
                    continue
                else:
                    url_photo = p['url']
                    size = p['type']
                    file_name = i['likes']['count']
                    photos.append(url_photo)
                    name_dict = {'file_name': file_name, 'size': size}
                    name_photos.append(name_dict)
                    url_dict = {'url': url_photo, 'name': file_name}
                name_files.append(url_dict)

        with open('photos.json', 'w') as f:
            json.dump(name_photos, f)

        def create_folder():
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization': f'OAuth {ya_token}'}
            link_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
            link_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            name_folder = "vk_photo"
            file_path = 'vk_photo/'
            requests.put(f'{link_folder}?path={name_folder}', headers=headers)

            def upload_photo():
                for h in name_files:
                    file_path = (f'vk_photo/{h["name"]}')
                    params = {'path': (file_path), 'url': h['url']}
                    response = requests.post(link_upload, params=params, headers=headers)
                pprint(response.status_code)

            return upload_photo()

        return create_folder()

    return photos_get()


if __name__ == '__main__':
    main('95301904', 'ya_token')
