"""
Create README file for each ISO3166-2 country subfolder, listing the name of 
each country's subdivision, its subdivision code and a link to the image in the repo.
"""
import os
from os import listdir
import flag
import pycountry

#base URL to iso3166-2-icons folder in repo
baseURL = 'https://github.com/amckenna41/iso3166-flag-icons/blob/main/iso3166-2-icons'

def createReadMe(country, code, url, outputFolder):
    """
    Create custom README for each countrys subdivision folder in the output folder. The
    README will list all of the country's subdivisions, their filename on the repo and 
    links to download them on the repo.

    Parameters
    ----------
    :country : string 
      country name.
    :code : string 
        2 letter ISO code of country.
    :url : string
        source url for where subdivisions were pulled from.
    :outputFolder : string
        filepath to output folder to write README
    Returns
    -------
    None 
    """  
    #get filepath to readme file in each output folder
    filepath = "{}/{}".format(outputFolder, code)
    readMeFilepath = os.path.join(filepath, 'README.md')

    #get list of all files in subfolder
    allFiles = sorted([f.lower() for f in listdir(filepath) if os.path.isfile(os.path.join(filepath, f))], key=str.casefold)
    allSubdivisions = list(pycountry.subdivisions.get(country_code=code))

    #remove readme file from list of files
    if ("README.md" in allFiles):
        allFiles.remove("README.md")

    #append subdivision name and code to readme
    outputStr = ""
    outputStr+= "# {} {} Subdivisions\n\n".format(country, flag.flag(code))
    outputStr+= "Source: {}\n\n".format(url)

    subdName = ""

    #iterate through all file names, appending to the output string 
    for file in allFiles:
        if (file.lower() == ".ds_store" or file.lower() == "readme.md"): #skip non-subdivision files
            continue
        outputStr+= "*"
        for subd in allSubdivisions:
            if (subd.code.lower() == os.path.splitext(os.path.basename(file))[0].replace('_', ' ').lower()):
                subdName = subd.name
        
        outputStr += " " + os.path.splitext(os.path.basename(file))[0].replace('_', ' ').upper()
        if (subdName != "" and subdName != None):
            outputStr += " (" + subdName.title() + ")"

        outputStr += " -> [{}]({}/{}/{})\n".format(file, baseURL, code, file)

    #get list of all filenames in folder
    allFiles = [os.path.splitext(file)[0] for file in allFiles]

    #delete readme file if exists
    if (os.path.isfile(readMeFilepath)):
        os.remove(readMeFilepath)
    
    allFileSubdivisions = []
    missingSubdivisions = []

    #get list of missing subdivision flags not present in country subfolder
    if (pycountry.subdivisions.get(country_code=code) != None):
        allFileSubdivisions = [subdivision.code.lower() for subdivision in pycountry.subdivisions.get(country_code=code)]
        for subd in allFileSubdivisions:
            if (subd not in allFiles):
                missingSubdivisions.append(subd)
        
    #print list of country's subdivisions that dont have any flags
    if len(missingSubdivisions) != 0:
        outputStr += f'\n{country} ISO3166-2 subdivisions with no available flags (https://en.wikipedia.org/wiki/ISO_3166-2:{code})\n'
        for subd in missingSubdivisions:
            for subdiv in pycountry.subdivisions.get(country_code=code):
                if (subdiv.code.lower() == subd):
                    outputStr += "\n* {}: {} ({})".format(subd.upper(), subdiv.name, subdiv.type)

    #create new readme file
    open(readMeFilepath, mode='a').close()

    #append output string to readme
    with open(readMeFilepath, "a") as readmeFile:
        readmeFile.write(outputStr)
