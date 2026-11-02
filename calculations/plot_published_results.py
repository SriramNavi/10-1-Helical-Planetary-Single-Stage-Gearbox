# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""Replot selected native results; no solver, geometry change or new FEA."""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=Path(__file__).resolve().parent/'reproduced'
if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    with (ROOT/'results/candidate_comparison.csv').open() as f:rows=list(csv.DictReader(f))
    fig,ax=plt.subplots(figsize=(8,4.5));bars=ax.bar(['Baseline','R0.20 mm','R0.35 mm'],[float(r['peak_VM_Pa'])/1e6 for r in rows],color=['#183548','#087f8c','#cb651c'])
    ax.bar_label(bars,fmt='%.4f',padding=4);ax.set(ylim=(0,18),ylabel='Recovered peak von Mises (MPa)',title='Archived native comparison | hypothetical Tz=0.15 N m')
    fig.tight_layout();fig.savefig(OUT/'candidate_stress.png',dpi=220);plt.close(fig)
    a=np.load(ROOT/'evidence/baseline_bore_surface.npz',allow_pickle=False)['field'];phi=np.degrees(np.arctan2(a[:,3]-.0296,a[:,2]))
    fig,ax=plt.subplots(figsize=(9,4.5));c=ax.tricontourf(a[:,1]*1e3,phi,a[:,4]/1e6,levels=22,cmap='inferno')
    ax.set(xlabel='Cross-hole axis x (mm)',ylabel='Cylinder angle (deg)',title='Native exported baseline field | E=1.2 GPa, nu=0.35, fixed root')
    fig.colorbar(c,ax=ax,label='Recovered von Mises (MPa)');fig.tight_layout();fig.savefig(OUT/'baseline_bore_stress.png',dpi=220);plt.close(fig)
    print('Replotted archived candidate table and native bore field; no new simulation.')
