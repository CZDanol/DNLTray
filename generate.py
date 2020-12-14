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
	scadDir = F"{baseDir}/scad"

	scadFileName = F"{scadDir}/{fileName}.scad"
	stlFileName = F"{baseDir}/stl/{fileName}.stl"
	previewScadFileName = F"{baseDir}/{fileName}.preview.scad"
	previewFileName = F"{baseDir}/png/{fileName}.png"

	makeFileDir(scadFileName)
	makeFileDir(stlFileName)
	makeFileDir(previewFileName)

	template = os.path.relpath(F"{template}.scad", scadDir)
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
		"innerWallPatternFile": None,

		"innerWallWidth": 0.6,

		#  Inner walls don't have to go up to the whole tray height. This number states how many millimeters are the inner walls below the tray height.
		"innerWallClearance": None,

		# HORIZONTAL MOUNT
		# =======================

		# How many extra free vertical space to allow better horizontal mount in-sliding
		"horizontalMountClearance": 1,

		# How much free space in the horizontal mount sliders
		"horizontalMountTolerance": 0.3,

		"horizontalMountDepth": 2,

		"horizontalMountBaseWidth": 2,

		"horizontalMountExtWidth": 5,

		# Distance between male and female part of the connector
		"horizontalMountConenctorDistance": None,

		# Height of the wedge for horizontal mounts on the bottom side (to prevent needing supports)
		"horizontalMountKickIn": 3,

		# Height of the wedge for horizontal mounts on the top side (so the thing isn't that sharp)
		"horizontalMountKickOut": 1,

		# VERTICAL MOUNT
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

				for unitCountZ in [1]:#[1, 2, 3]:
					cfg["unitCount"][2] = unitCountZ

					unitCountStr = F"{unitCountX}{unitCountY}{unitCountZ}"

					innerWallClearances = [
						{
							"name": "FULL",
							"val": 0
						},
						{
							"name": "HALF",
							"val": cfg["unitSize"][2] * unitCountZ / 2
						}
					]

					for pattern in patterns:
						cfg["pattern"] = pattern
						patternName = os.path.basename(os.path.splitext(pattern)[0])

						for innerWallClearance in innerWallClearances:
							cfg["innerWallClearance"] = innerWallClearance["val"]
							cfg["innerWallPatternFile"] = pattern

							innerWallClearanceName = innerWallClearance["name"]

							# Tray - no need for swapped width/height as they are symmetrical
							if unitCountX >= unitCountY:
								executor.submit(compileScad,
								F"{outputDir}/{systemDirName}/trays/{unitCountStr}",
								F"TRAY_{systemName}{unitCountStr}_{innerWallClearanceName}_{patternName}",
								copy.deepcopy(cfg), "template_tray")

	executor.shutdown()


main()