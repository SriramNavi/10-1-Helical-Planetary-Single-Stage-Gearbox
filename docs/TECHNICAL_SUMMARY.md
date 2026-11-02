# GB10-V2 technical summary

**Decision: retain the original output core. No qualified operating gearbox or torque rating is established.**

GB10-V2 is a single-stage helical planetary demonstrator with 12/48/108 teeth, three planets, fixed ring, sun input and carrier output. Native-audited static gearbox-body packaging is 79.681688 mm diameter x 39.5 mm thickness, inside the 80/40 mm limits with documented shaft/adapter exclusions. The six nominal 7 x 19 x 6 mm bearings have distinct support functions. Gearbox-body measurements apply the documented shaft/adapter exclusions; the full audited axial assembly span is 59 mm.

The investigation progressed from a frozen CAD/provenance audit through independent mechanics, native static FEA, numerical closure and a controlled local geometry comparison. Sixty-two analytical tests passed. Structural work executed 24, nine and 16 successful new static solves in Phases 3,3B,4A respectively; verification coverage and reused fields are disclosed rather than summed as independent tests.

The analytical model closes signed branch loads and identifies a 0.07378 N m hypothetical output transverse couple that an ideal point bearing cannot silently react. Zero net axial force on a planet does not eliminate its tipping couple. Carrier rear-plate x tilt changes by 34.07% when journal axial restraint is removed in the coarse native comparison, exposing support-model sensitivity.

Seven local refinements closed the declared output stress/probe trend at 15.241717 MPa under prescribed 0.15 N m, E=1.2 GPa, nu=0.35. The matched curvature baseline for local geometry comparison is 15.156654 MPa; these are different numerical protocols, not different certified capacities.

| Geometry | Peak MPa | Change | Decision |
| --- | --- | --- | --- |
| Baseline | 15.1567 | Reference | Retain |
| R0.20 mm | 15.5914 | +2.868% | No benefit |
| R0.35 mm | 15.6129 | +3.010% | No benefit |

Both fillets pass finite nominal refinement but fail the provisional 5% stress-improvement objective. They reduce bore land/flat area and slightly increase whole-component energy compliance. Seventeen Phase 4A exported equilibrium fields pass, including one frozen reuse; eight unusable attempts and the realized minimum mesh-setting discrepancy remain documented.

The demonstrated competencies are transmission mechanics, native geometric interrogation, analytical software, structural simulation, numerical verification, controlled computational experimentation and evidence-based trade-off decisions. This project does not demonstrate implemented controls/electronics or physically qualified robotic actuation.

Unverified gates include printed-material anisotropy/creep/fatigue/temperature, actual duty, bearing identity/compliance/capacity, physical contacts/retention, tolerance-dependent structural ranking, actual efficiency/backlash/stiffness and endurance. Future physical work requires a separately approved plan. Authoritative CAD and prior phase evidence remain preserved, including the earlier approved GEN/MAS exception.

The public package replays equations and selected data without CAD/FEA. Full native reproduction needs the retained private CAD/study archives and licensed commercial environment. The owner approved GitHub publication: public source code is MIT; engineering documentation and figures are CC BY 4.0. Private native CAD/FEA assets remain excluded; live portfolio deployment is outside this authorization.
