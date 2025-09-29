-- =====================================================
-- CONSULTAS ANALÍTICAS - BUSINESS INTELLIGENCE
-- E-commerce Database System
-- Autor:Ádyla Iasmin Barbosa da Silva
-- =====================================================

-- 1. TOP 10 PRODUTOS MAIS VENDIDOS (ÚLTIMO TRIMESTRE)
-- OBJETIVO: Identificar os produtos com maior volume de vendas para otimização de estoque,
-- priorização de fornecedores e estratégias de marketing segmentadas.

SELECT 
  p.IDPRODUTO,
  p.NOME_PRODUTO,
  SUM(ip.QUANTIDADE) AS total_vendido_qtd
FROM ITENS_PEDIDOS ip
JOIN PEDIDOS ped ON ip.ID_PEDIDO = ped.IDPEDIDO
JOIN PRODUTOS p ON ip.ID_PRODUTO = p.IDPRODUTO
WHERE ped.STATUS = 'PAGO'
  AND ped.DATA_PEDIDO >= DATE_SUB(CURRENT_DATE, INTERVAL 3 MONTH)
GROUP BY p.IDPRODUTO, p.NOME_PRODUTO
ORDER BY total_vendido_qtd DESC
LIMIT 10;


-- 2. TAXA DE CONVERSÃO POR MÊS (ÚLTIMOS 12 MESES)
-- OBJETIVO: Analisar a eficiência da conversão de clientes em pedidos, identificando
-- sazonalidades e eficácia das campanhas de marketing ao longo do tempo.

SELECT
  DATE_FORMAT(mes.m, '%Y-%m') AS ano_mes,
  COALESCE(pedidos_qt.pedidos, 0) AS pedidos,
  COALESCE(novos_clientes_qt.novos_clientes, 0) AS novos_clientes,
  CASE WHEN COALESCE(novos_clientes_qt.novos_clientes,0) = 0 THEN 0
       ELSE ROUND(pedidos_qt.pedidos / novos_clientes_qt.novos_clientes, 4)
  END AS taxa_conversao_por_cliente
FROM (
  SELECT LAST_DAY(DATE_SUB(CURRENT_DATE, INTERVAL seq MONTH)) - INTERVAL (DAY(LAST_DAY(DATE_SUB(CURRENT_DATE, INTERVAL seq MONTH)))-1) DAY AS m
  FROM (SELECT 0 AS seq UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11) seqs
) mes
LEFT JOIN (
  SELECT DATE_FORMAT(DATA_PEDIDO, '%Y-%m-01') AS mes_ref, COUNT(*) AS pedidos
  FROM PEDIDOS
  WHERE STATUS = 'PAGO'
    AND DATA_PEDIDO >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
  GROUP BY mes_ref
) pedidos_qt ON DATE_FORMAT(mes.m, '%Y-%m-01') = pedidos_qt.mes_ref
LEFT JOIN (
  SELECT DATE_FORMAT(DATA_CADASTRO, '%Y-%m-01') AS mes_ref, COUNT(*) AS novos_clientes
  FROM CLIENTES
  WHERE DATA_CADASTRO >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
  GROUP BY mes_ref
) novos_clientes_qt ON DATE_FORMAT(mes.m, '%Y-%m-01') = novos_clientes_qt.mes_ref
ORDER BY ano_mes;


-- 3. PRODUTOS COM MAIOR TAXA DE CANCELAMENTO
-- OBJETIVO: Identificar produtos problemáticos que podem indicar issues de qualidade,
-- descrição inadequada, preço não competitivo ou problemas logísticos.

SELECT
  p.IDPRODUTO,
  p.NOME_PRODUTO,
  SUM(CASE WHEN ped.STATUS = 'CANCELADO' THEN ip.QUANTIDADE ELSE 0 END) AS qtd_cancelada,
  SUM(ip.QUANTIDADE) AS qtd_total_vendida,
  ROUND(
    SUM(CASE WHEN ped.STATUS = 'CANCELADO' THEN ip.QUANTIDADE ELSE 0 END) / NULLIF(SUM(ip.QUANTIDADE),0),4) AS taxa_cancelamento
