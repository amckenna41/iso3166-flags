# ISO3166-1 Flag Icons

Directory of all flags for countries/territories/subdivisions according to the ISO3166-1 definition [[1]](#references). Flag icons imported from the open-source flag-icons repository [[2]](#references).

The flags can be implemented in-line by referencing the CSS class of the respective flag using the ISO3166-1. For ISO3166-1 icons add the classes `.fi` and `.fi-xx` (where `xx` is the ISO 3166-1-alpha-2 code [[1]](#references) of a country) to an empty `<span>`. To add a squared version flag then additionally add the class `fis`. For example, importing the Andorran and Romanian flag icons would look like:

```html
<span class="fi fi-ad"></span> <span class="fi fi-ad fis"></span>
```

```html
<span class="fi fi-ro"></span> <span class="fi fi-ro fis"></span>
```

References
----------
\[1\]: https://en.wikipedia.org/wiki/ISO_3166-1  <br>
\[2\]: https://github.com/lipis/flag-icons  <br>

