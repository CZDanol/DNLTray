/* -------------- Basic shape -------------- */

// Size of a single tray unit in mm
unitSize = [80, 80, 20];

// How many units the current tray consists of
unitCount = [1, 1, 1];

// Size of the wedges in the corners
cornerReinforcementSize = 4;

outerWallWidth = 1;

floorWidth = 1;

/* -------- Inner walls --------- */
innerWallPatternFile = "patterns/2x2.svg";

innerWallWidth = 0.6;

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
horizontalMountConenctorDistance = 16;

// Height of the wedge for horizontal mounts on the bottom side (to prevent needing supports)
horizontalMountKickIn = 3;

// Height of the wedge for horizontal mounts on the top side (so the thing isn't that sharp)
horizontalMountKickOut = 1;

/* -------------- Vertical mount -------------------- */
verticalMountHeight = 1;

verticalMountWidth = 1;

verticalMountLength = 10;

// How far away from the outer shell are the vertical mounts
verticalMountInset = 2;

// How much extra vertical space is in the female vertical mount
verticalMountClearance = 0.5;

// How much extra horizontal space is in the female vertical mount
verticalMountTolerance = 0.5;

// Plastic around the vertical mount hole
verticalMountReinforcementDistance = 0.5;