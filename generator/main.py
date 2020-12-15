import argparse
import concurrent.futures
import shutil
import copy
import re

from config import *
import funcs
from cargs import args

def main():
	outputDir = "models"

	executor = concurrent.futures.ThreadPoolExecutor()

	# Delete the "data" outputs directory
	if args.clear and os.path.exists("models"):
		print("Deleting old models...")
		while True:
			try:
				shutil.rmtree("models")
				break

			except OSError:
				continue

		print("Old models deleted")

	# Generate all the stuff
	for system in systems:
		for key in system:
			cfg[key] = system[key]

		systemName = cfg["systemName"]
		systemDirName = "SYS_" + systemName

		for horSizeOpt in system["horizontalUnitCountOptions"]:
			ucVariants = [horSizeOpt]

			# Add inverse option if it is not square
			if horSizeOpt[0] != horSizeOpt[1]:
				ucVariants.append([horSizeOpt[1], horSizeOpt[0]])
			
			for unitCountXY in ucVariants:
				unitCountX = unitCountXY[0]
				unitCountY = unitCountXY[1]

				cfg["unitCount"][0] = unitCountX
				cfg["unitCount"][1] = unitCountY

				for unitCountZ in system["verticalUnitCountOptions"]:
					cfg["unitCount"][2] = unitCountZ

					componentSize = [
						cfg["unitSize"][0] * unitCountX,
						cfg["unitSize"][1] * unitCountY,
						cfg["unitSize"][2] * unitCountZ
					]
					drawerEnabled = True # componentSize[2] >= 30

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
					if drawerEnabled:
						executor.submit(funcs.compileScad,
						F"{outputDir}/{systemDirName}/drawer_trays",
						F"{systemName}_W{unitCountStr}",
						copy.deepcopy(cfg), "drawer_tray")

					for pattern in patterns:
						patternBaseName = os.path.basename(os.path.splitext(pattern)[0])
						patternMatch = re.fullmatch("(.*?)(?:_x([A-Z]*))?", patternBaseName)
						patternName = patternMatch.group(1)
						patternFlags = str(patternMatch.group(2))

						rotations = [(0, "")]
						if "R" in patternFlags:
							rotations.append((90, "_R"))

						for rot in rotations:
							rotAngle, rotStr = rot
							cfg["innerWallRotation"] = rotAngle

							for innerWallPercentageHeight in innerWallPercentageHeights:
								cfg["innerWallPercentageHeight"] = innerWallPercentageHeight["val"]
								cfg["innerWallPatternFile"] = pattern

								innerHeightName = innerWallPercentageHeight["name"]

								# Tray - no need for swapped width/height as they are symmetrical
								if unitCountX >= unitCountY and (unitCountX != unitCountY or rot[0] == 0):
									executor.submit(funcs.compileScad,
									F"{outputDir}/{systemDirName}/trays/{unitCountDirStr}",
									F"{systemName}_T{unitCountStr}{innerHeightName}_{patternName}{rotStr}",
									copy.deepcopy(cfg), "tray")

								# Drawer
								if drawerEnabled:
									executor.submit(funcs.compileScad,
									F"{outputDir}/{systemDirName}/drawers/{unitCountDirStr}",
									F"{systemName}_D{unitCountStr}{innerHeightName}_{patternName}{rotStr}",
									copy.deepcopy(cfg), "drawer")

	executor.shutdown()