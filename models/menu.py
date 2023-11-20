# -*- coding: utf-8 -*-

if auth.user:
    
    response.menu = [
        (T('Empresa'), False, URL('acs_empresa', 'index'), []),
        (T('Usuarios'), False, URL('acs_usuario', 'index'), []),
        (T('Serviços'), False, URL('acs_servico', 'index'), []),
        (T('Clientes'), False, URL('acs_cliente', 'index'), []),
        (T('Registros'), False, URL('acs_registro', 'index'), [])
    ]
else:
    response.menu = [
        (T('Home'), False, URL('default', 'index'), [])
    ]


def dinheiro(numero):
    """
    Formata um número como uma string no formato de moeda (Real brasileiro).

    Esta função recebe um número e o formata como uma string no formato de moeda,
    com o símbolo "R$" e duas casas decimais separadas por vírgula.

    Args:
        numero (float): O número a ser formatado como moeda.

    Returns:
        str: A representação formatada do número como moeda (ou "0" se a conversão falhar).
    """
    try:
        numero = float(numero)
        retorno = "R$ {:,.2f}".format(round(numero, 2)).replace(",", "#").replace(".", ",").replace("#", ".")
    except:
        retorno = "0"
    return retorno
