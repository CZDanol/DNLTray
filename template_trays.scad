include <template_base.scad>;

/* -------- Inner wall/compartments --------- */
module innerWall() {
	// We intersect with the tray perimeter so that the offset lines do not go outside
	intersection() {
		linear_extrude(absTraySize[2] - innerWallClearance) offset(delta=innerWallWidth/2) resize([adjTraySize[0], adjTraySize[1], 0], auto=true) compartmentsProfile();
		linear_extrude(absTraySize[2]) trayPerimeter();
	}
}

difference() {
	union() {
		trayFloor();
		outerWall();
		cornerReinforcements();
		innerWall();
		horizontalMounts();
		verticalMountsIncl();
	}

	verticalMountsExcl();
}