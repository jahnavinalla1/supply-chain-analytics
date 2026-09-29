import random,sys
from datetime import date,timedelta
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import write_csv

def generate():
    rng=random.Random(4404);rows=[]
    for i in range(900):
        supplier=rng.choice(['Atlas','Beacon','Cedar']);sku=rng.choice(['SKU-01','SKU-02','SKU-03','SKU-04'])
        ordered=rng.randint(20,150);shipped=ordered if rng.random()>.12 else max(1,ordered-rng.randint(1,18))
        lead={'Atlas':7,'Beacon':10,'Cedar':8}[supplier]+rng.randint(-2,5)
        start=date(2025,1,1)+timedelta(days=rng.randrange(330));due=start+timedelta(days=10)
        rows.append(dict(po_id=f'P{i:05}',supplier=supplier,sku=sku,order_date=str(start),due_date=str(due),
            received_date=str(start+timedelta(days=lead)),ordered_units=ordered,received_units=shipped,
            unit_cost_cents={'SKU-01':800,'SKU-02':1600,'SKU-03':2800,'SKU-04':6000}[sku]))
    write_csv(Path(__file__).with_name('data.csv'),rows)
if __name__=='__main__':generate()
