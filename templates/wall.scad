include <common.scad>;

rotate([90, 0, 180]) {
	a = 1;

	d = rotatedDimensions[a];
	dUnitSize = unitSize[d];
	vUnitSize = unitSize[2];

	translate([absCornerPositions[a][0], 0]) rotate(a * 90) {
		for(x = [0 : unitCount[d] - 1]) {
			for(z = [0 : unitCount[2] - 1]) {
				translate([0, dUnitSize * (x + 0.5), vUnitSize * z]) {
					horizontalMount(a, inclKickIn=true);

					subFrameWidth = 1;
					translate([0, -dUnitSize * 0.5]) cube([horizontalMountDepth, subFrameWidth, vUnitSize]);
					translate([0, dUnitSize * 0.5 - subFrameWidth]) cube([horizontalMountDepth, subFrameWidth, vUnitSize]);
				}
			}
		}
	}

	translate([-absCornerPositions[a][0], 0]) rotate([90, 0, 0]) linear_extrude(wallWidth) {
		difference() {
			square([absComponentSize[0], absComponentSize[2]]);

			for(x = [0 : unitCount[d] - 1]) {
				for(z = [0 : unitCount[2] - 1]) {
					difference() {
						translate([dUnitSize * x, vUnitSize * z + unitSize[2] / 2])
						offset(delta=-1) square([unitSize[0], unitSize[2] / 2]);

						translate([dUnitSize * (x + 0.5), vUnitSize * z + unitSize[2] * 0.75])
						circle(d=vUnitSize * 0.5 + 2, $fn=32);
					}

					translate([dUnitSize * (x + 0.5), vUnitSize * z + unitSize[2] * 0.75])
					circle(d=screwHoleDiameter, $fn=32);
				}
			}
		}
	}
}