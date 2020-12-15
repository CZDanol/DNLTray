import argparse
import concurrent.futures
import shutil
import copy
import re

from config import *
from index import *
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

	addToIndex(
			F"{outputDir}",
			"0_T",
			"# Models\n"
			+ "This directory contains model scad files and image previews.\n"
			+ "## Systems"
			)

	# Generate all the stuff
	for system in systems:
		for key in system:
			cfg[key] = system[key]

		systemName = cfg["systemName"]
		systemDirName = "SYS_" + systemName

		addToIndex(
			F"{outputDir}/{systemDirName}",
			"0_T",
			"# System {}\n".format(systemName)
			+ "Unit size: {} x {} x {} mm\n".format(system["unitSize"][0], system["unitSize"][1], system["unitSize"][2])
			+ "## Directories\n"
			+ "* [Trays](trays/): Standard bins you put things to from top\n"
			+ "* [Drawers](drawers/): Well, drawers\n"
			+ "* [Drawer trays](drawer_trays/): Trays you put the drawers to, basically drawer slots\n"
			)

		addToIndex(
			F"{outputDir}",
			"1_{}_T".format(systemName),
			"* **[System {}]({}/)**\n".format(systemName, systemDirName)
			+ "\t* Unit size: {} x {} x {} mm\n".format(system["unitSize"][0], system["unitSize"][1], system["unitSize"][2])
			)

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
					componentSizeText = "(WxLxH) {} x {} x {} mm".format(componentSize[0], componentSize[1], componentSize[2])

					drawerEnabled = True # componentSize[2] >= 30

					unitCountText = F"(WxLxH) {unitCountX} x {unitCountY} x {unitCountZ}"
					unitCountStr = F"{unitCountX}{unitCountY}{unitCountZ}"
					unitCountDirStr = F"size_{unitCountX}x{unitCountY}x{unitCountZ}"

					innerWallPercentageHeights = [
						{
							"name": "F",
							"val": 1,
							"text": "Full height"
						},
						{
							"name": "H",
							"val": 0.5,
							"text": "Half height"
						}
					]

					# Drawer tray
					if drawerEnabled:
						cDir = F"{outputDir}/{systemDirName}/drawer_trays"
						fName = F"{systemName}_W{unitCountStr}"

						# Index title
						addToIndex(cDir, "0_T",
							"# {}_W*\n".format(systemName)
							+ "* System: {}\n".format(systemName)
							+ "* Path: `{}`\n".format(cDir)
							+ "# Components\n"
							)

						# Index entry
						addToIndex(cDir, "1_{}_T".format(fName),
							"## {}\n".format(fName)
							+ "* Unit count: {}\n".format(unitCountText)
							+ "* Component size: {}\n\n".format(componentSizeText)
							+ "![preview](png/{}.png)\n".format(fName)
							)

						executor.submit(funcs.compileScad,
						cDir,
						fName,
						copy.deepcopy(cfg), "drawer_tray")

					for pattern in patterns:
						patternBaseName = os.path.basename(os.path.splitext(pattern)[0])
						patternMatch = re.fullmatch("(.*?)(?:_x([A-Z]*))?", patternBaseName)
						patternName = patternMatch.group(1)
						patternFlags = str(patternMatch.group(2))

						rotations = [(0, "", "")]
						if "R" in patternFlags:
							rotations.append((90, "_R", "Rotated pattern"))

						for rot in rotations:
							rotAngle, rotStr, rotText = rot
							cfg["innerWallRotation"] = rotAngle

							for innerWallPercentageHeight in innerWallPercentageHeights:
								cfg["innerWallPercentageHeight"] = innerWallPercentageHeight["val"]
								cfg["innerWallPatternFile"] = pattern

								innerHeightName = innerWallPercentageHeight["name"]

								def componentAddToIndex(cDir, fName, cName):
									# Index title
									addToIndex(cDir, "0_T",
										"# {}_T{}*\n".format(systemName, unitCountStr)
										+ "* System: {}\n".format(systemName)
										+ "* Unit count: {}\n".format(unitCountText)
										+ "* Component size: {}\n".format(componentSizeText)
										+ "* Path: `{}`\n".format(cDir)
										+ "# Components\n"
										)

									# Common index entry
									addToIndex(cDir, "1#/{}#/0_T".format(cName),
										"## {}\n".format(cName)
										+ "* Unit count: {}\n".format(unitCountText)
										+ "* Size: {}\n\n".format(componentSizeText)
										)

									# Item index entry
									addToIndex(cDir, "1#/{}#/1_COLS/{}".format(cName, fName), [
										"**{}**".format(fName),
										innerWallPercentageHeight["text"],
										rotText,
										"![preview](png/{}.png)".format(fName)
										])

									# Spacing after
									addToIndex(cDir, "1#/{}#/2_T".format(cName), "\n---\n")

								# Tray - no need for swapped width/height as they are symmetrical
								if unitCountX >= unitCountY and (unitCountX != unitCountY or rot[0] == 0):
									cDir = F"{outputDir}/{systemDirName}/trays/{unitCountDirStr}"
									fName = F"{systemName}_T{unitCountStr}{innerHeightName}_{patternName}{rotStr}"
									cName = F"{systemName}_T{unitCountStr}*_{patternName}*"

									executor.submit(funcs.compileScad,
										cDir,
										fName,
										copy.deepcopy(cfg), "tray"
									)

									componentAddToIndex(cDir, fName, cName)

								# Drawer
								if drawerEnabled:
									cDir = F"{outputDir}/{systemDirName}/drawers/{unitCountDirStr}"
									fName = F"{systemName}_D{unitCountStr}{innerHeightName}_{patternName}{rotStr}"
									cName = F"{systemName}_D{unitCountStr}*_{patternName}*"

									executor.submit(funcs.compileScad,
										cDir,
										fName,
										copy.deepcopy(cfg), "drawer"
										)

									componentAddToIndex(cDir, fName, cName)

	executor.shutdown()

	if args.index:
		generateIndexes()