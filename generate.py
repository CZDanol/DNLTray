# USAGE: generate.py (OPEN SCAD EXE)

import sys
import os
import numbers
import shutil
import time
import subprocess
import copy
import threading
import concurrent.futures
import traceback

mutex = threading.Lock()

def makeFileDir(file):
	while True:
		try:
			os.makedirs(os.path.dirname(file), exist_ok=True)
			break

		except PermissionError:
			continue

def configVal(key, val):
	if isinstance(val, numbers.Number):
		return str(val)
	
	elif isinstance(val, str):
		return "\"" + val.replace("\\", "\\\\") + "\""

	elif isinstance(val, list):
		return "[" + ", ".join([configVal(key, i) for i in val]) + "]"

	else:
		raise Exception("Unsupported type for key " + key + ": " + str(type(val)))

def configStr(config):
	result = "// AUTO GENERATED CONFIG\n"

	for key in config:
		result += F"{key} = {configVal(key, config[key])};\n"

	result += "\n\n"

	return result

def writeFile(file, content):
	makeFileDir(file)
	f = open(file, "w")
	f.write(content)
	f.close()

def compileScad(baseDir, fileName, cfg, template):
	try:
		scadDir = F"{baseDir}/scad"

		scadFileName = F"{scadDir}/{fileName}.scad"
		stlFileName = F"{baseDir}/stl/{fileName}.stl"
		previewScadFileName = F"{baseDir}/{fileName}.preview.scad"
		previewFileName = F"{baseDir}/png/{fileName}.png"

		makeFileDir(scadFileName)
		makeFileDir(stlFileName)
		makeFileDir(previewFileName)

		template = os.path.relpath(F"templates/{template}.scad", scadDir)
		cfg["innerWallPatternFile"] = os.path.relpath("patterns/" + cfg["innerWallPatternFile"], scadDir)
		cfgStr = configStr(cfg)

		# Create the scad file
		writeFile(scadFileName, F"{cfgStr}\ninclude <{template}>;")

		# Create STL
		stlProc = subprocess.run([sys.argv[1], scadFileName, F"--o={stlFileName}"], capture_output=True)
		mutex.acquire()
		print("Compiled " + fileName)

		if len(stlProc.stdout):
			print(stlProc.stdout)

		if len(stlProc.stderr):
			print(stlProc.stderr)

		mutex.release()

		# Create preview of the STL
		# We create a preview scad importing the stl, should be faster than having to compile the original scad
		writeFile(previewScadFileName, "import(\"{}\");".format(os.path.relpath(stlFileName, baseDir).replace("\\", "\\\\")))
		subprocess.run([sys.argv[1], previewScadFileName, F"--o={previewFileName}.png", "--colorscheme=BeforeDawn"], capture_output=True)
		os.remove(previewScadFileName)

		print("Compiled " + fileName)

	except Exception as e:
		traceback.print_exc()

def main():
	cfg = {
		# CORE STUFF
		# =======================

		# Count of units in the tray, is dynamically changed
		"unitCount": [0, 0, 0],

		# Size of an atomic tray unit, dynamically changed
		"unitSize": [0, 0, 0],

		# OUTER WALL
		# =======================

		"outerWallWidth": 1,
		"floorWidth": 1,

		# Size of the wedges in the corners
		"cornerReinforcementSize": 4,
		
		# INNER WALL
		# =======================

		# Automaticaly filled
		"innerWallPatternFile": "",

		"innerWallWidth": 0.6,

		#  Inner walls don't have to go up to the whole tray height. This number represents a ratio of the total component height where the inner walls go.
		"innerWallPercentageHeight": 1,

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
		"verticalMountClearance": 0.5,

		# How much extra horizontal space is in the female vertical mount
		"verticalMountTolerance": 0.3,

		# Plastic around the vertical mount hole
		"verticalMountReinforcementDistance": 1,

		# DRAWERS
		# =======================
		
		# Distance of the bottom of the drawer from the bottom of the component
		# Drawer height is component height - bottom offset - top offset
		"drawerBottomOffset": 2,

		# Distance of the top of the drawer from the top of the component
		"drawerTopOffset": 2,

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
		"drawerRailTolerance": 0.3,

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
		"drawerNotchPosition": 10,

		# Depth of the notch - the higher the value, the harder it is to pull the drawer out
		"drawerNotchDepth": 0.5,

		# How much the notch slot is larger than the notch
		"drawerNotchTolerance": 0.5,

		# DRAWER HANDLES
		# =======================

		# Distance  of the handle ends from the drawer edges (left and right)
		"drawerHandleOffset": 5,

		# Z position of the handle
		"drawerHandlePos": 12,

		# Size of the handle
		"drawerHandleSize": 10,

		# Width of the handle outline
		"drawerHandleWidth": 1,
	}
	systems = [
		{
			"systemName": "A",
			"unitSize": [80, 80, 15],
			"horizontalMountConenctorDistance": 16
		}
	]
	patterns = [p for p in os.listdir("patterns") if p.endswith(".svg")]

	outputDir = "models"
	minComponentHeightForDrawers = 30

	executor = concurrent.futures.ThreadPoolExecutor()

	# Delete the "data" outputs directory
	if os.path.exists("models"):
		print("Deleting old models...")
		while True:
			try:
				shutil.rmtree("models")
				break

			except OSError:
				continue

		print("Old models deleted...")

	# Generate all the stuff
	for system in systems:
		for key in system:
			cfg[key] = system[key]

		systemName = cfg["systemName"]
		systemDirName = "SYS_" + systemName

		for unitCountX in [1, 2]:
			cfg["unitCount"][0] = unitCountX

			for unitCountY in [1, 2]:
				cfg["unitCount"][1] = unitCountY

				for unitCountZ in [1, 2, 3]:
					cfg["unitCount"][2] = unitCountZ

					componentHeight = cfg["unitSize"][2] * unitCountZ

					unitCountStr = F"{unitCountX}{unitCountY}{unitCountZ}"
					unitCountDirStr = F"size_{unitCountX}x{unitCountY}x{unitCountZ}"

					innerWallPercentageHeights = [
						{
							"name": "F",
							"val": 1
						},
						{
							"name": "H",
							"val": 0.5
						}
					]

					# Drawer tray
					if componentHeight >= minComponentHeightForDrawers:
						executor.submit(compileScad,
						F"{outputDir}/{systemDirName}/drawer_trays",
						F"{systemName}_DT{unitCountStr}",
						copy.deepcopy(cfg), "drawer_tray")

					for pattern in patterns:
						cfg["pattern"] = pattern
						patternName = os.path.basename(os.path.splitext(pattern)[0])

						for innerWallPercentageHeight in innerWallPercentageHeights:
							cfg["innerWallPercentageHeight"] = innerWallPercentageHeight["val"]
							cfg["innerWallPatternFile"] = pattern

							iwphn = innerWallPercentageHeight["name"]

							# Tray - no need for swapped width/height as they are symmetrical
							if unitCountX >= unitCountY:
								executor.submit(compileScad,
								F"{outputDir}/{systemDirName}/trays/{unitCountDirStr}",
								F"{systemName}_TR{unitCountStr}{iwphn}_{patternName}",
								copy.deepcopy(cfg), "tray")

							# Drawer
							if componentHeight >= minComponentHeightForDrawers:
								executor.submit(compileScad,
								F"{outputDir}/{systemDirName}/drawers/{unitCountDirStr}",
								F"{systemName}_DR{unitCountStr}{iwphn}_{patternName}",
								copy.deepcopy(cfg), "drawer")

	executor.shutdown()


main()