/*
 BLACK MANTA X-91 - civilian scale demonstrator exterior
 Conceptual visualization only; not structural or manufacturing authority.
 Units: millimeters.
*/

$fn = 64;

span = 1400;
length = 820;
body_thickness = 86;
skin_thickness = 3;
edf_diameter = 70;

module planform_2d() {
    polygon(points=[
        [ length * 0.50,    0],
        [ length * 0.28,  span * 0.22],
        [-length * 0.18,  span * 0.50],
        [-length * 0.35,  span * 0.48],
        [-length * 0.42,  span * 0.25],
        [-length * 0.30,  span * 0.08],
        [-length * 0.38,    0],
        [-length * 0.30, -span * 0.08],
        [-length * 0.42, -span * 0.25],
        [-length * 0.35, -span * 0.48],
        [-length * 0.18, -span * 0.50],
        [ length * 0.28, -span * 0.22]
    ]);
}

module blended_shell() {
    hull() {
        translate([80, 0, 0])
            linear_extrude(height=18, center=true, scale=0.98)
                planform_2d();
        translate([-70, 0, 0])
            scale([0.72, 0.40, 1])
                sphere(d=body_thickness);
        translate([80, 0, 16])
            scale([2.8, 1.5, 0.55]) sphere(d=74);
    }
}

module canopy() {
    translate([170, 0, 42])
        scale([2.0, 0.72, 0.52]) sphere(d=70);
}

module edf_duct(y) {
    translate([-65, y, 12])
        rotate([0, 90, 0])
            cylinder(h=240, d=edf_diameter, center=true);
}

module elevon_gap(y_sign=1) {
    translate([-275, y_sign * 375, 0])
        cube([260, 7, 35], center=true);
}

module x91_exterior() {
    difference() {
        union() {
            blended_shell();
            canopy();
        }
        edf_duct(145);
        edf_duct(-145);
        elevon_gap(1);
        elevon_gap(-1);
    }
}

x91_exterior();
