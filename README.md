# DNLTray - Danol's ultimate organizer system
![](etc/render_withLabels.png)

**WORK IN PROGRESS**

Due to size limitations, the repository doesn't contain .stl files. A selection of them is available in releases. The rest you have to build yourself. Simply download this repository, open the appropriate scad file and compile it. You can also use the attached python script and compile it using `python generate.py -m (model name) -c (scad binary filepath) --stl`

**You can see gallery of all components in the models/ folder.**

**We're using `.3mf` instead of `.stl` files because of their smaller size.**

# Features
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
    * `DT`: Drawer tray - slot for a drawer
    * `W`: Wall (frame you hang the trays onto)
    * `S`: Shelf (tray without a front side)
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

# How to compile
A lot of the models STL files can be downloaded in a release zip. Because compiling all the models takes a lot of time (and the zips would be way too big), I'm only putting a selection of the STLs to the releases.

You can however easily compile any model in the repository manually. Simply download this repository (source codes), locate your required `.scad` file in the `models/` folder, open in it OpenSCAD, compile it and export it.

# License
- Free for non-commercial use
- If you intend to use the designs commercially, please contact me to negotiate a commission.

## Contact
* Discord: Danol#2663
* Mail: czdanol@gmail.com
  
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
- Frames – you can put other organizers on (inner horizontal mounts don't fall through)
- STL fixed patterns
- Hex bit patterns
- Half-height variants for trays with height > 1?
- Maybe thicker walls for larger bins?
- Lids
  * With and without border
  * High lids
- Articulating side frames (so you can open up the organizer)