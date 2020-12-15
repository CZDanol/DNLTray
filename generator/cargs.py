import argparse

def parseArgs():
	p = argparse.ArgumentParser("Generate models & previews")
	p.add_argument("--scad", "-s", type=str, default=None, help="Location of the OpenSCAD executable. If specified, script generates STL files and preview. If not, it only generates SCAD files.")
	p.add_argument("--models", "-m", action="append", type=str, help="Generate only specific models (you can specify multiple). Use file name without extension (for example -m A_T221F_1x1). Accepts regexes. (for example -m A_.221F_1x1).")
	p.add_argument("--clear", "-c", action="store_true", help="Clear the models folder")

	g = p.add_mutually_exclusive_group()
	g.add_argument("--newOnly", "-n", action="store_true", help="Generate only new (not yet generated) models")
	g.add_argument("--existingOnly", "-e", action="store_true", help="Generate only existing (already generated) models")

	return p.parse_args()

args = parseArgs()