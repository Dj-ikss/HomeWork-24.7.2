from api import PetFriends
from settings import valid_email, valid_password, notvalid_password, notvalid_email
import json

pf = PetFriends()

#1 Неагтивный тест Проверка получения ключа авторизации при невалидном email
def test_negative_get_api_key_for_user_notvalid_email(email = notvalid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
'''При передаче невалидного email - авторизация не должна проходить'''

#2 Негативный тест, авторизация с невалидным логином и получения списка всех животных
def test_negative_get_list_all_pets_with_notvalid_password(filter=''):
    _, auth_key = pf.get_api_key(valid_email, notvalid_password)
    status, result = pf.get_list_pets(auth_key, filter)
    assert  status == 200
    assert len(result['pets']) > 0
'''При передаче невалидного пароля - авторизация не должна проходить'''

#3 Негативный тест. Проверка передачи пустого значения полей Имя, Порода, Возраст
def test_negativ_zerro_info_my_ped(name = '', animal_type = '', age = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age
'''Проводим негативный тест с добавлением питомца с пустыми полями ввода, пустые поля система не должна принимать'''

#4 Негативный тест. Проверка передачи спецсимволов в поля Имя, Порода, Возраст
def test_negativ_specsimvol_info_my_ped(name = '!@#', animal_type = '%^*', age = '&?'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age
'''При передачи спецсимволов в полях ввода - система должна выдать ошибку. Спецсимволы приниматься системой не должны'''

#5 Негативный тест. Проверка передачи отрицательного значения в поле Возраст
def test_negativ_age_info_my_ped(name = 'Рекс', animal_type = 'Собака', age = '-5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age
'''При вводе отрицательного числа в поле ввода Возраст - система должна выдать ошибку. Отрицательный возраст система не должна принимать'''

#6 Негативный тест. Проверка передачи буквенного значения в поле Возраст
def test_negativ_text_age_info_my_ped(name = 'Рекс', animal_type = 'Собака', age = 'Пять'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age
'''При вводе букв в поле ввода Возраст - система должна выдавать ошибку, Поле ввода должно принимать только положительные цыфры'''

#7 Негативный тест. Проверка грантичного значения в поле Возраст
def test_negativ_age_limit_info_my_ped(name = 'Рекс', animal_type = 'Собака', age = '500'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age
'''При вводе значения более 100 в поле возраст - система должна выдавать ошибку. Поле возраст принимает максимально езначение 100 (лет)'''

#8 Негативный тест. Проверка добавления фото к моему питомцу в формате отдичного от jpeg
def test_negative_add_other_format_in_info_my_pet(pet_photo = 'image/Proverka.docx'):
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрашиваем ключ авторизации
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")        #заправшиваем список питомцев
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_foto_in_my_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] != ""
'''Проводим негативный тест, добавляем вместо фото файл с другим форматом (docx), ответ сервера не должен быть равен 200. Система не должна принимать прочие расширения кроме jpeg'''

#9 Негативный тест. Проверка функции добавления фото, без вложенного файла.
def test_negative_add_null_foto(pet_photo = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрашиваем ключ авторизации
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")        #заправшиваем список питомцев
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_foto_in_my_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] == ""
'''Проверяем возможность дфункции добавления фото с пустым значением вместо файла. Система не должна принимать NULL место файла.'''

#10 Негативный тест. Удаление не своего питомца
def test_delete_pet(filter= ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрашиваем ключ авторизации
    _, my_pets = pf.get_list_pets(auth_key, filter=filter)        #заправшиваем список питомцев
    pet_id = my_pets['pets'][0]['id']                         #обращаемся к первому питомцу
    status, _ = pf.delete_my_pet(auth_key, pet_id)            #удаляем первого питомца из моего списка питомцев
    _, my_pets = pf.get_list_pets(auth_key, filter=filter)        #повторно запрашиваем список моих питомцев после удаления
    assert status == 200                                      # проверка наличия статуса 200 в ответе серв. после удаления
    assert pet_id != my_pets.values()                         #проверяем, что id питомца нет в списке питомцев после удаления
'''Проверяем возможность удаления питомца из общего списка питомцев. Система не должна позволять удалять чужого питомца'''
