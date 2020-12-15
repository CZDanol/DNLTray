import traceback
import threading
import os
import numbers
import subprocess
import sys
import re

from cargs import args

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
	if args.models and not any(re.fullmatch(m, fileName) for m in args.models):
		return

	try:
		scadDir = F"{baseDir}/scad"

		scadFileName = F"{scadDir}/{fileName}.scad"
		stlFileName = F"{baseDir}/stl/{fileName}.stl"
		previewScadFileName = F"{baseDir}/{fileName}.preview.scad"
		previewFileName = F"{baseDir}/png/{fileName}.png"

		template = os.path.relpath(F"templates/{template}.scad", scadDir)
		cfg["innerWallPatternFile"] = os.path.relpath("patterns/" + cfg["innerWallPatternFile"], scadDir)
		cfg["modelName"] = fileName
		cfgStr = configStr(cfg)

		alreadyExists = os.path.exists(scadFileName)
		if args.existingOnly and not alreadyExists:
			return

		if args.newOnly and alreadyExists:
			return

		# Create the scad file
		writeFile(scadFileName, F"{cfgStr}\ninclude <{template}>;")

		if args.scad:
			makeFileDir(stlFileName)

			# Create STL
			stlProc = subprocess.run([args.scad, scadFileName, F"--o={stlFileName}"], capture_output=True)
			mutex.acquire()
			print("Compiled " + fileName)

			if len(stlProc.stdout):
				print(stlProc.stdout)

			if len(stlProc.stderr):
				print(stlProc.stderr)

			mutex.release()

			# Create png preview of the stl
			makeFileDir(previewFileName)

			# We create a preview scad importing the stl, should be faster than having to compile the original scad
			writeFile(previewScadFileName, "import(\"{}\");".format(os.path.relpath(stlFileName, baseDir).replace("\\", "\\\\")))
			subprocess.run([args.scad, previewScadFileName, F"--o={previewFileName}.png", "--colorscheme=BeforeDawn"], capture_output=True)
			os.remove(previewScadFileName)

	except Exception:
		traceback.print_exc()