/* -------------- Basic shape -------------- */

// Size of a single tray unit in mm
unitSize = [80, 80, 20];

// How many units the current tray consists of
unitCount = [2, 1, 2];

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