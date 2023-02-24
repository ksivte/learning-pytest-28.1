import pytest
from selenium.webdriver.common.by import By


def test_major_elements_auth(auth_page):  # 1 - проверка наличия основных элементов на главной странице
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.XPATH, "//h1[contains(text(),'Авторизация')]")  # заголовок авторизации
    assert pytest.driver.find_element(By.XPATH, "//*[@id='page-right']/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]")  # элементы меню выбора способа авторизации
    assert pytest.driver.find_element(By.ID, 't-btn-tab-phone')
    assert pytest.driver.find_element(By.ID, 't-btn-tab-mail')
    assert pytest.driver.find_element(By.ID, 't-btn-tab-login')
    assert pytest.driver.find_element(By.ID, 't-btn-tab-ls')
    assert pytest.driver.find_element(By.XPATH, "//*[@id='username']")  # поле ввода нормера телефона/почты/логина/лицевого счета
    assert pytest.driver.find_element(By.XPATH, "//*[@id='password']")  # поле ввода пароля
    assert pytest.driver.find_element(By.XPATH, "//*[@id='kc-login']")  # кнопка "Войти"
    assert pytest.driver.find_element(By.XPATH, "//*[@id='forgot_password']")  # ссылка сброса пароля ("Забыл пароль")
    assert pytest.driver.find_element(By.XPATH, "//*[@id='kc-register']")  # ссылка регистрации ("Зарегистрироваться")


def test_social_network_elements_auth(auth_page):  # 2 - проверка наличия элементов авторизации через социальные сети
    pytest.driver.implicitly_wait(10)
    social = pytest.driver.find_elements(By.CLASS_NAME, "social-providers__provider")  # авторизация через социальные сети
    assert len(social) == 5
    if len(social) == 5:
        assert pytest.driver.find_element(By.CSS_SELECTOR, "a#oidc_vk")  # vk
        assert pytest.driver.find_element(By.CSS_SELECTOR, "a#oidc_ok")  # ok
        assert pytest.driver.find_element(By.CSS_SELECTOR, "a#oidc_mail")  # mail.ru
        assert pytest.driver.find_element(By.CSS_SELECTOR, "a#oidc_google")  # google
        assert pytest.driver.find_element(By.CSS_SELECTOR, "a#oidc_yandex")  # yandex


def test_minor_elements_auth(auth_page):  # 3 - проверка наличия второстепенных элементов на главной странице
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.CSS_SELECTOR, "header#app-header > div > div > svg")  # наличие лого в верхнем правом углу
    assert pytest.driver.find_element(By.CSS_SELECTOR, "section#page-left# page-left > div")  # наличие лого и слогана в левой половине страницы


def test_footer_elements_auth(auth_page):  # 4 - проверка наличия текста в футере главной страницы
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.XPATH, "//footer[contains(text(),'© 2023 ПАО «Ростелеком». 18+')]")  # наличие года, названия компании, возрастной маркировки
    assert pytest.driver.find_element(By.XPATH, """//footer[contains(text(),'Продолжая использовать наш сайт, вы даете согласие на обработку файлов 
Cookies
 и других пользовательских данных, в соответствии с Политикой конфиденциальности и Пользовательским соглашением')]""")  # наличие информации о cookies
    assert pytest.driver.find_element(By.XPATH, """Служба поддержки
8 800 100 0 800""")


def test_phone_number_login(auth_page):  # 5 - авторизация, логин по номеру телефона, позитивный сценарий
    pytest.driver.implicitly_wait(10)
    pytest.driver.find_element(By.XPATH, "//*[@id='username']").send_keys('0000000000')  # здесь указать корректный номер
    pytest.driver.find_element(By.XPATH, "//*[@id='password']").send_keys('здесь указать корректный пароль')  # здесь указать корректный пароль
    login = pytest.driver.find_element(By.XPATH, "//*[@id='kc-login']")
    login.click()  # нажимаем на кнопку входа в аккаунт
    last_name_element = pytest.driver.find_element(By.CSS_SELECTOR, ".user-name__last-name")
    assert last_name_element.get_text() == "Тест"
    first_name_element = pytest.driver.find_element(By.CSS_SELECTOR, ".user-name__first-patronymic")
    assert first_name_element.get_text() == "Тестов"


def test_phone_number_login_with_empty_fields(auth_page):  # 6 - авторизация, попытка логина с пустыми полями
    pytest.driver.implicitly_wait(10)
    login = pytest.driver.find_element(By.XPATH, "//*[@id='kc-login']")
    login.click()
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.XPATH, "//h1[contains(text(),'Авторизация')]")
    assert pytest.driver.find_element(By.XPATH, "//SPAN[contains(text(),'Введите номер телефона')]")


