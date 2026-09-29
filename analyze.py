import math,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import database,queries,publish
F=Path(__file__).resolve().parent
SCHEMA='po_id TEXT PRIMARY KEY,supplier TEXT,sku TEXT,order_date TEXT,due_date TEXT,received_date TEXT,ordered_units INTEGER CHECK(ordered_units>0),received_units INTEGER CHECK(received_units>=0 AND received_units<=ordered_units),unit_cost_cents INTEGER CHECK(unit_cost_cents>0)'
def reorder_point(demand_mean,demand_sd,lead_mean,lead_sd,z=1.645):
    if min(demand_mean,demand_sd,lead_mean,lead_sd)<0:raise ValueError('Inputs must be non-negative')
    safety=z*math.sqrt(lead_mean*demand_sd**2+demand_mean**2*lead_sd**2)
    return math.ceil(safety),math.ceil(demand_mean*lead_mean+safety)
def run():
    db=database(F,'shipments',SCHEMA);t=queries(db,F/'analysis.sql');worst=t['suppliers'][0]
    assert db.execute('SELECT COUNT(*) FROM shipments').fetchone()[0]==900
    assert db.execute('SELECT COUNT(*) FROM shipments WHERE received_date<order_date OR due_date<order_date').fetchone()[0]==0
    lead=[r[0] for r in db.execute('SELECT JULIANDAY(received_date)-JULIANDAY(order_date) FROM shipments')]
    # Planning assumptions are explicitly independent of shipment quantities (not demand observations).
    lm,ls=statistics.mean(lead),statistics.stdev(lead);scenarios=[]
    for demand in [16,20,24]:
        safety,rop=reorder_point(demand,5,lm,ls)
        scenarios.append(dict(assumed_daily_demand=demand,assumed_daily_sd=5,mean_lead_days=round(lm,3),
            lead_sd_days=round(ls,3),cycle_service_target_pct=95,safety_stock_units=safety,reorder_point_units=rop))
    t['inventory_scenarios']=scenarios
    total=db.execute('SELECT AVG(CASE WHEN received_date<=due_date AND received_units>=ordered_units THEN 1.0 ELSE 0.0 END) FROM shipments').fetchone()[0]
    publish(F,'Supplier reliability and inventory planning','Which suppliers need corrective action, and how sensitive is a reorder policy to demand?',
    {'Purchase orders':'900','Overall OTIF':f'{100*total:.1f}%','Mean lead time':f'{lm:.1f} days','Base-case reorder point':str(scenarios[1]['reorder_point_units'])+' units'},t,
    [f"{worst['supplier']} has the lowest OTIF ({worst['otif_pct']}%) across {worst['purchase_orders']} purchase orders.",
     f"At an assumed 20 units/day, the illustrative reorder point is {scenarios[1]['reorder_point_units']} units, including {scenarios[1]['safety_stock_units']} units of safety stock.",
     'Unit fill rate and purchase-order OTIF answer different questions; a nearly complete shipment can still fail OTIF.'],
    ['Review lateness and short shipments with the lowest-OTIF supplier; set a time-bound corrective-action plan.',
     'Prioritize A-class SKUs for supplier reviews, while considering criticality and substitutability alongside spend.',
     'Replace assumed demand with daily sales and stockout observations, then backtest SKU-specific policies before changing inventory.'],
    'Synthetic closed, single-line purchase orders; no open-order censoring or split receipts. ABC uses ordered spend and assigns a threshold-crossing item to the earlier class. Reorder scenarios assume independent daily demand and lead time, normal demand during lead time, and a 95% cycle-service target (not a 95% fill rate). Pooled lead times and assumed demand make this an illustration, not a purchasing recommendation.',
    {'title':'On-time, in-full deliveries by supplier','note':'Both the date and quantity requirement must pass for a purchase order to count.','unit':'%',
     'rows':[{'label':r['supplier'],'value':r['otif_pct']} for r in t['suppliers']]})
    return t
if __name__=='__main__':run()
