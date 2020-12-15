# Danol's Ultimate Organizer System
**WORK IN PROGRESS**
**Due to size limitations, the repository doesn't contain .stl files. A selection of them is available in releases. The rest you have to build yourself. Simply download this repository, open the appropriate scad file and compile it.**

**You can see gallery of all components in the models/ folder.**

## Features
System contains:
	- Trays/bins
	- Drawers

- Zero supports required
- Highly modular
- Components are horizontally and vertically stackable
- Many size and height variants (inter-compatible)
- Many pattern variants
- You can adjust parameters/add your own patterns and recompile (python required)
	- Feel free to use pull requests

## License
- Free for non-commercial use
- If you intend to use the designs commercially, please contact me to negotiate a commission

## Customizing
- Download the whole repo
- Adjust stuff in the `generator/config.py` or in `templates/*.scad`
- Run `python generate.py` with appropriate arguments (see `python generate.py --help`)
- Profit

### Creating custom patterns
- SVG file format
- Use rectangles with ZERO WIDTH (give them some outline for visualisation)
- Always put four rectangles around the pattern (determining position of outer walls)

## To-do
- Zipping
- Lids
- Side frames (vertically stackable)
  - Corner side frames - not necessary (you can just use two separate frames)
  - Double-sisded frames
  - Single-sided frames
- Articulating side frames (so you can open up the organizer)