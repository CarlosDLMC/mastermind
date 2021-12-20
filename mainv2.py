from browsermobproxy import Server
import undetected_chromedriver.v2 as uc
from time import sleep
from pprint import pprint
import sys

class ProxyManager:

    __BMP = "/home/mentefria/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy"

    def __init__(self):
        self.__server = Server(self.__BMP)
        self.__client = None

    def start_server(self):
        self.__server.start()
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(params={"trusAllServers": "true"})
        return  self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server

user = "giordano.calderon@hotmail.com"
password = "IA6AdJCgQ5nwKYJBAH2J"



class Courses():
    def __init__(self):
        self.proxy = ProxyManager()
        self.server = self.proxy.start_server()
        self.client = self.proxy.start_client()
        # self.client.new_har("mastermind.ac")
        options = uc.ChromeOptions()
        options.add_argument(f"--proxy-server={self.client.proxy}")
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = uc.Chrome(options=options)

    def start(self, login_url):
        self.driver.get(login_url)

    def login(self):
        input("Pulsa enter cuando pase la validación...")
        inicio_data = self.driver.find_element_by_xpath('//*[@id="user[email]"]')
        inicio_data.send_keys(user)
        password_data = self.driver.find_element_by_xpath('//*[@id="user[password]"]')
        password_data.send_keys(password)
        inicio_btn = self.driver.find_element_by_xpath("/html/body/main/div/div/article/form/div[4]/input")
        inicio_btn.click()
        input("Pulsa cuando hayas metido todos los captcha...")

    def get_link(self, requests):
        requests = requests['log']['entries']
        lista = list(filter(lambda x: x['request']['url'][-8:] == '.m3u8/v2', requests))
        s = {x['request']['url'] for x in lista}
        print("len(s) =", len(s))
        return "" if not s else next(iter(s))

    def get_requests(self):
        enlace = self.get_link(self.client.har)
        print(enlace)
        with open("enlaces.txt", "a") as file:
            print(enlace, file=file)
        return enlace

    def next_video(self):
        try:
            continuar = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[1]/div/main/section/div/div[2]/div/footer/div[2]/button/div/div/span")
        except:
            try:
                continuar = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[1]/div/main/section/div/div[2]/div/footer/button/div/div/span")
            except:
                print("Botón no encontrado")
                return
        continuar.click()

    def download(self, url):
        self.client.new_har("mastermind.ac")
        self.driver.get(url)
        sleep(3)
        primer_enlace = self.get_requests()
        otro_enlace = ""
        while otro_enlace != primer_enlace:
            self.client.new_har("mastermind.ac")
            self.next_video()
            sleep(3)
            otro_enlace = self.get_requests()

url = input("introduce la url de la primera clase del curso: ")
# n_videos = int(input("Introduce el número de clases que tiene el curso: "))
courses = Courses()
courses.start("https://www.mastermind.ac/users/sign_in")
courses.login()
courses.download(url)
