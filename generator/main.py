import argparse
import concurrent.futures
import shutil
import copy

from config import *
from funcs import *
from cargs import *

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

		for unitCountX in system["horizontalUnitCountOptions"]:
			cfg["unitCount"][0] = unitCountX

			for unitCountY in system["horizontalUnitCountOptions"]:
				cfg["unitCount"][1] = unitCountY

				for unitCountZ in system["verticalUnitCountOptions"]:
					cfg["unitCount"][2] = unitCountZ

					componentSize = [
						cfg["unitSize"][0] * unitCountX,
						cfg["unitSize"][1] * unitCountY,
						cfg["unitSize"][2] * unitCountZ
					]
					drawerEnabled = componentSize[2] >= 30

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
								F"{systemName}_T{unitCountStr}{iwphn}_{patternName}",
								copy.deepcopy(cfg), "tray")

							# Drawer
							if drawerEnabled:
								executor.submit(compileScad,
								F"{outputDir}/{systemDirName}/drawers/{unitCountDirStr}",
								F"{systemName}_D{unitCountStr}{iwphn}_{patternName}",
								copy.deepcopy(cfg), "drawer")

	executor.shutdown()