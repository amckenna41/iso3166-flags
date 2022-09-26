# To Do List for iso3166-flag-icons

* - Compress all files.
- [ ] - Add GitHub release of compressed images
- [ ] - Add different branches - ISO3166-1 branch and ISO3166-2 branch. 
- [X] - Add JSON files for each country https://github.com/hampusborgos/country-flags/blob/main/countries.json
- [ ] - Add sources JSOn
- [X] - Create automatically generated readme for each country folder.
- [X] - Add demo showing how it works like: https://flagicons.lipis.dev/
- [ ] - Create NPM of package: https://www.npmjs.com/package/flag-icons
- [ ] - add yarn.lock
- [X] - Add json of country info (https://en.wikipedia.org/wiki/ISO_3166-1#Naming_and_disputes, https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- [X] - Swap normal brackets for square brackets when saving files, for CSS capability OR remove brackets entirely from filename
- [X] - Skip historical states in getAllSubdivisionFlags.py 
- [X] - Create map visualisation using jsVectorMap with dropdown of each country etc.
- [X] - Maybe remove "" from output filenames
- [ ] - Alphabetise list of countrys in readme
- [X] - Add little svg flag to readme of each country e.g "Albania 🇦🇱 Subdivisions..."
- [X] - Delete original readme file in generate readme 
- [X] - Use pycountry to get list of all country subdivisions, includes name, country code and subdivision type.
- [X] - Split up filenames before matching with fuzzywuzzy - e.g "western_cape_province" -> "western cape province"
- [X] - Remove "province" filenames
- [ ] - Add option to download individual flags on front-end
- [X] - On main repo, have iso3166-2-icons.json & iso3166-2-icons-min.json (a minimmised version of flags without restcountries data)
- [X] - Add actual names of 2 letter subdivision codes, maybe using pycountry...
- [X] - Add play flagle to repo.
- [ ] - Add python badges to scripts dir.
- [X] - Remove "canton" etc from country name...
- [ ] - Add logging messages throughout process logging.info(f'processing {image_path}')
- [ ] - Get list of subdivison types using pycountry, remove from filenames or add to object. 
- [ ] - Try and convert all png's to svg's.
- [ ] - Upload bandit, package safety check etc to GCP bucket 
- [X] - Move requirements section from main readme to scripts dir.
- [ ] - Add download link to downloads/ folder for iso3166-2-icons, stored on AWS or GCP
- [ ] - Add getAllSubdiv and getISO3166... files into one.
- [ ] - Use noISO3166-2Flags.csv file to not download from any countries that don't have flags in getAllSubdivisionFlags.py
- [ ] - Add space b/w ISO 3166-1 and ISO 3166-2.
- [ ] - Add note that ISO 3166-2 jsons dont neccesarrily include all subdivisions just 
ones with flags in the repo.
- [ ] Replace '.svg.png' with '.png'
- [ ] Remove 'Ceuta, Melilla' from restcountries call in index.html.
- [ ] China countrys all wrong.
- [ ] Cambodia subdivisions incorrect order in dropdown.
<!-- https://flagmeister.github.io/?#repoanalyzer -->