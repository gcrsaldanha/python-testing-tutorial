# Desenvolvimento orientado à testes com Python e Django

Esse tutorial é baseado no livro [TDD com Python](https://amzn.to/2XM31f9) de Harry Percival, editora novatec.

## Configurando o ambiente

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


## Escrevendo nosso primeiro teste

- [ ] TODO: Adicionar exemplo com Firefox

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


### Rodando nosso servidor

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


## Configurando a suíte de testes
