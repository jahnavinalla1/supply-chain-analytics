# Supplier reliability and inventory planning

**Independent portfolio case study · simulated data · no client affiliation**

Procurement KPIs · ABC classification · scenario analysis

[Interactive dashboard](https://jahnavinalla1.github.io/analytics-projects/04-supply-chain-performance/) · [Decision memo](results/report.md) · [SQL](analysis.sql) · [Python](analyze.py)

## Business problem

A procurement team needs to prioritize supplier interventions and understand inventory sensitivity to demand assumptions.

## Reproduce

This is a self-contained repository. Python 3.10+ is the only dependency; no shared portfolio repository, API key, or third-party package is required.

```sh
git clone https://github.com/jahnavinalla1/supply-chain-analytics.git
cd supply-chain-analytics
python3 run.py
```

`run.py` regenerates the seeded dataset, rebuilds the dashboard and reports, and executes the tests. To analyze the included CSV without replacing it:

```sh
python3 analyze.py
python3 -m unittest discover -s tests -v
```

Open `index.html` in your browser to explore the dashboard. Its data is embedded, so no server is needed. The [hosted demo](https://jahnavinalla1.github.io/analytics-projects/04-supply-chain-performance/) is also linked from the portfolio. `generate.py` intentionally overwrites `data.csv` with the same simulated sample; `analyze.py` only reads it and rebuilds outputs.

## Data and provenance

One closed, single-line purchase order per row, 900 orders placed in 2025. Seed 4404; no split receipts. Data is authored by the deterministic generator in this folder. It contains no real people, company transactions, or external source material. Patterns in the simulation are intentionally constructed for analytical practice; they are not evidence about actual markets or employers.

| Field | Meaning |
|---|---|
| `po_id` | Unique purchase-order key |
| `supplier, sku` | Supplier and item dimensions |
| `order_date` | Purchase-order placement date |
| `due_date` | Contractual date, 10 days after placement |
| `received_date` | Actual receipt date |
| `ordered_units` | Positive ordered quantity |
| `received_units` | Received quantity, at most ordered units |
| `unit_cost_cents` | Unit acquisition cost in USD cents |

## Metric contract and method

OTIF = orders meeting received_date ≤ due_date AND received_units ≥ ordered_units / all closed orders. Unit fill = total received / total ordered. ABC uses ordered spend; A includes the item crossing 80%, B the item crossing 95%. Safety stock = z × sqrt(mean lead × daily demand variance + mean daily demand² × lead variance), z=1.645. Reorder point = mean daily demand × mean lead + safety stock, rounded up. Demand scenarios (16/20/24 units/day; SD 5) are assumptions.

`analysis.sql` is the actual executed SQL, not a decorative example. Python loads the CSV into constrained in-memory SQLite tables, executes named SQL blocks, validates key invariants, calculates any statistical/scenario outputs, and renders the result files. No network, API key, or paid BI license is needed.

## Stakeholders and decision ownership

Procurement owns supplier reviews; planning owns replenishment assumptions; operations owns receipt accuracy.

## Data quality and acceptance

PO keys must be unique; receipts cannot precede orders; OTIF requires both checks on the same order. Do not treat purchase quantities as observed customer demand. Scenario values require demand and stockout backtesting before operational use.

## Deliverables

- `data.csv`: complete reproducible source dataset.
- `generate.py`: seeded data-generation logic and business assumptions.
- `analysis.sql` / `analyze.py`: executable analytical logic.
- `index.html`: portable interactive dashboard with filtering and sorting.
- `results/metrics.json` and result CSVs: machine-readable, exportable outputs.
- `results/report.md`: computed findings, recommended actions and limitations.

## Interpretation

Read the decision memo for the actual computed results. Recommendations are proposals for a future pilot; no employer outcome, production deployment, cash saving, or measured improvement is claimed. Replacing the synthetic source requires revisiting schema constraints, hardcoded fixture sizes, missing-data policies and the metric contract.
