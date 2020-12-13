include <config.scad>

absTraySize = [
	unitSize[0] * unitCount[0],
	unitSize[1] * unitCount[1],
	unitSize[2] * unitCount[2]
	];

adjTraySize = [
	absTraySize[0] - horizontalMountDepth,
	absTraySize[1] - horizontalMountDepth,
	absTraySize[2]
	];

absCornerPositions = [
	[absTraySize[0] / 2, -absTraySize[1] / 2],
	[absTraySize[0] / 2, absTraySize[1] / 2],
	[-absTraySize[0] / 2, absTraySize[1] / 2],
	[-absTraySize[0] / 2, -absTraySize[1] / 2]
];

adjCornerPositions = [
	[adjTraySize[0] / 2, -adjTraySize[1] / 2],
	[adjTraySize[0] / 2, adjTraySize[1] / 2],
	[-adjTraySize[0] / 2, adjTraySize[1] / 2],
	[-adjTraySize[0] / 2, -adjTraySize[1] / 2]
];

rotatedDimensions = [1, 0, 1, 0];

module trayPerimeter() {
	square([adjTraySize[0], adjTraySize[1]], true);
}

module compartmentsProfile() {
	import(innerWallPatternFile, center=true);
}

/* -------- Floor --------- */
module trayFloor() {
	linear_extrude(floorWidth) trayPerimeter();
}

/* -------- Outer wall --------- */
module outerWall() {
	linear_extrude(absTraySize[2]) difference() {
		trayPerimeter();
		offset(delta=-outerWallWidth) trayPerimeter();
	}
}

/* -------- Corner reinforcements --------- */
module cornerReinforcementProfile() {
	linear_extrude(absTraySize[2]) polygon([[0, 0], [-cornerReinforcementSize, 0], [0, cornerReinforcementSize]]);
}
module cornerReinforcements() {
	for(a = [0 : 3]) {
		translate(adjCornerPositions[a]) rotate(a * 90) cornerReinforcementProfile();
	}
}

/* -------- Horizontal mounts --------- */
module horizontalMountProfile() {
	dp = horizontalMountDepth;
	ew = horizontalMountExtWidth/2;
	bw = horizontalMountBaseWidth/2;
	polygon([[0, bw], [dp, ew], [dp, -ew], [0, -bw]]);
}
module horizontalMounts() {
	for(a = [0 : 3]) translate(absCornerPositions[a]) rotate(a * 90) {
		d = rotatedDimensions[a];
		dUnitSize = unitSize[d];
		hUnitSize = unitSize[2];

		dp = horizontalMountDepth;
		ew = horizontalMountExtWidth/2;
		bw = horizontalMountBaseWidth/2;

		for(x = [0 : unitCount[d] - 1]) {
			for(z = [0 : unitCount[2] - 1]) translate([-dp/2, dUnitSize * (x + 0.5), hUnitSize * z]) {
				difference() {
					union() {
						// Male connector
						translate([0, horizontalMountConenctorDistance, 0]) linear_extrude(hUnitSize / 2) horizontalMountProfile();

						// Female connector
						translate([0, -horizontalMountConenctorDistance, 0]) linear_extrude(hUnitSize / 2) difference() {
							translate([0, -ew * 2, 0]) square([dp, ew * 4]);
							translate([dp, 0, 0]) rotate([0, 0, 180]) offset(delta=horizontalMountTolerance) horizontalMountProfile();
						}
					}

					// Kick in
					rotate([90, 0, 0]) linear_extrude(dUnitSize, center=true) polygon([[0, 0], [dp + 0, 0], [dp + 0, horizontalMountKickIn]]);

					// Kick out
					translate([0, 0, unitSize[2] / 2]) rotate([90, 0, 0]) linear_extrude(dUnitSize, center=true) polygon([[0, 0], [dp, 0], [dp + 0, -horizontalMountKickOut]]);
				}
			}
		}
	}
}

/* ---------- Vertical mounts ------------------ */
module verticalMountsProfile(inner = true) {
	offset = outerWallWidth + horizontalMountDepth / 2;
	hvm = verticalMountWidth / 2;

	for(y = [0 : unitCount[1] - 1]) {
		for(x = [0 : unitCount[0] - 1]) translate([-absTraySize[0] / 2 + unitSize[0] * x, -absTraySize[1] / 2 + unitSize[1] * y, 0]) {
			if(inner || x == 0)
				translate([offset - hvm, offset, 0]) square([verticalMountWidth, unitSize[1] - offset * 2]);

			if(inner || x == unitCount[0] - 1)
				translate([unitSize[0] - offset - hvm, offset, 0]) square([verticalMountWidth, unitSize[1] - offset * 2]);
			
			if(inner || y == 0)
				translate([offset, offset - hvm, 0]) square([unitSize[0] - offset * 2, verticalMountWidth]);

			if(inner || y == unitCount[1] - 1)	
				translate([offset, unitSize[1] - offset - hvm, 0]) square([unitSize[0] - offset * 2, verticalMountWidth]);
		}
	}
}
module verticalMountsIncl() {
	/*for(a = [0 : 3]) translate(absCornerPositions[a]) rotate(a * 90) {
		d = rotatedDimensions[a];
		dUnitSize = unitSize[d];
		hUnitSize = unitSize[2];

		for(x = [0 : unitCount[d] - 1]) translate([(horizontalMountDepth + outerWallWidth) / -2, dUnitSize * (x + 0.5), absTraySize[2]]) {
			linear_extrude(verticalMountHeight) square([verticalMountWidth, dUnitSize - outerWallWidth * 2 - horizontalMountDepth], center=true);
		}
	}*/
	translate([0, 0, absTraySize[2]])
		linear_extrude(verticalMountHeight) verticalMountsProfile(inner = false);
}
module verticalMountsExcl() {
	linear_extrude(verticalMountHeight + verticalMountTolerance) verticalMountsProfile();
}