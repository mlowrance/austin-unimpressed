# Development Workflow

## Environment
- **Modern Host:** macOS (M4 Mac Mini)
- **Compiler:** Open Watcom v2 (wcl / wlink)
- **Editor:** VS Code
- **Testing:** DOSBox-X (local) / Period-accurate DOS PC (hardware)

## Asset Pipeline
- Sprites are designed as indexed color bitmaps.
- Assets are converted to C headers (`assets/`) using a conversion script to be baked into the `.EXE`.

## Build Instructions
Run the following command to compile the project:
`wcl -bt=dos -0 -ms -i=include src/*.c`