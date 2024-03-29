from django.urls import resolve
from django.test import TestCase  # TestCase do Django é um TestCase com mais funcionalidades.
from django.http import HttpRequest, HttpResponse

from listas.views import home_page


# Precisamos incluir "Test" no nome de nossa classe, seja no início ou no fim
# Caso contrário, essa classe pode não ser encontrada pelo test runner
class PaginaInicialTest(TestCase):
    def test_root_url_resolve_para_home_page_view(self):
        view = resolve('/')

        self.assertEqual(view.func, home_page)

    def test_home_page_view_retorna_html_correto(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Lista de Tarefas</title>', html)
        self.assertIn('<h1>Lista de Tarefas</h1>', html)
