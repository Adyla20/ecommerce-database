# 📊 Análise de Business Intelligence - E-commerce Database  

📈 Relatório Completo de Análises e Insights  

---

## 1. 🏆 TOP 10 PRODUTOS MAIS VENDIDOS (ÚLTIMO TRIMESTRE)  

### Resultado Obtido:

| IDPRODUTO | NOME_PRODUTO          | total_vendido_qtd |
|-----------|-----------------------|-------------------|
| 29        | Longchamp Box-Trot    | 16                |
| 8         | Dell XPS 15           | 14                |
| 1         | iPhone 15 Pro Max     | 13                |
| 16        | Sony WF-1000XM4       | 13                |
| 13        | Sony WH-1000XM5       | 12                |
| 19        | Rolex Submariner Date | 11                |
| 18        | Lenovo Yoga Tab 13    | 11                |
| 24        | Fossil Carlie         | 11                |
| 9         | Huawei MateBook X Pro | 11                |
| 35        | Adidas NMD_R1         | 11                |


### 🔍 Análise de BI:
- **Produtos de Luxo Dominam:** Longchamp (16 unidades) e Rolex (11 unidades).  
- **Eletrônicos em Alta:** 6 dos 10 produtos são eletrônicos (60%).  
- **Diversidade de Categorias:** Mix entre bolsas, eletrônicos, relógios e tênis.  

**Recomendações:**  
- Manter estoque prioritário para Longchamp e Dell XPS.   
- Campanhas específicas para Apple e Rolex.  

---

## 2. 📊 TAXA DE CONVERSÃO POR MÊS (ÚLTIMOS 12 MESES)  

### Resultado Obtido:

| ano_mes | pedidos | novos_clientes | taxa_conversao_por_cliente |
|---------|---------|----------------|----------------------------|
| 2024-10 | 16      | 38             | 0.4211                     |
| 2024-11 | 27      | 25             | 1.0800                     |
| 2024-12 | 13      | 28             | 0.4643                     |
| 2025-01 | 22      | 26             | 0.8462                     |
| 2025-02 | 23      | 27             | 0.8519                     |
| 2025-03 | 20      | 19             | 1.0526                     |
| 2025-04 | 29      | 37             | 0.7838                     |
| 2025-05 | 21      | 37             | 0.5676                     |
| 2025-06 | 21      | 37             | 0.5676                     |
| 2025-07 | 17      | 32             | 0.5313                     |
| 2025-08 | 29      | 27             | 1.0741                     |
| 2025-09 | 17      | 16             | 1.0625                     |


### 🔍 Análise de BI:
- **Alta Performance:** Nov/2024, Mar/2025, Ago/2025 e Set/2025 (>1.0).  
- **Meses Críticos:** Out/2024 e Dez/2024 (<0.5).  
- **Padrão:** Final do ano apresenta queda.  

**Recomendações:**  
- Replicar campanhas de Novembro.  
- Revisar estratégias de fim de ano.  
- Explorar clientes recorrentes.  

---

## 3. ⚠️ PRODUTOS COM MAIOR TAXA DE CANCELAMENTO  

### Resultado Obtido:

| IDPRODUTO | NOME_PRODUTO                     | qtd_cancelada | qtd_total_vendida | taxa_cancelamento |
|-----------|----------------------------------|---------------|-------------------|-------------------|
| 10        | MacBook Air M2                   | 8             | 37                | 0.2162            |
| 41        | Jo Malone English Pear & Freesia | 8             | 38                | 0.2105            |
| 26        | Longchamp Le Pliage              | 5             | 27                | 0.1852            |
| 33        | New Balance 574                  | 7             | 38                | 0.1842            |
| 6         | Xiaomi Redmi Note 13 Pro         | 10            | 55                | 0.1818            |
| 15        | Lenovo Tab P12 Pro               | 7             | 41                | 0.1707            |
| 30        | Charles & Keith Tassel           | 4             | 24                | 0.1667            |
| 22        | Rolex Datejust 36                | 5             | 31                | 0.1613            |
| 11        | Dell Alienware x16               | 7             | 44                | 0.1591            |
| 3         | Xiaomi 14 Pro                    | 4             | 26                | 0.1538            |



