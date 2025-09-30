"""
GERADOR DE DADOS SINTÉTICOS PARA E-COMMERCE
Descrição: Script Python para gerar dados realistas no banco MySQL
"""


import mysql.connector
import random
from datetime import datetime, timedelta
from faker import Faker
import re
import unicodedata

# Configuração da conexão
conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1720",
    database="ecommerce_db"
)

cursor = conexao.cursor()
fake = Faker('pt_BR')

# Configurações
NUM_CLIENTES = 1400
DATA_INICIO = datetime(2022, 1, 1)
DATA_FIM = datetime(2025, 9, 19)

# --- Funções auxiliares ---

def remover_acentos(texto):
    """Remove acentos do texto"""
    return ''.join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn')

def remover_titulos(nome):
    """
    Remove títulos/honoríficos comuns dos nomes gerados pelo Faker.
    Ex.: 'Dr. João Silva' -> 'João Silva', 'Sra. Maria' -> 'Maria'
    """
    if not nome:
        return nome
    # Remove títulos comuns (com ou sem ponto, com ou sem vírgula), case-insensitive
    cleaned = re.sub(r'(?i)\b(?:sr|sra|senhor|senhora|dr|dra|doutor|doutora|profa|prof|professor|professora)\.?,?\s*', '', nome)
    # Colapsa espaços duplos e remove espaços extras
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Remove vírgulas ou pontos residuais no início/fim
    cleaned = cleaned.strip('., ')
    return cleaned


def gerar_email_do_nome(nome):
    """Gera um e-mail realista baseado no nome da pessoa"""
    nome_sem_acentos = remover_acentos(nome).lower()
    partes = nome_sem_acentos.split()

    if len(partes) >= 2:
        padroes_email = [
            f"{partes[0]}.{partes[-1]}",
            f"{partes[0][0]}{partes[-1]}",
            f"{partes[0]}_{partes[-1]}",
            f"{partes[0]}{partes[-1]}",
            f"{partes[0][0]}.{partes[-1]}",
            f"{partes[-1]}.{partes[0]}",
            f"{partes[0]}{random.randint(1, 99)}"
        ]
        email_user = random.choice(padroes_email)
        dominios = [
            'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com',
            'bol.com.br', 'uol.com.br', 'ig.com.br', 'terra.com.br',
            'globo.com', 'r7.com', 'live.com', 'icloud.com'
        ]
        return f"{email_user}@{random.choice(dominios)}"

    return fake.unique.email()

def gerar_cpf():
    cpf = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        val = sum((cpf[i] * (10 - i) for i in range(9))) % 11
        cpf.append(11 - val if val > 1 else 0)
    return ''.join(map(str, cpf))

def gerar_cnpj():
    cnpj = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
    for _ in range(2):
        val = sum((cnpj[i] * (6 - (i % 8)) for i in range(12))) % 11
        cnpj.append(11 - val if val > 1 else 0)
    return ''.join(map(str, cnpj))

# Lista abrangente de DDDs do Brasil para diversificar os telefones
DDD_LIST = [
    '11','12','13','14','15','16','17','18','19',
    '21','22','24','27','28',
    '31','32','33','34','35','37','38',
    '41','42','43','44','45','46',
    '47','48','49',
    '51','53','54','55',
    '61','62','64','63','65','66','67','68','69',
    '71','73','74','75','77','79',
    '81','82','83','84','85','86','87','88','89',
    '91','92','93','94','95','96','97','98','99'
]

def gerar_telefone():
    tipos = ['CELULAR', 'COMERCIAL', 'RESIDENCIAL']
    tipo = random.choice(tipos)
    ddd = random.choice(DDD_LIST)

    if tipo == 'CELULAR':
        # Celular no formato 9 + 8 dígitos (ex.: 9XXXXXXXX)
        numero = f'9{random.randint(10000000, 99999999)}'
    else:
        # Telefones fixos/comerciais com 8 dígitos (começando de 2 a 9 normalmente)
        numero = f'{random.randint(20000000, 99999999)}'

    return tipo, f'{ddd}{numero}'

