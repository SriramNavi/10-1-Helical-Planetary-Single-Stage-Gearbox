# Reproducibility

## Portable public replay

Use Python 3.11 or newer. From the publication root, install the pinned NumPy/SciPy versions in a local environment, then run:

```sh
python -m pip install -r calculations/requirements.txt
python -B calculations/tests/run_tests.py
python -B calculations/reproduce.py
```

The inherited mathematical suite contains 62 tests. The runner compares four selected analytical values with archived Phase 2 outputs and reconciles the retained-baseline decision against the selected native result table. It writes only `calculations/reproduced/`; the test runner writes `calculations/results/`. No SolidWorks installation, CAD opening, FEA, network request or source-project access is performed by these commands. The machine-readable reference inputs keep actual material/duty/operating limits null. The unrelated preliminary robot-application context was removed from the public input copy; the numerical model and test equations are unchanged.

The selected native tables can be inspected in `results/`. The baseline bore surface is included as a numeric NPZ export with node ID, x/y/z in m and von Mises in Pa; it is not a native solver deck. Run `python -B calculations/check_publication.py` to check that field's peak, the matched comparison, refinement-table decisions and the publication manifest. Public plot reproduction is available through `calculations/plot_published_results.py`; CAD illustrations are delivered as curated derived images rather than a complete public CAD model.

## Native reproduction boundary

These public commands do not rerun the 49 successful native solves across Phases 3/3B/4A. Full native reproduction needs the separately retained CAD/study archives, the installed commercial Simulation capability and its recorded native API environment. Per-phase private reproducibility files document unique study names, geometry identities, loads/materials, failures, raw result arrays and protection guards. See `SOURCES.md` for phase-relative artifact IDs and SHA-256 provenance. The public package does not claim a license-free or complete end-to-end native FEA replay.

No original or prior-phase file was overwritten to create this package. Phase 5 performed read-only evidence extraction, mathematical replay, numerical postprocessing and publication rendering only. The previously approved GEN/MAS exception remains part of the evidence history.
