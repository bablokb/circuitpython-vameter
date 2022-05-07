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

// --- keypad inset   --------------------------------------------------------------

pad_s = 13;
pad_xgap = 3;
pad_ygap = 2;
pad_h = 0.4;
pad_xoff = (xi - 3*pad_s - 2*pad_xgap)/2;
pad_yoff = (yi - 4*pad_s - 3*pad_ygap)/2;

module keypad_pad(text1,text2="",text3="") {
  difference() {
    cuboid([pad_s,pad_s,pad_h], rounding=1,edges="Z",
                                anchor=FRONT+LEFT+BOTTOM);
    if (text3) {
      translate([pad_s/2,5*pad_s/6,-fuzz]) text3d(text1,h=pad_h+2*fuzz,size=3,
                                anchor=BOTTOM+CENTER);
      translate([pad_s/2,3*pad_s/6,-fuzz]) text3d(text2,h=pad_h+2*fuzz,size=3,
                                anchor=BOTTOM+CENTER);
      translate([pad_s/2,pad_s/6,-fuzz]) text3d(text3,h=pad_h+2*fuzz,size=3,
                                anchor=BOTTOM+CENTER);
    } else if (text2) {
      translate([pad_s/2,3*pad_s/4,-fuzz]) text3d(text1,h=pad_h+2*fuzz,size=4,
                                anchor=BOTTOM+CENTER);
      translate([pad_s/2,pad_s/4,-fuzz]) text3d(text2,h=pad_h+2*fuzz,size=4,
                                anchor=BOTTOM+CENTER);
    } else {
      translate([pad_s/2,pad_s/2,-fuzz]) text3d(text1,h=pad_h+2*fuzz,size=6,
                                anchor=BOTTOM+CENTER);
    }
  }
}

module keypad_pads() {
  difference() {
    cube([xi-0.1,yi-0.1,pad_h]);
    translate([pad_xoff,yi-pad_yoff-pad_s,0]) keypad_pad("1");
    translate([pad_xoff+pad_s+pad_xgap,yi-pad_yoff-pad_s,0]) keypad_pad("2");
    translate([pad_xoff+2*pad_s+2*pad_xgap,yi-pad_yoff-pad_s,0]) keypad_pad("3");

    translate([pad_xoff,yi-pad_yoff-pad_ygap-2*pad_s,0]) keypad_pad("4");
    translate([pad_xoff+pad_s+pad_xgap,yi-pad_yoff-pad_ygap-2*pad_s,0])
             keypad_pad("View","5","View");
    translate([pad_xoff+2*pad_s+2*pad_xgap,yi-pad_yoff-pad_ygap-2*pad_s,0]) keypad_pad("6");

    translate([pad_xoff,yi-pad_yoff-2*pad_ygap-3*pad_s,0]) keypad_pad("7");
    translate([pad_xoff+pad_s+pad_xgap,yi-pad_yoff-2*pad_ygap-3*pad_s,0]) keypad_pad("8");
    translate([pad_xoff+2*pad_s+2*pad_xgap,yi-pad_yoff-2*pad_ygap-3*pad_s,0]) keypad_pad("9");

    translate([pad_xoff,yi-pad_yoff-3*pad_ygap-4*pad_s,0]) keypad_pad("Next","Start");
    translate([pad_xoff+pad_s+pad_xgap,yi-pad_yoff-3*pad_ygap-4*pad_s,0]) keypad_pad("0","Conf");
    translate([pad_xoff+2*pad_s+2*pad_xgap,yi-pad_yoff-3*pad_ygap-4*pad_s,0]) keypad_pad("CLR","Stop");
  }
}

module keypad_inset() {
  difference() {
    cube([xi-0.1,yi-0.1,zo]);
    translate([0,0,zo-pad_h+fuzz]) keypad_pads();
  }
}

keypad_inset();

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