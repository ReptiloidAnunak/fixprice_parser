import silly
from selenium.webdriver.common.proxy import ProxyType
from sqlalchemy import Column, Integer, String, Boolean
from data_base.db.db_init import Base


class Proxy(Base):
    __tablename__ = 'proxy'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    ip = Column(String, nullable=False, unique=True)
    port_http = Column(String, nullable=False)
    port_socks5 = Column(String, nullable=False)
    ip_port_arg = Column(String, nullable=False)
    country = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    source = Column(String, nullable=False)
    is_valid = Column(Boolean, default=False)

    def __init__(self, title, ip,
                 port_http, port_socks5,
                 username, password,
                 country, source,):

        self.title = title
        self.ip = ip
        self.port_http = port_http
        self.port_socks5 = port_socks5
        self.ip_port_arg = self._set_ip_port_arg()
        self.username = username
        self.password = password
        self.country = country
        self.source = source

    def __str__(self):
        return f'PROXY :: {self.__dict__}'

    def generate_ip_port_arg(self):
        return f"{self.username}:{self.password}@{self.ip}:{self.port_http}"

    def _set_ip_port_arg(self):
        return f"{self.ip}:{self.port_http}"

    def generate_requests_dict(self):
        http_proxy = f"http://{self.username}:{self.password}@{self.ip}:{self.port_http}"
        socks5_proxy = f"socks5://{self.username}:{self.password}@{self.ip}:{self.port_socks5}"
        return {
            'http': http_proxy,
            'https': http_proxy,
            'socks5': socks5_proxy
        }

    def generate_chrome_proxy_arg(self):
        proxy_server_arg = f'--proxy-server={self.ip}:{self.port_http}'
        return proxy_server_arg

    def generate_firefox_proxy_arg(self):
        options = {
            'proxy': {
                self.generate_ip_port_arg(),
            }
        }
        return options
