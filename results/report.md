# Supplier reliability and inventory planning

**Simulated portfolio case study — no client data or measured commercial impact.**

## Decision

Which suppliers need corrective action, and how sensitive is a reorder policy to demand?

## Results

- **Purchase orders:** 900
- **Overall OTIF:** 50.9%
- **Mean lead time:** 9.8 days
- **Base-case reorder point:** 287 units

## Findings

- Beacon has the lowest OTIF (30.03%) across 303 purchase orders.
- At an assumed 20 units/day, the illustrative reorder point is 287 units, including 91 units of safety stock.
- Unit fill rate and purchase-order OTIF answer different questions; a nearly complete shipment can still fail OTIF.

## Recommended next steps

- Review lateness and short shipments with the lowest-OTIF supplier; set a time-bound corrective-action plan.
- Prioritize A-class SKUs for supplier reviews, while considering criticality and substitutability alongside spend.
- Replace assumed demand with daily sales and stockout observations, then backtest SKU-specific policies before changing inventory.

## Limits

Synthetic closed, single-line purchase orders; no open-order censoring or split receipts. ABC uses ordered spend and assigns a threshold-crossing item to the earlier class. Reorder scenarios assume independent daily demand and lead time, normal demand during lead time, and a 95% cycle-service target (not a 95% fill rate). Pooled lead times and assumed demand make this an illustration, not a purchasing recommendation.
