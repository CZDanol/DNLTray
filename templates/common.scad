labelWidth = 60;
labelHeight = 10;
labelDepth = 0.5;
labelHolderWidth = 0.6;
labelHolderRamp = 1;

absComponentSize = [
	unitSize[0] * unitCount[0],
	unitSize[1] * unitCount[1],
	unitSize[2] * unitCount[2]
	];

adjComponentSize = [
	absComponentSize[0] - horizontalMountDepth,
	absComponentSize[1] - horizontalMountDepth,
	absComponentSize[2]
	];

absCornerPositions = [
	[absComponentSize[0] / 2, -absComponentSize[1] / 2],
	[absComponentSize[0] / 2, absComponentSize[1] / 2],
	[-absComponentSize[0] / 2, absComponentSize[1] / 2],
	[-absComponentSize[0] / 2, -absComponentSize[1] / 2]
];

adjCornerPositions = [
	[adjComponentSize[0] / 2, -adjComponentSize[1] / 2],
	[adjComponentSize[0] / 2, adjComponentSize[1] / 2],
	[-adjComponentSize[0] / 2, adjComponentSize[1] / 2],
	[-adjComponentSize[0] / 2, -adjComponentSize[1] / 2]
];

rotatedDimensions = [1, 0, 1, 0];

module componentPerimeter() {
	square([adjComponentSize[0], adjComponentSize[1]], true);
}

module compartmentsProfile() {
	import(innerWallPatternFile, center=true, convexity=10);
}

/* -------- Floor --------- */
module componentFloor() {
	linear_extrude(floorWidth) componentPerimeter();
}

/* -------- Outer wall --------- */
module outerWall() {
	linear_extrude(absComponentSize[2], convexity=10) difference() {
		componentPerimeter();
		offset(delta=-outerWallWidth) componentPerimeter();
	}
}

/* -------- Corner reinforcements --------- */
module cornerReinforcementProfile() {
	linear_extrude(absComponentSize[2]) polygon([[0, 0], [-cornerReinforcementSize, 0], [0, cornerReinforcementSize]]);
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
module horizontalMounts(skipFront = false) {
	for(a = [0 : 3]) if(a != 1 || !skipFront) translate(absCornerPositions[a]) rotate(a * 90) {
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
					rotate([90, 0, 0]) linear_extrude(dUnitSize, center=true) polygon([[0, 0], [dp, 0], [dp, horizontalMountKickIn]]);

					// Kick out
					translate([0, 0, unitSize[2] / 2]) rotate([90, 0, 0]) linear_extrude(dUnitSize, center=true) polygon([[0, 0], [dp, 0], [dp, -horizontalMountKickOut]]);
				}
			}
		}
	}
}

/* ---------- Vertical mounts ------------------ */
module verticalMountsProfile(inner = true) {
	offset = verticalMountInset + horizontalMountDepth / 2;
	hvm = verticalMountLength;
	ohvm = offset - hvm;

	for(y = [0 : unitCount[1] - 1]) {
		for(x = [0 : unitCount[0] - 1]) translate([-absComponentSize[0] / 2 + unitSize[0] * x, -absComponentSize[1] / 2 + unitSize[1] * y, 0]) {
			if(inner || x == 0)
				translate([offset, unitSize[1] / 2, 0]) square([verticalMountWidth, verticalMountLength], center=true);

			if(inner || x == unitCount[0] - 1)
				translate([unitSize[0] - offset, unitSize[1] / 2, 0]) square([verticalMountWidth, verticalMountLength], center=true);
			
			if(inner || y == 0)
				translate([unitSize[0] / 2, offset, 0]) square([verticalMountLength, verticalMountWidth], center=true);

			if(inner || y == unitCount[1] - 1)	
				translate([unitSize[0] / 2, unitSize[1] - offset, 0]) square([verticalMountLength, verticalMountWidth], center=true);
		}
	}
}
module verticalMountsIncl() {
	dp = verticalMountInset + horizontalMountDepth / 2;

	// Male top
	translate([0, 0, absComponentSize[2]])
		linear_extrude(verticalMountHeight) verticalMountsProfile(inner = false);

	// Top reinforcement
	intersection() {
		union() for(a = [0 : 3]) translate([0, 0, absComponentSize[2]]) translate(adjCornerPositions[a]) rotate(a * 90) {
			d = rotatedDimensions[a];
			rotate([90, 0, 180]) linear_extrude(adjComponentSize[d]) polygon([[0, -horizontalMountKickIn], [dp, 0], [0, 0]]);
		}

		linear_extrude(absComponentSize[2]) offset(delta=verticalMountReinforcementDistance) verticalMountsProfile(inner = false);
	}

	// Bottom reinforcement
	linear_extrude(verticalMountHeight + verticalMountClearance + verticalMountReinforcementDistance) intersection() {
		offset(delta=verticalMountReinforcementDistance) verticalMountsProfile();
		componentPerimeter();
	}
}
module verticalMountsExcl() {
	// Female bottom
	linear_extrude(verticalMountHeight + verticalMountClearance) offset(delta=verticalMountTolerance) verticalMountsProfile();
}

module labelHolder() {
	translate([0, 0, -labelHeight/2]) rotate([-90, 0, 0]) {
		difference() {
			linear_extrude(labelDepth + labelHolderWidth) difference() {
				square([labelWidth + labelHolderWidth * 2, labelHeight], center=true);
				translate([0, -labelHolderWidth / 2]) square([labelWidth - labelHolderWidth * 2, labelHeight - labelHolderWidth], center=true);
			}
			linear_extrude(labelDepth) square([labelWidth, labelHeight], center=true);
		}
		translate([0, labelHeight/2, 0]) rotate([0, 90, 0]) linear_extrude(labelWidth + labelHolderWidth * 2, center=true) polygon([[0, 0], [-labelHolderWidth - labelDepth, 0], [0, labelHolderRamp]]);
	}
}

module modelLabel() {
	sz = 2.5;
	spc = 4;
	fnt = "Andale Mono";

	rotate([0, 180, 0]) linear_extrude(0.6, center=true) {
		translate([0, 0, 0]) text(modelName, size=sz, valign="top", font=fnt);
		translate([0, -spc, 0]) text(version, size=sz, valign="top", font=fnt);
		translate([0, -spc*2, 0]) text("DESIGNED BY DANOL", size=sz, valign="top", font=fnt);
	}
}