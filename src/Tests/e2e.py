from selenium import webdriver

MIN_VALUE = 1
MAX_VALUE = 1000
EXIT_SUCCESS = 0
EXIT_FAIL = -1
DRIVER_PATH = 'C:/Temp/chromedriver.exe'
SUCESS_MSG = 'Congrats!'

def test_score_service(url):
    global MIN_VALUE,MAX_VALUE,DRIVER_PATH
    chrome_driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    chrome_driver.get(url)
    elem = chrome_driver.find_element_by_id("score")

    try:
        score = int(elem.text)
        result = (MIN_VALUE <= score and score <= MAX_VALUE)
    except ValueError:
        result = false

    chrome_driver.close()
    return result

def main_function(url):
    global EXIT_SUCCESS,EXIT_FAIL

    if test_score_service(url):
        return EXIT_SUCCESS
    else:
        return EXIT_FAIL

def test_guessgame(url):
    return test_game(url, "choise", '1')

def test_memorygame(url):
    return test_game(url, "numbers", '82,25')

def test_currency_rollete(url):
    return test_game(url, "shekels", '100')

def test_game(url, textbox_id, keys_to_send):
    chrome_driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    chrome_driver.get(url)
    chrome_driver.find_element_by_id(textbox_id).send_keys(keys_to_send)
    chrome_driver.find_element_by_id("btn_play").click()
    result = test_answer(chrome_driver.current_url)
    chrome_driver.close()
    return result

def test_answer(url):
    global DRIVER_PATH,EXIT_SUCCESS,EXIT_FAIL
    answer_driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    answer_driver.get(url)
    elem = chrome_driver.find_element_by_id("answer")
    if SUCESS_MSG in elem.text:
        result = EXIT_SUCCESS
    else:
        result = EXIT_FAIL
    answer_driver.close()
    return result