FROM ITENS_PEDIDOS ip
JOIN PEDIDOS ped ON ip.ID_PEDIDO = ped.IDPEDIDO
JOIN PRODUTOS p ON ip.ID_PRODUTO = p.IDPRODUTO
WHERE ped.DATA_PEDIDO >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY p.IDPRODUTO, p.NOME_PRODUTO
HAVING qtd_total_vendida > 0
ORDER BY taxa_cancelamento DESC
LIMIT 10;


-- 4. TICKET MÉDIO E DISTRIBUIÇÃO POR CATEGORIA
-- OBJETIVO: Analisar o valor médio gasto por pedido em cada categoria, orientando
-- estratégias de pricing, cross-selling e composição de mix de produtos.

SELECT
  c.IDCATEGORIA,
  c.NOME_CATEGORIA,
  COUNT(DISTINCT ped.IDPEDIDO) AS num_pedidos,
  ROUND(SUM(ip.SUBTOTAL) / NULLIF(COUNT(DISTINCT ped.IDPEDIDO),0), 2) AS ticket_medio_por_categoria,
  ROUND(STDDEV_POP(ip.SUBTOTAL), 2) AS sd_subtotal_item
FROM ITENS_PEDIDOS ip
JOIN PRODUTOS p ON ip.ID_PRODUTO = p.IDPRODUTO
LEFT JOIN CATEGORIAS c ON p.ID_CATEGORIA = c.IDCATEGORIA
JOIN PEDIDOS ped ON ip.ID_PEDIDO = ped.IDPEDIDO
WHERE ped.STATUS = 'PAGO'
  AND ped.DATA_PEDIDO >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY c.IDCATEGORIA, c.NOME_CATEGORIA
ORDER BY ticket_medio_por_categoria DESC;


-- 5. MÉTODO DE PAGAMENTO MAIS POPULAR
-- OBJETIVO: Entender as preferências de pagamento dos clientes para otimizar custos
-- operacionais (taxas), melhorar a experiência de checkout e planejar conciliações.

SELECT
  p.METODO,
  COUNT(DISTINCT p.ID_PEDIDO) AS num_pedidos,
  ROUND(SUM(p.VALOR_PAGO), 2) AS total_transacionado
FROM PAGAMENTOS p
JOIN PEDIDOS ped ON p.ID_PEDIDO = ped.IDPEDIDO
WHERE p.STATUS = 'APROVADO'
  AND ped.DATA_PEDIDO >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY p.METODO
ORDER BY total_transacionado DESC;


-- 6. ANÁLISE DE CHURN: CLIENTES RECORRENTES VS ONE-TIME
-- OBJETIVO: Mensurar a retenção de clientes e eficácia das estratégias de fidelização,
-- identificando oportunidades para aumentar o lifetime value dos clientes.

WITH analise_clientes AS (
  SELECT 
    c.IDCLIENTE,
    COUNT(DISTINCT p.IDPEDIDO) AS total_pedidos,
    SUM(p.VALOR_TOTAL) AS receita_total
  FROM CLIENTES c
  LEFT JOIN PEDIDOS p ON c.IDCLIENTE = p.ID_CLIENTE AND p.STATUS = 'PAGO'
  GROUP BY c.IDCLIENTE
)
SELECT
  CASE 
    WHEN total_pedidos = 0 THEN 'sem_pedido'
    WHEN total_pedidos = 1 THEN 'one_time' 
    ELSE 'recorrente'
  END AS tipo_cliente,
  COUNT(*) AS quantidade_clientes,
  ROUND(SUM(receita_total), 2) AS receita_total
FROM analise_clientes
GROUP BY tipo_cliente
ORDER BY receita_total DESC;


