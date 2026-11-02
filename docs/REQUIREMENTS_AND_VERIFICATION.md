# Requirements and verification

B/D/P/U classifications remain separate. No unknown acceptance value is populated from a hypothetical screen.

| ID | Class | Requirement | Evidence / status |
| --- | --- | --- | --- |
| R01 | Verified baseline | Counts/topology | 12/48/108; 3 planets; fixed ring; PASS_NATIVE_OBSERVATION |
| R02 | Derived | Reduction ratio | 10:1 ideal fixed-ring relation; PASS_ANALYTICAL |
| R03 | Verified baseline | Proper static diameter <=80 mm | 79.681688 mm; pose/exclusions bounded; PASS_STATIC_ONLY |
| R04 | Verified baseline | Gearbox-body thickness <=40 mm | 39.5 mm; full projections 59 mm; PASS_STATIC_ONLY |
| R05 | Verified baseline | Six bearing envelopes | 7 x 19 x 6 mm; functions distinct; PASS_NOMINAL_ONLY |
| R06 | Unknown | Coincident torque-speed-duration/life | Not established; UNVERIFIED |
| R07 | Unknown | Qualified printed properties/allowables | E/nu/rho used only as hypotheses; UNVERIFIED |
| R08 | Derived | Force/torque/moment conservation | Explicit branches, reference points and residuals; PASS_MODEL_INVARIANTS |
| R09 | Derived | Output equilibrium in exported fields | P3:9; P3B:11 incl reuse; P4A:17 incl reuse; PASS_EXPORTED_FIELDS_ONLY |
| R10 | Provisional | Output peak/probe local refinement | Final P3B peak .24%; mean .22%; probe 1.48%; CONDITIONAL_PASS |
| R11 | Unknown | Bearing finite-width moment load path | Point model incomplete; actual compliance unknown; OPEN |
| R12 | Provisional | Support robustness | 34.07% carrier x-tilt sensitivity; CONDITIONAL_MODEL_COMPARISON |
| R13 | Provisional | Modified peak reduction >=5% | R0.20 +2.868%; R0.35 +3.010%; FAIL_IMPROVEMENT_GATE_BASELINE_RETAINED |
| R14 | Baseline/derived | Retain constrained candidate dimensions | Throat/journal/hex envelope retained; land reduced; PASS_NOMINAL_CONTACT_UNVERIFIED |
| R15 | Provisional | Compliance penalty <=2% | Energy penalties .187% / .524%; PASS_CONDITIONAL_PROXY |
| R16 | Provisional | Mass increase <=1% | Assumed-density mass decreases <.006%; PASS_NOMINAL_MODEL |
| R17 | Derived | Document realized mesh settings | Post-mesh minimum .005 mm versus requested h/2; DECLARED_DEVIATION_RECONCILED |
| R18 | Unknown | Tolerance-dependent structural ranking | 63 scalar geometry cases; no tolerance FEA; UNVERIFIED |
| R19 | Unknown | Complete backlash / stiffness | Mesh-only deadband and component proxies only; UNVERIFIED_SYSTEM |
| R20 | Unknown | Measured efficiency / continuous thermal duty | Loss/heat parameters unqualified; UNVERIFIED |
| R21 | Unknown | Physical validation / certified capacity | No hardware tests; no capacity rating; NOT_ESTABLISHED |
| R22 | Evidence integrity | Preserve earlier evidence | Approved GEN/MAS exception retained; 2548 files guarded; PASS_NO_NEW_EXCEPTION |
| R23 | Release gate | Public ownership/license approval | Owner confirmed rights; MIT code / CC BY 4.0 documentation and figures; APPROVED_FOR_PUBLIC_PACKAGE |
