# DNLTray - Danol's ultimaze organizer system
**WORK IN PROGRESS**

**Due to size limitations, the repository doesn't contain .stl files. A selection of them is available in releases. The rest you have to build yourself. Simply download this repository, open the appropriate scad file and compile it.**

**You can see gallery of all components in the models/ folder.**

# Features
System contains:
	- Trays/bins
	- Drawers

- **Previews everywhere**. Just look in the `models` directory structure, every component has an image preview. 
- 3D printable (duh)
- Zero supports required
- Highly modular
- Components are horizontally and vertically stackable
- Many size and height variants (inter-compatible)
- Many pattern variants
- You can adjust parameters/add your own patterns and recompile (python required)
	- Feel free to use pull requests

# Print recommendations
* PLA
* Standard 0.2mm layers
* No supports
* Maybe add a 5mm brim so that the models don't warp (it's a little pain to get it off though)

# License
- Free for non-commercial use
- If you intend to use the designs commercially, please contact me to negotiate a commission.
  
# Customizing
- Download the whole repo
- Adjust stuff in the `generator/config.py` or in `templates/*.scad`
- Run `python generate.py` with appropriate arguments (see `python generate.py --help`)
- Profit

### Creating custom patterns
- SVG file format
- Use rectangles with ZERO WIDTH (give them some outline for visualisation)
- Always put four rectangles around the pattern (determining position of outer walls)

# To-do
- Move most settings to system_default.scad
- Zipping (auto generate PNG + STL zips from selection)
- Cut down patterns (extra patterns)
- Cut down sizes - only allow certain combinations (not too high)
- Disable half height variants?
- Pattern gallery
- Pattern flag explanations
- Lids
  * With and without border
  * High lids
- Side frames (vertically stackable)
  - Corner side frames - not necessary (you can just use two separate frames)
  - Double-sisded frames
  - Single-sided frames
- Articulating side frames (so you can open up the organizer)