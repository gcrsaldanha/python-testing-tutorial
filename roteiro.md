# Desenvolvimento orientado à testes com Python e Django

Esse tutorial é baseado no livro [TDD com Python](https://amzn.to/2XM31f9) de Harry Percival, editora novatec.

# Configurando o ambiente

* Python3+
* Virtualenv
* Django
* Selenium
* Google Chrome + chromedriver
* Firefox + geckodriver


```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


# Escrevendo nosso primeiro teste

## Utilizando o Selenium

- [ ] TODO: Adicionar exemplo com Firefox
- [x] TODO: Adicionar exemplo com MacOS
    Para MacOS: basta instalar com `pip install chromedriver` e funciona normalmente.

```python
# Utilizando Google Chrome (chromedriver)
from selenium import webdriver

browser = webdriver.Chrome('venv/chromedriver-Windows')
browser.get('http://localhost:8000')
assert 'Django' in browser.title
```

Ao executar o arquivo, uma janela do Google Chrome deve abrir e exibir um erro após alguns segundos:

`Message: unknown error: net::ERR_CONNECTION_REFUSED`

O que faz sentido, pois nosso servidor **não está** rodando. Nosso teste falhou. Vamos corrigí-lo a seguir.

> Você pode se deparar com um `AssertionError`, o que é a mensagem ideal - não encontrou 'Django' no título da página. Curiosamente no MacOS esse foi o erro que apareceu para mim, enquanto no Windows o teste *quebrou* (ao invés de apenas falhar) ao não conseguir se conectar com o servidor na porta 8000.

Obs.: Caso o seu navegador não abra, verifique o console e tente identificar qual o problema. A seção a seguir ilustra alguns dos problemas que podem ser encontrados e como resolvê-los.

### Problemas com Selenium

Caso você não tenha problemas com o Selenium, pode pular essa seção.

- Verificar a versão do Chrome e fazer download do [respectivo chromedriver](https://sites.google.com/chromium.org/driver/downloads)
- Adicionar o binário do chromedriver dentro de `venv`
- Se ainda assim tiver problemas, verificar os passos a seguir:

Não encontrou `chromedriver` no `PATH`
```
Message: 'chromedriver-Windows' executable needs to be in PATH.
```

Não encontrou `chrome binary` instalado
```
Message: unknown error: cannot find Chrome binary
```

```python
# Caminho do bináriod o Google Chrome
options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
browser = webdriver.Chrome(
    executable_path='./venv/chromedriver.exe',  # Caminho do chromedriver
    options=options,
)
```

- [ ] COMMIT: Ambiente configurado e primeiro teste escrito.


## Rodando nosso servidor

Verifique que você está na raíz do projeto (`python-testing-tutorial/`) e execute no terminal:
```bash
django-admin startprojects listadetarefas
cd listadetarefas
python manage.py runserver
```

Em um outro terminal (verifique se seu ambiente virtual está ativado), execute o teste novamente:
```bash
python test.py

# Output:
DevTools listening on ws://127.0.0.1:62166/devtools/browser/9c6eeb65-afb9-4c87-ac01-2bb7866e1bb0
Traceback (most recent call last):
  File "C:\Users\gabri\Repositories\python-testing-tutorial\test.py", line 12, in <module>
    assert 'Django' in browser.title
AssertionError
```

Ao inspecionar a página, podemos ver que o título realmente não contém "Django":
> The install worked successfully! Congratulations!

Mas o `<header>` contém. Vamos alterar nosso teste:

```python
assert 'django' in browser.find_element_by_tag_name('header').text
```


# Configurando a suíte de testes

# unittest

Testes geralmente possuem três etapas:
1. Configuração (`setup`): onde configuramos o cenário para a execução do teste, no nosso caso, criamos uma instância do navegador. Em outros casos, poderíamos criar um arquivo de texto ou instâncias no banco de dados para o nosso caso de teste.
2. `Assertion`: execução de um trecho de código e verificar (`assert`) que o resultado é o esperado.
3. Finalização (`teardown/cleanup`): encerrar recursos, no nosso caso, encerrar a janela do Chrome. Poderia ser fechar um arquivo de texto e excluí-lo, ou resetar o banco de dados.

Não queremos fazer esses passos para todo caso de teste que escrevermos. Para resolver isso, vamos utilizar o módulo `unittest` do Python.

Nossos teste agora ficará assim:

```python
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


if __name__ == '__main__':
    unittest.main()
```

Agora para casa novo caso de teste, a gente só precisa escrever um novo método `test_meu_novo_caso`.

Com a nossa suíte de testes configurada, podemos finalmente começar a desenvolver, ou melhor, testar!


## Nosso primeiro teste funcional: acessando a página inicial

Toda aplicação, por mais simples que seja, tem o que chamamos de Histórias de Usuário (ou User Stories). Elas são uma maneira de descrever funcionalidades que o sistema deve possuir através de uma história com um usuário fictício. Por exemplo:

> Alice acessa a página inicial da Lista de Tarefas pela primeira vez. Ela é recebida com uma página contendo um cabeçalho "Lista de Tarefas", um campo textual para escrever a primeira tarefa e um botão de enviar ao lado. Ao escrever "Escrever um teste" e clicar no botão, Alice percebe que um novo item apareceu logo abaixo do campo textual, contendo a tarefa que ela escreveru.

Essa é uma história que descreve a **funcionalidade da nossa aplicação para um novo visitante**.

Mas o que isso tem a ver com testes, você pode se perguntar. *User Stories* são facilmente traduzidas em *testes funcionais*, como o nome já diz, testes que vão verificar que as funcionalidades da nossa aplicação estão funcionando como esperado.

Por exemplo:
>  Alice acessa a página inicial da Lista de Tarefas pela primeira vez. Ela é recebida com uma página contendo um cabeçalho "Lista de Tarefas"

Pode ser traduzido como:

```python
def test_novo_visitante(self):
    self.browser.get('http://localhost:8000')  # Acessa a página inicial da aplicação

    text_cabeçalho = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('Lista de Tarefas', text_cabeçalho)
```

Ao executar nosso arquivo de testes, devemos obter o seguinte `AssertionError`:

> AssertionError: 'Lista de Tarefas' not found in 'The install worked successfully! Congratulations!'

Muito bem, temos um **teste falhando**, agora podemos desenvolver parte da nossa aplicação para que esse teste passe! Por isso é chamado de desenvolvimento orientado a testes!


## Criando nossa aplicação

Primeiro, precisamos criar nossa aplicação:

```bash
python manage.py startapp listas
```

Com esse comando, o Django vai criar uma pasta `listas` dentro do nosso projeto (`listadetarefas`) contendo alguns arquivos: models, views, e... testes.

Ao contrário do nosso arquivo `test.py` que executamos manualmente (`python test.py`), o arquivo do Django é executando pelo próprio `test runner` do Django. Vamos verificar que ele realmente está sendo executado:

```python
from django.test import TestCase


class TestDummy(TestCase):
    def test_fails(self):
        self.assertEqual(1 + 1, 3)

    def test_passes(self):
        self.assertTrue(True)
```

Agora, para executar esse teste com o `test runner` do Django, basta executar

```bash
python manage.py test
```
! Observe que não executamos o nosso arquivo diretamente, mas sim o script `test` através do módulo `manage.py` do Django.

Um teste deve passar e outro deve falhar:
> AssertionError: 2 != 3.

Ótimo, o test runner do Django está funcionando como esperado!


## Criando nossa página inicial

### Revisão Django

MVC: Model - View - Controller vs MVT: Model - View - Template

Arquitetura básica de Request/Response do Django:
* Request chega em uma determinada url: `http://localhost:8000/` (raíz)
* É resolvida para `view` que está associada à essa URL (`/`) (geralmente uma função)
* `view` retorna uma `Response`

Assim, precisamos verificar 2 coisas (testes):
1. Acessar a URL `/` envia o `request` para a view correta (página inicial).
2. A `view` executada retorna a página inicial (HTML) esperada.


```python
# tests.py
class PaginaInicialTest(TestCase):
    def test_root_url_resolve_para_home_page_view(self):
        view = resolve('/')

        self.assertEqual(view.func, home_page)
```
> ImportError: cannot import name 'home_page' from 'listas.views' (C:\Users\gabri\Repositories\python-testing-tutorial\listadetarefas\listas\views.py)

```python
# views.py
home_page = None
```
> django.urls.exceptions.Resolver404: {'tried': [[<URLResolver <URLPattern list> (admin:admin) 'admin/'>]], 'path': ''}

```python
from listas.views import home_page

urlpatterns = [
    path('', home_page),
]
```
> TypeError: view must be a callable or a list/tuple in the case of include().

> P.S.: Ao executar a primeira vez com `path('/', home_page)`, eu recebi o seguinte erro: `(urls.W002) Your URL pattern '/' has a route beginning with a '/'. Remove this slash as it is unnecessary.`.
Trocar `'/'` por `''` resolveu a warning e o teste passou (view foi resolvida).

## (WIP) Teste unitário vs Teste funcional

Até o momento estávamos pensando em testes funcionais: que verificam que determinada funcionalidade da aplicação está se comportando como esperado, **do ponto de vista do usuário**.

Também existe o que chamamos de **testes unitários** (*unit tests*): eles testam que a **lógica interna da aplicação** funciona como esperado.

Nem sempre a linha entre esses dois conceitos é muito clara, mas em linhas gerais:
* Testes funcionais são mais abrangentes, testam funcionalidades da perspectiva do usuário.
* Testes unitários são mais específicos, testam componenentes individuais da perspectiva do próprio código.
* Caixa fechada vs caixa aberta


- [ ] Unit tests vs functional tests