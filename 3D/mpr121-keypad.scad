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

$fa = 1;
$fs = 0.4;
$fn = 48;

fuzz = 0.01;
w4 = 1.67;   // 4 walls Prusa3D
gap = 0.1;

// outer dimensions
xo = 49;
yo = 78.6;
zo = 1.4;
rim   = 5;

// inner dimensions
xi = 45;
yi = 60.5;
xi_off =2;
yi_off = 13;

// cutouts
xc_l = 14;
yc_l = 3.5;
zc_l = 0.4;

// cylinders
cyl_d   = 3;
cyl_h   = 3;
cyl_off_lx = cyl_d/2+2.5;
cyl_off_ly = cyl_d/2+2.5;
cyl_off_ux = cyl_d/2+2.6;
cyl_off_uy = cyl_d/2+1;

// --- frame for keypad   ----------------------------------------------------------

module keypad_frame() {
  // base
  difference() {
    // outer cube
    translate([-rim,-rim,0]) cube([xo+2*rim,yo+2*rim,zo]);
    // inner cutout
    translate([xi_off,yi_off,-fuzz]) cube([xi,yi,zo+2*fuzz]);
    // lower cutout
    translate([(xo-xc_l)/2,0,zc_l]) cube([xc_l,yc_l+fuzz,zo+2*fuzz]);
  }
  // cylinders
  translate([cyl_off_lx,cyl_off_ly,zo-fuzz]) cylinder(cyl_h,d=cyl_d);
  translate([xo-cyl_off_lx,cyl_off_ly,zo-fuzz]) cylinder(cyl_h,d=cyl_d);
  translate([cyl_off_ux,yo-cyl_off_uy,zo-fuzz]) cylinder(cyl_h,d=cyl_d);
  translate([xo-cyl_off_ux,yo-cyl_off_uy,zo-fuzz]) cylinder(cyl_h,d=cyl_d);
}

// keypad_frame();