import traceback
import threading
import os
import numbers
import subprocess
import sys
import re
import zipfile

from cargs import args
import index

mutex = threading.Lock()
modelsGenerated = 0

zipsmutex = threading.Lock()
zips = {}

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

def configStr(config, diffConfig = {}):
	result = "// AUTO GENERATED CONFIG\n"

	for key in config:
		if config[key] != diffConfig.get(key, None):
			result += F"{key} = {configVal(key, config[key])};\n"

	return result

def writeFile(file, content):
	makeFileDir(file)

	f = open(file, "w")
	f.write(content)
	f.close()

def runProcess(args):
	proc = subprocess.run(args, capture_output=True)
	mutex.acquire()

	if len(proc.stdout):
		print("STDOUT " + str(args))
		print(proc.stdout)

	if len(proc.stderr) and proc.stderr != b"OpenGL Program Validation results:\r\nValidation successful.\r\n":
		print("STDERR " + str(args))
		print(proc.stderr)

	mutex.release()

def shouldGenerateFile(file):
	result = not os.path.exists(file) or args.overwrite
	if result:
		makeFileDir(file)

		mutex.acquire()
		print(F"Generating '{file}'")
		mutex.release()

	return result

def compileScad(template : str, baseDir : str, fileName : str, releases, cfg : dict, diffCfg : dict = {}):
	if not any(re.fullmatch(m, fileName) for m in args.models):
		return

	try:
		scadDir = F"{baseDir}/scad"

		scadFileName = F"{scadDir}/{fileName}.scad"
		stlFileName = F"{baseDir}/stl/{fileName}.stl"
		previewFileName = F"{baseDir}/png/{fileName}.png"

		template = os.path.relpath(F"templates/{template}.scad", scadDir)
		systemConfigPath = os.path.relpath(cfg["systemConfigFilePath"], scadDir)

		cfg["innerWallPatternFile"] = os.path.relpath("patterns/" + cfg["innerWallPatternFile"], scadDir)
		cfg["modelName"] = fileName
		cfgStr = configStr(cfg, diffCfg)

		release = releases and args.zip

		# Create the scad file
		if (args.scad or release) and shouldGenerateFile(scadFileName):
			writeFile(scadFileName, F"include <{systemConfigPath}>;\n\n{cfgStr}\ninclude <{template}>;")

		# Create STL
		if (args.stl or release) and shouldGenerateFile(stlFileName):
			runProcess([args.compiler, scadFileName, F"--o={stlFileName}"])

		# Create png preview
		if args.img and shouldGenerateFile(previewFileName):
			runProcess([args.compiler, scadFileName, F"--o={previewFileName}", "--colorscheme=BeforeDawn", "--imgsize=128,128", "--quiet", "--projection=o"])

		if args.zip:
			for release in releases:
				zipFileName = "releases/{}_{}.zip".format(cfg["systemName"], release)

				zipsmutex.acquire()
				zd = zips.get(zipFileName)
				if not zd:
					zd = [zipfile.ZipFile(zipFileName, "w"), threading.Lock()]
					zips[zipFileName] = zd

				zipsmutex.release()

				mutex.acquire()
				print(F"Packing '{stlFileName}' -> '{zipFileName}'")
				mutex.release()

				zd[1].acquire()
				zd[0].write(stlFileName)
				zd[1].release()

		mutex.acquire()
		global modelsGenerated
		modelsGenerated += 1
		mutex.release()

	except Exception:
		traceback.print_exc()