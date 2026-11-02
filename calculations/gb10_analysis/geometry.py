# SPDX-FileCopyrightText: 2026 SriramNavi
# SPDX-License-Identifier: MIT
"""G01–G03: normal/transverse involute geometry and Willis kinematics (R1,R2)."""
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Gearset:
    zs: int = 12
    zp: int = 48
    zr: int = 108
    planets: int = 3
    mn: float = 0.00058
    alpha_n: float = math.radians(20)
    beta: float = math.radians(20)
    width: float = 0.0072
    ha: float = 0.8
    hf: float = 1.2
    backlash_sp: float = 0.0002
    backlash_pr: float = 0.0002

    def __post_init__(self):
        if any(not isinstance(z, int) or z < 1 for z in [self.zs, self.zp, self.zr, self.planets]):
            raise ValueError('Tooth/planet counts must be positive integers')
        if self.zr != self.zs + 2*self.zp:
            raise ValueError('Incompatible concentric center distances')
        if min(self.mn, self.width, self.ha, self.hf) <= 0 or self.ha >= self.hf:
            raise ValueError('Invalid lengths or tooth coefficients')
        if not 0 < self.alpha_n < math.pi/2 or not abs(self.beta) < math.pi/2:
            raise ValueError('Invalid angles in radians')
        if min(self.backlash_sp, self.backlash_pr) < 0:
            raise ValueError('Negative backlash')

    @property
    def ratio(self): return 1 + self.zr/self.zs

    def geometry(self):
        mt = self.mn/math.cos(self.beta)
        at = math.atan(math.tan(self.alpha_n)/math.cos(self.beta))
        radii = [mt*z/2 for z in [self.zs, self.zp, self.zr]]
        rs, rp, rr = radii
        base = [r*math.cos(at) for r in radii]
        tips = [rs+self.ha*self.mn, rp+self.ha*self.mn, rr-self.ha*self.mn]
        roots = [rs-self.hf*self.mn, rp-self.hf*self.mn, rr+self.hf*self.mn]
        if any(t < b for t,b in zip(tips,base)):
            raise ValueError('Tip below base circle: active involute model unavailable')
        lengths = [math.sqrt(t*t-b*b) for t,b in zip(tips,base)]
        a = rs+rp
        pb = math.pi*mt*math.cos(at)
        ea_sp = (lengths[0]+lengths[1]-a*math.sin(at))/pb
        ea_pr = (lengths[1]-lengths[2]+a*math.sin(at))/pb
        eb = self.width*abs(math.sin(self.beta))/(math.pi*self.mn)
        return dict(mt_m=mt, alpha_t_rad=at, pitch_radii_m=radii, base_radii_m=base,
                    tip_radii_m=tips, root_radii_m=roots, orbit_m=a,
                    internal_center_m=rr-rp, base_pitch_m=pb,
                    external_contact_ratio=ea_sp, internal_contact_ratio=ea_pr,
                    overlap_ratio=eb, total_external_ratio=ea_sp+eb, total_internal_ratio=ea_pr+eb,
                    phasing_integer=(self.zs+self.zr)/self.planets,
                    equal_spacing_compatible=(self.zs+self.zr)%self.planets==0,
                    adjacent_planet_tip_gap_m=2*a*math.sin(math.pi/self.planets)-2*tips[1],
                    output_mesh_backlash_rad=(self.backlash_sp+self.backlash_pr)/(2*a),
                    virtual_sun_teeth=self.zs/math.cos(self.beta)**3,
                    stub_rack_undercut_threshold=2*self.ha/math.sin(self.alpha_n)**2)

    def kinematics(self, sun_rad_s, ring_rad_s=0):
        carrier = (self.zs*sun_rad_s+self.zr*ring_rad_s)/(self.zs+self.zr)
        planet = carrier-self.zs/self.zp*(sun_rad_s-carrier)
        return dict(sun_rad_s=sun_rad_s, ring_rad_s=ring_rad_s, carrier_rad_s=carrier,
                    planet_absolute_rad_s=planet, planet_relative_carrier_rad_s=planet-carrier,
                    external_residual=self.zs*(sun_rad_s-carrier)+self.zp*(planet-carrier),
                    internal_residual=self.zr*(ring_rad_s-carrier)-self.zp*(planet-carrier))
