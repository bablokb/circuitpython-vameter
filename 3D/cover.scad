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
    cuboid([x_mcu,y_mcu,b+fuzz],p1=[w4+gap+x_mcu_off,0,0]);                // cutout for mcu
    cuboid([x_sw,y_sw,b+fuzz],p1=[w4+gap+x_sw_off,y-y_sw,0]);              // cutout for switch
    cuboid([y_oled,x_oled,b+fuzz],p1=[w4+gap+x_mcu_off,
                                      (y-x_oled)/2,0]);                    // empty space for oled
    cuboid([xo_kp,yo_kp,b+fuzz],p1=[xr_mcu + (x-xr_mcu-xo_kp)/2,y_kp,0]);  // empty space for keypad
  }
}

cover();
move([y_oled+w4+gap+x_mcu_off,(y-x_oled)/2,b])
           zrot(90) zflip() oled();
color("blue") 
  move([xr_mcu + (x-xr_mcu-xo_kp)/2,y_kp,b])
  mirror([0,0,1]) yflip(y=yo_kp/2) keypad_frame();