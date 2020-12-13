# USAGE: generate.py (OPEN SCAD EXE)

import sys
import os
import numbers
import shutil
import time
import subprocess
import concurrent.futures

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
	while True:
		try:
			os.makedirs(os.path.dirname(file), exist_ok=True)
			break

		except PermissionError:
			continue

	f = open(file, "w")
	f.write(content)
	f.close()

	print("Created " + file)

def compileScad(file):
	subprocess.run([
		sys.argv[1],
		file + ".scad",
		"--o", file + ".stl",
		"--o", file + ".png",
		])
	print("Compiled " + file)

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
		"verticalMountReinforcementDistance": 0.5,
	}
	systems = [
		{
			"systemName": "A",
			"unitSize": [40, 40, 20],
			"horizontalMountConenctorDistance": 8
		}
	]
	patterns = [p for p in os.listdir("patterns") if p.endswith(".svg")]

	executor = concurrent.futures.ThreadPoolExecutor()

	# Delete the "data" outputs directory
	if os.path.exists("data"):
		shutil.rmtree("data")

	# Generate all the stuff
	for system in systems:
		for key in system:
			cfg[key] = system[key]

		for unitCountX in [1, 2]:
			cfg["unitCount"][0] = unitCountX

			for unitCountY in [1, 2]:
				cfg["unitCount"][1] = unitCountY

				for unitCountZ in [1]:#[1, 2, 3]:
					cfg["unitCount"][2] = unitCountZ

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
						patternBaseName = os.path.basename(os.path.splitext(pattern)[0])

						for innerWallClearance in innerWallClearances:
							cfg["innerWallClearance"] = innerWallClearance["val"]

							fileDir = "{}/{}x{}x{}".format(cfg["systemName"], unitCountX, unitCountY, unitCountZ)
							filename = "{}__{}__{}".format(fileDir.replace("/", "__"), patternBaseName, innerWallClearance["name"])
							filePath = "data/{}/{}".format(fileDir, filename)
							filePathDir = os.path.dirname(filePath)

							cfg["innerWallPatternFile"] = os.path.relpath("patterns/" + pattern, filePathDir)
							configString = configStr(cfg)

							# Create the scad file
							writeFile(filePath + ".scad", configString + "include <{}>;".format(os.path.relpath("template_tray.scad", filePathDir)))

							# Compile the scad file
							executor.submit(compileScad, filePath)

	executor.shutdown()


main()