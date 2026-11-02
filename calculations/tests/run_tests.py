# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""Persist honest unittest results; SciPy quadrature provides independent beam/contact checks."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


class Recorded(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.identifiers=[]
    def startTest(self,test):self.identifiers.append(test.id());super().startTest(test)


if __name__=='__main__':
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    result=unittest.TextTestRunner(verbosity=1,resultclass=Recorded).run(suite)
    out=ROOT/'results';out.mkdir(exist_ok=True)
    record=dict(tests_run=result.testsRun,successful=result.wasSuccessful(),failures=[{'test':x.id(),'traceback':t} for x,t in result.failures],
                errors=[{'test':x.id(),'traceback':t} for x,t in result.errors],skipped=[{'test':x.id(),'reason':r} for x,r in result.skipped],test_ids=result.identifiers)
    (out/'test_results.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
