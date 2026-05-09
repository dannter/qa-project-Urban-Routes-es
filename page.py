import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from helpers import Helpers


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.CLASS_NAME, 'button.round')
    comford_button = (By.XPATH, "//img[@alt='Comfort']")
    phone_button = (By.CLASS_NAME, 'np-button')
    phone_field = (By.NAME, 'phone')
    phone_button_form = (By.CLASS_NAME, 'button.full')
    code_field = (By.ID, 'code')
    button_code_confirm =(By.XPATH, "//button[text()='Confirmar']")
    phone_final_text = (By.CLASS_NAME, "np-text")

    #payment method elements
    payment_button = (By.CLASS_NAME, 'pp-button.filled')
    add_card = (By.CLASS_NAME, 'pp-plus')
    input_card = (By.CLASS_NAME,'card-input')
    input_card_code = (By.XPATH, "//input[@id='code']")
    button_add_card = (By.XPATH, "//button[text()='Agregar']")
    close_frame_form = (By.CSS_SELECTOR, "button.close-button.section-close")



    manta_panuelos_toggle = (By.XPATH, '(//span[@class="slider round"])[1]')

    icecream_activate_options = (By.CLASS_NAME,"reqs")
    icecream_value = ( By.XPATH,
        "//div[@class='r-group'][.//div[normalize-space()='Cubeta de helado']]//div[contains(@class,'counter-value')][1]"
    )

    icecream_plus_button = (
        By.XPATH,
        "//div[@class='r-counter-label' and normalize-space()='Helado']/ancestor::div[contains(@class,'r-counter-container')]//div[contains(@class,'counter-plus')]"
    )

    close_button = (
        By.CSS_SELECTOR,
        ".payment-picker .section.active button.section-close"
    )

    #Driver elements
    driver_msg_field = (By.ID,'comment')

    wait_driver_button = (By.CLASS_NAME,'smart-button' )
    wait_driver_modal = (By.CSS_SELECTOR, ".order-header-title")


    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_final_text).text

    def get_driver_msg_field(self):
        return self.driver.find_element(*self.driver_msg_field).text

    def get_icecrem_value(self):
        return self.driver.find_element(*self.icecream_value).text

    def click_pedir_taxi(self):
        self.driver.find_element(*self.taxi_button).click()

    def click_comford_button(self):
        WebDriverWait(self.driver, 5000)
        self.driver.find_element(*self.comford_button).click()
        return True

    def set_route(self, from_address, to_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_phone_number(self, number):
        WebDriverWait(self.driver, 15)

        self.driver.find_element(*self.phone_button).click()
        self.driver.find_element(*self.phone_field).send_keys(number)
        self.driver.find_element(*self.phone_button_form).click()
        WebDriverWait(self.driver, 100)
        
        confirm_code = Helpers.retrieve_phone_code(self.driver)
        WebDriverWait(self.driver, 60)

        self.driver.find_element(*self.code_field).send_keys( confirm_code)
        self.driver.find_element(*self.button_code_confirm).click()

        WebDriverWait(self.driver, 100)

    def payment_method(self ):
        self.driver.find_element(*self.payment_button).click()
        WebDriverWait(self.driver, 500)

        self.driver.find_element(*self.add_card).click()

        self.driver.find_element(*self.input_card).send_keys(data.card_number+Keys.TAB+data.card_code+Keys.TAB)
        WebDriverWait(self.driver, 500)

        self.driver.find_element(*self.button_add_card).click()
        WebDriverWait(self.driver, 500)

        self.driver.find_element(*self.close_button).click()
        return True

    def write_driver_message(self):
        self.driver.find_element(*self.driver_msg_field).send_keys("Hola")

    def ask_manta_panuelos(self):
        self.driver.find_element(*self.manta_panuelos_toggle).click()
        WebDriverWait(self.driver, 9000)
        return True
        
    def ask_icecream(self):
        self.driver.find_element(*self.icecream_activate_options).click()
        WebDriverWait(self.driver, 4000)

        self.driver.find_element(*self.icecream_plus_button).click()
        WebDriverWait(self.driver, 1000)
        self.driver.find_element(*self.icecream_plus_button).click()

    def click_find_taxi(self):
        self.driver.find_element(*self.wait_driver_button).click()
        WebDriverWait(self.driver, 4000)
        return True

    def wait_driver(self):
        wait = WebDriverWait(self.driver, 80)

        show_modal = wait.until(
            lambda d: (
                          el := self.driver.find_element(*self.wait_driver_modal)
                      ) and el.text.lower().startswith("el conductor") and el
            )
        return show_modal
