// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD): case for prototype-pcb.
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
//$fn = 64;
$fn = 24;

fuzz = 0.001;

// dimensions
w4 = 1.67;           // wall 4 layers
d  = 0.2;            // delta

x_pcb = 100;         // pcb dimensions
y_pcb = 35;
z_pcb = 15;
d_pcb = 1.6;         // thickness

x_sd     = 10;       // cutout for SD-connector
x_off_sd = 11;       // offset relative to inner
z_off_sd = 1.4;      // offset relative to top of pcb

x_screw     = 14.5;    // cutout for screw-terminal
x_off_screw = 62.0;
z_off_screw = 0;

y_grove     = 12;      // cutout for grove-connector
y_off_grove = 5.75;
z_off_grove = 0;

r = 3;               // edges 3mm rounding
b = 1.2;             // bottom-plate
s_x = 5;             // support in the corners
s_y = s_x;
s_z = 4;

// --- inner void   --------------------------------------------------------------

module inner() {
  cuboid([x_pcb+2*d,y_pcb+2*d,z_pcb+b], p1=[-d,-d,b]);                      // pcb
}

// --- outer shell   ------------------------------------------------------------

module outer() {
  cuboid(
      [x_pcb+2*d+2*w4,y_pcb+2*d+2*w4,z_pcb], p1=[-d-w4,-d-w4,0],
      rounding=r,
      edges=[LEFT+FRONT,RIGHT+FRONT,LEFT+BACK,RIGHT+BACK]
  );
}

difference() {
  outer();
  inner();
  cuboid([x_sd,   10,      z_pcb+b], p1=[x_off_sd,    y_pcb-5,     b+s_z+d_pcb+z_off_sd]);
  cuboid([x_screw,10,      z_pcb+b], p1=[x_off_screw, y_pcb-5,     b+s_z+d_pcb+z_off_screw]);
  cuboid([10,     y_grove, z_pcb+b], p1=[-5,          y_off_grove, b+s_z+d_pcb+z_off_grove]);
}
cuboid([s_x,s_y,s_z], p1=[-d,-d,b]);
cuboid([s_x,s_y,s_z], p1=[-d,y_pcb+d-s_y,b]);
cuboid([s_x,s_y,s_z], p1=[x_pcb-s_x+d,-d,b]);
cuboid([s_x,s_y,s_z], p1=[x_pcb-s_x+d,y_pcb+d-s_y,b]);
