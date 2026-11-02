# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""Simplified demands, elastic surrogates, and conditional capacities (R3–R6)."""
import math
import numpy as np


def positive(*values):
    if any(not math.isfinite(x) or x <= 0 for x in values):
        raise ValueError('Finite positive physical parameters required')


def material_moduli(E, nu):
    positive(E)
    if not -1 < nu < .5: raise ValueError('Invalid isotropic Poisson ratio')
    return E/(2*(1+nu))


def lewis_stress(Ft, width, module, Y, face_factor=1.):
    positive(width,module,Y,face_factor)
    return abs(Ft)*face_factor/(width*module*Y)


def hertz_line(force, length, radius1, radius2, E1, nu1, E2, nu2, internal=False):
    """Transverse pitch-point elastic-cylinder surrogate, NOT full helical/ISO rating."""
    positive(length,radius1,radius2,E1,E2)
    if force < 0 or not (-1<nu1<.5 and -1<nu2<.5): raise ValueError('Invalid load/material')
    curvature=1/radius1+(-1 if internal else 1)/radius2
    if curvature <= 0: raise ValueError('Non-positive reduced curvature')
    radius=1/curvature
    effective_E=1/((1-nu1*nu1)/E1+(1-nu2*nu2)/E2)
    halfwidth=math.sqrt(4*force*radius/(math.pi*length*effective_E))
    pressure=math.sqrt(force*effective_E/(math.pi*length*radius))
    return dict(p0_Pa=pressure,half_width_m=halfwidth,effective_E_Pa=effective_E,reduced_radius_m=radius)


def section(d):
    positive(d)
    return dict(A_m2=math.pi*d*d/4,I_m4=math.pi*d**4/64,J_m4=math.pi*d**4/32)


def cantilever_compliance(length,d,E,nu,kappa=6/7):
    positive(length,kappa);q=section(d);G=material_moduli(E,nu)
    EI=E*q['I_m4']
    return np.array([[length**3/(3*EI)+length/(kappa*G*q['A_m2']), length**2/(2*EI)],
                     [length**2/(2*EI),length/EI]])


def overhung_compliance(span,overhang,d,E,nu,kappa=6/7,include_shear=True):
    """Tip force/couple flexibility; simple supports, uniform shaft, Timoshenko shear energy."""
    positive(span,overhang,kappa);q=section(d);G=material_moduli(E,nu);EI=E*q['I_m4']
    L,h=span,overhang
    matrix=np.array([[h*h*(L+h)/(3*EI),(h*L/3+h*h/2)/EI],
                     [(h*L/3+h*h/2)/EI,(L/3+h)/EI]])
    if include_shear:
        matrix+=np.array([[h*h/L+h,h/L],[h/L,1/L]])/(kappa*G*q['A_m2'])
    return matrix


def cantilever_load(force_xy,couple_xy,length,d,E,nu):
    f=np.asarray(force_xy,float);m=np.asarray(couple_xy,float)
    equivalent_m=np.array([m[1],-m[0]])
    C=cantilever_compliance(length,d,E,nu)
    disp=C[0,0]*f+C[0,1]*equivalent_m
    root_m=np.array([-length*f[1],length*f[0]])+m
    sigma=32*np.linalg.norm(root_m)/(math.pi*d**3)
    return dict(tip_displacement_m=disp.tolist(),bending_demand_Pa=float(sigma),
                root_bending_moment_Nm=root_m.tolist(),length_over_diameter=length/d,
                limitation='Short-pin uniform isotropic surrogate; no notch, contact, plate flexure or validated restraint.')


def torsion(length,d,E,nu,torque=1.):
    positive(length);G=material_moduli(E,nu);q=section(d)
    compliance=length/(G*q['J_m4'])
    return dict(compliance_rad_Nm=compliance,stiffness_Nm_rad=1/compliance,
                twist_rad=torque*compliance,shear_demand_Pa=16*abs(torque)/(math.pi*d**3))


def equivalent_dynamic_load(Fr,Fa,X,Y,V):
    if min(Fr,Fa,X,Y,V)<0 or V==0: raise ValueError('Invalid bearing factors/loads')
    return max(V*Fr,X*V*Fr+Y*Fa)


def bearing_basic_life(C,P,omega):
    positive(C)
    if P<0: raise ValueError('Negative equivalent load')
    if P==0: return dict(revolutions=None,hours=None,status='ZERO_LOAD_FORMULA_NOT_A_SERVICE_LIFE')
    revolutions=1e6*(C/P)**3
    return dict(revolutions=revolutions,hours=None if omega==0 else revolutions*2*math.pi/(abs(omega)*3600),
                status='CONDITIONAL_L10_ONLY; excludes moment, lubrication, minimum load and maker mismatch')


def variable_load_equivalent(loads,speeds,fractions):
    if not len(loads)==len(speeds)==len(fractions) or min(loads+speeds+fractions)<0 or not math.isclose(sum(fractions),1):
        raise ValueError('Nonnegative equal-length arrays and normalized time fractions required')
    rotations=sum(n*f for n,f in zip(speeds,fractions))
    if rotations==0:return None
    return (sum(p**3*n*f for p,n,f in zip(loads,speeds,fractions))/rotations)**(1/3)


def output_compliance(gearset,E,nu,pin_length,pin_d,input_length,input_d,output_length,output_d,
                      weights,mesh_stiffness_sp=None,mesh_stiffness_pr=None):
    g=gearset.geometry();a=g['orbit_m'];rs,rp,_=g['pitch_radii_m']
    Cs=torsion(input_length,input_d,E,nu)['compliance_rad_Nm']/gearset.ratio**2
    Co=torsion(output_length,output_d,E,nu)['compliance_rad_Nm']
    Cpin=cantilever_compliance(pin_length,pin_d,E,nu)
    # dF/dTout = w/a; dMtip/dTout = rp*tan(beta)*w/a, orthogonal bending planes.
    branch_factor=sum(x*x for x in weights)/a**2
    Cp=branch_factor*(Cpin[0,0]+Cpin[1,1]*(rp*math.tan(gearset.beta))**2)
    Cm=None
    if mesh_stiffness_sp is not None and mesh_stiffness_pr is not None:
        positive(mesh_stiffness_sp,mesh_stiffness_pr)
        Cm=sum(x*x for x in weights)/(4*a*a)*(1/mesh_stiffness_sp+1/mesh_stiffness_pr)
    known=Cs+Co+Cp+(Cm or 0)
    return dict(input_shaft_referred_rad_Nm=Cs,output_core_rad_Nm=Co,
                prescribed_sharing_pin_energy_rad_Nm=Cp,mesh_rad_Nm=Cm,
                modeled_compliance_rad_Nm=known,modeled_subsystem_stiffness_Nm_rad=1/known,
                complete_gearbox_stiffness_Nm_rad=None,
                limitation='Hypothetical elastic surrogate; bearing, housing, hex contacts and joint compliance unresolved. Pin energy uses prescribed sharing, not a solved stiffness distribution.')
