/* -------------- Basic shape -------------- */

// Size of a single tray unit in mm
unitSize = [80, 80, 20];

// How many units the current tray consists of
unitCount = [1, 1, 1];

// Size of the wedges in the corners
cornerReinforcementSize = 4;

outerWallWidth = 1;

floorWidth = 2;

/* -------- Inner walls --------- */
innerWallPatternFile = "patterns/2x2.svg";

innerWallWidth = 1;

// Inner walls don't have to go up to the whole tray height. This number states how many millimeters are the inner walls below the tray height.
innerWallClearance = 0;

/* ----------- Horizontal mount ----------------- */
// How many extra free vertical space to allow better horizontal mount in-sliding
horizontalMountClearance = 1;

// How much free space in the horizontal mount sliders
horizontalMountTolerance = 0.4;

horizontalMountDepth = 2;

horizontalMountBaseWidth = 2;

horizontalMountExtWidth = 4;

// Distance between male and female part of the connector
horizontalMountConenctorDistance = 20;

// Height of the wedge for horizontal mounts on the bottom side (to prevent needing supports)
horizontalMountKickIn = 3;

// Height of the wedge for horizontal mounts on the top side (so the thing isn't that sharp)
horizontalMountKickOut = 1;

/* -------------- Vertical mount -------------------- */
verticalMountHeight = 1;
verticalMountWidth = 0.5;
verticalMountClearance = 0.4;
verticalMountTolerance = 0.5;