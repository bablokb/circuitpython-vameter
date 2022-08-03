// -----------------------------------------------------------------------------
// 3D-Model frame for OLED-128x64 I2C-display.
//
// Author: Bernhard Bablok
// License: GPL3
//
// Website: https://github.com/bablokb/circuitpython-vameter
//
// -----------------------------------------------------------------------------

// outer dimensions
oled_x = 27.8;
oled_y = 28;
oled_z = 2.3;

// inner dimensions
oled_xi = oled_x;
oled_yi = 19.3+2*gap;

// cutouts
oled_xc_l = 13;
oled_yc_l = 4.4;
oled_zc_l = 0.4;
oled_xc_u = 9.0;
oled_yc_u = 4.1;
oled_zc_u = 0.4;

// cylinders
oled_cyl_d =   1.9;
oled_cyl_off = 1.1;

module oled() {
  // base
  difference() {
    // outer cube
    cube([oled_x,oled_y,oled_z]);
    // inner cutout
    translate([0,oled_yc_l,-fuzz]) cube([oled_xi,oled_yi,oled_z+2*fuzz]);
    // lower cutout
    translate([(oled_x-oled_xc_l)/2,0,oled_zc_l]) cube([oled_xc_l,oled_yc_l+fuzz,oled_z+2*fuzz]);
    // upper cutout
    translate([(oled_x-oled_xc_u)/2,oled_yc_l+oled_yi-fuzz,oled_zc_u]) cube([oled_xc_u,oled_yc_u,oled_z+2*fuzz]);
  }
  // inner frame
  translate([0,oled_yc_l-fuzz,0]) cube([oled_x,3,oled_zc_l]);
  // cylinders
  translate([oled_cyl_off+oled_cyl_d/2,oled_cyl_off+oled_cyl_d/2,oled_z-fuzz]) cylinder(3,d=1.9);
  translate([oled_x-(oled_cyl_off+oled_cyl_d/2),oled_cyl_off+oled_cyl_d/2,oled_z-fuzz]) cylinder(3,d=1.9);
  translate([oled_cyl_off+oled_cyl_d/2,oled_y-(oled_cyl_off+oled_cyl_d/2),oled_z-fuzz]) cylinder(3,d=1.9);
  translate([oled_x-(oled_cyl_off+oled_cyl_d/2),oled_y-(oled_cyl_off+oled_cyl_d/2),oled_z-fuzz]) cylinder(3,d=1.9);
}

oled();