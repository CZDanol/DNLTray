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

def compileScad(baseDir, fileName, cfg, template):
	if not any(re.fullmatch(m, fileName) for m in args.models):
		return

	try:
		scadDir = F"{baseDir}/scad"

		scadFileName = F"{scadDir}/{fileName}.scad"
		stlFileName = F"{baseDir}/stl/{fileName}.stl"
		previewFileName = F"{baseDir}/png/{fileName}.png"

		template = os.path.relpath(F"templates/{template}.scad", scadDir)
		cfg["innerWallPatternFile"] = os.path.relpath("patterns/" + cfg["innerWallPatternFile"], scadDir)
		cfg["modelName"] = fileName
		cfgStr = configStr(cfg)

		# Create the scad file
		if args.scad and shouldGenerateFile(scadFileName):
			writeFile(scadFileName, F"{cfgStr}\ninclude <{template}>;")

		# Create STL
		if args.stl and shouldGenerateFile(stlFileName):
			runProcess([args.compiler, scadFileName, F"--o={stlFileName}"])

		# Create png preview
		if args.img and shouldGenerateFile(previewFileName):
			runProcess([args.compiler, scadFileName, F"--o={previewFileName}", "--colorscheme=BeforeDawn", "--imgsize=256,256", "--quiet"])

	except Exception:
		traceback.print_exc()