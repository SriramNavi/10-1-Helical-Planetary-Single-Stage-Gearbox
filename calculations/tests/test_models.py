# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
import dataclasses
import json
import math
import random
import unittest
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from gb10_analysis.geometry import Gearset
from gb10_analysis.statics import mesh_statics,sharing_weights,two_support_reactions
from gb10_analysis.mechanics import (lewis_stress,hertz_line,section,material_moduli,
    cantilever_compliance,overhung_compliance,torsion,bearing_basic_life,
    variable_load_equivalent,equivalent_dynamic_load,output_compliance)
from gb10_analysis.losses import power_flow,thermal_rise,required_thermal_resistance
from gb10_analysis.pipeline import screen,partial_limits

INPUTS=json.loads((Path(__file__).resolve().parents[1]/'inputs/parameters.json').read_text())


class GeometryTests(unittest.TestCase):
    def setUp(self):self.s=Gearset();self.g=self.s.geometry()
    def test_ratio(self):self.assertEqual(self.s.ratio,10)
    def test_centers_independent(self):self.assertAlmostEqual(self.g['orbit_m'],self.g['internal_center_m'])
    def test_native_orbit_crosscheck(self):self.assertAlmostEqual(self.g['orbit_m'],.018516693241080868,places=14)
    def test_phasing(self):self.assertTrue(self.g['equal_spacing_compatible']);self.assertEqual(self.g['phasing_integer'],40)
    def test_contacts_historical_scalar_crosscheck(self):
        c=INPUTS['historical_comparators_not_certificates']
        for key,old in [('external_contact_ratio','contact_ratio_sp'),('internal_contact_ratio','contact_ratio_pr'),('overlap_ratio','overlap_ratio')]:
            self.assertAlmostEqual(self.g[key],c[old],places=11)
    def test_spur_limit(self):self.assertEqual(dataclasses.replace(self.s,beta=0).geometry()['overlap_ratio'],0)
    def test_overlap_reverse_hand(self):self.assertEqual(dataclasses.replace(self.s,beta=-self.s.beta).geometry()['overlap_ratio'],self.g['overlap_ratio'])
    def test_root_radial_clearance(self):
        self.assertAlmostEqual(self.g['orbit_m']-self.g['tip_radii_m'][0]-self.g['root_radii_m'][1],.000232)
    def test_backlash_linear(self):
        doubled=dataclasses.replace(self.s,backlash_sp=.0004,backlash_pr=.0004)
        self.assertAlmostEqual(doubled.geometry()['output_mesh_backlash_rad'],2*self.g['output_mesh_backlash_rad'])
    def test_backlash_constraint_interval_independent(self):
        # Subtract the two signed mesh constraints: 2a*dtheta_c = eps2-eps1.
        a=self.g['orbit_m'];j1=self.s.backlash_sp;j2=self.s.backlash_pr
        extremes=[(e2-e1)/(2*a) for e1 in [-j1/2,j1/2] for e2 in [-j2/2,j2/2]]
        self.assertAlmostEqual(max(extremes)-min(extremes),self.g['output_mesh_backlash_rad'])
    def test_kinematics_independent_linear_solve(self):
        for ws,wr in [(1,0),(-10,0),(2,3),(0,7)]:
            A=np.array([[-60,48],[-60,-48]])
            c,p=np.linalg.solve(A,[-12*ws,-108*wr]);r=self.s.kinematics(ws,wr)
            self.assertAlmostEqual(c,r['carrier_rad_s']);self.assertAlmostEqual(p,r['planet_absolute_rad_s'])
    def test_rigid_rotation(self):
        k=self.s.kinematics(5,5);self.assertEqual(k['carrier_rad_s'],5);self.assertEqual(k['planet_absolute_rad_s'],5)
    def test_relative_planet_speed(self):self.assertAlmostEqual(self.s.kinematics(1)['planet_relative_carrier_rad_s'],-.225)
    def test_invalid_teeth(self):
        with self.assertRaises(ValueError):Gearset(zr=109)
    def test_angle_units_guard(self):
        with self.assertRaises(ValueError):Gearset(beta=20)