def test_login_phone_number_not_in_database(auth_page):  # 7 - авторизация, логин по номеру телефона, отсутствующему в базе
    pytest.driver.implicitly_wait(10)
    pytest.driver.find_element(By.XPATH, "//*[@id='username']").send_keys('0000000000')  # здесь указать некорректный номер
    pytest.driver.find_element(By.XPATH, "//*[@id='password']").send_keys('здесь указать корректный пароль')  # здесь указать корректный пароль
    login = pytest.driver.find_element(By.XPATH, "//*[@id='kc-login']")
    login.click()
    assert pytest.driver.find_element(By.XPATH, "//h1[contains(text(),'Авторизация')]")
    assert pytest.driver.find_element(By.XPATH, "//SPAN[contains(text(), 'Неверный логин или пароль')]")


def test_availability_user_agreement(reg_page):  # 8 - доступность пользовательского соглашения
    pytest.driver.implicitly_wait(10)
    user_agreement = pytest.driver.find_element(By.XPATH, "//*[@id='page-right']/div[1]/div[1]/div[1]/form[1]/div[4]/a[1]")
    user_agreement.click()
    assert pytest.driver.find_element(By.XPATH, "//h1[contains(text(),'Публичная оферта о заключении Пользовательского соглашения на использование Сервиса «Ростелеком ID»')]")


def test_major_elements_reg(reg_page):  # 9 - проверка наличия основных элеменов на странице регистрации
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.XPATH, "//h1[contains(text(),'Регистрация')]")  # заголовок регистрации
    assert pytest.driver.find_element(By.XPATH, "//p[contains(text(),'Личные данные')]")  # подзаголовок "Личные данные"
    assert pytest.driver.find_element(By.NAME, "firstName")  # поле ввода имени
    assert pytest.driver.find_element(By.NAME, "lastName")  # поле ввода фамилии
    assert pytest.driver.find_element(By.XPATH, "//p[contains(text(),'Данных для входа')]")  # подзаголовок "Данных для входа"
    assert pytest.driver.find_element(By.NAME, "address")  # поле ввода e-mail
    assert pytest.driver.find_element(By.NAME, "password")  # поле ввода пароля
    assert pytest.driver.find_element(By.NAME, "password-confirm")  # поле ввода подтверждения пароля
    assert pytest.driver.find_element(By.XPATH, "//*[@id='page-right']/div[1]/div[1]/div[1]/form[1]/button[1]")  # кнопка "Зарегистрироваться"


def test_minor_elements_reg(reg_page):  # 10 - проверка наличия второстепенных элементов на странице регистрации
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.CSS_SELECTOR, "header#app-header > div > div > svg")  # наличие лого в верхнем правом углу
    assert pytest.driver.find_element(By.CSS_SELECTOR, "section#page-left# page-left > div")  # наличие лого и слогана в левой половине страницы


def test_footer_elements_reg(reg_page):  # 11 - проверка наличия текста в футере страницы регистрации
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.XPATH, "//footer[contains(text(),'© 2023 ПАО «Ростелеком». 18+')]")  # наличие года, названия компании, возрастной маркировки
    assert pytest.driver.find_element(By.XPATH, """//footer[contains(text(),'Продолжая использовать наш сайт, вы даете согласие на обработку файлов 
Cookies
 и других пользовательских данных, в соответствии с Политикой конфиденциальности и Пользовательским соглашением')]""")  # наличие информации о cookies
    assert pytest.driver.find_element(By.XPATH, """Служба поддержки
8 800 100 0 800""")


def test_footer_elements_restore_password(restore_password_page):  # 12 - проверка наличия основных элементов на странице восстановления пароля
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.XPATH, "//h1[contains(text(),'Восстановление пароля')]")  # заголовок восстановления пароля
    assert pytest.driver.find_element(By.XPATH, "//p[contains(text(),'Введите данные и нажмите «Продолжить»')]")  # подзаголовок "Введите данные и нажмите «Продолжить»"
    assert pytest.driver.find_element(By.NAME, "username")  # поле ввода телефона/почты/логина/лицевого счета
    assert pytest.driver.find_element(By.NAME, "Captcha")  # капча
    assert pytest.driver.find_element(By.XPATH, "//*[@id='page-right']/div[1]/div[1]/div[1]/form[1]/div[2]/div[1]/div[2]/svg[1]")  # кнопка обновления капчи
    assert pytest.driver.find_element(By.NAME, "code")  # поле ввода капчи
    assert pytest.driver.find_element(By.XPATH, "//span[contains(text(),'Введите символы с картинки')]")
    assert pytest.driver.find_element(By.NAME, "reset")  # кнопка "Продолжить"
    assert pytest.driver.find_element(By.NAME, "back_to_login")  # кнопка "Вернуться назад"


