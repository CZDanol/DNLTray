include <common.scad>;

a = 1;

d = rotatedDimensions[a];
dUnitSize = unitSize[d];
vUnitSize = unitSize[2];

rotate([90, 0, 180]) {
	difference() {
		union() {
			translate([absCornerPositions[a][0], 0]) rotate(a * 90) {
				for(x = [0 : unitCount[d] - 1]) {
					for(z = [0 : unitCount[2] - 1]) {
						translate([0, dUnitSize * (x + 0.5), vUnitSize * z])
							horizontalMount(a, inclKickIn=true);
					}
				}
			}

			translate([-absCornerPositions[a][0], 0]) rotate([90, 0, 0]) linear_extrude(wallWidth, convexity=10) {
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
						}
					}
				}
			}
		}

		translate([-absCornerPositions[a][0], 0.005, 0]) rotate([a * 90, 0, 0])	
		for(x = [0 : unitCount[d] - 1]) {
			for(z = [0 : unitCount[2] - 1]) {
				translate([dUnitSize * (x + 0.5), vUnitSize * z + unitSize[2] * 0.75])
				cylinder(h=wallWidth + 0.01, d1=wallTopScrewHoleDiameter, d2=wallBottomScrewHoleDiameter, $fn=32);
			}
		}

		rotate([-90, 0, 0]) translate([adjComponentSize[0]/2 - 1, adjComponentSize[1]/2 - 1, -wallWidth]) modelLabel(singleLine=true);
	}
}