# Convert fonts to woff2

- Compresses fonts by only including the latin characters

## Usage

Install dependency:
```
pip install fonttools
```

Edit python file to point to your font files in the same directory:

```python
convert_font_to_woff2('font1.otf')
convert_font_to_woff2('font2.otf')
```

Run script
```
python convert_fonts.py
```

