# CSS Files for the ISO 3166-1 and ISO 3166-2 flags

* [iso3166-1.css](https://github.com/amckenna41/iso3166-flags/blob/main/css/iso3166-1.css) - CSS containing selectors for all ISO 3166-1 flags on the repo.
* [iso3166-2.css](https://github.com/amckenna41/iso3166-flags/blob/main/css/iso3166-2.css) - CSS containing selectors for all ISO 3166-2 flags on the repo.

Usage
-----
The flags can be implemented in-line by referencing the CSS class of the respective flag using the ISO 3166-1 or ISO 3166-2 CSS file. For ISO 3166-1 icons add the classes `.fi` and `.fi-xx` (where `xx` is the ISO 3166-1-alpha-2 code of a country) to an empty `<span>`. To add a squared version flag then additionally add the class `fis`.  

For example, adding the normal and squared flags for Andorra, Denmark & Panama:
```html
<span class="fi fi-ad"></span> <span class="fi fi-ad fis"></span>
<span class="fi fi-dk"></span> <span class="fi fi-dk fis"></span>
<span class="fi fi-pa"></span> <span class="fi fi-pa fis"></span>
```

For the ISO 3166-2 icons add the classes `.fi` and `.fi-xx-yy` (where `xx` is the ISO 3166-1-alpha-2 code [[2]](#references) of a country and `yy` is the ISO 3166-2 code, both in lower-case) to an empty `<span>`. 

For example, adding the Hungarian county of Heves (HU-HE), the South Sudanese state of Eastern Equatoria (SS-EE) & the Taiwanese county of Miaoli (TW-MIA):
```html
<span class="fi fi-hu-he"></span> <span class="fi fi-hu-he fis"></span>
<span class="fi fi-ss-ee"></span> <span class="fi fi-ss-ee fis"></span>
<span class="fi fi-tw-mia"></span> <span class="fi fi-tw-mia fis"></span>
```

SVG Sprites
-----------
As an alternative to the CSS `background-image` classes above, `scripts/generate_css.py` can generate SVG sprite files, embedding each flag as a `<symbol>` referenced with `<use>` - useful for inlining flags directly as scalable, styleable SVG elements rather than background images.

For ISO 3166-1, generate a single sprite file for all country flags with symbol ids in the form `fi-xx`:
```bash
python3 scripts/generate_css.py --sprite --export_sprite_filepath="css/iso3166-1-sprite.svg"
```

For ISO 3166-2, given the dataset spans ~2,800 flags, a single combined sprite can get impractically large for web delivery. By default a single global sprite is still generated (symbol ids in the form `fi-xx-yy`), but pass `--iso3166_2_sprite_per_country` to instead generate one smaller sprite file per country (`css/iso3166-2-sprites/{xx}.svg`) so a UI only has to load the subdivisions it needs:
```bash
# Single global sprite
python3 scripts/generate_css.py --iso3166_2_sprite --export_iso3166_2_sprite_filepath="css/iso3166-2-sprite.svg"

# One sprite file per country instead (recommended)
python3 scripts/generate_css.py --iso3166_2_sprite --iso3166_2_sprite_per_country --export_iso3166_2_sprite_dir="css/iso3166-2-sprites"
```

Once a sprite file is included in the page, reference a flag with:
```html
<svg><use href="#fi-gb"/></svg>
<svg><use href="#fi-hu-he"/></svg>
```