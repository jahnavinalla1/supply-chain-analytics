-- name: suppliers
SELECT supplier,COUNT(*) purchase_orders,
 ROUND(100.0*AVG(CASE WHEN received_date<=due_date AND received_units>=ordered_units THEN 1 ELSE 0 END),2) otif_pct,
 ROUND(100.0*SUM(received_units)/SUM(ordered_units),2) unit_fill_pct,
 ROUND(AVG(JULIANDAY(received_date)-JULIANDAY(order_date)),2) mean_lead_days,
 ROUND(AVG(MAX(0,JULIANDAY(received_date)-JULIANDAY(due_date))),2) mean_late_days,
 ROUND(SUM(ordered_units*unit_cost_cents)/100.0,2) ordered_spend
FROM shipments GROUP BY supplier ORDER BY otif_pct;
-- name: monthly_otif
SELECT SUBSTR(due_date,1,7) due_month,COUNT(*) purchase_orders,
 ROUND(100.0*AVG(CASE WHEN received_date<=due_date AND received_units>=ordered_units THEN 1 ELSE 0 END),2) otif_pct
FROM shipments GROUP BY due_month ORDER BY due_month;
-- name: abc_spend
WITH sku AS (
 SELECT sku,SUM(ordered_units*unit_cost_cents)/100.0 spend FROM shipments GROUP BY sku
), cumulative AS (
 SELECT *,SUM(spend) OVER(ORDER BY spend DESC,sku ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) cumulative,
 SUM(spend) OVER() total FROM sku
)
SELECT sku,ROUND(spend,2) ordered_spend,ROUND(100.0*cumulative/total,2) cumulative_spend_pct,
 CASE WHEN (cumulative-spend)/total<.80 THEN 'A' WHEN (cumulative-spend)/total<.95 THEN 'B' ELSE 'C' END abc_class
FROM cumulative ORDER BY spend DESC,sku;
