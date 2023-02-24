import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def auth_page():  # страница авторизации
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://b2c.passport.rt.ru')
    yield pytest.driver
    pytest.driver.quit()


@pytest.fixture
def reg_page():  # страница регистрации
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    pytest.driver.get('http://b2c.passport.rt.ru')
    pytest.driver.implicitly_wait(10)
    reg = pytest.driver.find_element(By.XPATH, "//*[@id='kc-register']")
    reg.click()
    yield pytest.driver
    pytest.driver.quit()


@pytest.fixture
def restore_password_page():  # страница восстановления пароля
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    pytest.driver.get('http://b2c.passport.rt.ru')
    pytest.driver.implicitly_wait(10)
    restore_password = pytest.driver.find_element(By.XPATH, "//*[@id='forgot_password']")
    restore_password.click()
    yield pytest.driver
    pytest.driver.quit()
