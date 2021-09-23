import unittest  # Faz parte da biblioteca padrão do Python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Test(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
        self.browser = webdriver.Chrome(
            executable_path='./venv/chromedriver.exe',
            options=options,
        )

    def tearDown(self):
      self.browser.quit()

    def test_case(self):
        self.browser.get('http://localhost:8000')
        header_text = self.browser.find_element_by_tag_name('header').text
        self.assertIn('django', header_text)
        # equivalente a assert 'django' in header_text
        # unittest fornece alguns métodos como asssertIn, assertTrue, assertFalse

    def test_novo_visitante(self):
        self.browser.get('http://localhost:8000')  # Acessa a página inicial da aplicação

        text_cabeçalho = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Lista de Tarefas', text_cabeçalho)


if __name__ == '__main__':
    unittest.main()