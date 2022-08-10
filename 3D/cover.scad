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

module snap_female(orient) {
  difference() {
    cuboid([snap_h+gap+2*snap_f,snap_y,2*(snap_h+gap+snap_f)],
              chamfer=3*snap_f,
              edges=[BOTTOM+LEFT],
              anchor=FRONT+LEFT+BOTTOM
    );
    translate([-fuzz,(snap_y-(snap_w+2*gap))/2,snap_f]) prismoid(size1=[2*(snap_h+gap),snap_w+2*gap],
                                    size2=[0,snap_w-2*(snap_h+gap)], 
             h=snap_h+gap, orient=orient, anchor=FRONT+RIGHT+BOTTOM
    );
  }
}
//snap_female(RIGHT);

x      = xsize+2*w4;
y      = ysize+2*w4;
xr_mcu = w4+gap+x_mcu_off+x_mcu;                                     // right border of x_mcu

module cover() {
  difference() {
    cuboid(
        [x,y,b], rounding=3,
        edges="Z", p1=[0,0,0],
        anchor=FRONT+LEFT+BOTTOM
    );
    cuboid([x_mcu,y_mcu,b+fuzz],p1=[w4+gap+x_mcu_off,0,0]);              // cutout for mcu/grove
    cuboid([x_sw,y_sw,b+fuzz],p1=[w4+gap+x_sw_off,y-y_sw,0]);            // cutout for switch
    cuboid([y_oled,x_oled,b+fuzz],p1=[w4+gap+x_mcu_off+(x_mcu-y_oled)/2,
                                      (y-x_oled)/2,0]);                  // empty space for oled
    cuboid([xo_kp,yo_kp,b+fuzz],p1=[xr_mcu + (x-xr_mcu-xo_kp)/2,
                                    (y-yo_kp)/2,0]);                     // empty space for keypad
  }
  translate([w4+gap-fuzz,w4+(ysize-snap_y)/2,fuzz-2*(snap_h+gap+snap_f)])
           snap_female(RIGHT);
  xflip(x=w4+xsize/2) translate([w4+gap-fuzz,w4+(ysize-snap_y)/2,fuzz-2*(snap_h+gap+snap_f)])
           snap_female(RIGHT);
}

cover();
move([y_oled+w4+gap+x_mcu_off+(x_mcu-y_oled)/2,(y-x_oled)/2,b])
           zrot(90) zflip() oled();
color("blue") 
  move([xr_mcu + (x-xr_mcu-xo_kp)/2,(y-yo_kp)/2,b])
  mirror([0,0,1]) yflip(y=yo_kp/2) keypad_frame();