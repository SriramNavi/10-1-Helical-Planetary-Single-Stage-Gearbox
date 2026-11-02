# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""Carrier-relative basic-train power model and parameterized bearing losses (R7)."""
import math


def power_flow(gearset,torque,speed,eta_sp,eta_pr,input_drag,planet_drag,output_drag,viscous_equiv=0):
    """Sun-driven motoring in either rotation direction; not backdrive/regeneration."""
    if torque<0 or min(input_drag,planet_drag,output_drag,viscous_equiv)<0 or not 0<eta_sp<=1 or not 0<eta_pr<=1:
        raise ValueError('Invalid motoring or loss parameters')
    omega=abs(speed);kin=gearset.kinematics(omega)
    eta0=eta_sp*eta_pr
    eta_mesh=(1+(gearset.ratio-1)*eta0)/gearset.ratio
    pin=torque*omega
    mesh_loss=(1-eta_mesh)*pin
    bearing_loss=(2*input_drag*omega+gearset.planets*planet_drag*abs(kin['planet_relative_carrier_rad_s'])
                  +output_drag*abs(kin['carrier_rad_s']))
    viscous_loss=viscous_equiv*omega**2
    loss=mesh_loss+bearing_loss+viscous_loss
    raw=pin-loss
    if omega==0:
        return dict(status='STATIC_EFFICIENCY_UNDEFINED; breakaway torque unmodeled',input_power_W=0.,
                    predicted_output_power_W=None,loss_power_W=0.,efficiency=None,output_torque_Nm=None)
    if raw<0:
        return dict(status='NO_POSITIVE_OUTPUT_MOTORING_SOLUTION',input_power_W=pin,loss_power_W=loss,
                    predicted_output_power_W=None,raw_power_residual_W=raw,efficiency=None,output_torque_Nm=None)
    out_speed=omega/gearset.ratio;out_torque=raw/out_speed
    return dict(status='CONDITIONAL_MODEL',input_power_W=pin,predicted_output_power_W=raw,
                mesh_loss_W=mesh_loss,bearing_loss_W=bearing_loss,viscous_loss_W=viscous_loss,
                loss_power_W=loss,efficiency=None if pin==0 else raw/pin,output_torque_Nm=out_torque,
                combined_housing_reaction_Nm=out_torque-torque,
                power_residual_W=pin-raw-loss,carrier_relative_basic_train_efficiency=eta0,
                mesh_only_stage_efficiency=eta_mesh)


def thermal_rise(power,Rtheta,Ctheta,time_s):
    if min(power,time_s)<0 or min(Rtheta,Ctheta)<=0:raise ValueError('Invalid thermal parameters')
    return power*Rtheta*(-math.expm1(-time_s/(Rtheta*Ctheta)))


def required_thermal_resistance(power,allowed_rise):
    if power<0 or allowed_rise<=0:raise ValueError('Invalid heat budget')
    return None if power==0 else allowed_rise/power