class EquilibriumTests(unittest.TestCase):
    def setUp(self):self.s=Gearset()
    def test_random_equilibrium(self):
        rng=random.Random(23)
        for _ in range(40):
            T=rng.uniform(-2,2);k=rng.uniform(1,3)
            r=mesh_statics(self.s,T,sharing_weights(k))
            np.testing.assert_allclose(r['total_force_residual_N'],0,atol=1e-11)
            self.assertAlmostEqual(r['global_torque_residual_Nm'],0,places=11)
            np.testing.assert_allclose(r['input_bearing_reactions']['force_residual_N'],0,atol=1e-11)
            np.testing.assert_allclose(r['input_bearing_reactions']['moment_residual_Nm'],0,atol=1e-11)
            self.assertAlmostEqual(r['carrier_mesh_torque_Nm'],10*T,places=10)
    def test_equal_sharing_radial_balance(self):
        r=mesh_statics(self.s,.01)
        np.testing.assert_allclose(r['sun_mesh_force_N'][:2],0,atol=1e-12)
        np.testing.assert_allclose(r['output_point_support_unresolved_moment_Nm'],0,atol=1e-12)
    def test_cancellation_does_not_remove_planet_tipping(self):
        r=mesh_statics(self.s,.01);b=r['branches'][0];rp=self.s.geometry()['pitch_radii_m'][1]
        self.assertAlmostEqual(b['planet_bearing_nominal_axial_N'],0)
        self.assertAlmostEqual(b['planet_tipping_moment_Nm'],2*rp*b['axial_each_mesh_N'])
        self.assertGreater(b['planet_tipping_moment_Nm'],0)
    def test_sun_and_ring_axial_reactions(self):
        r=mesh_statics(self.s,.01)
        self.assertAlmostEqual(r['sun_mesh_force_N'][2],-r['ring_mesh_force_N'][2])
    def test_unequal_sharing_moment_gap(self):
        r=mesh_statics(self.s,.01,sharing_weights(2))
        self.assertEqual(r['output_point_support_status'],'MOMENT_CAPACITY_REQUIRED_UNVERIFIED')
    def test_spur_tipping_zero(self):
        r=mesh_statics(dataclasses.replace(self.s,beta=0),.01)
        self.assertEqual(r['branches'][0]['planet_tipping_moment_Nm'],0)
    def test_input_axial_split_extremes(self):
        for fraction in [0,.5,1]:
            r=mesh_statics(self.s,.01,axial_fraction=fraction);f=r['sun_mesh_force_N'][2]
            self.assertAlmostEqual(r['input_bearing_reactions']['a_N'][2],-fraction*f)
    def test_ring_torque(self):self.assertAlmostEqual(mesh_statics(self.s,.01)['required_ground_ring_torque_Nm'],.09)
    def test_zero_torque(self):
        r=mesh_statics(self.s,0)
        self.assertEqual(r['branches'][0]['planet_tipping_moment_Nm'],0)
    def test_one_planet_limit(self):self.assertEqual(sharing_weights(3).tolist(),[1,0,0])
    def test_physical_weights_reject(self):
        with self.assertRaises(ValueError):mesh_statics(self.s,.01,[.5,.5,.5])
    def test_external_output_overhang_gap(self):
        r=mesh_statics(self.s,0,external_output_force_N=[10,0,0],external_output_z_m=.031)
        self.assertAlmostEqual(r['output_point_support_unresolved_moment_Nm'][1],.1)
    def test_reverse_flank_radial_sign(self):
        a=mesh_statics(self.s,.01)['branches'][0];b=mesh_statics(self.s,-.01)['branches'][0]
        self.assertEqual(a['Fr_N'],b['Fr_N']);self.assertEqual(a['Ft_N'],-b['Ft_N'])
    def test_normal_force_vector_norm(self):
        b=mesh_statics(self.s,.01)['branches'][0]
        self.assertAlmostEqual(b['normal_force_N'],math.sqrt(b['Ft_N']**2+b['Fr_N']**2+b['axial_each_mesh_N']**2))