### 🔍 Análise de BI:
- **Eletrônicos em Risco:** 5 dos 10 são eletrônicos.  
- **Premium Afetados:** MacBook Air M2 e Jo Malone.  
- **Maior Volume:** Xiaomi Redmi Note (10 cancelamentos).  

**Recomendações:**  
- Investigar problemas no MacBook Air.  
- Revisar política de perfumes.  
- Avaliar concorrência de preços Xiaomi.  

---

## 4. 💰 TICKET MÉDIO POR CATEGORIA  

### Resultado Obtido:
| IDCATEGORIA | NOME_CATEGORIA         | num_pedidos | ticket_medio_por_categoria | sd_subtotal_item |
|-------------|-----------------------|-------------|----------------------------|-----------------|
| 4           | Relógios               | 83          | 39251.59                   | 56005.85        |
| 2           | Notebooks              | 85          | 28929.17                   | 18378.88        |
| 1           | Smartphones            | 92          | 12412.82                   | 7115.32         |
| 3           | Acessórios Eletrônicos | 82          | 7316.83                    | 3277.72         |
| 5           | Bolsas e Carteiras     | 83          | 2672.05                    | 1372.36         |
| 7           | Perfumes               | 82          | 2007.71                    | 929.23          |
| 6           | Tênis                  | 72          | 1502.56                    | 605.03          |



### 🔍 Análise de BI:
- **Premium:** Relógios 26x maior que tênis.  
- **Alta Variabilidade:** Relógios com alto desvio padrão.  
- **Volume:** Smartphones com maior volume.  

**Recomendações:**  
- Aplicar estratégias segmentadas.  

---

## 5. 💳 MÉTODO DE PAGAMENTO MAIS POPULAR  

### Resultado Obtido:

| METODO  | num_pedidos | total_transacionado |
|---------|-------------|-------------------|
| PIX     | 76          | 2588461.20        |
| CARTÃO  | 55          | 1711172.90        |
| BOLETO  | 73          | 1355214.20        |



### 🔍 Análise de BI:
- **PIX Dominante:** Maior volume e valor.  
- **Cartão:** Menos pedidos, maior ticket.  
- **Boleto em Declínio:** Menor valor total.  

**Recomendações:**  
- Incentivar PIX.  
- Cartão com promoções de parcelamento.  
- Manter boleto para nicho específico.  

---

## 6. 🔄 ANÁLISE DE CHURN: CLIENTES RECORRENTES VS ONE-TIME  

### Resultado Obtido:

| tipo_cliente | quantidade_clientes | receita_total  |
|--------------|-------------------|----------------|
| one_time     | 650               | 19536171.90    |
| recorrente   | 108               | 9330347.60     |
| sem_pedido   | 642               | 0.00           |


### 🔍 Análise de BI:
- **Baixa Fidelização:** Apenas 7.7% recorrentes.  
- **Potencial:** 642 clientes sem pedidos.  
- **Valor:** Recorrentes = 32% da receita.  

**Recomendações:**  
- Programa de recompensas.  
- Campanhas de reativação.  
- Clube de vantagens.  

---

## 7. 🚚 TEMPO MÉDIO DE ENTREGA POR TRANSPORTADORA  

### Resultado Obtido:

| TRANSPORTADORA | pedidos_entregues | tempo_medio_dias | menor_dias | maior_dias |
|----------------|------------------|-----------------|------------|------------|
| Jadlog         | 15               | 8.20            | 2          | 14         |
| DHL            | 26               | 9.35            | 4          | 15         |
| Correios       | 14               | 9.36            | 5          | 13         |
| Loggi          | 22               | 10.27           | 6          | 17         |
| Azul Cargo     | 15               | 11.20           | 6          | 16         |


### 🔍 Análise de BI:
- **Mais Rápida:** Jadlog (8.2 dias).  
- **Consistência:** DHL (4-15 dias).  
- **Crítica:** Azul Cargo (11.2 dias).  

