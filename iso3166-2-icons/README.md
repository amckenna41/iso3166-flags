# ISO3166-2 Flag Icons

Directory of all flags for principle subdivisions (provinces, states, counties, emirates etc) according to the ISO3166-2 definition [[1]](#references). 

Method
------
From researching, there exists no reliable and high quality dataset of SVG icons for all related ISO3166-2 subdivisions. After researching, there exists several GitHub repos with all ISO3166-1 realted icons but not one including all ISO3166-2 icons. The most relaible source for accurate and high-quality icons seemed to be the country's respective wiki page. Therefore, a Python script was created to download all flag icons from the country's wiki page using the BS4 web scraping library. Many of the SVG files were unnessarily large in size, therefore a secondary bash script was created to compress the files using the Python Scour library. A more in-depth analyse of the scripts can be found within the scripts directory. 

Stats
-----

- X number of countries (note that not all countrys/territories have subdivision flags)
- 7492 number of SVG files
- Country with most flag icons ->  
- Original: 2.01 GB -> Compressed: 1.59 GB

References
----------
\[1\]: https://en.wikipedia.org/wiki/ISO_3166-2  <br>


