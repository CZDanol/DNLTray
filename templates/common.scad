use <Quantico-Regular.ttf>

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
	rotate([0, 0, innerWallRotation]) import(innerWallPatternFile, center=true, convexity=10);
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

module verticalMountsProfileUnit(delta, onlySquare=false) {
	pts = [[-verticalMountWidth/2, 0], [0, verticalMountHeight], [verticalMountWidth/2, 0]];

	if(onlySquare)
		square([verticalMountWidth + delta*2, verticalMountLength + delta*2], center=true);
	else
		rotate([90, 0, 0]) linear_extrude(verticalMountLength + delta, center=true) offset(delta) polygon(pts);
}

/* ---------- Vertical mounts ------------------ */
module verticalMountsProfile(inner=true, delta=0, onlySquare=false) {
	offset = verticalMountInset + horizontalMountDepth / 2;
	hvm = verticalMountLength;
	ohvm = offset - hvm;

	for(y = [0 : unitCount[1] - 1]) {
		for(x = [0 : unitCount[0] - 1]) translate([-absComponentSize[0] / 2 + unitSize[0] * x, -absComponentSize[1] / 2 + unitSize[1] * y, 0]) {
			if(inner || x == 0)
				translate([offset, unitSize[1] / 2, 0]) verticalMountsProfileUnit(delta, onlySquare);

			if(inner || x == unitCount[0] - 1)
				translate([unitSize[0] - offset, unitSize[1] / 2, 0]) verticalMountsProfileUnit(delta, onlySquare);
			
			if(inner || y == 0)
				translate([unitSize[0] / 2, offset, 0]) rotate([0, 0, 90]) verticalMountsProfileUnit(delta, onlySquare);

			if(inner || y == unitCount[1] - 1)	
				translate([unitSize[0] / 2, unitSize[1] - offset, 0]) rotate([0, 0, 90]) verticalMountsProfileUnit(delta, onlySquare);
		}
	}
}
module verticalMountsIncl() {
	dp = verticalMountInset + horizontalMountDepth / 2;

	// Male top
	translate([0, 0, absComponentSize[2]])
		verticalMountsProfile(inner = false);

	// Top reinforcement
	intersection() {
		union() for(a = [0 : 3]) translate([0, 0, absComponentSize[2]]) translate(adjCornerPositions[a]) rotate(a * 90) {
			d = rotatedDimensions[a];
			rotate([90, 0, 180]) linear_extrude(adjComponentSize[d]) polygon([[0, -horizontalMountKickIn], [dp, 0], [0, 0]]);
		}

		linear_extrude(absComponentSize[2]) verticalMountsProfile(inner=false, delta=verticalMountReinforcementDistance, onlySquare=true);
	}

	// Bottom reinforcement
	linear_extrude(verticalMountHeight + verticalMountClearance) intersection() {
		verticalMountsProfile(delta=verticalMountReinforcementDistance, onlySquare=true);
		componentPerimeter();
	}
}
module verticalMountsExcl() {
	// Female bottom
	// linear_extrude(verticalMountHeight + verticalMountClearance) offset(delta=verticalMountTolerance) verticalMountsProfile();
	verticalMountsProfile(verticalMountTolerance);
}

module labelHolder() {
	if(adjComponentSize[2] >= 30)	translate([0, 0, -labelHeight/2]) rotate([-90, 0, 0]) {
		difference() {
			linear_extrude(labelDepth + labelHolderWidth) difference() {
				square([labelWidth + labelHolderWidth * 2, labelHeight], center=true);
				translate([0, -labelHolderInset / 2]) square([labelWidth - labelHolderInset * 2, labelHeight - labelHolderInset], center=true);
			}
			linear_extrude(labelDepth) square([labelWidth, labelHeight], center=true);
		}
		translate([0, labelHeight/2, 0]) rotate([0, 90, 0]) linear_extrude(labelWidth + labelHolderWidth * 2, center=true) polygon([[0, 0], [-labelHolderWidth - labelDepth, 0], [0, labelHolderRamp]]);
	}
}

module modelLabel() {
	sz = 3;
	spc = 4;
	fnt = "Quantico";
	fn = 0;

	rotate([0, 180, 0]) linear_extrude(0.6, center=true) {
		translate([0, 0, 0]) text(modelName, size=sz, valign="top", font=fnt, $fn=fn);
		translate([0, -spc, 0]) text(version, size=sz, valign="top", font=fnt, $fn=fn);
		translate([0, -spc*2, 0]) text("DNLTray", size=sz, valign="top", font=fnt, $fn=fn);
	}
}