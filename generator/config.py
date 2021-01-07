import os

patterns = [p for p in os.listdir("patterns") if p.endswith(".svg")]

compartmentsHeights = [
	{
		"id": "F",
		"text": "",

		"config": {
			"innerWallPercentageHeight": 1
		}
	},
	{
		"id": "H",
		"text": "Half height",

		"config": {
			"innerWallPercentageHeight": 0.5
		}
	}
]

compartmentsTransforms = [
	{
		"id": "",
		"text": "",

		"config": {
			"innerWallRotation": 0
		}
	},
	{
		"id": "R",
		"text": "Rotated pattern",

		"config": {
			"innerWallRotation": 90
		}
	}
]

drawerTrayVersions = [
	{
		"id": "",
		"text": "",
		"config": {}
	},
	{
		"id": "L",
		"text": "Without floor",
		"config": {
			"floorOutlineOnly": 1
		}
	}
]

defaultConfig = {
	# CORE STUFF
	# =======================

	# ID of the current version
	"version": "v0.9.1",

	# Count of units in the tray, is dynamically changed
	"unitCount": [0, 0, 0],

	# Size of an atomic tray unit, dynamically changed
	"unitSize": [0, 0, 0],

	# LABEL
	# ==========================
	"labelWidth": 35,
	"labelHeight": 10,
	"labelDepth": 0.5,

	# Width of the label holder frame
	"labelHolderWidth": 0.6,

	# How much paper the label holder hides
	"labelHolderInset": 2,

	# Size of the ramp on the bottom of the holder
	"labelHolderRamp": 1,

	# OUTER WALL
	# =======================

	"outerWallWidth": 1,
	"floorWidth": 1,
	"floorOutlineOnly": 0,

	# Size of the wedges in the corners
	"cornerReinforcementSize": 4,
	
	# INNER WALL
	# =======================

	# Automaticaly filled
	"innerWallPatternFile": "",

	"innerWallWidth": 0.6,

	#  Inner walls don't have to go up to the whole tray height. This number represents a ratio of the total component height where the inner walls go.
	"innerWallPercentageHeight": 1,

	# Rotation (in degrees) of the inner walls profile
	"innerWallRotation": 0,

	# HORIZONTAL MOUNTS
	# =======================

	# How many extra free vertical space to allow better horizontal mount in-sliding
	"horizontalMountClearance": 1,

	# How much free space in the horizontal mount sliders
	"horizontalMountTolerance": 0.3,

	"horizontalMountDepth": 2,

	"horizontalMountBaseWidth": 2,

	"horizontalMountExtWidth": 5,

	# Distance between male and female part of the connector
	"horizontalMountConenctorDistance": 0,

	# Height of the wedge for horizontal mounts on the bottom side (to prevent needing supports)
	"horizontalMountKickIn": 3,

	# Height of the wedge for horizontal mounts on the top side (so the thing isn't that sharp)
	"horizontalMountKickOut": 1,

	# VERTICAL MOUNTS
	# =======================

	"verticalMountHeight": 1.5,

	"verticalMountWidth": 1,

	"verticalMountLength": 10,

	# How far away from the outer shell are the vertical mounts
	"verticalMountInset": 2,

	# How much extra vertical space is in the female vertical mount
	"verticalMountClearance": 0.2,

	# How much extra horizontal space is in the female vertical mount
	"verticalMountTolerance": 0.4,

	# Plastic around the vertical mount hole
	"verticalMountReinforcementDistance": 1,

	# DRAWERS
	# =======================
	
	# Distance of the bottom of the drawer from the bottom of the component
	# Drawer height is component height - bottom offset - top offset
	"drawerBottomOffset": 2,

	# Distance of the top of the drawer from the top of the component
	"drawerTopOffset": 1,

	# Distance of the drawer from the side walls (outer edge)
	"drawerSideOffset": 4,

	# How much space is there above the drawer (in the drawer slot hole)
	"drawerTopTolerance": 0.5,

	# How much space is there on the sides (in the drawer slot hole)
	"drawerSideTolerance": 0.3,

	# Z position of the drawer rail (from the component bottom)
	"drawerRailPos": 10,

	# Height of the drawer rail
	"drawerRailHeight": 4,

	# Depth of the drawer rail 
	"drawerRailWidth": 2,

	# How much extra space is there in the drawer rail slots
	"drawerRailTolerance": 0.5,

	# Size of the wedge on the bottom of the drawer rail slot (in the tray component)
	"drawerRailHolderWedge": 2,

	# Outer width of the drawer walls (inner width the same as in trays)
	"drawerWallWidth": 1,

	# Width of the drawer floor
	"drawerFloorWidth": 1,

	# Distance of the label holder from the top
	"drawerLabelHolderOffset": 2,

	# DRAWER NOTCHES
	# =======================
	# Drawers have a little notch that prevents them from sliding out

	# This is the length of the notch (how long part of the rail it occupies)
	"drawerNotchLength": 1,

	# Position of the notch -> distance from the front of the drawer
	"drawerNotchPosition": 5,

	# Depth of the notch - the higher the value, the harder it is to pull the drawer out
	"drawerNotchDepth": 0.8,

	# How much the notch slot is larger than the notch
	"drawerNotchTolerance": 0.5,

	# DRAWER HANDLES
	# =======================

	# Distance  of the handle ends from the drawer edges (left and right)
	"drawerHandleOffset": 5,

	# Z position of the handle
	"drawerHandlePos": 10.5,

	# Size of the handle
	"drawerHandleSize": 10,

	# Width of the handle outline
	"drawerHandleWidth": 1,

	# WALLS
	# =========================

	# Width of the wall (in mm)
	"wallWidth": 2,

	# Diameter of the hole for a screw
	"screwHoleDiameter": 4,
}
