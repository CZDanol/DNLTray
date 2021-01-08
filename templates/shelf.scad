include <common.scad>

rotate([0, 0, 180]) {
	difference() {
		union() {
			componentFloor();
			outerWall();
			cornerReinforcements(skipFront=true);
			horizontalMounts(skipFront=true);
			verticalMountsIncl(skipTopFront=true);

			if(shelfRail)
				translate([0, adjComponentSize[1]/2, unitSize[2] - 2]) labelHolder();
		}

		verticalMountsExcl();
		translate([adjComponentSize[0]/2 - 4, adjComponentSize[1]/2 - 4]) modelLabel();

		// Hole
		translate([0, (adjComponentSize[1] - outerWallWidth) / 2, (shelfRail ? unitSize[2] : floorWidth)]) linear_extrude(1000) square([adjComponentSize[0] - outerWallWidth * 2 - 0.005, outerWallWidth + 0.005], center=true);
	}
}