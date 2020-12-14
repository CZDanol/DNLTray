include <drawer_common.scad>

rotate([0, 0, 180]) {
	drawerRails();
	drawerShell();
	drawerInnerWalls();
	drawerHandle();
	translate([0, drawerLength/2 + drawerSideOffset/2, drawerHeight + drawerBottomOffset - drawerLabelHolderOffset]) labelHolder();
}