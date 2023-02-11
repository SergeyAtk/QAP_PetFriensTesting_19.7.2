import os

from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()

def test_get_api_key_for_valid_user(email: str = valid_email,
                                    password: str = valid_password) -> None:
    """ Метод делает запрос к API сервера и возвращает статус запроса
    и результат с уникальным ключом пользователя, найденного по укзанным
    email и паролю
    :param email: email
    :param password: password
    :return: api_key """

    ststus, result = pf.get_api_key(email, password)
    assert ststus == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter: str = '') -> None:
    """ Метод делает запрос к API сервера и возвращает статус запроса
    и результат со списком найденных питомцев."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Шарик', animal_type='лайка',
                                     age='4', pet_photo='images/dog.jpg'):
    """Проверяем что можно добавить питомца с фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
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
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/tiger.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Test 1
def test_get_my_pets_with_valid_key(filter: str = 'my_pets') -> None:
    """ Тест делает запрос к API сервера и возвращает статус запроса
        и результат со списком моих питомцев."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#Test 2
def test_add_pet_photo_valid_data(pet_photo='images/tiger.jpg'):
    """Тест добавляет фото существующего питомца в формате .jpg"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) != 0:
    # Берём id первого питомца из списка
        pet_id = my_pets['pets'][0]["id"]
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 200

#Test 3
def test_add_pet_photo_valid_data_webp(pet_photo='images/cote.webp'):
    """Тест добавляет фото существующего питомца в формате .webp"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) != 0:
    # Берём id первого питомца из списка
        pet_id = my_pets['pets'][0]["id"]
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 200

#Test 4
def test_add_new_pet_without_photo(name='Лайкин',
                                   animal_type='лайка',
                                   age='5'):
    """ Тест добавляет нового питомца на сайт без фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# Test 5
def test_get_api_key_for_invalid_psw(email: str = valid_email,
                                    password: str = 'invalid_password') -> None:
    """ Негативный тест. Метод делает запрос c неправильным паролем к API сервера
    и возвращает статус запроса и результат с кодом 403, api_key отсутствует в ответе"""

    ststus, result = pf.get_api_key(email, password)
    assert ststus == 403
    assert 'key' not in result

# Test 6
def test_get_api_key_without_data(email="", password=""):
    """Тест проверяет отсутствие api-ключа в ответе от сервера без данных логина и пароля
    код ответа 403"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# Test 7
def test_get_all_pets_with_invalid_key(filter=""):
    """Негативный тест. Метод проверяет что запрос при использовании невалидного api
    ключа возвращает статус 4ХХ"""

    auth_key = {"key": "invalid_api_key"} # используем невалдный  api ключ
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert 400 <= status < 500  # сверяем, статус код должен быть 4ХХ

#Test 8
def test_add_info_new_pet_without_photo_invalid_data_age(name = "NEW", animal_type = "INFO", age = "abc"):
    """Тест проверяет что можно добавить информацию о питомце с не корректными данными age = 'abc'
    если возраст указан в цифрах, то получаем True, в противном случае False """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200  # Проверяем что статус ответа 200
    assert result['name'] == name  # и имя питомца соответствует заданному
    assert result['age'].isdigit() == True # Bug. Сайт принимает буквы вместо цифр.

#Test 9
def test_add_info_new_pet_without_photo_invalid_data_age_(name = "NEW", animal_type = "INFO", age = "-5"):
    """Тест проверяет что можно добавить информацию о питомце с не корректными данными age = '-5'"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200  # Проверяем что статус ответа 200
    assert result['name'] == name  # и имя питомца соответствует заданному
    assert int(result['age'])  >= 0 # Bug. Сайт принимает отрицательные числа в возрасте питомца.

# Test 10
def test_get_list_of_all_pets_incorrected_key():
    """Тест на проверку получения списка всех питомцев при авторизации с неверным ключом
    ожидается ответ со статусом 403"""

    auth_key = {'key': 'invalid_api_key'}
    status, results = pf.get_list_of_pets(auth_key=auth_key, filter="")
    assert status == 403

