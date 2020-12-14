include <common.scad>;

drawerWidth = adjComponentSize[0] - drawerSideOffset * 2;
drawerHeight = adjComponentSize[2] - drawerTopOffset - drawerBottomOffset;
drawerLength = adjComponentSize[1] - drawerSideOffset;

module drawerRails(tolerance=false, holder=false) {
	hdrh = drawerRailHeight / 2;
	to = hdrh + 1;

	railPoints = [[0, -hdrh], [drawerRailWidth, 0], [0, hdrh]];
	holderPoints = [[0, -to], [drawerRailWidth, -to - drawerRailHolderWedge], [drawerRailWidth, to + drawerRailHolderWedge], [0, to]];
	notchPoints = [[0, -hdrh - drawerNotchDepth], [drawerRailWidth, 0], [0, hdrh]];

	delta = tolerance ? drawerRailTolerance : 0;
	points = holder ? holderPoints : railPoints;
	len = holder ? adjComponentSize[1] : drawerLength;

	translate([0, holder ? 0 : drawerSideOffset/2, drawerRailPos]) rotate([90, 0, 0]) {
		// Rails
		translate([drawerWidth/2, 0, 0]) linear_extrude(len, center=true) offset(delta) polygon(points);
		translate([-drawerWidth/2, 0, 0]) rotate([0, 180, 0]) linear_extrude(len, center=true) offset(delta) polygon(points);

		// A little notch so that the drawers stay close
		translate([drawerWidth/2, 0, -drawerLength/2 + drawerNotchPosition]) linear_extrude(drawerNotchLength + (tolerance ? drawerNotchTolerance : 0), center=true) offset(delta) polygon(notchPoints);
		translate([-drawerWidth/2, 0, -drawerLength/2 + drawerNotchPosition]) rotate([0, 180, 0]) linear_extrude(drawerNotchLength + (tolerance ? drawerNotchTolerance : 0), center=true) offset(delta) polygon(notchPoints);
	}
}

module drawerRailsHolder() {
	translate([0, drawerSideOffset, drawerRailPos]) cube([10, 10, drawerRailHeight + 2], center=true);
	drawerRails(holder=true);
}

module drawerHoleExcl() {
	translate([0, drawerSideOffset/2, drawerBottomOffset]) linear_extrude(1000) square([drawerWidth + drawerSideTolerance * 2, drawerLength], center=true);
	drawerRails(tolerance=true);
}

module drawerShell() {
	translate([0, drawerSideOffset/2, drawerBottomOffset]) difference() {
		linear_extrude(drawerHeight) square([drawerWidth, drawerLength], center=true);
		translate([0, 0, drawerFloorWidth]) linear_extrude(drawerHeight) offset(delta=-drawerFloorWidth) square([drawerWidth, drawerLength], center=true);
	}
}

module drawerInnerWalls() {
	// We intersect with the tray perimeter so that the offset lines do not go outside
	translate([0, drawerSideOffset/2, drawerBottomOffset]) linear_extrude(drawerHeight * innerWallPercentageHeight) offset(delta=innerWallWidth/2) intersection() {
		offset(delta=+0.0001) resize([drawerWidth - drawerWallWidth * 2 + 0.002, drawerLength - drawerWallWidth * 2 + 0.002, 0], auto=true) compartmentsProfile();
		offset(delta=-outerWallWidth) square([drawerWidth, drawerLength], center=true);
	}
}

module drawerHandle() {
	handlePoints = [[0, 0], [0, drawerHandleSize], [drawerHandleSize, 0]];
	width = drawerWidth - drawerHandleOffset * 2;

	translate([0, drawerLength / 2 + drawerSideOffset / 2, drawerBottomOffset + drawerHandlePos]) rotate([0, 90, 0]) difference() {
		linear_extrude(width, center=true) polygon(handlePoints);
		translate([-drawerHandleWidth, 0, 0]) linear_extrude(width - drawerHandleWidth * 2, center=true) polygon(handlePoints);
	}
}