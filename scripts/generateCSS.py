"""
Create CSS files for both ISO3166-1 and ISO3166-2 flag icons allowing for all of the available
flags to be easily integrated into a front-end project using its CSS selector in the respective
CSS file.

"""
import os 
import argparse

def createISO3166_1_css(countryFolder="../iso3166-1-icons", cssFileName="iso3166-1-icons.css"):
    """
    Create custom CSS file for all ISO3166-1 flag icons. By default the CSS files will be stored
    in the "CSS" dir in the main repo dir. Each flag will have its own custom CSS selector 
    that is linked to the filepath of the flag.

    Parameters
    ----------
    :countryFolder : (string)
        filename of folder for ISO3166-1 subdivisions.
    :cssFileName : (string)
        filename for CSS file.

    Returns
    -------
    None
    """
    #path to CSS file will be in the CSS folder in the main repo dir by default
    css_filepath = os.path.join("../", "css", cssFileName)

    cssOutputStr = ""

    #create css file, append the initial required CSS selectors and attributes
    if not(os.path.isfile(css_filepath)):
        open(css_filepath, mode='a').close()
        cssOutputStr += ".fib { \n\tbackground-size: contain; \n\tbackground-position: 50%; \n\tbackground-repeat: no-repeat; \n} \
                    \n\n.fi { \n\tbackground-size: contain; \n\tbackground-position: 50%; \n\tbackground-repeat: no-repeat; \n\tposition: relative; \
                    \n\tdisplay: inline-block; \n\twidth: 1.33333333em; \n\tline-height: 1em; \n} \
                    \n\n.fi.fis { \n\twidth: 1em; \n}\n"
                    # \n.fi:before { \ncontent: '\00a0'; \n} \n.fi.fis { \nwidth: 1em; \n}"

    #get list of all ISO3166-1 svg files
    allFiles = [f for f in os.listdir(countryFolder) if os.path.isfile(os.path.join(countryFolder, f))]

    #iterate through all flag files, creating a custom and unique CSS class selector for each 
    for isoCode in allFiles:
        cssOutputStr += "\n.fi-" + os.path.splitext(isoCode)[0] + " {\n" + "\tbackground-image: url(" + countryFolder + "/" + isoCode + ");\n}\n"

    #append output string to CSS file
    with open(css_filepath, "a") as css_file:
        css_file.write(cssOutputStr)

def createISO3166_2_css(countryFolder="../iso3166-2-icons", cssFileName="iso3166-2-icons.css"):
    """
    Create custom CSS file for all ISO3166-2 flag icons. By default the CSS files will be stored
    in the "CSS" dir in the main repo dir. Each subdivision flag will have its own custom CSS selector 
    that is linked to the filepath of the flag.

    Parameters
    ----------
    :countryFolder : (string)
        filename of folder for ISO3166-2 subdivisions.
    :cssFileName : (string)
        filename for CSS file.

    Returns
    -------
    None
    """
    #path to CSS file will be in the CSS folder in the main repo dir by default
    css_filepath = os.path.join("../", "css", cssFileName)

    cssOutputStr = ""

    #create css file, append the initial required CSS selectors and attributes
    if not(os.path.isfile(css_filepath)):
        open(css_filepath, mode='a').close()
        cssOutputStr += ".fib { \n\tbackground-size: contain; \n\tbackground-position: 50%; \n\tbackground-repeat: no-repeat; \n} \
                    \n.fi { \n\tbackground-size: contain; \n\tbackground-position: 50%; \n\tbackground-repeat: no-repeat; \n\tposition: relative; \
                    \n\tdisplay: inline-block; \n\twidth: 1.33333333em; \n\tline-height: 1em; \n} \
                    \n.fi.fis { \n\twidth: 1em; \n}\n"
                    # \n.fi:before { \ncontent: '\00a0'; \n} \n.fi.fis { \nwidth: 1em; \n}"

    #get list of all country subfolders in ISO3166-2 folder
    allFolders = sorted([f for f in os.listdir(countryFolder) if os.path.isdir(os.path.join(countryFolder, f))])

    #iterate over each subfolder and each subdivision flag, creating a custom and unique CSS class selector for each   
    for country in allFolders:
        allFiles = [f for f in os.listdir(os.path.join(countryFolder, country)) if os.path.isfile(os.path.join(countryFolder, country, f))]
        allFiles.sort()
        for file in allFiles:
            #ignore readme file
            if (os.path.splitext(file)[0].lower() == "readme" or file.lower() == ".ds_store"):
                continue
            cssOutputStr += "\n.fi-" + country.lower() + "-" + os.path.splitext(file)[0].lower() + " {\n" + "\tbackground-image: url(" + countryFolder + "/" + country + "/" + file + ");\n}\n"

    #append output string to CSS file
    with open(css_filepath, "a") as css_file:
        css_file.write(cssOutputStr)

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-countryFolder', '--countryFolder', type=str, required=False, default="../iso3166-1-icons", help='Output folder of ISO3166 countrys, ../iso3166-2-icons by default.')
    parser.add_argument('-cssFileName', '--cssFileName', type=str, required=False, default="iso3166-1-icons.css", help='Filename of CSS, iso3166-1-icons.css by default.')
    parser.add_argument('-iso3166Type', '--iso3166Type', type=str, required=False, default="iso3166-1", help='Create ISO3166-1 or ISO3166-2 CSS file, ISO3166-1 by default.')

    #parse input args
    args = parser.parse_args()
    countryFolder = args.countryFolder
    cssFileName = args.cssFileName
    iso3166Type = args.iso3166Type

    #create CSS file for either ISO3166-1 or ISO3166-2
    if (iso3166Type == "iso3166-1"):
        createISO3166_1_css(countryFolder=countryFolder, cssFileName=cssFileName)
    else:
        createISO3166_2_css(countryFolder=countryFolder, cssFileName=cssFileName)