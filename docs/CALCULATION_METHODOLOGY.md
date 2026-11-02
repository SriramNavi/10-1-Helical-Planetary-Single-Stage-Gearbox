# Calculation methodology

The portable package retains the Phase 2 numerical model, with a public runner that has no CAD import, proprietary API dependency, procurement path or source-workspace mutation. SI units are used internally; presentation tables may use mm, MPa and mrad.

## Geometry and kinematics

`mt=mn/cos(beta)`; `alpha_t=atan(tan(alpha_n)/cos(beta))`; `r=mt*z/2`.

`a=rs+rp=rr-rp`. The external path length is `sqrt(ra_s^2-rb_s^2)+sqrt(ra_p^2-rb_p^2)-a*sin(alpha_t)`; divide by `pi*mt*cos(alpha_t)` for the transverse contact ratio. The internal path uses the planet term minus the internal-ring tip term plus `a*sin(alpha_t)`. `eps_beta=b*abs(sin(beta))/(pi*mn)`. Stub/root assumptions are explicit; generated-root and loaded-contact qualification are absent.

`zs*(ws-wc)+zr*(wr-wc)=0`; `zp*(wp-wc)=-zs*(ws-wc)`.

## Forces and support equilibrium

`Td=KA*Tin`, `sum(wi)=1`, `Kgamma=N*max(wi)`; do not multiply every branch by Kgamma while preserving the same total torque. `Ft_i=Td*wi/rs`; `Fr_i=abs(Ft_i)*tan(alpha_t)`; `Fa_i=Ft_i*tan(beta)`.

For a planet, sun/ring tangential forces add, radial components oppose, axial components cancel in the ideal case, and axial forces leave a transverse couple `2*rp*Fa`. All force/couple vectors retain their reference points. Frame shifts use `M_B=M_A-r_AB cross F`. An unresolved couple is reported rather than assigned to an ideal point bearing.

## Simplified stress and compliance

Lewis demand: `sigma_F=Kface*abs(Ft)/(b*mn*Y)`; Y and face factors are hypotheses. No full ISO/JGMA/AGMA rating is claimed.

Isotropic pitch-point cylinder surrogate: `1/Eprime=sum((1-nu^2)/E)`, `1/Rprime=1/rho1 +/- 1/rho2`, `aH=sqrt(4*Fline*Rprime/(pi*b*Eprime))`, `p0=sqrt(Fline*Eprime/(pi*b*Rprime))`. The internal curvature uses subtraction. Skew contact, friction, roughness, wear and viscoelasticity are unresolved; the surrogate is not asserted conservative.

Circular sections: `I=pi*d^4/64`, `J=pi*d^4/32`, `sigma_b=32*M/(pi*d^3)`, `tau=16*T/(pi*d^3)`, `theta=T*L/(G*J)`. Short-member shear-energy terms remain assumptions; hole/hex geometry is not represented by an unnotched circular stress. Input compliance reflects to output as `Cs/i^2`.

## Power, clearance, life and uncertainty

Power balance separates nominal loss assumptions from design-multiplied force cases. Reference mesh eta=0.98 and bearing drag=1e-4 N m at nominal Tin=0.01 N m and input 10 rad/s predict 0.93661 efficiency; that is not an efficiency measurement or operating recommendation. The 216-point grid retains 36 infeasible assumed motoring points and 54 static cases with undefined efficiency.

Mesh-only full deadband is `(j_sp+j_pr)/(2*a)=0.010801065 rad`, or 0.618855 deg, using the two assumed 0.20 mm transverse clearances. Complete backlash remains unknown. Basic ball-bearing `L10=1e6*(C/P)^3` requires manufacturer factors and actual relative speed; actual bearing life is null. Thermal rise equations require unknown thermal resistance, heat capacity, allowable material temperature and duty.

The 1,944-point deterministic uncertainty grid is not a statistical confidence interval. Partial conditional component ceilings exclude unresolved gates and are never converted into a system torque rating. The public runner retains null system-capacity fields. Sixty-two mathematical tests and four archived-value comparisons verify software/model arithmetic, not hardware performance.
