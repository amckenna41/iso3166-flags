
import unittest
import iso3166_

class GetSubdivisionScriptTests(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()

totalSubdivisions = {
    ""
    "UZ": 1,
    "VC": 1,
    "VE": 28
    "VU": 7,
    "WF": 4,
    "WS": 2,
    "XK": 12,
    "YE": 9,
    "ZA": 10,
    "ZW": 3
}

#use pycountry 
#len(pycountry.subdivisions.get(country_code="UY")) == 19
#test both wiki endpoints