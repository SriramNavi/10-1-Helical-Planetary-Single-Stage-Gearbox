# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""Check selected native evidence and integrity of the prepared public package."""
import csv,json,hashlib,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    with (ROOT/'results/candidate_comparison.csv').open() as f:rows=list(csv.DictReader(f))
    expected=[15.156654e6,15.591397e6,15.612941e6]
    for row,value in zip(rows,expected):assert math.isclose(float(row['peak_VM_Pa']),value,rel_tol=1e-10)
    assert all(float(r['peak_change_vs_matched_relative'])>0 and r['convergence']=='PASS' for r in rows[1:])
    field=np.load(ROOT/'evidence/baseline_bore_surface.npz',allow_pickle=False)['field']
    assert field.shape[1]==5 and np.isfinite(field).all()
    assert np.max(abs(np.hypot(field[:,2],field[:,3]-.0296)-.0012))<2e-8
    assert math.isclose(float(field[:,4].max()),expected[0],rel_tol=1e-6)
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_text())
    for record in manifest:
        path=ROOT/record['path'];assert path.is_relative_to(ROOT) and path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],record['path']
    print('PASS: native stress field, matched decision and',len(manifest),'publication file hashes. No CAD or FEA executed.')