-- 7. TEMPO MÉDIO DE PROCESSAMENTO POR TRANSPORTADORA
-- OBJETIVO: Avaliar a performance logística das transportadoras, impactando diretamente
-- na satisfação do cliente (NPS), taxas de devolução e reputação do e-commerce.

SELECT
  e.TRANSPORTADORA,
  COUNT(*) AS pedidos_entregues,
  ROUND(AVG(DATEDIFF(e.DATA_ENTREGA, e.DATA_ENVIO)), 2) AS tempo_medio_dias,
  MIN(DATEDIFF(e.DATA_ENTREGA, e.DATA_ENVIO)) AS menor_dias,
  MAX(DATEDIFF(e.DATA_ENTREGA, e.DATA_ENVIO)) AS maior_dias
FROM ENTREGAS e
WHERE e.STATUS = 'ENTREGUE'
  AND e.DATA_ENTREGA IS NOT NULL
  AND e.DATA_ENVIO IS NOT NULL
GROUP BY e.TRANSPORTADORA
ORDER BY tempo_medio_dias ASC;


-- 8. TOP 5 ESTADOS COM MAIOR NÚMERO DE CLIENTES
-- OBJETIVO: Suportar decisões de expansão geográfica, planejamento logístico
-- (centros de distribuição) e campanhas de marketing regionalizadas.

SELECT 
  e.ESTADO AS uf,
  COUNT(DISTINCT e.ID_CLIENTE) AS clientes_uf
FROM ENDERECOS e
GROUP BY e.ESTADO
ORDER BY clientes_uf DESC
LIMIT 5;


-- 9. PRODUTOS MELHOR E PIOR AVALIADOS
-- OBJETIVO: Identificar best-sellers e produtos problemáticos para orientar ações de
-- merchandising, gestão de catálogo e desenvolvimento de produto.
-- Top 3 Melhores Avaliados

SELECT 
  p.IDPRODUTO, 
  p.NOME_PRODUTO, 
  ROUND(AVG(a.NOTA), 2) AS avg_nota, 
  COUNT(a.IDAVALIACAO) AS num_reviews
FROM PRODUTOS p
JOIN AVALIACOES a ON p.IDPRODUTO = a.ID_PRODUTO
GROUP BY p.IDPRODUTO, p.NOME_PRODUTO
HAVING COUNT(a.IDAVALIACAO) >= 3
ORDER BY avg_nota DESC, num_reviews DESC
LIMIT 3;

-- Bottom 3 Piores Avaliados

SELECT 
  p.IDPRODUTO, 
  p.NOME_PRODUTO, 
  ROUND(AVG(a.NOTA), 2) AS avg_nota, 
  COUNT(a.IDAVALIACAO) AS num_reviews
FROM PRODUTOS p
JOIN AVALIACOES a ON p.IDPRODUTO = a.ID_PRODUTO
GROUP BY p.IDPRODUTO, p.NOME_PRODUTO
HAVING COUNT(a.IDAVALIACAO) >= 3
ORDER BY avg_nota ASC, num_reviews DESC
LIMIT 3;


-- 10. FATURAMENTO POR CATEGORIA (ÚLTIMO ANO)
-- OBJETIVO: Analisar a performance financeira por categoria, suportando decisões
-- de investimento, expansão de mix e estratégias comerciais segmentadas.

SELECT
  c.IDCATEGORIA,
  c.NOME_CATEGORIA,
  ROUND(SUM(ip.SUBTOTAL), 2) AS faturamento_total
FROM ITENS_PEDIDOS ip
JOIN PRODUTOS p ON ip.ID_PRODUTO = p.IDPRODUTO
LEFT JOIN CATEGORIAS c ON p.ID_CATEGORIA = c.IDCATEGORIA
JOIN PEDIDOS ped ON ip.ID_PEDIDO = ped.IDPEDIDO
WHERE ped.STATUS = 'PAGO'
  AND ped.DATA_PEDIDO >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY c.IDCATEGORIA, c.NOME_CATEGORIA
ORDER BY faturamento_total DESC;
