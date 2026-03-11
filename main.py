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


    manta_panuelos_toggle = (By.XPATH, "//div[text()='Manta y pañuelos']/following::input[@type='checkbox'][1]")

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

    def ask_icecream(self):
        self.driver.find_element(*self.icecream_activate_options).click()

        WebDriverWait(self.driver, 9000)

        self.driver.find_element(*self.icecream_plus_button).click()
        WebDriverWait(self.driver, 1000)
        self.driver.find_element(*self.icecream_plus_button).click()


    def wait_driver(self):
        self.driver.find_element(*self.wait_driver_button).click()

        wait = WebDriverWait(self.driver, 80)

        show_modal = wait.until(
            lambda d: (
                          el := self.driver.find_element(*self.wait_driver_modal)
                      ) and el.text.lower().startswith("el conductor") and el
            )
        return show_modal

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

        #test phone process
        routes_page.set_phone_number(data.phone_number)
        assert routes_page.get_phone_number() == data.phone_number

        #test payment process
        complete = routes_page.payment_method()
        assert complete

        #test text driver message
        routes_page.write_driver_message()
        assert routes_page.get_driver_msg_field() is not None

        #test ice cream
        routes_page.ask_icecream()
        assert  routes_page.get_icecrem_value() == '2'


        #wait driver
        assert routes_page.wait_driver() is not None


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
