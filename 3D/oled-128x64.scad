// -----------------------------------------------------------------------------
// 3D-Model frame for OLED-128x64 I2C-display.
//
// Author: Bernhard Bablok
// License: GPL3
//
// Website: https://github.com/bablokb/circuitpython-vameter
//
// -----------------------------------------------------------------------------

$fa = 1;
$fs = 0.4;
$fn = 48;

fuzz = 0.01;
w4 = 1.67;   // 4 walls Prusa3D
gap = 0.1;

// outer dimensions
xo = 27.8;
yo = 28;
zo = 2.3;
rim   = 5;

// inner dimensions
xi = xo;
yi = 19.3+2*gap;

// cutouts
xc_l = 13;
yc_l = 4.4;
zc_l = 0.4;
xc_u = 9.0;
yc_u = 4.1;
zc_u = 0.4;

// cylinders
cyl_d =   1.9;
cyl_off = 1.1;

module oled() {
  // base
  difference() {
    // outer cube
    translate([-rim,-rim,0]) cube([xo+2*rim,yo+2*rim,zo]);
    // inner cutout
    translate([0,yc_l,-fuzz]) cube([xi,yi,zo+2*fuzz]);
    // lower cutout
    translate([(xo-xc_l)/2,0,zc_l]) cube([xc_l,yc_l+fuzz,zo+2*fuzz]);
    // upper cutout
    translate([(xo-xc_u)/2,yc_l+yi-fuzz,zc_u]) cube([xc_u,yc_u,zo+2*fuzz]);
  }
  // inner frame
  translate([0,yc_l-fuzz,0]) cube([xo,3,zc_l]);
  // cylinders
  translate([cyl_off+cyl_d/2,cyl_off+cyl_d/2,zo-fuzz]) cylinder(3,d=1.9);
  translate([xo-(cyl_off+cyl_d/2),cyl_off+cyl_d/2,zo-fuzz]) cylinder(3,d=1.9);
  translate([cyl_off+cyl_d/2,yo-(cyl_off+cyl_d/2),zo-fuzz]) cylinder(3,d=1.9);
  translate([xo-(cyl_off+cyl_d/2),yo-(cyl_off+cyl_d/2),zo-fuzz]) cylinder(3,d=1.9);
}

oled();