class MechanicsTests(unittest.TestCase):
    def test_historical_stress_crosscheck_independent_code(self):
        r=screen(INPUTS);c=INPUTS['historical_comparators_not_certificates']
        self.assertAlmostEqual(r['root_sun_Pa']/c['lewis_reference_Pa'],1,places=12)
        self.assertAlmostEqual(r['external_contact_Pa']/c['transverse_hertz_reference_Pa'],1,places=12)
    def test_lewis_linear_torque(self):self.assertEqual(lewis_stress(2,.01,.001,.3),2*lewis_stress(1,.01,.001,.3))
    def test_hertz_pressure_integrates_load(self):
        r=hertz_line(20,.007,.002,.004,1e9,.3,1e9,.3);h=r['half_width_m']
        integrated=quad(lambda x:r['p0_Pa']*math.sqrt(max(0,1-(x/h)**2)),-h,h)[0]*.007
        self.assertAlmostEqual(integrated,20,places=7)
    def test_internal_curvature_sign(self):
        ext=hertz_line(20,.007,.002,.004,1e9,.3,1e9,.3)
        internal=hertz_line(20,.007,.002,.004,1e9,.3,1e9,.3,True)
        self.assertGreater(internal['reduced_radius_m'],ext['reduced_radius_m'])
    def test_hertz_sqrt_load(self):
        args=(.007,.002,.004,1e9,.3,1e9,.3)
        self.assertAlmostEqual(hertz_line(4,*args)['p0_Pa'],2*hertz_line(1,*args)['p0_Pa'])
    def test_overhung_castigliano_independent_quadrature(self):
        L=.006;h=.0077;E=1.2e9;d=.00695;EI=E*section(d)['I_m4'];a=L+h
        unit_M=lambda x: h*x/L if x<L else a-x
        integral=quad(lambda x:unit_M(x)**2/EI,0,L)[0]+quad(lambda x:unit_M(x)**2/EI,L,a)[0]
        self.assertAlmostEqual(overhung_compliance(L,h,d,E,.35,include_shear=False)[0,0]/integral,1,places=12)
    def test_beam_compliance_reciprocity_and_positive_energy(self):
        for C in [cantilever_compliance(.0044,.00695,1e9,.3),overhung_compliance(.006,.0077,.00695,1e9,.3)]:
            np.testing.assert_allclose(C,C.T);self.assertTrue(np.all(np.linalg.eigvalsh(C)>0))
    def test_shear_compliance_increases_short_beam_deflection(self):
        a=overhung_compliance(.006,.0077,.00695,1e9,.3);b=overhung_compliance(.006,.0077,.00695,1e9,.3,include_shear=False)
        self.assertGreater(a[0,0],b[0,0])
    def test_torsion_energy(self):
        r=torsion(.01,.006,1e9,.3,.1);G=material_moduli(1e9,.3);J=section(.006)['J_m4']
        self.assertAlmostEqual(.5*.1*r['twist_rad'],.1**2*.01/(2*G*J))
    def test_input_compliance_reflects_ratio_squared(self):
        g=Gearset();q=output_compliance(g,1e9,.3,.004,.007,.02,.006,.01,.006,[1/3]*3)
        self.assertAlmostEqual(q['input_shaft_referred_rad_Nm']*100,torsion(.02,.006,1e9,.3)['compliance_rad_Nm'])
    def test_complete_stiffness_is_not_fabricated(self):self.assertIsNone(screen(INPUTS)['compliance']['complete_gearbox_stiffness_Nm_rad'])
    def test_no_actual_capacity_from_hypothetical_limits(self):self.assertIsNone(partial_limits(INPUTS)['system_allowable_input_torque_Nm'])
    def test_contact_pressure_capacity_scales_quadratically(self):
        a=partial_limits(INPUTS,contact_allowable=10e6)['conditional_component_input_limits_Nm']['external_cylinder_contact']
        b=partial_limits(INPUTS,contact_allowable=20e6)['conditional_component_input_limits_Nm']['external_cylinder_contact']
        self.assertAlmostEqual(b/a,4)
    def test_no_actual_allowable(self):self.assertIsNone(INPUTS['actual_unknowns']['root_service_allowable_Pa'])
    def test_missing_ring_root_is_explicit(self):self.assertIsNone(screen(INPUTS)['ring_root_Pa'])
    def test_bearing_life_units(self):
        r=bearing_basic_life(100,100,2*math.pi);self.assertAlmostEqual(r['revolutions'],1e6);self.assertAlmostEqual(r['hours'],1e6/3600)
    def test_bearing_static_speed_no_infinite_hours(self):self.assertIsNone(bearing_basic_life(100,10,0)['hours'])
    def test_bearing_zero_load_not_infinite_service_claim(self):self.assertIsNone(bearing_basic_life(100,0,1)['hours'])
    def test_bearing_cubic_load_sensitivity(self):self.assertAlmostEqual(bearing_basic_life(100,20,1)['hours']*8,bearing_basic_life(100,10,1)['hours'])
    def test_rotation_weighted_load(self):self.assertAlmostEqual(variable_load_equivalent([10,20],[1,0],[.5,.5]),10)
    def test_equivalent_load_parameters(self):self.assertAlmostEqual(equivalent_dynamic_load(10,4,.56,2,1),13.6)


