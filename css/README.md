# CSS Files for the ISO 3166-1 and ISO 3166-2 flags

* [iso3166-1.css](https://github.com/amckenna41/iso3166-flag-icons/css/iso3166-1.css) - CSS containing selectors for all ISO 3166-1 flags on the repo.
* [iso3166-2.css](https://github.com/amckenna41/iso3166-flag-icons/css/iso3166-2.css) - CSS containing selectors for all ISO 3166-2 flags on the repo.

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