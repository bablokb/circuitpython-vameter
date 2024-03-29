// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) cover (top) for INA219-pcb.
//
// Author: Bernhard Bablok
// License: GPL3
//
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <mpr121-keypad.scad>
include <oled-128x64.scad>

include <BOSL2/std.scad>


x      = xsize+2*w4;
y      = ysize+2*w4;
xr_mcu = w4+gap+x_mcu_off+x_mcu;         // right border of x_mcu

y_kp = (y-yi_kp)/2 -                     // (total size - cutout keypad size)/2 minus
       (yo_kp - yi_kp - yi_kp_off);      // lower offset of cutout keypad

module cover() {
  difference() {
    cuboid(
        [x,y,b], rounding=3,
        edges="Z", p1=[0,0,0],
        anchor=FRONT+LEFT+BOTTOM
    );
    cuboid([x_mcu,y_mcu,b+2*fuzz],p1=[w4+gap+x_mcu_off,-fuzz,-fuzz]);      // cutout for mcu
    cuboid([x_sw,y_sw,b+2*fuzz],p1=[w4+gap+x_sw_off,y-y_sw+fuzz,-fuzz]);   // cutout for switch
    cuboid([y_oled,x_oled,b+2*fuzz],p1=[w4+gap+x_mcu_off,
                                      (y-x_oled)/2,-fuzz]);                // empty space for oled
    cuboid([xo_kp,yo_kp,b+2*fuzz],p1=[xr_mcu + (x-xr_mcu-xo_kp)/2,
                                      y_kp,-fuzz]);                        // empty space for keypad
    }
  // add oled
  move([y_oled+w4+gap+x_mcu_off,(y-x_oled)/2,b]) zrot(90) zflip() oled();

  // add keypad
  move([xr_mcu + (x-xr_mcu-xo_kp)/2,y_kp,b]) mirror([0,0,1]) yflip(y=yo_kp/2) keypad_frame();
}

module wall() {
  z = zsize - 1;
  difference() {
    cuboid([xsize-gap,ysize-gap,z], rounding=3, edges="Z",
           anchor=FRONT+LEFT+TOP,p1=[w4+gap/2,w4+gap/2,-z]);
    cuboid([xsize-gap-2*w2,ysize-gap-2*w2,z+2*fuzz], rounding=3, edges="Z",
            anchor=FRONT+LEFT+TOP,p1=[w4+gap/2+w2,w4+gap/2+w2,-z]);
    cuboid([x_mcu_grove,w4+w2+gap+fuzz,b+z+2*fuzz],
            anchor=TOP+CENTER,
            p1=[w4+gap+x_mcu_off,-fuzz,-z-b]);         // cutout for mcu+grove
    cuboid([x_conn,w4+w2+gap+fuzz,b+z+2*fuzz],
            anchor=TOP+CENTER,
            p1=[w4+gap+x_conn_off,ysize-fuzz,-z-b]);   // cutout for connectors

  }
}
cover();
wall();
