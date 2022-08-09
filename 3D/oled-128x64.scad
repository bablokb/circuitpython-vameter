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
x_oled = 27.8;
y_oled = 28;
z_oled = 2.3;

// inner dimensions
x_oled_i = x_oled;
y_oled_i = 19.3+2*gap;

// cutouts
xc_oled_l = 13;
yc_oled_l = 4.4;
zc_oled_l = 0.4;

xc_oled_u = 9.0;
yc_oled_u = 4.1;
zc_oled_u = 0.4;

// cylinders
oled_cyl_d =   1.9;
oled_cyl_off = 1.1;

module oled() {
  // base
  difference() {
    // outer cube
    cube([x_oled,y_oled,z_oled]);
    // inner cutout
    translate([0,yc_oled_l,-fuzz]) cube([x_oled_i,y_oled_i,z_oled+2*fuzz]);
    // lower cutout
    translate([(x_oled-xc_oled_l)/2,0,zc_oled_l]) cube([xc_oled_l,yc_oled_l+fuzz,z_oled+2*fuzz]);
    // upper cutout
    translate([(x_oled-xc_oled_u)/2,yc_oled_l+y_oled_i-fuzz,zc_oled_u]) cube([xc_oled_u,yc_oled_u,z_oled+2*fuzz]);
  }
  // inner frame
  translate([0,yc_oled_l-fuzz,0]) cube([x_oled,3,zc_oled_l]);
  // cylinders
  translate([oled_cyl_off+oled_cyl_d/2,oled_cyl_off+oled_cyl_d/2,z_oled-fuzz]) cylinder(3,d=1.9);
  translate([x_oled-(oled_cyl_off+oled_cyl_d/2),oled_cyl_off+oled_cyl_d/2,z_oled-fuzz]) cylinder(3,d=1.9);
  translate([oled_cyl_off+oled_cyl_d/2,y_oled-(oled_cyl_off+oled_cyl_d/2),z_oled-fuzz]) cylinder(3,d=1.9);
  translate([x_oled-(oled_cyl_off+oled_cyl_d/2),y_oled-(oled_cyl_off+oled_cyl_d/2),z_oled-fuzz]) cylinder(3,d=1.9);
}

//oled();