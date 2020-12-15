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
	
	result += "\n|"
	for key in keys:
		result += "--- | "

	rowCount = max(len(data[key]["value"]) for key in keys)
	for row in range(1, rowCount):
		result += "\n| "

		for key in keys:
			lst = data[key]["value"]
			result += lst[row] if len(lst) > row else ""
			result += " | "

	result += "\n"

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

def generateIndexes():
	for indexDir in indexes:
		funcs.writeFile(indexDir + "/README.md", genIndexScope(indexes[indexDir]))