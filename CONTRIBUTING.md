## Contributing to Sirenus

#### Overview
Anyone is welcome to submit patches to the project

#### Web UI
The Web UI for Sirenus uses TailwindCSS to handle styling

##### Requirements
- **TailwindCSS** at `3.4.10`

#### Notes
Tailwind is set up to scan all HTML files in `templates/` for classes, as well as all SVG's in `templates/svg`. Any Tailwind classes applied to files of those formats in those places will automatically be recognized and applied.