**Recomendações:**  
- Priorizar Jadlog para urgência.  
- Revisar contrato Azul Cargo.  
  

---

## 8. 🗺️ TOP 5 ESTADOS COM MAIOR NÚMERO DE CLIENTES  

### Resultado Obtido:

| uf | clientes_uf |
|----|-------------|
| TO | 90          |
| AC | 89          |
| SC | 87          |
| GO | 86          |
| MT | 82          |


### 🔍 Análise de BI:
- **Interior Forte:** Norte e Centro-Oeste dominam.  
- **Ausência de SP/RJ/MG:** Grandes centros fora do top 5.  
- **Mercado Nichado:** Regiões menos atendidas.  

**Recomendações:**  
- Estratégias regionais específicas.  
- Investigar baixa penetração em SP/RJ/MG.  

---

## 9. ⭐ PRODUTOS MELHOR E PIOR AVALIADOS  

### Top 3 Melhores Avaliados:

| IDPRODUTO | NOME_PRODUTO             | avg_nota | num_reviews |
|-----------|--------------------------|----------|-------------|
| 4         | iPhone 14                | 4.08     | 24          |
| 6         | Xiaomi Redmi Note 13 Pro | 4.00     | 19          |
| 35        | Adidas NMD_R1            | 4.00     | 12          |


### Bottom 3 Piores Avaliados:

| IDPRODUTO | NOME_PRODUTO                     | avg_nota | num_reviews |
|-----------|----------------------------------|----------|-------------|
| 41        | Jo Malone English Pear & Freesia | 2.61     | 18          |
| 20        | Casio G-Shock DW5600             | 2.69     | 13          |
| 15        | Lenovo Tab P12 Pro               | 2.93     | 14          |


### 🔍 Análise de BI:
- **Apple Lidera:** iPhone 14 melhor avaliado.  
- **Problemas:** Perfumes e Casio.  
- **Xiaomi Bem Posicionado:** Boa avaliação com preço acessível.  

**Recomendações:**  
- Investigar motivos de baixa avaliação nos produtos Jo Malone, Casio e Lenovo. 
- Explorar sucesso Apple e Xiaomi.  

---

## 10. 💎 FATURAMENTO POR CATEGORIA (ÚLTIMO ANO)  

### Resultado Obtido:

| IDCATEGORIA | NOME_CATEGORIA         | faturamento_total |
|-------------|-----------------------|------------------|
| 4           | Relógios               | 3257881.80       |
| 2           | Notebooks              | 2458979.40       |
| 1           | Smartphones            | 1141979.60       |
| 3           | Acessórios Eletrônicos | 599979.70        |
| 5           | Bolsas e Carteiras     | 221780.50        |
| 7           | Perfumes               | 164632.10        |
| 6           | Tênis                  | 108184.30        |


### 🔍 Análise de BI:
- **Relógios:** 47% do faturamento.  
- **Tecnologia:** Notebooks + Smartphones = 52%.  
- **Baixo Desempenho:** Moda e perfumes.  

**Recomendações:**  
- Expandir relógios premium.  
- Estratégia agressiva para acessórios eletrônicos.  
- Revisar categorias de baixa performance.  

---

# 🎯 RESUMO EXECUTIVO DOS PRINCIPAIS INSIGHTS  

### ✅ Pontos Fortes:
1. Segmento Premium sólido (47% em relógios).  
2. PIX é o método preferido e eficiente.  
3. Produtos Apple bem avaliados e demandados.  

### ⚠️ Áreas de Atenção:
1. Baixa retenção (7.7% recorrentes).  
2. Altas taxas de cancelamento (eletrônicos).  
3. Forte sazonalidade (quedas em períodos críticos).  

### 🚀 Oportunidades Imediatas:
1. Programa de fidelidade para clientes one-time.  
2. Otimização de estoque baseado no top 10.  
3. Reposicionamento de produtos mal avaliados.  



### Resultado Obtido:
