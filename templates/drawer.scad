include <drawer_common.scad>

rotate([0, 0, 180]) {
	difference() {
		union() {
			drawerRails();
			drawerShell();
			drawerInnerWalls();
			drawerHandle();
			translate([0, drawerLength/2 + drawerSideOffset/2, drawerHeight + drawerBottomOffset - drawerLabelHolderOffset]) labelHolder();
		}

		translate([drawerWidth/2 - 3, drawerSideOffset/2 + drawerLength/2 - 3, drawerBottomOffset]) modelLabel();
	}
}