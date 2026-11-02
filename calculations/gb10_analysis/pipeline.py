# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""Composition of separately identified ideal-force and hypothetical strength models."""
import math
import numpy as np
from .geometry import Gearset
from .statics import mesh_statics, sharing_weights
from .mechanics import (lewis_stress, hertz_line, torsion, cantilever_load,
                        overhung_compliance, section, output_compliance)


def screen(inputs,torque=None,kgamma=None,E=None,Y=None,face_factor=None,notch_factor=1.):
    gear=Gearset(**inputs['baseline']);g=gear.geometry();p=inputs['geometry_surrogates'];r=inputs['reference_screen']
    T=r['input_torque_Nm'] if torque is None else torque
    kg=r['Kgamma'] if kgamma is None else kgamma
    E=r['E_Pa'] if E is None else E
    Y=r['Y_sun'] if Y is None else Y
    face=r['face_factor'] if face_factor is None else face_factor
    nu=r['nu'];weights=sharing_weights(kg)
    s=mesh_statics(gear,T,weights,r['application_factor'],p['mesh_load_plane_m'],
        *p['input_bearing_centers_m'],p['output_bearing_center_m'],r['bearing_axial_split'])
    peak=max(s['branches'],key=lambda b:abs(b['Ft_N']));ft=abs(peak['Ft_N']);rs,rp,rr=g['pitch_radii_m']
    alpha=g['alpha_t_rad'];normal_transverse=ft/math.cos(alpha)*face
    hp=hertz_line(normal_transverse,gear.width,rs*math.sin(alpha),rp*math.sin(alpha),E,nu,E,nu)
    hr=hertz_line(normal_transverse,gear.width,rp*math.sin(alpha),rr*math.sin(alpha),E,nu,E,nu,True)
    pin=cantilever_load(peak['planet_mesh_force_N'][:2],peak['planet_mesh_couple_Nm'][:2],
                       p['pin_effective_length_m'],p['journal_diameter_m'],E,nu)
    input_t=s['applied_sun_torque_Nm'];output_t=s['ideal_output_torque_Nm']
    ti=torsion(p['input_effective_torsion_length_m'],p['input_equivalent_core_diameter_m'],E,nu,input_t)
    to=torsion(p['output_effective_torsion_length_m'],p['output_equivalent_core_diameter_m'],E,nu,output_t)
    L=p['input_bearing_centers_m'][1]-p['input_bearing_centers_m'][0]
    h=p['mesh_load_plane_m']-p['input_bearing_centers_m'][1]
    C=overhung_compliance(L,h,p['journal_diameter_m'],E,nu)
    F=np.array(s['sun_mesh_force_N'][:2]);M=np.array(s['sun_mesh_moment_Nm'][:2]);Mconj=np.array([M[1],-M[0]])
    u=C[0,0]*F+C[0,1]*Mconj
    mfront=np.array([-h*F[1],h*F[0]])+M
    bend=32*max(np.linalg.norm(mfront),np.linalg.norm(M))/(math.pi*p['journal_diameter_m']**3)
    axial=abs(s['sun_mesh_force_N'][2])/section(p['journal_diameter_m'])['A_m2']
    journal_tau=16*abs(input_t)/(math.pi*p['journal_diameter_m']**3)
    vm=math.sqrt((bend+axial)**2+3*journal_tau**2)*notch_factor
    compliance=output_compliance(gear,E,nu,p['pin_effective_length_m'],p['journal_diameter_m'],
        p['input_effective_torsion_length_m'],p['input_equivalent_core_diameter_m'],
        p['output_effective_torsion_length_m'],p['output_equivalent_core_diameter_m'],weights)
    return dict(statics=s,root_sun_Pa=lewis_stress(ft,gear.width,gear.mn,Y,face),
        root_planet_Pa=lewis_stress(ft,gear.width,gear.mn,r['Y_planet'],face),
        ring_root_Pa=None,external_contact_Pa=hp['p0_Pa'],internal_contact_Pa=hr['p0_Pa'],
        contact_model='Transverse pitch-point cylinder; not full skew helical contact',
        contact_half_width_m=hp['half_width_m'],pin=pin,
        input_core_torsion=ti,output_core_torsion=to,
        input_core_equivalent_von_mises_Pa=math.sqrt(3)*ti['shear_demand_Pa']*notch_factor,
        output_core_equivalent_von_mises_Pa=math.sqrt(3)*to['shear_demand_Pa']*notch_factor,
        input_journal_equivalent_demand_Pa=float(vm),input_beam_deflection_m=u.tolist(),
        compliance=compliance,notch_factor=notch_factor,
        status='CONDITIONAL_ISOTROPIC_SCREEN; not full structural or bearing equilibrium qualification')


def partial_limits(inputs,kgamma=None,E=None,Y=None,root_allowable=None,contact_allowable=None,
                   shaft_allowable=None,face_factor=None,notch_factor=1.):
    """Unit-torque demand coefficients; no actual safe system capacity is returned."""
    unit=screen(inputs,torque=1.,kgamma=kgamma,E=E,Y=Y,face_factor=face_factor,notch_factor=notch_factor)
    r=inputs['reference_screen']
    ar=r['hypothetical_root_service_allowable_Pa'] if root_allowable is None else root_allowable
    ah=r['hypothetical_contact_service_allowable_Pa'] if contact_allowable is None else contact_allowable
    ash=r['hypothetical_shaft_service_allowable_Pa'] if shaft_allowable is None else shaft_allowable
    if min(ar,ah,ash)<=0:raise ValueError('Conditional allowables must be positive')
    limits={
        'sun_Lewis': ar/(r['root_safety_factor']*unit['root_sun_Pa']),
        'planet_Lewis': ar/(r['root_safety_factor']*unit['root_planet_Pa']),
        'external_cylinder_contact':(ah/(r['contact_pressure_safety_factor']*unit['external_contact_Pa']))**2,
        'internal_cylinder_contact':(ah/(r['contact_pressure_safety_factor']*unit['internal_contact_Pa']))**2,
        'input_journal_surrogate':ash/(r['shaft_safety_factor']*unit['input_journal_equivalent_demand_Pa']),
        'input_circular_core':ash/(r['shaft_safety_factor']*unit['input_core_equivalent_von_mises_Pa']),
        'output_circular_core':ash/(r['shaft_safety_factor']*unit['output_core_equivalent_von_mises_Pa']),
        'planet_cantilever_bending':ash/(r['shaft_safety_factor']*unit['pin']['bending_demand_Pa']),
    }
    governing=min(limits,key=limits.get)
    return dict(conditional_component_input_limits_Nm=limits,partial_model_governing_component=governing,
        partial_conditional_input_ceiling_Nm=limits[governing],system_allowable_input_torque_Nm=None,
        unresolved_gates=['Actual allowables and service duty','Planet bearing tipping-moment capacity',
                          'Output bearing moment support under unequal sharing/external loading',
                          'Internal ring root and housing/bolt/nut retention',
                          'Cross holes, real hex contacts, creep, fatigue, wear and thermal limits'],
        status='INCOMPLETE_HYPOTHETICAL_COMPONENT_ENVELOPE; NOT A TORQUE RATING')
