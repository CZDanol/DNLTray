include <template_base.scad>;

/* -------- Inner wall/compartments --------- */
// We intersect with the tray perimeter so that the offset lines do not go outside
intersection() {
	linear_extrude(traySize[2] - innerWallClearance) offset(delta=innerWallWidth/2) resize([traySize[0], traySize[1], 0], auto=true) compartmentsProfile();
	linear_extrude(traySize[2]) trayPerimeter();
}