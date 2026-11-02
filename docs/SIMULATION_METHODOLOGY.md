# Simulation methodology

## Scope and native preparation

Native SolidWorks Simulation 2025 static studies were executed in independent workspaces. The original assembly was never rebuilt or saved. Phase 3 remapped 23 native documents and checked 37 reference edges / 79 live component nodes. The exact commercial license SKU was not established; capability is supported by successful solves. Proprietary bindings, commercial binaries and native CAD/CWR archives are excluded from this public package.

## Loads, materials and restraints

The output model fixes the broad underside at z=13.9 mm and applies distributed end torque Tz=0.15 N m at z=34 mm. An alternative fixes the three tie-hole barrels. End loading does not reproduce actual hex/collar/fastener contact. Carrier models use two original solids, rigid end coupling and a finite journal foundation, with bonded-contact/load-transfer limitations. Radial-only support removes journal axial restraint; it does not identify a real bearing compliance.

Hypothetical isotropic E=1.2e9 Pa, nu=0.35 and density=1230 kg/m3 are assigned/read back. No qualified strength/yield allowable is assigned. Quadratic high-quality solid elements are used. Output soft springs, inertial relief and large-displacement options are disabled. Solver configuration/return codes, material readback, node/element counts, boundary node mapping and diagnostics remain in the private authoritative run records.

Phase 4A's combined end-wrench screen adds Mx=0.0704769466 and My=-0.0218382141 N m to Mz=0.15 N m. These Phase 2 overturning components are deliberately reassigned to the output end for sensitivity, not asserted to be a verified coincident application load. Alternative cases have one fine mesh and no independent convergence claim.

## Numerical verification

Reactions satisfy `sum(R)+sum(F)=0` and `sum(x cross R + Mnodal)+sum(Mapplied + r cross F)=0` about the same origin. Moment residual tolerance is 0.001 relative; zero-resultant-force cases use the declared characteristic force normalization. Native six-component stresses are independently recombined into von Mises. Displacement norms and relevant section rotations are checked where exported.

Phase 3B's seven-level local standard series resolves peak/area/probe trends. Phase 4A uses three local face-control levels per modified candidate: 0.160,0.125,0.100 mm, global maximum 1.2 mm. The pre-mesh requested minimum h/2 differs from the post-mesh API MinElementSize=0.005 mm in all 13 successful curvature cases. The exact API overwrite/interpretation behavior and actual minimum edge length remain unverified. Compare the realized common protocol; do not claim an h/2-minimum refinement sequence.

The Phase 4A common bore patch uses |x|=2.00..2.45 mm and radius 1.20 mm. Fixed probes use x=-2.25,0,+2.25 mm at angles 30,150,210,330 deg. This differs from the Phase 3B mouth patch because the latter is trimmed by candidate fillets. Mean/probe values from those patches are not interchangeable. Final-step criteria: peak 5%, area mean 2%, worst fixed probe 5%, displacement 2%, energy 2%. The finite criteria are not an asymptotic error estimate or proof that all singularities/contact artifacts are absent.

Whole-component energy stiffness T^2/(2U) applies to a pure-torque case. A fitted shaft gauge is a separate measure; combined-load energy is not relabelled pure torsion. Modulus was not tuned to force agreement.

## Failures and limits

Retained failures include four initial output peak-convergence failures; an unsupported remote setup; failed explicit-band preparation with zero band solves; two standard fine blend mesh return-8 cases; no-load startup diagnostics despite load readback; missing fresh-template material; and an invalid-LBC suppression diagnostic. A zero native return code with no usable result was not accepted. The precise intermittent startup cause remains unresolved. Native estimated error indicators and SVD text are not automatically interpreted as local stress error bounds or singularities.

Phase 3 has 24 successful solves but only nine independent exported-field equilibrium checks. Phase 3B has nine new solves and 11 checked fields including two reused; Phase 4A has 16 successful solves, eight unusable attempts and 17 checked fields including one reused. These are conditional simulations, not physical experiments. No torque capacity, fatigue limit, actual bearing life or thermal duty is established.
