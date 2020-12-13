include <config.scad>

traySize = [unitSize[0] * unitCount[0], unitSize[1] * unitCount[1], unitSize[2] * unitCount[2]];

cornerPositions = [
	[-traySize[0] / 2, -traySize[1] / 2],
	[traySize[0] / 2, -traySize[1] / 2],
	[traySize[0] / 2, traySize[1] / 2],
	[-traySize[0] / 2, traySize[1] / 2]
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
	linear_extrude(traySize[2]) polygon([[0, 0], [cornerReinforcementSize, 0], [0, cornerReinforcementSize]]);
}
for(a = [0 : 3]) {
	translate(cornerPositions[a]) rotate(a * 90) cornerReinforcementProfile();
}

/* -------- Horizontal mounts --------- */
module horizontalMountProfile() {
	depth = 2;
	baseWidth = 3;
	extWidth = 4;

	polygon([[0, baseWidth/2], [-depth, extWidth/2], [-depth, -extWidth/2], [0, -baseWidth/2]]);
}
for(a = [0 : 3]) translate(cornerPositions[a]) rotate(a * 90) {
	d = rotatedDimensions[a];
	dUnitSize = unitSize[d];
	hUnitSize = unitSize[2];

	for(x = [0 : unitCount[d] - 1]) {
		for(y = [0 : unitCount[2] - 1]) translate([0, dUnitSize * (x + 0.5), hUnitSize * y]) {
			linear_extrude(hUnitSize / 2) horizontalMountProfile();
		}
	}
}