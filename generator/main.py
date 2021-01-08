import argparse
import concurrent.futures
import collections
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

workerCount = max(2, os.cpu_count() - 2) # Leave some free cores so the computer is actually usable

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

class StateGuard:
	stack = []
	state = None

	def __init__(self, state):
		cfg = copy.deepcopy(config.defaultConfig)
		self.stack.append(cfg)
		self.state = state
		state.config = cfg

	def __enter__(self):
		cfg = copy.deepcopy(self.stack[len(self.stack) - 1])
		self.stack.append(cfg)
		self.state.config = cfg

	def __exit__(self, t, v, tb):
		cfg = self.stack.pop()
		self.state.config = cfg

def main():
	outputDir = "models"

	executor = concurrent.futures.ThreadPoolExecutor(max_workers=workerCount)

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
	sg = StateGuard(s)

	# Generate all the stuff
	for system in systems.systems:
		with sg:
			s.system = system

			systemName = system.name
			systemDirName = "{}__system_{}".format(systemName, systemName)

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
				+ "* [Trays](T__trays/): Standard bins you put things to from top\n"
				+ "* [Drawers](D__drawers/): Well, drawers\n"
				+ "* [Drawer trays](DT__drawer_trays/): Slots you put the drawers to, basically drawer slots\n"
				+ "* [Walls](W__walls/): Support you can hang the trays onto.\n"
				)

			index.addToIndex(
				F"{outputDir}",
				"1_{}_T".format(systemName),
				"## [System {}]({}/)\n".format(systemName, systemDirName)
				+ "* Unit size: {} x {} x {} mm\n".format(s.config["unitSize"][0], s.config["unitSize"][1], s.config["unitSize"][2])
				)

			systemConfig = s.config
			for ucX, ucY, ucZ in itertools.product(range(9), range(9), range(17)):
				with sg:
					s.config["unitCount"] = [ucX, ucY, ucZ]
					s.componentSize = [s.config["unitSize"][0] * ucX, s.config["unitSize"][1] * ucY, s.config["unitSize"][2] * ucZ]
					componentSizeText = "(WxLxH) {} x {} x {} mm".format(s.componentSize[0], s.componentSize[1], s.componentSize[2])

					unitCountText = F"(WxLxH) {ucX} x {ucY} x {ucZ}"
					unitCountStr = F"{ucX}{ucY}{ucZ}"
					unitCountDirStr = "{}{}{}__{}x{}x{}_units__{}x{}x{}_mm".format(ucX, ucY, ucZ, ucX, ucY, ucZ, s.componentSize[0], s.componentSize[1], s.componentSize[2])

					if ucY == 0:
						with sg:
							if system.shouldGenerateComponent(s, "wall"):
								cDir = F"{outputDir}/{systemDirName}/W__walls"
								cName = F"{systemName}_W{unitCountStr}"
								fName = F"{systemName}_W{unitCountStr}"

								# Index title
								index.addToIndex(cDir, "0_T",
									"# {}_W*\n".format(systemName)
									+ "* System: {}\n".format(systemName)
									+ "* Path: `{}`\n".format(cDir)
									+ "# Components\n"
									)

								# Index common
								index.addToIndex(cDir, "1#/{}#/0_T".format(cName),
									"## {}\n".format(cName)
									+ "* Unit count: {}\n".format(unitCountText)
									+ "* Component size: {}\n\n".format(componentSizeText)
									)

								# Index item
								index.addToIndex(cDir, "1#/{}#/1_COLS/{}".format(cName, fName), [
									"**{}**".format(fName),
									index.releasesListStr(s, "", ""),
									"![preview](png/{}.png)".format(fName)
									])

								# Spacing after
								index.addToIndex(cDir, "1#/{}#/2_T".format(cName), "\n---\n")

								executor.submit(funcs.compileScad,
									"wall",
									cDir, fName, copy.deepcopy(s.targetReleases),
									copy.deepcopy(s.config), systemConfig
								)

					# Drawer tray
					for s.drawerTrayVersion in config.drawerTrayVersions:
						with sg:
							for key, value in s.drawerTrayVersion["config"].items():
								s.config[key] = value

							drawerTrayVersionID = s.drawerTrayVersion["id"]

							if system.shouldGenerateComponent(s, "drawerTray"):
								cDir = F"{outputDir}/{systemDirName}/DT__drawer_trays"
								cName = F"{systemName}_DT{unitCountStr}"
								fName = F"{systemName}_DT{unitCountStr}{drawerTrayVersionID}"

								# Index title
								index.addToIndex(cDir, "0_T",
									"# {}_DT*\n".format(systemName)
									+ "* System: {}\n".format(systemName)
									+ "* Path: `{}`\n".format(cDir)
									+ "# Components\n"
									)

								# Index common
								index.addToIndex(cDir, "1#/{}#/0_T".format(cName),
									"## {}\n".format(cName)
									+ "* Unit count: {}\n".format(unitCountText)
									+ "* Component size: {}\n\n".format(componentSizeText)
									)

								# Index item
								index.addToIndex(cDir, "1#/{}#/1_COLS/{}".format(cName, fName), [
									"**{}**".format(fName),
									s.drawerTrayVersion["text"],
									index.releasesListStr(s, "", ""),
									"![preview](png/{}.png)".format(fName)
									])

								# Spacing after
								index.addToIndex(cDir, "1#/{}#/2_T".format(cName), "\n---\n")

								executor.submit(funcs.compileScad,
									"drawer_tray",
									cDir, fName, copy.deepcopy(s.targetReleases),
									copy.deepcopy(s.config), systemConfig
								)

					# Shelvves
					for s.shelfVersion in config.shelfVersions:
						with sg:
							for key, value in s.shelfVersion["config"].items():
								s.config[key] = value

							shelfVersionID = s.shelfVersion["id"]

							if system.shouldGenerateComponent(s, "shelf"):
								cDir = F"{outputDir}/{systemDirName}/S__shelves"
								cName = F"{systemName}_S{unitCountStr}"
								fName = F"{systemName}_S{unitCountStr}{shelfVersionID}"

								# Index title
								index.addToIndex(cDir, "0_T",
									"# {}_S*\n".format(systemName)
									+ "* System: {}\n".format(systemName)
									+ "* Path: `{}`\n".format(cDir)
									+ "# Components\n"
									)

								# Index common
								index.addToIndex(cDir, "1#/{}#/0_T".format(cName),
									"## {}\n".format(cName)
									+ "* Unit count: {}\n".format(unitCountText)
									+ "* Component size: {}\n\n".format(componentSizeText)
									)

								# Index item
								index.addToIndex(cDir, "1#/{}#/1_COLS/{}".format(cName, fName), [
									"**{}**".format(fName),
									s.shelfVersion["text"],
									index.releasesListStr(s, "", ""),
									"![preview](png/{}.png)".format(fName)
									])

								# Spacing after
								index.addToIndex(cDir, "1#/{}#/2_T".format(cName), "\n---\n")

								executor.submit(funcs.compileScad,
									"shelf",
									cDir, fName, copy.deepcopy(s.targetReleases),
									copy.deepcopy(s.config), systemConfig
								)

					for pattern in config.patterns:
						with sg:
							patternBaseName = os.path.basename(os.path.splitext(pattern)[0])
							patternMatch = re.fullmatch("(.*?)(?:_x([A-Z]*))?", patternBaseName)
							patternName = patternMatch.group(1)
							patternFlags = str(patternMatch.group(2))

							s.config["innerWallPatternFile"] = pattern

							for s.compartmentsTransform in config.compartmentsTransforms:
								with sg:
									for key, value in s.compartmentsTransform["config"].items():
										s.config[key] = value

									# Rotate only patterns that require it
									if "R" not in patternFlags and s.config["innerWallRotation"] != 0:
										continue

									# Generate extra patterns only when explicitly requested
									if "X" in patternFlags and not args.extraPatterns:
										continue

									compartmentsTransformId = s.compartmentsTransform["id"]

									for s.compartmentsHeight in config.compartmentsHeights:
										with sg:
											for key, value in s.compartmentsHeight["config"].items():
												s.config[key] = value

											# Do not generate non-full inner wall variants unless explicitly requested
											if s.config["innerWallPercentageHeight"] != 1 and not args.compartmentHeightVariants:
												continue

											compartmentsHeightId = s.compartmentsHeight["id"]

											# Tray - no need for swapped width/height as they are symmetrical
											if ucX >= ucY and (ucX != ucY or s.config["innerWallRotation"] == 0) and system.shouldGenerateComponent(s, "tray"):
												cDir = F"{outputDir}/{systemDirName}/T__trays/{unitCountDirStr}"
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
												cDir = F"{outputDir}/{systemDirName}/D__drawers/{unitCountDirStr}"
												fName = F"{systemName}_D{unitCountStr}{compartmentsHeightId}_{patternName}{compartmentsTransformId}"
												cName = F"{systemName}_D{unitCountStr}_{patternName}"

												executor.submit(funcs.compileScad,
													"drawer",
													cDir, fName, copy.deepcopy(s.targetReleases),
													copy.deepcopy(s.config), systemConfig
													)

												index.componentAddToIndex(s, cDir, fName, cName)

	executor.shutdown()
	executor = concurrent.futures.ThreadPoolExecutor(max_workers=workerCount)

	print("Done. Generated {} models.".format(funcs.modelsGenerated))

	if args.zip:
		rmDirs("releases")
		funcs.makeFileDir("releases/file")

		print("Zipping...")

		def mzip(zipFileName):
			z = zipfile.ZipFile(zipFileName, "w", compression=zipfile.ZIP_LZMA, compresslevel=9)

			for stlFileName in funcs.zips[zipFileName]:
				print(F"Packing '{stlFileName}' -> '{zipFileName}'")
				z.write(stlFileName)

		executor.map(mzip, funcs.zips.keys())

		executor.shutdown()
		print("Done zipping.")

	if args.index:
		index.generateIndexes()