def gerar_data_aleatoria(data_inicio, data_fim):
    delta = data_fim - data_inicio
    random_days = random.randint(0, delta.days)
    return data_inicio + timedelta(days=random_days)

def gerar_comentario_avaliacao(produto_id, nota):
    """Gera comentários dinâmicos e variados em português baseados no produto e nota"""
    cursor.execute("SELECT NOME_PRODUTO, ID_CATEGORIA FROM PRODUTOS WHERE IDPRODUTO = %s", (produto_id,))
    produto_info = cursor.fetchone()

    if produto_info:
        nome_produto, id_categoria = produto_info
        cursor.execute("SELECT NOME_CATEGORIA FROM CATEGORIAS WHERE IDCATEGORIA = %s", (id_categoria,))
        categoria = cursor.fetchone()
        categoria_nome = categoria[0] if categoria else "produto"

        comentarios_positivos = [
            f"Excelente {nome_produto}! Superou todas as expectativas.",
            f"Qualidade impressionante deste {nome_produto}, recomendo muito.",
            f"Produto incrível! O {nome_produto} atende perfeitamente às minhas necessidades.",
            f"Adorei o {nome_produto}! Entrega rápida e produto em perfeito estado."
        ]

        comentarios_neutros = [
            f"O {nome_produto} é bom, mas poderia ser melhor.",
            f"Produto satisfatório, o {nome_produto} atende às necessidades básicas."
        ]

        comentarios_negativos = [
            f"Decepcionado com o {nome_produto}, qualidade inferior ao esperado.",
            f"O {nome_produto} não atendeu às expectativas, muito frágil."
        ]

        if nota >= 4:
            return random.choice(comentarios_positivos)
        elif nota == 3:
            return random.choice(comentarios_neutros)
        else:
            return random.choice(comentarios_negativos)
    else:
        comentarios_genericos = [
            "Produto excelente, superou minhas expectativas!",
            "Qualidade impressionante, recomendo muito.",
            "Entrega rápida e produto em perfeito estado."
        ]
        return random.choice(comentarios_genericos)

# Buscar dados existentes
def buscar_dados_existentes():
    cursor.execute("SELECT IDPRODUTO, PRECO_UNITARIO FROM PRODUTOS")
    produtos = cursor.fetchall()

    cursor.execute("SELECT IDCATEGORIA FROM CATEGORIAS")
    categorias = [cat[0] for cat in cursor.fetchall()]

    cursor.execute("SELECT IDFORNECEDOR FROM FORNECEDORES")
    fornecedores = [forn[0] for forn in cursor.fetchall()]

    return produtos, categorias, fornecedores

produtos, categorias, fornecedores = buscar_dados_existentes()

print("Iniciando geração de dados...")

# Gerar clientes
clientes_gerados = []
emails_utilizados = set()

