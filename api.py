import requests
import json

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email, password):    #Получения ключа авторизации
        headers = {'email': email, 'password': password}
        res = requests.get(self.base_url +'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
        '''Делаем запрос к серверу с указанным логином и паролем, получаем в ответе уникальный ключ доступа для этих регистрационных данных'''

    def get_list_pets(self, auth_key, filter):#Получения списка животных
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
        '''Делаем запрос к API сервера и получаем в ответ список животных с параметрами в фильтре (формат json), фильтр можно указать пустой или my_pets'''

    def add_new_pet_without_foto(self, auth_key, name, animal_type, age):      #добавление нового питомца без ФОТО (Задание 24.7.2)
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_foto_in_my_pet(self, auth_key, pet_id, pet_photo):   # добавляем фото к моему созданному питомцу (Задание 24.7.2)
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pets(self, auth_key, name, animal_type, age, pet_photo):      #добавление нового питомца с ФОТО
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
        '''делаем запрос к API сервера с данными животного, в ответ получаем в json данные по добавленному питомцу '''

    def update_info_pet(self, auth_key, pet_id, name, animal_type, age):     # обновляем данные питомца
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
        '''обновляем данные по питомцу по указанному ID, получаем статус от сервера и данные по питомцу после обновления'''

    def delete_my_pet(self, auth_key, pet_id):  # удаляем питомца
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
        '''Делаем запрос к API сервера на удаление питомца по указанному ID, получаем ответ от сервера и результат после удаления'''
