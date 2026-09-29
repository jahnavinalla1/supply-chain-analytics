"""Behavioral tests for this standalone analytical project."""
import importlib.util,math,sqlite3,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from common import queries

def module(slug):
    spec=importlib.util.spec_from_file_location(slug,ROOT/'analyze.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def fixture(slug,table,rows):
    m=module(slug);db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE '+table+' ('+m.SCHEMA+')')
    db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for _ in rows[0])+')',rows)
    return queries(db,ROOT/'analysis.sql')

class AnalystTests(unittest.TestCase):
    def test_otif_requires_both_conditions_on_same_order(self):
        t=fixture('04-supply-chain-performance','shipments',[
          ('a','Atlas','s','2025-01-01','2025-01-10','2025-01-09',10,9,100),
          ('b','Atlas','s','2025-01-01','2025-01-10','2025-01-11',10,10,100),
          ('c','Atlas','s','2025-01-01','2025-01-10','2025-01-10',10,10,100)])
        self.assertEqual(t['suppliers'][0]['otif_pct'],33.33)
        self.assertEqual(t['suppliers'][0]['unit_fill_pct'],96.67)
    def test_deterministic_demand_has_no_safety_stock(self):
        f=module('04-supply-chain-performance').reorder_point
        self.assertEqual(f(20,0,10,0),(0,200))
        self.assertGreater(f(20,5,10,2)[1],200)
    def test_full_analysis_runs_and_exports(self):
        result=module('standalone').run()
        self.assertTrue(result)
        self.assertTrue((ROOT/'index.html').is_file())
        self.assertTrue((ROOT/'results/metrics.json').is_file())
if __name__=='__main__':unittest.main()
