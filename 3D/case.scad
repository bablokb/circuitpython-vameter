// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) case (bottom) for INA219-pcb.
//
// Author: Bernhard Bablok
// License: GPL3
//
// ---------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>


// --- pcb-support   ---------------------------------------------------------

module pcb_support() {
  h = z_sup;
  d = 2*r_pcb;
  z = b-fuzz;
  move([r_pcb+w4+gap,r_pcb+w4+gap,z]) cyl(h=h,d=d,anchor=BOTTOM+CENTER);
  move([r_pcb+w4+gap,y_pcb-r_pcb+w4,z]) cyl(h=h,d=d,anchor=BOTTOM+CENTER);
  move([x_pcb-r_pcb+w4,r_pcb+w4+gap,z]) cyl(h=h,d=d,anchor=BOTTOM+CENTER);
  move([x_pcb-r_pcb+w4,y_pcb-r_pcb+w4,z]) cyl(h=h,d=d,anchor=BOTTOM+CENTER);
}


// --- pcb-holder (fits to mounting holes)   ---------------------------------

module pcb_holder() {
  h = 2*z_pcb;
  d = d_sup - gap;
  z = b + z_sup-2*fuzz;
  move([r_pcb+w4+gap,r_pcb+w4+gap,z]) cyl(h=h,d=d,anchor=BOTTOM+CENTER);
  move([r_pcb+w4+gap,y_pcb-r_pcb+w4,z]) cyl(h=h,d=d,anchor=BOTTOM+CENTER);
  move([x_pcb-r_pcb+w4,r_pcb+w4+gap,z]) cyl(h=h,d=d,anchor=BOTTOM+CENTER);
  move([x_pcb-r_pcb+w4,y_pcb-r_pcb+w4,z]) cyl(h=h,d=d,anchor=BOTTOM+CENTER);
}

// --- connector for cover-snap   --------------------------------------------

module snap_male(orient) {
  prismoid(size1=[2*snap_h,snap_w], size2=[0,snap_w-2*snap_h], 
           h=snap_h, orient=orient, anchor=FRONT+RIGHT+BOTTOM
  );
}


// --- case (bottom-part)   --------------------------------------------------

module case() {
  z = b + z_sup + z_pcb + zsize;
  difference() {
    cuboid(                                          // outer
      [xsize+2*w4,ysize+2*w4,z], rounding=r_pcb,
      edges="Z",
      anchor=FRONT+LEFT+BOTTOM
    );
    cuboid(                                          // minus inner
      [xsize,ysize,z], rounding=r_pcb,
      edges="Z", p1=[w4,w4,b],
      anchor=FRONT+LEFT+BOTTOM
    );

    cuboid([x_mcu_grove,w4+2*fuzz,z],
      p1=[w4+gap+x_mcu_off,0,b+z_sup+z_pcb]);               // cutout mcu/grove
    cuboid([x_conn,w4+2*fuzz,z],
      p1=[w4+gap+x_conn_off,ysize+w4-fuzz,b+z_sup+z_pcb]);  // cutout connectors
  }

  pcb_support();
  pcb_holder();
}

// --- top-level object   ----------------------------------------------------

case();