class LossTests(unittest.TestCase):
    def setUp(self):self.s=Gearset()
    def test_ideal_power(self):
        r=power_flow(self.s,.01,10,1,1,0,0,0);self.assertAlmostEqual(r['efficiency'],1);self.assertAlmostEqual(r['output_torque_Nm'],.1)
    def test_carrier_relative_power_independent(self):
        r=power_flow(self.s,.01,10,.95,.98,0,0,0);tr=r['combined_housing_reaction_Nm'];wc=1
        self.assertAlmostEqual(tr*wc/(.01*(10-wc)),.95*.98)
    def test_total_energy_conservation(self):
        r=power_flow(self.s,.1,20,.98,.98,.0001,.0001,.0001)
        self.assertAlmostEqual(r['input_power_W'],r['predicted_output_power_W']+r['loss_power_W'])
    def test_relative_planet_bearing_speed(self):
        r=power_flow(self.s,.1,10,1,1,0,.001,0)
        self.assertAlmostEqual(r['bearing_loss_W'],3*.001*2.25)
    def test_no_clipping_invalid_motoring(self):
        r=power_flow(self.s,.001,10,.98,.98,.001,.001,.001)
        self.assertEqual(r['status'],'NO_POSITIVE_OUTPUT_MOTORING_SOLUTION');self.assertIsNone(r['efficiency'])
    def test_static_efficiency_undefined(self):self.assertIsNone(power_flow(self.s,.01,0,.98,.98,0,0,0)['efficiency'])
    def test_reversed_motoring_same_losses(self):self.assertEqual(power_flow(self.s,.1,10,.98,.98,0,0,0),power_flow(self.s,.1,-10,.98,.98,0,0,0))
    def test_thermal_initial(self):self.assertEqual(thermal_rise(5,10,20,0),0)
    def test_thermal_steady(self):self.assertAlmostEqual(thermal_rise(5,10,20,1e6),50)
    def test_required_cooling_budget(self):self.assertEqual(required_thermal_resistance(2,20),10)


class DimensionalTests(unittest.TestCase):
    def test_independent_dimension_exponents(self):
        # Exponents (kg,m,s). Formula checks independent of production numerical code.
        M=np.array([1,0,0]);L=np.array([0,1,0]);time=np.array([0,0,1]);force=M+L-2*time;pressure=force-2*L;torque=force+L
        np.testing.assert_array_equal(force-(L+L),pressure) # Lewis F/(b*m*Y)
        np.testing.assert_array_equal((force+pressure-2*L)/2,pressure) # sqrt(F E/(length*radius))
        np.testing.assert_array_equal(torque-3*L,pressure) # torsion stress
        np.testing.assert_array_equal(force+3*L-pressure-4*L,L) # beam deflection
        np.testing.assert_array_equal(L-pressure-4*L,-torque) # torsion compliance
        np.testing.assert_array_equal(torque-time,M+2*L-3*time) # P=T*omega
    def test_geometric_scaling_stress_invariant(self):
        s=Gearset();g=s.geometry();scale=2.7;t=.1
        def demands(s):
            q=s.geometry();ft=t/(q['pitch_radii_m'][0]*3)
            h=hertz_line(ft/math.cos(q['alpha_t_rad']),s.width,q['pitch_radii_m'][0]*math.sin(q['alpha_t_rad']),q['pitch_radii_m'][1]*math.sin(q['alpha_t_rad']),1e9,.3,1e9,.3)
            return lewis_stress(ft,s.width,s.mn,.25),h['p0_Pa']
        d=demands(s);e=demands(dataclasses.replace(s,mn=s.mn*scale,width=s.width*scale,backlash_sp=s.backlash_sp*scale,backlash_pr=s.backlash_pr*scale))
        self.assertAlmostEqual(e[0]/d[0],scale**-3);self.assertAlmostEqual(e[1]/d[1],scale**-1.5)


if __name__=='__main__':unittest.main()
