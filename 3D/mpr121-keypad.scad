// -----------------------------------------------------------------------------
// 3D-Model frame for MPR121-based 3x4 keypad
//
// Author: Bernhard Bablok
// License: GPL3
//
// Website: https://github.com/bablokb/circuitpython-vameter
//
// -----------------------------------------------------------------------------

include <BOSL2/std.scad>

// outer dimensions
xo_kp = 49;
yo_kp = 78.6;
zo_kp = 1.4;

// inner dimensions
xi_kp = 45;
yi_kp = 60.5;
xi_kp_off =2;
yi_kp_off = 13;

// cutouts
xc_kp_l = 14;
yc_kp_l = 3.5;
zc_kp_l = 0.4;

// cylinders
kp_cyl_d   = 3;
kp_cyl_h   = 3;
kp_cyl_off_lx = kp_cyl_d/2+2.5;
kp_cyl_off_ly = kp_cyl_d/2+2.5;
kp_cyl_off_ux = kp_cyl_d/2+2.6;
kp_cyl_off_uy = kp_cyl_d/2+1;

// --- frame for keypad   ----------------------------------------------------------

module keypad_frame() {
  // base
  difference() {
    // outer cube
    translate([0,0,0]) cube([xo_kp,yo_kp,zo_kp]);
    // inner cutout
    translate([xi_kp_off,yi_kp_off,-fuzz]) cube([xi_kp,yi_kp,zo_kp+2*fuzz]);
    // lower cutout
    translate([(xo_kp-xc_kp_l)/2,0,zc_kp_l]) cube([xc_kp_l,yc_kp_l+fuzz,zo_kp+2*fuzz]);
  }
  // cylinders
  translate([kp_cyl_off_lx,kp_cyl_off_ly,zo_kp-fuzz]) cylinder(kp_cyl_h,d=kp_cyl_d);
  translate([xo_kp-kp_cyl_off_lx,kp_cyl_off_ly,zo_kp-fuzz]) cylinder(kp_cyl_h,d=kp_cyl_d);
  translate([kp_cyl_off_ux,yo_kp-kp_cyl_off_uy,zo_kp-fuzz]) cylinder(kp_cyl_h,d=kp_cyl_d);
  translate([xo_kp-kp_cyl_off_ux,yo_kp-kp_cyl_off_uy,zo_kp-fuzz]) cylinder(kp_cyl_h,d=kp_cyl_d);
}

//keypad_frame();
