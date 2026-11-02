# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""L01/B01: ideal quasi-static mesh free bodies. Loss model is separate."""
import math
import numpy as np

Z = np.array([0., 0., 1.])


def sharing_weights(kgamma, count=3):
    if count < 2 or not 1 <= kgamma <= count:
        raise ValueError('Require 1 <= Kgamma <= planet count')
    peak = kgamma/count
    return np.array([peak]+[(1-peak)/(count-1)]*(count-1))


def two_support_reactions(force, couple, z_load, z_a, z_b, axial_fraction=0.5):
    """Two ideal radial supports; axial split explicitly assumed, no moment capacity."""
    if z_b <= z_a or not 0 <= axial_fraction <= 1:
        raise ValueError('Invalid support span or axial split')
    f = np.asarray(force, dtype=float)
    m = np.asarray(couple, dtype=float).copy()
    if abs(m[2]) > 1e-10:
        raise ValueError('Drive torque must balance torsion separately from radial supports')
    span = z_b-z_a
    rb = -(z_load-z_a)/span*f + np.cross(Z,m)/span
    rb[2] = -(1-axial_fraction)*f[2]
    ra = -f-rb
    residual_m = np.cross((z_load-z_a)*Z,f)+np.cross(span*Z,rb)+m
    return dict(a_N=ra.tolist(), b_N=rb.tolist(), force_residual_N=(f+ra+rb).tolist(),
                moment_residual_Nm=residual_m.tolist())


def mesh_statics(gearset, input_torque_Nm, weights=None, application_factor=1.,
                 z_load=0.0036, z_a=-0.0101, z_b=-0.0041, z_output=0.021,
                 axial_fraction=0.5, external_output_force_N=None, external_output_z_m=None):
    """Signed sun torque; 120-degree branches; no mesh losses, inertial or external gravity loads."""
    if application_factor <= 0:
        raise ValueError('Application factor must be positive')
    w = np.ones(gearset.planets)/gearset.planets if weights is None else np.asarray(weights,float)
    if len(w)!=gearset.planets or np.any(w<0) or not np.isclose(sum(w),1,atol=1e-12):
        raise ValueError('Physical nonnegative sharing fractions must sum to one')
    g = gearset.geometry(); rs,rp,rr=g['pitch_radii_m']; orbit=g['orbit_m']
    total_t = input_torque_Nm*application_factor
    total_ft = total_t/rs
    sun_f=np.zeros(3); sun_m=np.zeros(3); ring_f=np.zeros(3); ring_m=np.zeros(3)
    carrier_f=np.zeros(3); carrier_m_output=np.zeros(3); branches=[]
    for j, fraction in enumerate(w):
        phi = j*2*math.pi/gearset.planets
        er=np.array([math.cos(phi),math.sin(phi),0.]); et=np.cross(Z,er)
        ft=total_ft*fraction
        # Radial separating load does not reverse when the drive flank reverses.
        fr=abs(ft)*math.tan(g['alpha_t_rad']); fa=ft*math.tan(gearset.beta)
        f_sp=ft*et+fr*er-fa*Z
        f_rp=ft*et-fr*er+fa*Z
        planet_f=f_sp+f_rp
        planet_m=np.cross(-rp*er,f_sp)+np.cross(rp*er,f_rp)
        fs=-f_sp; fs_m=np.cross(rs*er,fs)
        frg=-f_rp; frg_m=np.cross(rr*er,frg)
        sun_f+=fs;sun_m+=fs_m;ring_f+=frg;ring_m+=frg_m
        carrier_f+=planet_f
        carrier_m_output+=np.cross(orbit*er+(z_load-z_output)*Z,planet_f)+planet_m
        branches.append(dict(index=j+1,weight=float(fraction),Ft_N=float(ft),Fr_N=float(fr),
            axial_each_mesh_N=float(abs(fa)),normal_force_N=float(abs(ft)/(math.cos(gearset.alpha_n)*math.cos(gearset.beta))),
            planet_mesh_force_N=planet_f.tolist(),planet_mesh_couple_Nm=planet_m.tolist(),
            required_bearing_force_on_planet_N=(-planet_f).tolist(),
            required_bearing_moment_on_planet_Nm=(-planet_m).tolist(),
            planet_bearing_radial_N=float(np.linalg.norm(planet_f[:2])),
            planet_bearing_nominal_axial_N=float(abs(planet_f[2])),
            uncancelled_axial_triangle_bound_N=float(2*abs(fa)),
            planet_tipping_moment_Nm=float(np.linalg.norm(planet_m[:2]))))
    sun_couple=sun_m.copy();sun_couple[2]=0
    supports=two_support_reactions(sun_f,sun_couple,z_load,z_a,z_b,axial_fraction)
    external_f=np.zeros(3) if external_output_force_N is None else np.asarray(external_output_force_N,float)
    if np.linalg.norm(external_f)>0 and external_output_z_m is None:
        raise ValueError('External output force requires its application plane')
    if external_output_z_m is not None:
        carrier_m_output+=np.cross((external_output_z_m-z_output)*Z,external_f)
    carrier_f+=external_f
    residual=carrier_m_output.copy();residual[2]=0
    output_reaction=-carrier_f
    return dict(model='IDEAL_QUASISTATIC; loss and dynamic force redistribution excluded',
        applied_sun_torque_Nm=total_t, nominal_input_torque_Nm=input_torque_Nm,
        Kgamma=float(gearset.planets*max(w)),weights=w.tolist(),branches=branches,
        sun_mesh_force_N=sun_f.tolist(),sun_mesh_moment_Nm=sun_m.tolist(),
        input_bearing_reactions=supports,ring_mesh_force_N=ring_f.tolist(),ring_mesh_moment_Nm=ring_m.tolist(),
        required_ground_ring_torque_Nm=float(-ring_m[2]),
        ideal_output_torque_Nm=gearset.ratio*total_t,
        carrier_external_force_N=carrier_f.tolist(),output_bearing_reaction_N=output_reaction.tolist(),
        output_point_support_unresolved_moment_Nm=residual.tolist(),
        output_point_support_status='BALANCED_IDEAL' if np.linalg.norm(residual)<1e-11 else 'MOMENT_CAPACITY_REQUIRED_UNVERIFIED',
        carrier_mesh_torque_Nm=float(carrier_m_output[2]),
        total_force_residual_N=(sun_f+ring_f+carrier_f-external_f).tolist(),
        global_torque_residual_Nm=float(total_t-ring_m[2]-gearset.ratio*total_t))
