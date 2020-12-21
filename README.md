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

# File naming convention
`(system)_(type)(w)(l)(h)(flags)_(pattern)(patternFlags)`

* `system`
  * Component system. Different systems can vary in base unit size and other parameters and don't have to be cross-compatible.
* `component`
  * Component type:
    * `T`: Tray; a component with open top, basically a bin
    * `D`: Drawer
    * `W`: Drawer tray - slot for a drawer
* `w, l, h`
  * Width, length, height - size of the component (in base unit counts)
* `flags`
  * Various flags, depending on the component type:
    * `F`: Internal compartments are up to the full height
    * `H`: Internal compartments are up to half the height of the component
    * `L`: Lightweight
      * For drawer trays, the floor is removed because it's not necessary
* `pattern`
  * Pattern of the inner compartments
* `patternFlags`
  * Flags further modifying the pattern:
    * `R`: The pattern is rotated by 90°. This can be useful in drawers or if the component is not square sized.

For example:
* `A_T221F_1x1R`

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
- Half-height variants for trays with height > 1?
- Maybe thicker walls for larger bins?
- Releases
- Lids
  * With and without border
  * High lids
- Side frames (vertically stackable)
  - Corner side frames - not necessary (you can just use two separate frames)
  - Double-sisded frames
  - Single-sided frames
- Articulating side frames (so you can open up the organizer)