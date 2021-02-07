import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/chromedriver.exe')
    pytest.driver.implicitly_wait(10)
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    pytest.driver.find_element_by_id('email').send_keys('testmail@gmail.com')
    pytest.driver.find_element_by_id('pass').send_keys('12345')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.find_element_by_xpath('//a[@href="/my_pets"]').click()
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//tbody/tr')))

    yield

    pytest.driver.quit()


def test_number_of_my_pets():
    pets = pytest.driver.find_elements_by_xpath('//tbody/tr')
    stat = pytest.driver.find_element_by_class_name('.col-sm-4')
    number_of_pets = stat.text.split(' ')
    assert len(pets) == int(number_of_pets[1][0])


def test_half_pets_with_photo():
    pets = pytest.driver.find_elements_by_xpath('//tbody/tr')
    photos = pytest.driver.find_elements_by_xpath('//tbody/tr/th[@scope="row"]/img')
    count = 0
    for i in range(len(pets)):
        if photos[i].get_attribute('src') != '':
            count += 1
    assert count >= (len(pets) // 2)


def test_all_pet_description():
    descriptions = pytest.driver.find_elements_by_xpath('//tbody/tr/td')
    for i in range(len(descriptions)):
        assert descriptions[i].text != ''


def test_different_names():
    names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
    for i in range(len(names)):
        name = names[i].text
        names_without_current = names.copy()
        names_without_current.pop(i)
        for name_without_current in names_without_current:
            assert name != name_without_current.text


def test_different_pets():
    pets = pytest.driver.find_elements_by_xpath('//tbody/tr')
    pets_list = []
    for i in range(len(pets)):
        name = pets[i].find_element_by_xpath('./td[1]')
        type = pets[i].find_element_by_xpath('./td[2]')
        age = pets[i].find_element_by_xpath('./td[3]')
        pet_list = [name.text, type.text, age.text]
        pets_list.append(pet_list)
    for j in range(len(pets_list)):
        pets_without_current = pets_list.copy()
        pets_without_current.pop(j)
        for pet_without_current in pets_without_current:
            assert pet_without_current[0] != pets_list[j][0]
            assert pet_without_current[1] != pets_list[j][1]
            assert pet_without_current[2] != pets_list[j][2]
