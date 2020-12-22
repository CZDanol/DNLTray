import collections

from cargs import args
import funcs

def createDict():
	return collections.defaultdict(createDict)

indexes = createDict()

def addToIndex(indexDir, path, value):
	if not args.index:
		return

	dct = indexes[indexDir]
	for p in path.split("/"):
		dct = dct[p]

	dct["value"] = value

def genScopeCols(data):
	keys = sorted(data.keys())

	result = "| "
	for key in keys:
		result += data[key]["value"][0] + " | "
	
	result += "\n| "
	for key in keys:
		result += "--- | "

	rowCount = max(len(data[key]["value"]) for key in keys)
	for row in range(1, rowCount):
		vals = []
		for key in keys:
			lst = data[key]["value"]
			vals.append(lst[row] if len(lst) > row else "")

		if all(val == "" for val in vals):
			continue

		result += "\n| "

		for val in vals:
			result += val
			result += " | "

	result += "\n\n"

	return result

def genIndexScope(data):
	result = ""

	for key in sorted(data.keys()):
		val = data[key]

		if key.endswith("#"):
			result += genIndexScope(val)

		elif key.endswith("_T"):
			result += val["value"]

		elif key.endswith("_COLS"):
			result += genScopeCols(val)

		else:
			raise Exception("Unknown key " + key)

	return result

def releasesListStr(s, prefix = "", suffix = ""):
	if not s.targetReleases:
		return ""

	return "{}STL: {}{}".format(prefix, ", ".join("[{}](https://github.com/CZDanol/DNLTray/releases/latest/download/DNLTray_{}_{}.zip)".format(rel, s.system.name, rel) for rel in s.targetReleases), suffix)

def componentAddToIndex(s, cDir, fName, cName):
	# Index title
	addToIndex(cDir, "0_T",
		"# {}_T{}{}{}\n".format(s.system.name, s.config["unitCount"][0], s.config["unitCount"][1], s.config["unitCount"][2])
		+ "* System: {}\n".format(s.system.name)
		+ "* Unit count: {} x {} x {} units\n".format(s.config["unitCount"][0], s.config["unitCount"][1], s.config["unitCount"][2])
		+ "* Component size: (WxHxL) {} x {} x {} mm\n".format(s.componentSize[0], s.componentSize[1], s.componentSize[2])
		+ "* Path: `{}`\n".format(cDir)
		+ "# Components\n"
		)

	# Common index entry
	addToIndex(cDir, "1#/{}#/0_T".format(cName),
		"## {}\n".format(cName)
		)

	# Item index entry
	addToIndex(cDir, "1#/{}#/1_COLS/{}".format(cName, fName), [
		"**{}**".format(fName),
		s.compartmentsHeight["text"],
		s.compartmentsTransform["text"],
		releasesListStr(s, "", ""),
		"![preview](png/{}.png)".format(fName)
		])

	# Spacing after
	addToIndex(cDir, "1#/{}#/2_T".format(cName), "\n---\n")

def generateIndexes():
	for indexDir in indexes:
		funcs.writeFile(indexDir + "/README.md", genIndexScope(indexes[indexDir]))