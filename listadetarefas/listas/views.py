from django.http.response import HttpResponse
from django.shortcuts import render

def home_page(request):
    return HttpResponse('''
    <html>
        <title>Lista de Tarefas</title>
        <h1>Lista de Tarefas</h1>
    </html>
    ''')