// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) cover for INA219-pcb.
//
// Author: Bernhard Bablok
// License: GPL3
//
// -----------------------------------------------------------------------------

$fa = 1;
$fs = 0.4;
$fn = 48;

fuzz = 0.01;
w4 = 1.67;                 // 4 walls Prusa3D
gap = 0.2;                 // gap pcb to case

x_pcb = 100;               // pcb-dimensions
y_pcb = 100;
z_pcb = 1.6;
r_pcb = 3.0;               // corner radius

z_sup = 3;                 // hight of pcb-support
d_sup = 2.5;               // diameter mounting-hole

xsize = x_pcb+2*gap;       // inner size
ysize = y_pcb+2*gap;
zsize = 14;                // height above pcb 
b     = 1.2;               // base thickness

snap_h = 1.5;
snap_w = ysize/3;
snap_f = 0.4;
snap_y = snap_w+2*(gap+snap_f)+ysize/3;

x_mcu      = 35;          // cutout for mcu/grove connector
x_mcu_off  =  4;
y_mcu      = 22.5;

x_conn     = 59;          // cutout input/output connectors
x_conn_off =  4;

x_sw       = 10;          // cutout switch
x_sw_off   = 32;
y_sw       =  7;
