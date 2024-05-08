from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_addresses import abi,contract
import re


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract, abi=abi)


def auth():
    public_key = input("Введите публичный ключ: ")
    password = input("Введите пароль: ")

    try:
        w3.geth.personal.unlock_account (public_key, password)
        print("Авторизация прошла успешно.")
        return public_key
    except Exception as e:
        print (e)
        return None

def passwdcheck(password):

    if len(password) < 12:
        return False, "Пароль должен содержать не менее 12 символов."


    if not re.search(r"[A-Z]", password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву."
    if not re.search(r"[a-z]", password):
        return False, "Пароль должен содержать хотя бы одну строчную букву."
    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру."
    if not re.search(r"[!@#$%^&*()_+=-]", password):
        return False, "Пароль должен содержать хотя бы один специальный символ (!, @, #, $, % и т. д.)."

    if re.search(r"password|qwerty", password):
        return False, "Пароль не должен быть простым шаблоном (например, 'password' или 'qwerty')."

    return True, "Пароль соответствует требованиям сложности."

def registration():
    password = input("Введите пароль для регистрации: ")
    is_valid, message = passwdcheck(password)

    if is_valid:
        print("Пароль принят.")
    else:
        print("Ошибка:", message)
    address = w3.geth.personal.new_account(password)
    print(f"Адрес нового аккаунта: {address}")

def createN (account):
    name = input("Введите название недвижимости: ")
    estAddress = input("Введите адрес недвижимости: ")

    print("\n\tТипы недвижимости:")
    print("1. Дом \n2. Апартамент \n3. Квартира \n4. Лофт")
    while (True):
        try:
            eType = int(input("Введите тип недвижимости: "))
            break
        except (ValueError):

            print("Введите число типа.")
            continue
    while (True):
        try:
            rooms = int(input("Введите количество комнат: "))
            break
        except (ValueError):

            print("Введите число комнат: ")
            continue
    opisanieN = input("Описание недвижимости: ")
    try:
        tx_hash = contract.functions.createEstate(name, estAddress, eType, rooms, opisanieN).transact(
            {
                "from": account
            }
        )
        print("Транзакция на создание недвижимости отправлена успешно. Хэш транзакции: ", tx_hash.hex())
    except Exception as e:
        print("Ошибка при создании недвижимости: ", e)

def createObj(account):
    try:
        print("Недвижимость: ", contract.functions.getEstates().call())
    except Exception as e:
        print("Ошибка при просмотре недвижимости: ", e)

    while (True):
        try:
            idN = int(input("\nВведите ID недвижимости: "))
            break
        except (ValueError):
            print("Такого ID нет.")
            continue
    while (True):
        try:
            price = int(input("Введите цену недвижимости: "))
            if (price < 0):
                price = 0
            break
        except (ValueError):
            print("Введите число.")
            continue
    try:
        tx_hash = contract.functions.createAd(idN, price).transact(
            {
                "from": account
            }
        )
        print("Транзакция на создание объявления отправлена успешно. Хэш транзакции: ", tx_hash.hex())
    except Exception as e:
        print("Ошибка при создании объявления: ", e)

def buyN(account):
    try:
        n = contract.functions.getAds().call()
        print("Список объявлений: ", n)
    except Exception as e:
        print("Ошибк, не не не не: ", e)
    while (True):
        try:
            idAD = int(input("\nВведите ID обьявления: "))
            break
        except (ValueError):
            print("Такого ID не существует")
            continue
    try:
        hashN = contract.functions.buyEstate(idAD).transact(
            {
                "from": account
            }
        )
        print("Оплата прошла успешно. Чек: ", hashN.hex())
    except Exception as e:
        print("Ошибка при покупке недвижимости: ", e)

def updateN(account):
    try:
        upN = contract.functions.getEstates().call()
        print("Список недвижимостей: ", upN)
    except Exception as e:
        print("Ошибка, не не не не: ", e)
    while (True):
        try:
            idN = int(input("\nВведите ID недвижимости: "))
            break
        except (ValueError):
            print("Такого ID не существует")
            continue
    while (True):
        try:
            status = bool(input("Заблокировать (false) или разблокировать (true) недвижимость?\n"))
            break
        except (ValueError):
            print("Введите true или false.")
            continue
    try:
        tx_hash = contract.functions.updateEstateStatus(idN, status).transact(
            {
                "from": account
            }
        )
        print("Оплата прошла успешно. Чек: ", tx_hash.hex())
    except Exception as e:
        print("Ошибка при обновлении статуса: ", e)

def updateObj(account):
    try:
        Obj = contract.functions.getAds().call()
        print("Список объявлений: ", Obj)
    except Exception as e:
        print("Ошибка при выводе объявлений: ", e)
    while (True):
        try:
            idAd = int(input("\nВведите ID объявления: "))
            break
        except (ValueError):
            print("Такого ID не существует")
            continue
    while (True):
        try:
            status = int(input("Заблокировать (1) или разблокировать (0) объявление?\n"))
            break
        except (ValueError):
            print("Введите 0 или 1.")
            continue
    try:
        tx_hash = contract.functions.updateAdStatus(idAd, status).transact(
            {
                "from": account
            }
        )
        print("Обновление прошло успешно. Чек: ", tx_hash.hex())
    except Exception as e:
        print("Ошибка при обновлении статуса: ", e)

def withdraw(account):
    while (True):
        try:
            amount = int(input("Введите сумму для снятия: "))
            break
        except(ValueError):
            print("Введите число.")
            continue
    try:
        tx_hash = contract.functions.withDraw(amount).transact(
            {
                "from": account
            }
        )
        print("Транзакция на снятие средств успешно отправлена. Хэш транзакции: ", tx_hash.hex())
    except Exception as e:
        print("Ошибка при снятии средств: ", e)

def main():

    account = ""
    is_auth = False
    while True:
        if not is_auth:
            choice = input("Выберите: \n1. Авторизация\n2. Регистрация\n")
            match choice:
                case "1":
                    account = auth()
                    if account is not None:
                        is_auth = True
                case "2":
                    registration()
        else:
            choice = input("Выберите: \n1. Отправить денюжки \n2. Посмотреть баланс контракта "
                           "\n3. Вывести денюжки \n4. Посмотреть баланс аккаунта \n5. Выход\n")
            match choice:
                case "1":
                    createN(account)
                case "2":
                    createObj(account)
                case "3":
                    buyN(account)
                case "4":
                    ch = input("Выберите: \n1. Обновить статус недвижимости \n2. Обновить статус объявления\n")
                    if (ch == "1"):
                        updateN(account)
                    elif (ch == "2"):
                        updateObj(account)
                    else:
                        print("Такой опции нет.")
                case "5":
                    withdraw(account)
                case "6":
                    print(f"Баланс аккаунта: {w3.eth.get_balance(account)}")
                case "7":
                    is_auth = False
                case _:
                    print("Введите корректное число!")

if __name__ == "__main__":
    main()
