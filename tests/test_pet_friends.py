from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password, empty_email, empty_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Тиха', animal_type='Енот',
                                     age='4', pet_photo='images/raccoon1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Енот3", "Енот", "123", "images/raccoon2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Змий', animal_type='Змея', age=1):
    """Проверяем возможность обновления информации о питомце. Должен быть добавлен хотя бы
    один питомец"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Реализация дополнительных двух методов курса обучения

def test_add_new_pet_without_photo_with_valid_data(name='Проходимец', animal_type='конь', age='2'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_add_pet_photo(pet_photo='images/raccoon1.jpg'):
    """Проверяем возможность обновления фото питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Дополнительные 10 тестов домашнего задания 24.7.2

# Негативные тесты PASSED, когда соблюдаются условия, что сервер выдал ошибки.

# 1
def test_get_api_key_for_not_valid_email(email=not_valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при неверном е-майл и верном пароле.
    А также отсутствуют данные ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 2
def test_get_api_key_for_not_valid_password(email=valid_email, password=not_valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при верном е-майл и неверном пароле.
    А также отсутствуют данные ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 3
def test_get_api_key_for_empty_password(email=valid_email, password=empty_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при верном е-майл и пустом пароле.
    А также отсутствуют данные ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 4
def test_get_api_key_for_empty_email(email=empty_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 при пустом е-майл и правильном пароле.
    А также отсутствуют данные ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 5
def test_get_all_pets_with_not_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев с неправильным ключом возвращает ответ сервера 403"""

    auth_key = {'key': '11992166c0dcac116eb41f1f46076fadb60530f4568b82603b2244ee1'}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'pets' not in result


# 6
def test_get_all_pets_with_empty_key(filter=''):
    """ Проверяем что запрос всех питомцев с пустым ключом возвращает ответ сервера 403/
    А также отсутствуют данные питомцев в ответе"""

    auth_key = {'key': ''}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'pets' not in result


# 7
def test_add_new_pet_with_empty_name(name='', animal_type='Енот',
                                     age='1', pet_photo='images/raccoon1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными: Пустое имя.
    Ожидаем ошибку от сервера.
    Тест падает, так как получаем от сервера ответ 200"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    print(result)
    assert status != 200
    assert result['name'] == name


# 8
def test_add_new_pet_with_empty_type(name='Бегун', animal_type='',
                                     age='1', pet_photo='images/raccoon1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными: Пустой тип питомца.
    Ожидаем ошибку от сервера.
    Тест падает, так как питомец добавлен и получаем от сервера ответ 200"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert result['name'] == name


# 9
def test_add_new_pet_with_negative_age(name='Енотище', animal_type='Енот',
                                       age='-11', pet_photo='images/raccoon1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными: Отрицательный возраст.
    Ожидаем ошибку от сервера.
    Тест падает, так как питомец добавлен и получаем от сервера ответ 200"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert result['name'] == name


# 10
def test_add_new_pet_with_empty_age(name='Енотище', animal_type='Енот',
                                    age='', pet_photo='images/raccoon1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными: Пустой возраст.
    Ожидаем ошибку от сервера.
    Тест падает, так как питомец добавлен и получаем от сервера ответ 200"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert result['name'] == name
