import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.CLASS_NAME, 'button.round')
    comford_button = (By.CLASS_NAME, 'tcard.active')
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
    close_frame_form = (By.CLASS_NAME, "close-button.section-close")


    #Driver elements
    driver_msg_field = (By.ID,'comment')


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

    def click_pedir_taxi(self):
        self.driver.find_element(*self.taxi_button).click()

    def click_comford_button(self):
        self.driver.find_element(*self.comford_button).click()

    def set_route(self, from_address, to_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_phone_number(self, number):
        WebDriverWait(self.driver, 15)

        self.driver.find_element(*self.phone_button).click()
        self.driver.find_element(*self.phone_field).send_keys(number)
        self.driver.find_element(*self.phone_button_form).click()
        WebDriverWait(self.driver, 100)
        confirm_code = retrieve_phone_code(self.driver)
        WebDriverWait(self.driver, 60)

        self.driver.find_element(*self.code_field).send_keys( confirm_code)
        self.driver.find_element(*self.button_code_confirm).click()

        WebDriverWait(self.driver, 100)

    def payment_method(self ):
        self.driver.find_element(*self.payment_button).click()
        WebDriverWait(self.driver, 500)

        self.driver.find_element(*self.add_card).click()



        self.driver.find_element(*self.input_card).send_keys(data.card_number)
        WebDriverWait(self.driver, 1000)

        self.driver.find_element(*self.input_card).send_keys(Keys.TAB)

        self.driver.find_element(*self.input_card_code).send_keys(data.card_code)
        WebDriverWait(self.driver, 9000)



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        routes_page.click_pedir_taxi()
        routes_page.click_comford_button()

        #phone field
        routes_page.set_phone_number(data.phone_number)


        assert routes_page.get_phone_number() == data.phone_number

        routes_page.payment_method()
        #assert routes_page.get_phone_number() == data.phone_number


    #def test_taxi_button(self):
    #    self.driver.get(data.urban_routes_url)
    #    routes_page = UrbanRoutesPage(self.driver)



    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
