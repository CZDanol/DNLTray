import argparse

def parseArgs():
	p = argparse.ArgumentParser("generate")

	p.add_argument("--models", "-m", action="append", type=str, help="Model names to be generated. Select all models using '-m .*'. Use file name without extension (for example -m A_T221F_1x1). Accepts regexes. (for example -m A_.221F_1x1).")

	p.add_argument("--compiler", "-c", type=str, default=None, help="Location of the OpenSCAD executable.")

	p.add_argument("--clear", action="store_true", help="Clear the models folder")
	p.add_argument("--overwrite", "-o", action="store_true", help="If a file (model/image/..) exists, overwrite it (skipped by default)")

	p.add_argument("--index", action="store_true", help="Generate index (readme files) (considers all existing models, not only those generated with the current run)")
	p.add_argument("--scad", action="store_true", help="Generate SCAD files.")
	p.add_argument("--img", action="store_true", help="Generate model previews. Automatically generates SCAD files.")
	p.add_argument("--stl", action="store_true", help="Generate STL models. Automatically generates SCAD files.")
	p.add_argument("--zip", action="store_true", help="Generate STL models and pack them in releases (as specified in system configs)")

	p.add_argument("--extraPatterns", action="store_true", help="Generate extra patterns (those that have the X flag).")
	p.add_argument("--compartmentHeightVariants", action="store_true", help="Generate extra variants with half inner wall heights.")
	p.add_argument("--allCombinations", action="store_true", help="Generate all combinations (ignore what combinations the system suggests) -- still can be combined with --extraPatterns and other.")

	result = p.parse_args()

	if result.img or result.stl:
		result.scad = True

	if result.scad and not result.compiler:
		raise Exception("No compiler specified")

	return result

args = parseArgs()