def test_minor_elements_restore_password(restore_password_page):  # 13 - проверка наличия второстепенных элементов на странице восстановления пароля
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.CSS_SELECTOR, "header#app-header > div > div > svg")  # наличие лого в верхнем правом углу
    assert pytest.driver.find_element(By.CSS_SELECTOR, "section#page-left# page-left > div")  # наличие лого и слогана в левой половине страницы


def test_footer_elements_restore_password(restore_password):  # 14 - проверка наличия текста в футере страницы регистрации
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.XPATH, "//footer[contains(text(),'© 2023 ПАО «Ростелеком». 18+')]")  # наличие года, названия компании, возрастной маркировки
    assert pytest.driver.find_element(By.XPATH, """//footer[contains(text(),'Продолжая использовать наш сайт, вы даете согласие на обработку файлов 
Cookies
 и других пользовательских данных, в соответствии с Политикой конфиденциальности и Пользовательским соглашением')]""")  # наличие информации о cookies
    assert pytest.driver.find_element(By.XPATH, """Служба поддержки
8 800 100 0 800""")


def test_restore_password_with_empty_fields(restore_password):  # 15 - попытка восстановления пароля с пустыми полями ввода
    pytest.driver.implicitly_wait(10)
    reset = pytest.driver.find_element(By.NAME, "reset")  # кнопка "Продолжить"
    reset.click()
    assert pytest.driver.find_element(By.XPATH, "//span[contains(text(),'Введите номер телефона')]")


def test_restore_password_correct_number_and_empty_capcha(restore_password_page):  # 16 - попытка восстановления пароля с корректным номером и пустым полем ввода капчи
    pytest.driver.implicitly_wait(10)
    pytest.driver.find_element(By.XPATH, "//*[@id='username']").send_keys('0000000000')  # здесь указать корректный номер
    reset = pytest.driver.find_element(By.NAME, "reset")  # кнопка "Продолжить"
    reset.click()
    assert pytest.driver.find_element(By.XPATH, "//span[contains(text(),'Неверный логин или текст с картинки')]")


def test_restore_password_back_reg(restore_password_page):  # 17 - возвращение на страницу регистрации со страницы восстановления пароля
    pytest.driver.implicitly_wait(10)
    back = pytest.driver.find_element(By.NAME, "back_to_login")
    back.click()
    pytest.driver.implicitly_wait(10)
    assert pytest.driver.find_element(By.XPATH, "//h1[contains(text(),'Авторизация')]")


def test_reg_with_empty_fields(reg_page):  # 18 - регистрация с пустыми полями ввода
    pytest.driver.implicitly_wait(10)
    reg = pytest.driver.find_element(By.XPATH, "//*[@id='page-right']/div[1]/div[1]/div[1]/form[1]/button[1]")  # кнопка "Зарегистрироваться"
    reg.click()
    assert pytest.driver.find_element(By.XPATH, "//span[contains(text(),'Необходимо заполнить поле кириллицей. От 2 до 30 символов.')]")
    assert pytest.driver.find_element(By.XPATH,
                                      "//span[contains(text(),'НВведите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru')]")
    assert pytest.driver.find_element(By.XPATH, "//span[contains(text(),'Длина пароля должна быть не менее 8 символов')]")


def test_reg(reg_page):  # 19 - регистрация с несовпадающими паролями
    pytest.driver.implicitly_wait(10)
    pytest.driver.find_element(By.NAME, "firstName").send_keys('Тест')  # поле ввода имени
    pytest.driver.find_element(By.NAME, "lastName").send_keys('Тесттест')  # поле ввода фамилии
    pytest.driver.find_element(By.NAME, "address").send_keys('здесь указать корректный e-mail')  # здесь указать корректный e-mail
    pytest.driver.find_element(By.NAME, "password").send_keys('123456uU')  # поле ввода пароля
    pytest.driver.find_element(By.NAME, "password-confirm").send_keys('Uu654321')  # поле ввода подтверждения пароля
    reg = pytest.driver.find_element(By.XPATH,
                                     "//*[@id='page-right']/div[1]/div[1]/div[1]/form[1]/button[1]")  # кнопка "Зарегистрироваться"
    reg.click()
    assert pytest.driver.find_element(By.XPATH, "//span[contains(text(),'Пароли не совпадают')]")
