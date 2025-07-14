# **3D Digital Rain Style Screensaver - Egyptian Glyphs**

The screensaver is done in the style of other 'Matrix' style digital rain screen savers. It creates 3D illusion by creating a cube, with (determined by formula from screen size) are rows & columns with an arbitraty set of layers(6). This enhances the generation ability and puts 3D effects changes of several kinds within reach of the code.

 - Rows = left to right of the screen
 - Columns = top to bottom 
 - Layers = front to back.  

## Features
💠 Sparse activation per layer: Only ~30% of columns are active at startup, randomized by layer.
🌌 Spacing & offset: Columns have widened gaps and staggered alignment to avoid overlap.
🌀 Staggered reactivation: Faded columns reawaken gradually based on probability, removing pause effect.
🔠 Clear depth effect: Font sizes now range more dramatically from foreground to background (36pt → 12pt).
🔱 Watermark: Optional floating Ankh or custom symbol.
🌿 Theme toggle: Green glow or Lapis Lazuli blue
⚡ Parameterization: Customized changes you would like to make can be set at command line
✨ Glyph Generation: (customizable) Egyptian Hieroglyphs used for this particular implementation

## **Matrix-Style Egyptian Hieroglyph Screensaver in Python**
This script uses Pygame to create a “digital rain” effect with Unicode Egyptian Hieroglyphs.
By default the falling glyphs glow green; switch to Lapis Lazuli blue with a command-line flag.
You can also float a watermark (e.g., an Ankh image) behind the streams, adjust fall speed, spawn rate, font size, etc.

## **Requirements**
- Python 3.7+
- Pygame (`pip install pygame`)

(Optional)
- A font supporting your character set to use 
    e.g. Ancient Egyptian (Kemet) Unicode Glyph range U+13000–U+1342F, for example 'NotoSansEgyptianHieroglyphs-Regular.ttf'
- A PNG watermark (e.g., an Ankh) with alpha channel
- Can be run as-is by downloading the default compilation for Windows 'KemetCode.exe'

## **Usage**
The defaults are below; each of these can be changed.
These switches work with the KemetCode.exe or the main.py script

💡 **Available Command-Line Switches**
| Switch        | Type  | Default | Description                                           |
| ------------- | ----- | ------- | ----------------------------------------------------- | 
| --color       | text  | green   | Theme glow color (green or blue)                      | 
| --font        | path  | font.ttf| Path to compatible font                               | 
| --min_font    | int   | 12      | Smallest font size (back grid layers)                 | 
| --max_font    | int   | 36      | Largest font size (front grid layers)                 | 
| --rows        | int   | 6       | Number of 3D grid layers (depth rows)                 | 
| --rain_speed  | float | 1.0     | Speed multiplier (0.5 = slower, 2.0 = faster)         | 
| --watermark   | path  | None    | Optional PNG image with transparency (e.g., ankh.png) | 
| --fps         | int   | 30      | Frames per second (controls render smoothness)        | 
| --help        | flag  | message | Prints this help menu to terminal                     |
| --debug       | flag  | None    | Enable grid debug overlays                            | 

Parameterization (command switch) Example: 
`python main.py --color blue --rows 8 --font NotoSansEgyptianHieroglyphs-Regular.ttf --watermark ankh.png`

Press any key or any mouse click to exit fullscreen

### **Glyphs (Unicode Characters)**
Ancient Egyptian Hieroglyphs are hard coded, but can be changed and then the font is passed into the screen saver by a command line switch. Together with a valid font; this allows any set of Unicode Character ranges to be used.  A font with the Uinicode character set you would like to use embedded in a font, and include that font in the installation. Google has a full set of all languages published.