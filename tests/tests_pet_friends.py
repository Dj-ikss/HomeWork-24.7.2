from api import PetFriends
from settings import valid_email, valid_password
import json

pf = PetFriends()

#1 Проверка получения ключа авторизации
def test_get_api_key_for_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
'''Проверяем наличие статуса 200 в ответе сервера и наличие ключа key в ответе'''

#2 Проверка получения списка всех животных
def test_get_list_all_pets(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
'''Запрашиваем список питомцев, проверяем ответ от сервера 200, проверяем, что список не пустой, фильтр оставляем пустым'''

#3 Проверка добавления питомца без фото (Задание 24.7.2)
def test_add_pet_without_foto(name = 'Пушок', animal_type = 'Кот', age = '5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['animal_type'] == animal_type
'''Проверяем, что питомец добавлен, ответ от сервера 200, порода добавляемого питомца совпадает с породой в ответе в списке животных'''

#4 Проверка добавления фото к моему питомцу (Задание 24.7.2)
def test_add_foto_in_my_pet(pet_photo = 'image/Cat.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрашиваем ключ авторизации
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")        #заправшиваем список питомцев
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_foto_in_my_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] != ""        # проверяем, что фото добавилось
'''Проверяем, что фото добавлено, ответ от сервера 200, проверяем, что значение ФОТО не пустое.'''

#5 Проверка добавления питомца с фото
def test_add_pet_with_foto(name = 'Пес', animal_type = 'Собака', age = '2', pet_photo = 'image/Dog.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
'''Проверяем, что питомец добавлен, ответ от сервера 200б имя добавляемого питомца совпадает с именем в ответе в списке животных'''

#6 обновляем фото питомца в карточке питомца с фото (Задание 24.7.2)
def test_replace_foto_in_my_pet(pet_photo = 'image/Cat.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрашиваем ключ авторизации
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")        #заправшиваем список питомцев
    pet_id = my_pets['pets'][0]['id']                         #определяем ID питомца
    id_foto = my_pets['pets'][0]['pet_photo']                 #определяем ID фото из запрошенного id питомца
    status, result = pf.add_foto_in_my_pet(auth_key, pet_id, pet_photo)    #загружаем новое фото
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")  # заправшиваем список питомцев после обновления фото
    id_foto_new = my_pets['pets'][0]['pet_photo']  # определяем ID фото после обновления фото
    assert status == 200                                                   # проверяем ответ 200 от сервера
    assert id_foto_new != id_foto       # проверяем, что фото обновилось и не совпадает с предыдущим
'''Проверяем, что новое фото отправлено на сервер, в ответе код 200, и проверяем что ID нового фото не совпдает с предыдущим значением ID'''

#7 Проверка обновления инфо о питомце
def test_update_info_pet(name = 'Пес', animal_type = 'Шпиц', age = '3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрашиваем ключ авторизации
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")        #заправшиваем список питомцев
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_info_pet(auth_key, pet_id, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
'''Проверяем, что данные по питомцу обновились, ответ сервера 200, имя совпадает с тем, что пришло от сервера при новом запросе списка животных'''

#8 Проверка факта удаления питомца
def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрашиваем ключ авторизации
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")        #заправшиваем список питомцев
    pet_id = my_pets['pets'][0]['id']                         #обращаемся к первому питомцу
    status, _ = pf.delete_my_pet(auth_key, pet_id)            #удаляем первого питомца из моего списка питомцев
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")        #повторно запрашиваем список моих питомцев после удаления
    assert status == 200                                      # проверка наличия статуса 200 в ответе серв. после удаления
    assert pet_id != my_pets.values()                         #проверяем, что id питомца нет в списке питомцев после удаления
'''Проверяем, что первый питомец [0] удалён, ответ сервера 200, id нашего питомца в запрошенном списке животных'''
