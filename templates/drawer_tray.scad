include <drawer_common.scad>

rotate([0, 0, 180]) {
	difference() {
		union() {
			componentFloor(outlineOnly=floorOutlineOnly);
			outerWall();
			cornerReinforcements();
			horizontalMounts(skipFront=true);
			verticalMountsIncl(floorOutlineOnly=floorOutlineOnly);
			drawerRailsHolder();
		}

		verticalMountsExcl();
		drawerHoleExcl();
		translate([adjComponentSize[0]/2 - 4, adjComponentSize[1]/2 - 4]) modelLabel();
	}
}