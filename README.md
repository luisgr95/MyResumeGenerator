
# CV Generator 

This Python script generates a CV tailored for a **Sysadmin** position. It uses the `python-docx` library to create a well-formatted Word document with custom sections, including personal details, work experience, skills, and certifications. Additionally, it converts SVG icons to PNG using **Inkscape** to enrich the CV with visual elements.

## Features

- Automatically generates a CV with sections for:
  - Personal Information
  - Work Experience
  - Education
  - Skills
  - Certifications
- Includes icons for contact details and sections (converted from SVG to PNG using Inkscape).
- Customizable formatting with specific fonts, margins, and spacing.

## Requirements

- **Python 3.6+**
- **Inkscape** (for SVG to PNG conversion)
- Python libraries:
  - `python-docx`
  - `subprocess`

### Install Python Libraries

You can install the required libraries using `pip`:

```bash
pip install python-docx
```

Make sure **Inkscape** is installed and accessible via your system's `PATH` to convert SVG files to PNG.

## Usage

1. Place your **SVG icons** for contact information and sections in the same directory as the script.
2. Make sure you have a profile picture (e.g., `image.png`) to include in your CV.
3. Run the script:

```bash
python generate_cv.py
```

4. The generated CV will be saved as `SRE_CV_LuisGallardo.docx`.

### Example Contact Information Section

The script automatically adds icons and personal details to the contact section, as shown below:

- Phone
- Location
- Email
- LinkedIn
- GitHub

### Customization

You can customize the following:
- Update work experience and skills directly in the script.
- Replace or add icons to match your personal style.
- Modify formatting, such as font sizes, margins, or alignment, as needed.

## Troubleshooting

- **Inkscape not found**: Ensure that Inkscape is installed and added to your system's `PATH` so it can be called via the `subprocess` module.
- **Missing icons**: Make sure that all icons are in the same directory as the script and named correctly as `*.svg` files.

## License

This project is open-source and available under the MIT License.
