# ISO3166-2 Flag Icons

Directory of all flags for countries/territories/subdivisions according to the ISO3166-2 definition [[1]](#references). Flag icons scraped from Wikipedia using the Wikimedia API with the custom-built pyWikiCommons library [[2]](#references). Various custom-built scripts were created (getAllSubdivisionFlags.py & getISO3166-2Flags.py) to pull the thousands of subdivision flags. After cleaning and compressing, using the custom-built svgCompress.sh script, flags were stored in this iso3166-2-icons dir. For usage and more info about the scripts used, please go to the README in the /scripts dir.

For ISO3166-2 icons add the classes `.fi` and `.fi-xx-yy` (where `xx` is the ISO 3166-1-alpha-2 code [[1]](#references) of a country and `yy` is the ISO 3166-2 code) to an empty `<span>`. 

```html
<span class="fi fi-ad-02"></span> <span class="fi fi-ad-02 fis"></span>
```

References
----------
\[1\]: https://en.wikipedia.org/wiki/ISO_3166-2  <br>
\[2\]: https://pypi.org/project/pyWikiCommons/ <br>