for i in range(NUM_CLIENTES):
    try:
        # 85% pessoa física, 15% pessoa jurídica
        tipo = random.choices(
            ['PESSOA_FÍSICA', 'PESSOA_JURIDICA'],
            weights=[85, 15]
        )[0]

        data_cadastro = gerar_data_aleatoria(DATA_INICIO, DATA_FIM)

        if tipo == 'PESSOA_FÍSICA':
            nome = fake.name()  
            # Remover possíveis títulos/honoríficos
            nome = remover_titulos(nome)

            cpf = gerar_cpf()
            cnpj = None
            razao_social = None

            # Gerar e-mail baseado no nome
            email = gerar_email_do_nome(nome)
            # Garantir e-mail único
            while email in emails_utilizados:
                email = gerar_email_do_nome(nome)
            emails_utilizados.add(email)

        else:
            # Para pessoa jurídica
            razao_social = fake.company()
            nome = fake.name()  
            # Remover possíveis títulos/honoríficos do nome do representante
            nome = remover_titulos(nome)
]

            cpf = None
            cnpj = gerar_cnpj()

            # Gerar e-mail corporativo baseado na razão social
            nome_sem_acentos = remover_acentos(razao_social).lower()
            partes = nome_sem_acentos.replace(' ', '').replace(',', '').replace('.', '').split()
            if partes:
                email_base = partes[0]
                email = f"contato@{email_base}.com.br"
                # Garantir e-mail único
                while email in emails_utilizados:
                    email = f"{email_base}{random.randint(1, 99)}@empresa.com.br"
                emails_utilizados.add(email)
            else:
                email = fake.unique.email()

        cursor.execute(
            "INSERT INTO CLIENTES (NOME, EMAIL, TIPO, CPF, CNPJ, RAZAO_SOCIAL, DATA_CADASTRO) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nome, email, tipo, cpf, cnpj, razao_social, data_cadastro)
        )
        conexao.commit()

        cliente_id = cursor.lastrowid
        clientes_gerados.append(cliente_id)

        # Gerar telefones (1-3 por cliente)
        num_telefones = random.randint(1, 3)
        for _ in range(num_telefones):
            tipo_tel, numero_tel = gerar_telefone()
            cursor.execute(
                "INSERT INTO TELEFONES (ID_CLIENTE, TIPO, NUMERO) VALUES (%s, %s, %s)",
                (cliente_id, tipo_tel, numero_tel)
            )

        # Gerar endereços (1-2 por cliente)
        num_enderecos = random.randint(1, 2)
        for j in range(num_enderecos):
            tipo_end = random.choice(['RESIDENCIAL', 'COMERCIAL'])

            # Gerar complemento de forma mais simples
            complemento = None
            if random.random() > 0.7:
                complemento_options = ['Apto', 'Casa', 'Sala', 'Bloco', 'Lote']
                complemento = f"{random.choice(complemento_options)} {random.randint(1, 999)}"

            cursor.execute(
                """INSERT INTO ENDERECOS (ID_CLIENTE, TIPO, LOGRADOURO, NUMERO, COMPLEMENTO, BAIRRO, CIDADE, ESTADO, CEP)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (cliente_id, tipo_end, fake.street_name(), str(random.randint(1, 9999)),
                 complemento,
                 fake.bairro(), fake.city(), fake.estado_sigla(), fake.postcode().replace('-', ''))
            )

        if (i + 1) % 100 == 0:
            print(f"Clientes gerados: {i + 1}/{NUM_CLIENTES}")
            conexao.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao gerar cliente {i}: {err}")
        conexao.rollback()

print("Clientes, telefones e endereços gerados com sucesso!")

# Gerar pedidos, pagamentos, entregas, itens e avaliações
for i, cliente_id in enumerate(clientes_gerados):
    try:
        # 70% dos clientes fazem pelo menos 1 pedido
        if random.random() > 0.3:
            num_pedidos = random.randint(1, 5) if random.random() > 0.8 else 1

            for _ in range(num_pedidos):
                # Buscar endereços do cliente
                cursor.execute("SELECT IDENDERECO FROM ENDERECOS WHERE ID_CLIENTE = %s", (cliente_id,))
                enderecos_cliente = [end[0] for end in cursor.fetchall()]

                data_pedido = gerar_data_aleatoria(DATA_INICIO, DATA_FIM)
                status_pedido = random.choices(
                    ['PENDENTE', 'PAGO', 'CANCELADO'],
                    weights=[0.1, 0.8, 0.1]
                )[0]

                # Inserir pedido
                cursor.execute(
                    "INSERT INTO PEDIDOS (ID_CLIENTE, VALOR_TOTAL, DATA_PEDIDO, STATUS) VALUES (%s, %s, %s, %s)",
                    (cliente_id, 0, data_pedido, status_pedido)
                )
                pedido_id = cursor.lastrowid

                valor_total = 0
                num_itens = random.randint(1, 4)
                produtos_pedido = random.sample(produtos, min(num_itens, len(produtos)))

                # Inserir itens do pedido
                for produto_id, preco_unitario in produtos_pedido:
                    quantidade = random.randint(1, 3)
                    subtotal = preco_unitario * quantidade
                    valor_total += subtotal

                    cursor.execute(
                        """INSERT INTO ITENS_PEDIDOS (ID_PEDIDO, ID_PRODUTO, PRECO_UNITARIO, QUANTIDADE)
                        VALUES (%s, %s, %s, %s)""",
                        (pedido_id, produto_id, preco_unitario, quantidade)
                    )

                # Atualizar valor total do pedido
                cursor.execute(
                    "UPDATE PEDIDOS SET VALOR_TOTAL = %s WHERE IDPEDIDO = %s",
                    (valor_total, pedido_id)
                )

                # Gerar pagamento (80% dos pedidos têm pagamento)
                if status_pedido != 'CANCELADO' and random.random() > 0.2:
                    metodo = random.choice(['CARTÃO', 'BOLETO', 'PIX'])
                    status_pagamento = 'APROVADO' if random.random() > 0.1 else 'RECUSADO'
                    data_pagamento = data_pedido + timedelta(hours=random.randint(1, 72))

                    cursor.execute(
                        """INSERT INTO PAGAMENTOS (ID_PEDIDO, VALOR_PAGO, METODO, STATUS, DATA_PAGAMENTO)
                        VALUES (%s, %s, %s, %s, %s)""",
                        (pedido_id, valor_total, metodo, status_pagamento, data_pagamento)
                    )

                # Gerar entrega (90% dos pedidos têm entrega)
                if status_pedido != 'CANCELADO' and random.random() > 0.1 and enderecos_cliente:
                    id_endereco = random.choice(enderecos_cliente)
                    transportadoras = ['Correios', 'Loggi', 'Jadlog', 'Azul Cargo', 'DHL']
                    status_entrega = random.choices(
                        ['PREPARAÇÃO', 'ENVIADO', 'EM_TRANSITO', 'ENTREGUE', 'CANCELADO'],
                        weights=[0.1, 0.2, 0.3, 0.35, 0.05]
                    )[0]

                    data_envio = data_pedido + timedelta(days=random.randint(1, 3))
                    data_prevista = data_envio + timedelta(days=random.randint(3, 10))

                    if status_entrega == 'ENTREGUE':
                        data_entrega = data_prevista + timedelta(days=random.randint(-2, 5))
                    else:
                        data_entrega = None

                    codigo_rastreio = f'BR{random.randint(100000000000000, 999999999999999)}'

                    cursor.execute(
                        """INSERT INTO ENTREGAS (ID_PEDIDO, ID_ENDERECO, TRANSPORTADORA, DATA_ENVIO,
                        DATA_PREVISTA, CODIGO_RASTREAMENTO, STATUS, DATA_ENTREGA)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (pedido_id, id_endereco, random.choice(transportadoras), data_envio,
                         data_prevista, codigo_rastreio, status_entrega, data_entrega)
                    )

                # Gerar avaliações (50% dos pedidos têm avaliação)
                if status_pedido == 'PAGO' and random.random() > 0.5:
                    for produto_id, _ in produtos_pedido:
                        if random.random() > 0.3:  # 70% chance de avaliar cada produto
                            nota = random.randint(3, 5) if random.random() > 0.2 else random.randint(1, 2)

                            # 60% chance de ter comentário, 40% chance de ser apenas nota
                            comentario = gerar_comentario_avaliacao(produto_id, nota) if random.random() > 0.4 else None
                            data_avaliacao = data_pedido + timedelta(days=random.randint(1, 30))

                            cursor.execute(
                                """INSERT INTO AVALIACOES (ID_CLIENTE, ID_PRODUTO, NOTA, COMENTARIO, DATA_AVALIACAO)
                                VALUES (%s, %s, %s, %s, %s)""",
                                (cliente_id, produto_id, nota, comentario, data_avaliacao)
                            )

            if (i + 1) % 100 == 0:
                print(f"Processados: {i + 1}/{len(clientes_gerados)} clientes")
                conexao.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao processar cliente {cliente_id}: {err}")
        conexao.rollback()

print("Todos os dados foram gerados com sucesso!")

# Fechar conexão
cursor.close()
conexao.close()
