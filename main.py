import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from page import UrbanRoutesPage

class TestUrbanRoutes:

    driver = None
    routes_page = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado
        # para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.driver.get(data.urban_routes_url)

    
    def get_page(self):
        return UrbanRoutesPage(self.driver)
    
    #Tarea 1
    def test_set_route(self):
        page = self.get_page()
        address_from = data.address_from
        address_to = data.address_to
        page.set_route(address_from, address_to)
        assert page.get_from() == address_from
        assert page.get_to() == address_to


    #Tarea 2
    def test_comford_button(self):
        page = self.get_page()
        page.click_pedir_taxi()
        assert page.click_comford_button() is not None


    #Tarea 3
    def test_set_phone(self):
        #test phone process
        page = self.get_page()
        page.set_phone_number(data.phone_number)
        assert page.get_phone_number() == data.phone_number

    #Tarea 4 
    def test_set_credit_card(self):
        #test payment process
        page = self.get_page()
        complete = page.payment_method()
        assert complete

    #Tarea 5
    def test_write_driver_msg(self):
        #test text driver message
        page = self.get_page()
        page.write_driver_message()
        assert page.get_driver_msg_field() is not None

    #Tarea 6 
    def test_ask_panuelo_manta(self):
        page = self.get_page()
        assert page.ask_manta_panuelos() 

    #Tarea 7
    def test_ask_ice_cream(self):
        #test ice cream
        page = self.get_page()
        page.ask_icecream()
        assert  page.get_icecrem_value() == '2'

    #Tarea 8
    def test_find_taxi(self):
        #find driver
        page = self.get_page()
        assert page.click_find_taxi()
    
    #Tarea 9
    def test_wait_driver(self):
        #wait driver
        page = self.get_page()
        assert page.wait_driver()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()


# def main():
#     print('asdasdads')
#     test = TestUrbanRoutes()
#     test.setup_class()
#     test.test_set_route()


#main()
     