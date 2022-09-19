import iso3166_
import unittest

class ISO3166_Tests(unittest.TestCase):
    """ Testing ISO3166 module. """
    
    def setUp(self) -> None:        
        return super().setUp()
    
    def test_iso3166(self):
        """ Testing iso3166_ module object values and types. """

        self.assertEqual(len(iso3166_.countries), 312, f'There should be 312 countries, but got {len(iso3166_.countries)}.')
        self.assertEqual(len(iso3166_.countries_by_name), 312, f'There should be 312 countries, but got {len(iso3166_.countries_by_name)}.')
        self.assertEqual(len(iso3166_.countries_by_apolitical_name), 310, f'There should be 310 countries, but got {len(iso3166_.countries_by_apolitical_name)}.')
        self.assertEqual(len(iso3166_.countries_by_alpha2), 275, f'There should be 275 countries, but got {len(iso3166_.countries_by_alpha2)}.')
        self.assertEqual(len(iso3166_.countries_by_alpha3), 262, f'There should be 262 countries, but got {len(iso3166_.countries_by_alpha3)}.')
        self.assertEqual(len(iso3166_.countries_by_numeric), 257, f'There should be 257 countries, but got {len(iso3166_.countries_by_numeric)}.')
        self.assertEqual(len(iso3166_._records), 312, f'There should be 312 countries, but got {len(iso3166_._records)}.')

        self.assertIsInstance(iso3166_.countries, dict, f'countries object should be a dict, got {type(iso3166_.countries)}')
        self.assertIsInstance(iso3166_.countries_by_name, dict, f'countries_by_name object should be a dict, got {type(iso3166_.countries_by_name)}')
        self.assertIsInstance(iso3166_.countries_by_apolitical_name, dict, f'countries_by_apolitical_name object should be a dict, got {type(iso3166_.countries_by_apolitical_name)}')
        self.assertIsInstance(iso3166_.countries_by_alpha2, dict, f'countries_by_alpha2 object should be a dict, got {type(iso3166_.countries_by_alpha2)}')
        self.assertIsInstance(iso3166_.countries_by_alpha3, dict, f'countries_by_alpha3 object should be a dict, got {type(iso3166_.countries_by_alpha3)}')
        self.assertIsInstance(iso3166_._records, list, f'_records object should be a list, got {type(iso3166_._records)}')

    def test_country_names(self):
        """ Testing ISO3166 country names. """

        test_country1 = "Albania"
        test_country2 = "Bolivia"
        test_country3 = "Cuba" 
        test_country4 = "Dominica"
        test_country5 = "Venezuela"
        test_country6 = "Wallis and Futuna"
        test_country7 = "abcdefg"
        test_country8 = False

        self.assertEqual(iso3166_.countries_by_name[test_country1].name, "Albania", "Incorrect country name returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country2].name, "Bolivia", "Incorrect country name returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country3].name, "Cuba", "Incorrect country name returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country4].name, "Dominica", "Incorrect country name returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country5].name, "Venezuela", "Incorrect country name returned.")        self.assertEqual(iso3166_.countries_by_name[test_country6].name, "Wallis and Futuna", "Incorrect country name returned.")

        with(self.assertRaises(KeyError, msg="Key Error raised, invalid country name.")):
            iso3166_.countries_by_name[test_country7].name

        with(self.assertRaises(KeyError, msg="Key Error raised, invalid country name.")):
            iso3166_.countries_by_name[test_country8].name

    def test_country_alpha2(self):
        """ Testing ISO3166 alpha-2 codes. """
        
        test_country1 = "AZ"
        test_country2 = "CO"
        test_country3 = "ET" 
        test_country4 = "LA"
        test_country5 = "UZ"
        test_country6 = "YE"
        test_country7 = "abcdefg"
        test_country8 = False

        self.assertEqual(iso3166_.countries_by_name[test_country1].alpha2, "AZ", "Incorrect country alpha-2 code returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country2].alpha2, "CO", "Incorrect country alpha-2 code returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country3].alpha2, "ET", "Incorrect country alpha-2 code returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country4].alpha2, "LA", "Incorrect country alpha-2 code returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country5].alpha2, "UZ", "Incorrect country alpha-2 code returned.")        self.assertEqual(iso3166_.countries_by_name[test_country6].name, "Wallis and Futuna", "Incorrect country name returned.")
        self.assertEqual(iso3166_.countries_by_name[test_country6].alpha2, "", "Incorrect country alpha-2 code returned.")        self.assertEqual(iso3166_.countries_by_name[test_country6].name, "Wallis and Futuna", "Incorrect country name returned.")

        with(self.assertRaises(KeyError, msg="Key Error raised, invalid country alpha-2 code.")):
            iso3166_.countries_by_name[test_country7].name

        with(self.assertRaises(KeyError, msg="Key Error raised, invalid country alpha-2 code.")):
            iso3166_.countries_by_name[test_country8].name
    
    def test_country_alpha3(self):
        """ Testing ISO3166 alpha-3 codes. """
        
        test_country1 = "Cabo Verde"
        test_country2 = "Fiji"
        test_country3 = "Georgia" 
        test_country4 = "Liberia"
        test_country5 = "Qatar"
        test_country6 = "US"
        test_country7 = "Burma"
        test_country8 = "abcdefg"
        test_country9 = False

        self.assertEqual(iso3166_.countries_by_name[test_country1].alpha3, "CBV", "Incorrect country alpha-3 code returned: got {iso3166_.countries_by_name[test_country1].alpha3}, expected CBV.")
        self.assertEqual(iso3166_.countries_by_name[test_country2].alpha3, "FIJ", "Incorrect country alpha-3 code returned: got {iso3166_.countries_by_name[test_country2].alpha3}, expected FIJ.")
        self.assertEqual(iso3166_.countries_by_name[test_country3].alpha3, "GEO", "Incorrect country alpha-3 code returned: got {iso3166_.countries_by_name[test_country3].alpha3}, expected GEO.")
        self.assertEqual(iso3166_.countries_by_name[test_country4].alpha3, "LIB", "Incorrect country alpha-3 code returned: got {iso3166_.countries_by_name[test_country4].alpha3}, expected LIB.")
        self.assertEqual(iso3166_.countries_by_name[test_country5].alpha3, "QAT", "Incorrect country alpha-3 code returned: got {iso3166_.countries_by_name[test_country5].alpha3}, expected QAT.")      
        self.assertEqual(iso3166_.countries_by_name[test_country6].alpha3, "USA", "Incorrect country alpha-3 code returned: got {iso3166_.countries_by_name[test_country6].alpha3}, expected USA.")     
        self.assertEqual(iso3166_.countries_by_name[test_country7].alpha3, "", "Incorrect country alpha-3 code returned: got {iso3166_.countries_by_name[test_country7].alpha3}, expected CBV.")    

        with(self.assertRaises(KeyError, msg="Key Error raised, invalid country alpha-3 code.")):
            iso3166_.countries_by_name[test_country8].alpha3

        with(self.assertRaises(KeyError, msg="Key Error raised, invalid country alpha-3 code.")):
            iso3166_.countries_by_name[test_country9].alpha3
    
    def test_country_apolitical_name(self):
        """ Testing ISO3166 apolitical names. """

        test_country1 = "Åland Islands"
        test_country2 = "Bulgaria"
        test_country3 = "China" 
        test_country4 = "Honduras"
        test_country5 = "Peru"
        test_country6 = "Vietnam"
        test_country7 = "abcdefg"
        test_country8 = False

        self.assertEqual(iso3166_.countries_by_name[test_country1].apolitical_name, "Åland Islands", "Incorrect country apolitical name returned: got {iso3166_.countries_by_name[test_country1].apolitical_name}, expected Åland Islands.")
        self.assertEqual(iso3166_.countries_by_name[test_country2].apolitical_name, "Bulgaria", "Incorrect country apolitical name returned: got {iso3166_.countries_by_name[test_country2].apolitical_name}, expected Bulgaria.")
        self.assertEqual(iso3166_.countries_by_name[test_country3].apolitical_name, "China", "Incorrect country apolitical name returned: got {iso3166_.countries_by_name[test_country3].apolitical_name}, expected China.")
        self.assertEqual(iso3166_.countries_by_name[test_country4].apolitical_name, "Honduras", "Incorrect country apolitical name returned: got {iso3166_.countries_by_name[test_country4].apolitical_name}, expected Honduras.")
        self.assertEqual(iso3166_.countries_by_name[test_country5].apolitical_name, "Peru", "Incorrect country apolitical name returned: got {iso3166_.countries_by_name[test_country5].apolitical_name}, expected Peru.")      
        self.assertEqual(iso3166_.countries_by_name[test_country6].apolitical_name, "Vietnam", "Incorrect country apolitical name returned: got {iso3166_.countries_by_name[test_country6].apolitical_name}, expected Vietnam.")     

        with(self.assertRaises(KeyError, msg="Key Error raised, invalid country apolitical name.")):
            iso3166_.countries_by_name[test_country7].apolitical_name

        with(self.assertRaises(KeyError, msg="Key Error raised, invalid country apolitical name.")):
            iso3166_.countries_by_name[test_country8].apolitical_name

    def tearDown(self) -> None:
        return super().tearDown()        
