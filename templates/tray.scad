include <common.scad>;

/* -------- Inner wall/compartments --------- */
module innerWall() {
	// We intersect with the tray perimeter so that the offset lines do not go outside
	linear_extrude(absComponentSize[2] * innerWallPercentageHeight, convexity=20) offset(delta=innerWallWidth/2) intersection() {
		offset(delta=+0.0001) resize([adjComponentSize[0] - outerWallWidth * 2 + 0.002, adjComponentSize[1] - outerWallWidth * 2 + 0.002, 0], auto=true) compartmentsProfile();
		offset(delta=-outerWallWidth) componentPerimeter();
	}
}

rotate([0, 0, 180]) {
	difference() {
		union() {
			componentFloor();
			outerWall();
			cornerReinforcements();
			innerWall();
			horizontalMounts();
			verticalMountsIncl();
		}

		verticalMountsExcl();
		translate([adjComponentSize[0]/2 - 3, adjComponentSize[1]/2 - 3]) modelLabel();
	}
}