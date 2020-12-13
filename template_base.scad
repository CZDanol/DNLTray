include <config.scad>

traySize = [unitSize[0] * unitCount[0], unitSize[1] * unitCount[1], unitSize[2] * unitCount[2]];

cornerPositions = [
	[traySize[0] / 2, -traySize[1] / 2],
	[traySize[0] / 2, traySize[1] / 2],
	[-traySize[0] / 2, traySize[1] / 2],
	[-traySize[0] / 2, -traySize[1] / 2]
];

rotatedDimensions = [1, 0, 1, 0];

module trayPerimeter() {
	square([traySize[0], traySize[1]], true);
}

module compartmentsProfile() {
	import(innerWallPatternFile, center=true);
}

/* -------- Floor --------- */
linear_extrude(floorWidth) trayPerimeter();

/* -------- Outer wall --------- */
linear_extrude(traySize[2]) difference() {
	trayPerimeter();
	offset(delta=-outerWallWidth) trayPerimeter();
}

/* -------- Corner reinforcements --------- */
module cornerReinforcementProfile() {
	linear_extrude(traySize[2]) polygon([[0, 0], [-cornerReinforcementSize, 0], [0, cornerReinforcementSize]]);
}
for(a = [0 : 3]) {
	translate(cornerPositions[a]) rotate(a * 90) cornerReinforcementProfile();
}

/* -------- Horizontal mounts --------- */
module horizontalMountProfile() {
	dp = horizontalMountDepth;
	ew = horizontalMountExtWidth/2;
	bw = horizontalMountBaseWidth/2;
	polygon([[0, bw], [dp, ew], [dp, -ew], [0, -bw]]);
}
for(a = [0 : 3]) translate(cornerPositions[a]) rotate(a * 90) {
	d = rotatedDimensions[a];
	dUnitSize = unitSize[d];
	hUnitSize = unitSize[2];

	dp = horizontalMountDepth;
	ew = horizontalMountExtWidth/2;
	bw = horizontalMountBaseWidth/2;

	for(x = [0 : unitCount[d] - 1]) {
		for(y = [0 : unitCount[2] - 1]) translate([0, dUnitSize * (x + 0.5), hUnitSize * y]) {
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
				rotate([90, 0, 0]) linear_extrude(dUnitSize, center=true) polygon([[0, -0.01], [dp + 0.01, -0.01], [dp + 0.01, horizontalMountKickIn]]);

				// Kick out
				translate([0, 0, unitSize[2] / 2]) rotate([90, 0, 0]) linear_extrude(dUnitSize, center=true) polygon([[0, 0.01], [dp + 0.01, 0.01], [dp + 0.01, -horizontalMountKickOut]]);
			}
		}
	}
}