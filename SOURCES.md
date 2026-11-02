# Sources, provenance and attribution

The identifiers below refer to the retained authoritative engineering workspace. They are phase-relative identifiers, not broken links to files claimed to be bundled. Selected numeric exports and public code are included separately. Full source hashes are in `evidence/SOURCE_PROVENANCE.json`; selected-file ancestry is in `evidence/EXPORT_PROVENANCE.json`. Phase 0/2/3 reports contain historical stop gates; later approvals/results supersede those gates without rewriting their original reports.

| ID | Authoritative artifact |
| --- | --- |
| P0 | `00_Audit/PHASE_0_AUDIT.md` |
| P0-N | `00_Audit/NATIVE_READ_ONLY_AUDIT.json` |
| P1 | `02_Phases_1_2/PHASE_1_REQUIREMENTS.md` |
| P2 | `02_Phases_1_2/PHASE_2_ANALYTICAL_REPORT.md` |
| P2-D | `02_Phases_1_2/results/summary.json` |
| P3 | `03_Phase_3/PHASE_3_ENGINEERING_REPORT.md` |
| P3-BC | `03_Phase_3/BOUNDARY_CONDITIONS.md` |
| P3B | `Phase_3B/PHASE_3B_ENGINEERING_DECISION.md` |
| P3B-R | `Phase_3B/ANALYTICAL_NUMERICAL_RECONCILIATION.md` |
| P4A | `Phase_4A/ENGINEERING_SELECTION_REPORT.md` |
| P4A-D | `Phase_4A/PARAMETRIC_COMPARISON.csv` |
| P4A-M | `Phase_4A/CURVATURE_PROTOCOL_ACTUAL.json` |

## Method references

- [SDP/SI, Elements of Metric Gear Technology](https://sdp-si.com/resources/elements-of-metric-gear-technology/page4.php): normal/transverse helical conventions, as recorded in Phase 2. Phase 5 re-access returned 403; no inaccessible content was reconstructed.
- [KHK, Internal Gears technical information](https://khkgears.net/pdf/internal-tech.pdf): geometry/interference context cited by the analytical work; no stock product rating is applied.
- [Jönköping University, Gear strength](https://mechanics.ju.se/MachineElements/gear-strength.html): simplified Lewis/contact-method context from the Phase 2 source register.
- [JTEKT/Koyo, Calculation of service life](https://www.jtekt.co.jp/products/bearing/en/support/bearing-knowledge/5-2000.html): basic rating-life method and applicability; re-accessed in Phase 5. No actual GB10 bearing life is calculated without its missing factors.
- [MIT, Beams in Bending](https://web.mit.edu/emech/admin/OldFiles/dontindex-build/full-text/emechbk_7.pdf), and [TU Delft, Torsion summary](https://ocw.tudelft.nl/course-readings/summary-key-formulas-torsion-2/): mechanics-method references retained from Phase 2.
- [NASA TP-3063, Timothy L. Krantz (1990)](https://ntrs.nasa.gov/citations/19910003643): loss-model/calibration context. No helicopter-stage efficiency or lubrication result is transferred to this PLA demonstrator. Re-accessed in Phase 5.
- [SolidWorks part-analysis API example](https://help.solidworks.com/2025/english/api/swsimulationapi/Analyze_Part_Example_VB.htm) and [reaction-force/moment API](https://help.solidworks.com/2023/english/api/swsimulationapi/SolidWorks.Interop.cosworks~SolidWorks.Interop.cosworks.ICWResults~GetReactionForcesAndMoments.html): native-method references from the preserved structural methodology. The Phase 5 tessellation documentation page was inaccessible; actual readback and unchanged dirty flags, not remembered API semantics, support the extraction claim.

All technical figures are generated from this project's CAD tessellation, numerical exports or explicitly labelled analytical constructions. No AI-generated technical image, stock photograph, vendor drawing, supplier screenshot, logo or copied external simulation result is used. Publication preparation uses automated/AI-assisted engineering documentation and rendering workflows; the claims are tied to retained evidence rather than an assertion of unaided manual authorship.

SolidWorks is a third-party product. Its software, proprietary API bindings and native solver binaries are not distributed here. The owner approved the scoped MIT/CC BY 4.0 release; see `LICENSE_SCOPE.md`, `ATTRIBUTION.md` and `THIRD_PARTY_NOTICES.md`.
