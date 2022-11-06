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
- [X] - Alphabetise list of countrys in readme
- [X] - Add little svg flag to readme of each country e.g "Albania 🇦🇱 Subdivisions..."
- [X] - Delete original readme file in generate readme 
- [X] - Use pycountry to get list of all country subdivisions, includes name, country code and subdivision type.
- [X] - Split up filenames before matching with fuzzywuzzy - e.g "western_cape_province" -> "western cape province"
- [X] - Remove "province" filenames
- [X] - On main repo, have iso3166-2-icons.json & iso3166-2-icons-min.json (a minimmised version of flags without restcountries data)
- [X] - Add actual names of 2 letter subdivision codes, maybe using pycountry...
- [X] - Add play flagle to repo.
- [ ] - Add python badges to scripts dir.
- [X] - Remove "canton" etc from country name...
- [ ] - Get list of subdivison types using pycountry, remove from filenames or add to object. 
- [ ] - Try and convert all png's to svg's.
- [ ] - Upload bandit, package safety check etc to GCP bucket 
- [X] - Move requirements section from main readme to scripts dir.
- [X] - Add download link to downloads/ folder for iso3166-2-icons, stored on AWS or GCP
- [X] - Add getAllSubdiv and getISO3166... files into one.
- [ ] - Use noISO3166-2Flags.csv file to not download from any countries that don't have flags in getAllSubdivisionFlags.py
- [ ] - Add space b/w ISO 3166-1 and ISO 3166-2.
- [ ] - Add note that ISO 3166-2 jsons dont neccesarrily include all subdivisions just 
ones with flags in the repo.
- [ ] Replace '.svg.png' with '.png'
- [X] Remove 'Ceuta, Melilla' from restcountries call in index.html.
- [X] China countrys all wrong.
- [ ] Create CDN 
- [ ] Import CSS flags on index.html using css.
- [ ] Upload dataset to Kaggle.
- [X] Fix LI vertical flags.
- [ ] Fix Taiwan.
- [ ] PM, GQ, icons not in correct format.
- [X] Sort noISO3166-2Flags.csv in alphabetical order.
- [ ] Fix char_to_replace dict in getAllSubdivisionFlags.
- [X] Check all folders dont contain any files not in form XX-YY etc.
- [X] MD file showing list of countrys/subdivisions with outstanding files with no current svg.
- [ ] Complete /scripts/README
- [ ] Create API for accessing subdivision imgs, similar to restcountries.
- [ ] Add download button for img on front-end.
- [ ] Add shading to subdivision info table.
- [ ] Read the docs (.readthedocs.yml)
- [ ] Create CSS for bootstrap package (https://github.com/lipis/bootstrap-social).
- [ ] Add emojis to subdivision info table, similar to https://bondok-world-data.herokuapp.com/
- [ ] Build restful API with country flags as endpoints.
- [X] Create script/function to double check no duplicate subdiv flags, regardless of file type.
- [ ] Add open issue about flags with no easily accessible SVG's - convert all flags first & calculate non-svg count.
- [ ] If img wikimedia URL ends in .png etc, see if SVG version of URL exists.
- [X] DRC flags: https://en.wikipedia.org/wiki/ISO_3166-2:CD
- [ ] Look into implementing lambda functions for efficency.
- [X] Pass raw filename through download function then only create path to it at end
- [ ] Ignore filenames for download that have year in brackets & remove country name from filename.
- [ ] Some sort of workflow that polls original /flag-icons repo to see if any updates to iso3166-1 flags.
- [ ] Check variable naming conventions.
- [ ] Check output of bandit and flake8 check.
- [ ] Have multiple urls to download from in getAllSubdivisionFlags.py
- [X] Convert all gifs to pngs using convert lib: convert SI-038.gif/jpg SI-038.png - split into its own function in bash script. 
- [ ] Add updates.md file which outlines changes to repo bw versions.
- [X] Change iso3166-2_min -> iso3166-2-min.
- [ ] Mention that iso3166-2 doesnt contain all country info just that of those that have flags in repo.

<!-- AL-04 -> https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Stema_e_Qarkut_Fier.svg/1024px-Stema_e_Qarkut_Fier.svg.png
Change to:
https://upload.wikimedia.org/wikipedia/commons/2/29/Stema_e_Qarkut_Fier.svg -->

<!-- https://flagmeister.github.io/?#repoanalyzer -->