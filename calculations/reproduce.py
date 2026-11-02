# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""Portable offline replay of published analytical values; never opens CAD or solves FEA."""
import csv,json,math
from pathlib import Path
import numpy as np
from gb10_analysis.geometry import Gearset
from gb10_analysis.pipeline import screen,partial_limits
ROOT=Path(__file__).resolve().parent

def plain(value):
    if isinstance(value,np.ndarray):return value.tolist()
    if isinstance(value,np.generic):return value.item()
    raise TypeError(type(value).__name__)

def main():
    inputs=json.loads((ROOT/'inputs/parameters.json').read_text());gear=Gearset(**inputs['baseline'])
    reference=screen(inputs);geometry=gear.geometry();out=ROOT/'reproduced';out.mkdir(exist_ok=True)
    result=dict(classification='CONDITIONAL CALCULATION, NOT HARDWARE VALIDATION',geometry=geometry,
        reference_screen=reference,partial_limits=partial_limits(inputs),
        certified_torque_rating_Nm=None,validated_operating_envelope=None,
        warning='Reference loads, E/nu, sharing, allowables and loss parameters are assumptions; incomplete modeled-component ceilings are not a gearbox rating.')
    (out/'analytical_summary.json').write_text(json.dumps(result,indent=2,default=plain,allow_nan=False)+'\n')
    target=json.loads((ROOT/'inputs/reference_checks.json').read_text())
    actual=dict(orbit_m=geometry['orbit_m'],root_sun_Pa=reference['root_sun_Pa'],external_contact_Pa=reference['external_contact_Pa'],
                output_core_equivalent_von_mises_Pa=reference['output_core_equivalent_von_mises_Pa'])
    checks={k:math.isclose(actual[k],v,rel_tol=1e-8,abs_tol=1e-11) for k,v in target.items()}
    if not all(checks.values()):raise AssertionError(checks)
    comparison=list(csv.DictReader((ROOT.parent/'results/candidate_comparison.csv').open()))
    assert all(float(r['peak_change_vs_matched_relative'])>0 for r in comparison[1:])
    verify=dict(status='PASS',archived_reference_checks=checks,candidate_decision='RETAIN_BASELINE',
        FEA_replay='Not performed; compares archived native-result tables only')
    (out/'verification.json').write_text(json.dumps(verify,indent=2)+'\n')
    print('PASS: four archived analytical checks; candidate decision reconciled; no FEA or CAD access.')

if __name__=='__main__':main()
