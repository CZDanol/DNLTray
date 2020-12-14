include <drawer_common.scad>

rotate([0, 0, 180]) {
	difference() {
		union() {
			componentFloor();
			outerWall();
			cornerReinforcements();
			horizontalMounts(skipFront=true);
			verticalMountsIncl();
			drawerRailsHolder();
		}

		verticalMountsExcl();
		drawerHoleExcl();
	}
}