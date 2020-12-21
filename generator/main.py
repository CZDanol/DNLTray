import argparse
import concurrent.futures
import shutil
import copy
import re
import os
import itertools
import time
import zipfile

import config
import state
import systems
import system_a
import funcs
import index

from cargs import args

def rmDirs(path):
	if not os.path.exists(path):
		return

	print("Deleting {}...".format(path))
	while True:
		try:
			shutil.rmtree(path)
			time.sleep(1)
			break

		except OSError:
			continue

	print("{} deleted".format(path))

def main():
	outputDir = "models"

	executor = concurrent.futures.ThreadPoolExecutor()

	# Delete the "data" outputs directory
	if args.clear:
		rmDirs("models")

	index.addToIndex(
			F"{outputDir}",
			"0_T",
			"# Models\n"
			+ "This directory contains model scad files and image previews.\n"
			+ "# Systems\n"
			)

	s = state.GeneratorState()

	# Generate all the stuff
	for system in systems.systems:
		s.system = system
		s.config = copy.deepcopy(config.defaultConfig)

		systemName = system.name
		systemDirName = "SYS_" + systemName

		s.config["systemConfigFilePath"] = F"{outputDir}/{systemDirName}/system_config.scad"

		for key, value in system.config.items():
			s.config[key] = value

		s.config["systemName"] = system.name

		if args.scad or args.zip:
			funcs.writeFile(s.config["systemConfigFilePath"], funcs.configStr(s.config))

		index.addToIndex(
			F"{outputDir}/{systemDirName}",
			"0_T",
			"# System {}\n".format(systemName)
			+ "Unit size: {} x {} x {} mm\n".format(s.config["unitSize"][0], s.config["unitSize"][1], s.config["unitSize"][2])
			+ "## Directories\n"
			+ "* [Trays](trays/): Standard bins you put things to from top\n"
			+ "* [Drawers](drawers/): Well, drawers\n"
			+ "* [Drawer trays](drawer_trays/): Trays you put the drawers to, basically drawer slots\n"
			)

		index.addToIndex(
			F"{outputDir}",
			"1_{}_T".format(systemName),
			"## [System {}]({}/)\n".format(systemName, systemDirName)
			+ "* Unit size: {} x {} x {} mm\n".format(s.config["unitSize"][0], s.config["unitSize"][1], s.config["unitSize"][2])
			)

		systemConfig = s.config
		for ucX, ucY, ucZ in itertools.product(range(8), range(8), range(8)):
			s.config = copy.deepcopy(systemConfig)

			s.config["unitCount"] = [ucX, ucY, ucZ]

			s.componentSize = [s.config["unitSize"][0] * ucX, s.config["unitSize"][1] * ucY, s.config["unitSize"][2] * ucZ]
			componentSizeText = "(WxLxH) {} x {} x {} mm".format(s.componentSize[0], s.componentSize[1], s.componentSize[2])

			unitCountText = F"(WxLxH) {ucX} x {ucY} x {ucZ}"
			unitCountStr = F"{ucX}{ucY}{ucZ}"
			unitCountDirStr = "{}x{}x{}_units__{}x{}x{}_mm".format(ucX, ucY, ucZ, s.componentSize[0], s.componentSize[1], s.componentSize[2])

			# Drawer tray
			if system.shouldGenerateComponent(s, "drawerTray"):
				cDir = F"{outputDir}/{systemDirName}/drawer_trays"
				fName = F"{systemName}_W{unitCountStr}"

				# Index title
				index.addToIndex(cDir, "0_T",
					"# {}_W*\n".format(systemName)
					+ "* System: {}\n".format(systemName)
					+ "* Path: `{}`\n".format(cDir)
					+ "# Components\n"
					)

				# Index entry
				index.addToIndex(cDir, "1_{}_T".format(fName),
					"## {}\n".format(fName)
					+ "* Unit count: {}\n".format(unitCountText)
					+ "* Component size: {}\n\n".format(componentSizeText)
					+ index.releasesListStr(s, "* ", "\n")
					+ "![preview](png/{}.png)\n".format(fName)
					)

				executor.submit(funcs.compileScad,
					"drawer_tray",
					cDir, fName, copy.deepcopy(s.targetReleases),
					copy.deepcopy(s.config), systemConfig
				)

			for pattern in config.patterns:
				patternBaseName = os.path.basename(os.path.splitext(pattern)[0])
				patternMatch = re.fullmatch("(.*?)(?:_x([A-Z]*))?", patternBaseName)
				patternName = patternMatch.group(1)
				patternFlags = str(patternMatch.group(2))

				s.config["innerWallPatternFile"] = pattern

				prevCfg = s.config
				for s.compartmentsTransform in config.compartmentsTransforms:
					s.config = copy.deepcopy(prevCfg)

					for key, value in s.compartmentsTransform["config"].items():
						s.config[key] = value

					# Rotate only patterns that require it
					if "R" not in patternFlags and s.config["innerWallRotation"] != 0:
						continue

					# Generate extra patterns only when explicitly requested
					if "X" in patternFlags and not args.extraPatterns:
						continue

					compartmentsTransformId = s.compartmentsTransform["id"]

					prevCfg2 = s.config
					for s.compartmentsHeight in config.compartmentsHeights:
						s.config = copy.deepcopy(prevCfg2)

						for key, value in s.compartmentsHeight["config"].items():
							s.config[key] = value

						# Do not generate non-full inner wall variants unless explicitly requested
						if s.config["innerWallPercentageHeight"] != 1 and not args.compartmentHeightVariants:
							continue

						compartmentsHeightId = s.compartmentsHeight["id"]

						# Tray - no need for swapped width/height as they are symmetrical
						if ucX >= ucY and (ucX != ucY or s.config["innerWallRotation"] == 0) and system.shouldGenerateComponent(s, "tray"):
							cDir = F"{outputDir}/{systemDirName}/trays/{unitCountDirStr}"
							fName = F"{systemName}_T{unitCountStr}{compartmentsHeightId}_{patternName}{compartmentsTransformId}"
							cName = F"{systemName}_T{unitCountStr}_{patternName}"

							executor.submit(funcs.compileScad,
								"tray",
								cDir, fName, copy.deepcopy(s.targetReleases),
								copy.deepcopy(s.config), systemConfig
							)

							index.componentAddToIndex(s, cDir, fName, cName)

						# Drawer
						if system.shouldGenerateComponent(s, "drawer"):
							cDir = F"{outputDir}/{systemDirName}/drawers/{unitCountDirStr}"
							fName = F"{systemName}_D{unitCountStr}{compartmentsHeightId}_{patternName}{compartmentsTransformId}"
							cName = F"{systemName}_D{unitCountStr}_{patternName}"

							executor.submit(funcs.compileScad,
								"drawer",
								cDir, fName, copy.deepcopy(s.targetReleases),
								copy.deepcopy(s.config), systemConfig
								)

							index.componentAddToIndex(s, cDir, fName, cName)

	executor.shutdown()
	executor = concurrent.futures.ThreadPoolExecutor()

	print("Done. Generated {} models.".format(funcs.modelsGenerated))

	if args.zip:
		rmDirs("releases")
		funcs.makeFileDir("releases/file")

		print("Zipping...")

		def mzip(zipFileName):
			z = zipfile.ZipFile(zipFileName, "w")

			for stlFileName in funcs.zips[zipFileName]:
				print(F"Packing '{stlFileName}' -> '{zipFileName}'")
				z.write(stlFileName)

		executor.map(mzip, funcs.zips.keys())

		executor.shutdown()
		print("Done zipping.")

	if args.index:
		index.generateIndexes()