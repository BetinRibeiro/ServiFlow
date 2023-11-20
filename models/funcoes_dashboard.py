# -*- coding: utf-8 -*-
def calcular_soma_valor_total(id_empresa, tipo, liquidado=False):
    # Obtém os registros da tabela registro_financeiro de acordo com os parâmetros
    query = (db.registro_financeiro.empresa == id_empresa) & \
            (db.registro_financeiro.tipo == tipo) & \
            (db.registro_financeiro.liquidado == liquidado)
    
    # Calcula a soma dos valores totais
    soma_valores = db(query).select(db.registro_financeiro.valor_total.sum()).first()[db.registro_financeiro.valor_total.sum()]
    
    return soma_valores or 0  # Retorna a soma total ou 0 se não houver registros


from datetime import datetime, timedelta
import calendar

def calcular_mes_referencia(meses):
    """
    Calcula o mês de referência com base no número de meses fornecido.

    Parâmetros:
    meses (int): O número de meses a serem deslocados. Positivo para meses no futuro, negativo para meses no passado.

    Retorna:
    tuple: Uma tupla contendo duas datas - a primeira data do mês de referência e a última data do mês de referência.

    A função utiliza a biblioteca `datetime` para manipular datas e a função `calendar.monthrange()`
    para obter o último dia do mês de referência. O parâmetro `meses` define o deslocamento
    em relação ao mês atual.

    Exemplo de uso:
    >>> calcular_mes_referencia(2)
    (datetime.date(2023, 11, 1), datetime.date(2023, 11, 30))
    >>> calcular_mes_referencia(-1)
    (datetime.date(2023, 8, 1), datetime.date(2023, 8, 31))
    """
    # Obtém a data atual
    data_atual = datetime.now()
    
    # Calcula o mês de referência
    mes_referencia = data_atual + timedelta(days=30 * meses)
    
    # Define o primeiro dia do mês de referência
    primeiro_dia = mes_referencia.replace(day=1)
    
    # Obtém o último dia do mês de referência
    ultimo_dia = datetime(
        mes_referencia.year,
        mes_referencia.month,
        calendar.monthrange(mes_referencia.year, mes_referencia.month)[1]
    )
    
    return primeiro_dia, ultimo_dia

def calcular_soma_registros_periodo(id_empresa, meses, tipo, liquidado=True):
    # Calcula o mês de referência com base no número de meses fornecido
    primeiro_dia, ultimo_dia = calcular_mes_referencia(meses)
    
    # Obtém os registros da tabela registro_financeiro dentro do período e com os critérios fornecidos
    query = (db.registro_financeiro.empresa == id_empresa) & \
            (db.registro_financeiro.tipo == tipo) & \
            (db.registro_financeiro.liquidado == liquidado) & \
            (db.registro_financeiro.data_operacao >= primeiro_dia) & \
            (db.registro_financeiro.data_operacao <= ultimo_dia)
    
    # Calcula a soma dos valores totais dentro do período
    soma_valores = db(query).select(db.registro_financeiro.valor_total.sum()).first()[db.registro_financeiro.valor_total.sum()]
    
    return soma_valores or 0  # Retorna a soma total ou 0 se não houver registros dentro do período


def media_faturamento_por_dia(id_empresa, tipo, meses):
    # Calcula a soma total dos registros para o período de meses
    total_faturado = calcular_soma_registros_periodo(id_empresa, meses, tipo)
    
    # Calcula a média de faturamento por dia
    _, ultimo_dia = calcular_mes_referencia(0)  # Obtém o último dia do mês atual
    dias_no_mes_atual = ultimo_dia.day  # Obtém a quantidade de dias no mês atual

    # Verifica se estamos considerando um mês anterior ao mês atual
    if meses < 0:
        _, ultimo_dia_mes_passado = calcular_mes_referencia(meses)  # Obtém o último dia do mês passado
        dias_no_mes_passado = ultimo_dia_mes_passado.day  # Obtém a quantidade de dias no mês passado
        # Retorna a média de faturamento por dia para o mês passado
        return total_faturado / dias_no_mes_passado if dias_no_mes_passado > 0 else 0
    else:
        dias_no_mes_atual = datetime.now().day
    
    # Retorna a média de faturamento por dia para o mês atual
    return total_faturado / dias_no_mes_atual if dias_no_mes_atual > 0 else 0
