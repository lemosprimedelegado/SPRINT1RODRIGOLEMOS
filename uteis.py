# Função para calcular a idade do artista
import datetime


def calcular_idade(data_nascimento):
    hoje = datetime.now()
    dia, mes, ano = map(int, data_nascimento.split('/'))
    idade = hoje.year - ano
    if (hoje.month, hoje.day) < (mes, dia):
        idade -= 1
    return idade
