from scripts.generate_readme import *
import shutil
import os
import textwrap
import unittest
import warnings
unittest.TestLoader.sortTestMethodsUsing = None

#ignore resource warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

# @unittest.skip("Skipping tests.")
class Generate_Readme_Tests(unittest.TestCase):
    """
    Test suite for testing generate_readme.py script that exports the markdown files
    per flag subdivision sub-folder.

    Test Cases
    ==========
    test_create_markdown_str:
        testing the function that creates the markdown string per subfolder.
    test_create_readme:
        testing the function that generates the full markdown file per subfolder. 
    """
    @classmethod
    def setUp(self):
        """ Initialise test variables. """
        self.test_output_dir = os.path.join("tests", "test_output_dir")
        self.test_markdown_output_folder = os.path.join(self.test_output_dir, "test_markdown")
        self.test_input_flag_folder = "iso3166-2-flags"

        #create test directory if not already present
        if not (os.path.isdir(self.test_output_dir)):
            os.makedirs(self.test_output_dir)

    # @unittest.skip("")
    def test_create_markdown_str(self):
        """ Testing the function that creates the markdown string per subfolder. """
        test_markdown_ad = "AD" #Andorra
        test_markdown_et = "ET" #Ethiopia
        test_markdown_mu = "MU" #Mauritius
        test_markdown_pa = "PA" #Panama
#1.)
        test_ad_markdown = create_markdown_str(test_markdown_ad, "iso3166-2-flags/AD")
        test_ad_markdown_expected = textwrap.dedent("""\
            # Andorra Subdivisions ![](https://flagcdn.com/h40/ad.png)

            - **ISO Code**: AD
            - **Number of subdivisions**: 7
            - **Subdivision Type**: Parish
            - **ISO 3166-2 API link**: https://iso3166-2-api.vercel.app/api/alpha/AD

            | Code  | Subdivision Name         | Type | Flag Preview | Link |
            |-------|--------------------------|--------------| -------------- |----------|
            | AD-02 | Canillo | Parish | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-02.svg' height='80'> | [AD-02.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-02.svg) |
            | AD-03 | Encamp | Parish | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-03.svg' height='80'> | [AD-03.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-03.svg) |
            | AD-04 | La Massana | Parish | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-04.svg' height='80'> | [AD-04.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-04.svg) |
            | AD-05 | Ordino | Parish | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-05.svg' height='80'> | [AD-05.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-05.svg) |
            | AD-06 | Sant Julià de Lòria | Parish | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-06.svg' height='80'> | [AD-06.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-06.svg) |
            | AD-07 | Andorra la Vella | Parish | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-07.svg' height='80'> | [AD-07.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-07.svg) |
            | AD-08 | Escaldes-Engordany | Parish | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-08.svg' height='80'> | [AD-08.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/AD/AD-08.svg) |
            """)
        
        self.assertEqual(test_ad_markdown, test_ad_markdown_expected, f"Expected and observed markdown string output do not match:\n{test_ad_markdown}")
#2.)
        test_et_markdown = create_markdown_str(test_markdown_et, "iso3166-2-flags/ET")
        test_et_markdown_expected = textwrap.dedent("""\
            # Ethiopia Subdivisions ![](https://flagcdn.com/h40/et.png)

            - **ISO Code**: ET
            - **Number of subdivisions**: 13
            - **Subdivision Type**: Administration, Regional state
            - **ISO 3166-2 API link**: https://iso3166-2-api.vercel.app/api/alpha/ET

            | Code  | Subdivision Name         | Type | Flag Preview | Link |
            |-------|--------------------------|--------------| -------------- |----------|
            | ET-AA | Addis Ababa | Administration | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-AA.svg' height='80'> | [ET-AA.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-AA.svg) |
            | ET-AF | Afar | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-AF.svg' height='80'> | [ET-AF.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-AF.svg) |
            | ET-AM | Amara | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-AM.svg' height='80'> | [ET-AM.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-AM.svg) |
            | ET-BE | Benshangul-Gumaz | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-BE.svg' height='80'> | [ET-BE.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-BE.svg) |
            | ET-DD | Dire Dawa | Administration | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-DD.png' height='80'> | [ET-DD.png](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-DD.png) |
            | ET-GA | Gambela Peoples | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-GA.svg' height='80'> | [ET-GA.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-GA.svg) |
            | ET-HA | Harari People | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-HA.svg' height='80'> | [ET-HA.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-HA.svg) |
            | ET-OR | Oromia | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-OR.svg' height='80'> | [ET-OR.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-OR.svg) |
            | ET-SI | Sidama | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-SI.svg' height='80'> | [ET-SI.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-SI.svg) |
            | ET-SN | Southern Nations, Nationalities and Peoples | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-SN.svg' height='80'> | [ET-SN.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-SN.svg) |
            | ET-SO | Somali | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-SO.svg' height='80'> | [ET-SO.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-SO.svg) |
            | ET-SW | Southwest Ethiopia Peoples | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-SW.svg' height='80'> | [ET-SW.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-SW.svg) |
            | ET-TI | Tigrai | Regional state | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-TI.svg' height='80'> | [ET-TI.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/ET/ET-TI.svg) |
            """)

        self.assertEqual(test_et_markdown, test_et_markdown_expected, f"Expected and observed markdown string output do not match:\n{test_et_markdown}")
#3.)
        test_mu_markdown = create_markdown_str(test_markdown_mu, "iso3166-2-flags/MU")
        test_mu_markdown_expected = textwrap.dedent("""\
        # Mauritius Subdivisions ![](https://flagcdn.com/h40/mu.png)

        - **ISO Code**: MU
        - **Number of subdivisions**: 12
        - **Subdivision Type**: Dependency, District
        - **ISO 3166-2 API link**: https://iso3166-2-api.vercel.app/api/alpha/MU

        | Code  | Subdivision Name         | Type | Flag Preview | Link |
        |-------|--------------------------|--------------| -------------- |----------|
        | MU-PL | Port Louis | District | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/MU/MU-PL.svg' height='80'> | [MU-PL.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/MU/MU-PL.svg) |
        | MU-RO | Rodrigues Island | Dependency | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/MU/MU-RO.svg' height='80'> | [MU-RO.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/MU/MU-RO.svg) |

        Mauritius ISO 3166-2 subdivisions with no available flags:

        * **MU-AG: Agalega Islands (Dependency)**
        * **MU-BL: Black River (District)**
        * **MU-CC: Cargados Carajos Shoals (Dependency)**
        * **MU-FL: Flacq (District)**
        * **MU-GP: Grand Port (District)**
        * **MU-MO: Moka (District)**
        * **MU-PA: Pamplemousses (District)**
        * **MU-PW: Plaines Wilhems (District)**
        * **MU-RR: Rivière du Rempart (District)**
        * **MU-SA: Savanne (District)**

        ## Notes
        Only two of the districts have official flags, the others usually only have coat of arms.
        """).rstrip("\n")

        # self.assertEqual(test_mu_markdown, test_mu_markdown_expected, f"Expected and observed markdown string output do not match:\n{test_mu_markdown}")
#4.)
        test_pa_markdown = create_markdown_str(test_markdown_pa, "iso3166-2-flags/PA")
        test_pa_markdown_expected = textwrap.dedent("""\
        # Panama Subdivisions ![](https://flagcdn.com/h40/pa.png)

        - **ISO Code**: PA
        - **Number of subdivisions**: 14
        - **Subdivision Type**: Indigenous region, Province
        - **ISO 3166-2 API link**: https://iso3166-2-api.vercel.app/api/alpha/PA

        | Code  | Subdivision Name         | Type | Flag Preview | Link |
        |-------|--------------------------|--------------| -------------- |----------|
        | PA-1 | Bocas del Toro | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-1.svg' height='80'> | [PA-1.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-1.svg) |
        | PA-10 | Panamá Oeste | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-10.svg' height='80'> | [PA-10.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-10.svg) |
        | PA-2 | Coclé | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-2.svg' height='80'> | [PA-2.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-2.svg) |
        | PA-3 | Colón | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-3.svg' height='80'> | [PA-3.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-3.svg) |
        | PA-4 | Chiriquí | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-4.svg' height='80'> | [PA-4.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-4.svg) |
        | PA-5 | Darién | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-5.svg' height='80'> | [PA-5.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-5.svg) |
        | PA-6 | Herrera | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-6.svg' height='80'> | [PA-6.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-6.svg) |
        | PA-7 | Los Santos | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-7.svg' height='80'> | [PA-7.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-7.svg) |
        | PA-9 | Veraguas | Province | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-9.svg' height='80'> | [PA-9.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-9.svg) |
        | PA-EM | Emberá | Indigenous region | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-EM.svg' height='80'> | [PA-EM.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-EM.svg) |
        | PA-KY | Guna Yala | Indigenous region | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-KY.svg' height='80'> | [PA-KY.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-KY.svg) |
        | PA-NB | Ngäbe-Buglé | Indigenous region | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-NB.svg' height='80'> | [PA-NB.svg](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-NB.svg) |
        | PA-NT | Naso Tjër Di | Indigenous region | <img src='https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-NT.png' height='80'> | [PA-NT.png](https://raw.githubusercontent.com/amckenna41/iso3166-flags/main/iso3166-2-flags/PA/PA-NT.png) |

        Panama ISO 3166-2 subdivisions with no available flags:

        * **PA-8: Panamá (Province)**

        ## Notes
        All of Panama's provinces have their own official flag, except for PA-8 (Panamá), the widely circulated flag is that of Panama city not the province itself.
        """).rstrip("\n")

        self.assertEqual(test_pa_markdown, test_pa_markdown_expected, f"Expected and observed markdown string output do not match:\n{test_pa_markdown}")
#5.)
        with self.assertRaises(ValueError):
            test_error_markdown = create_markdown_str("ad,de,fr", "iso3166-2-flags/AD")
            test_error1_markdown = create_markdown_str("ug,us", "iso3166-2-flags/UG")
            test_error2_markdown = create_markdown_str("abc", "iso3166-2-flags/AD")
#6.)
        with self.assertRaises(OSError):
            test_error3_markdown = create_markdown_str("HU", "blahblah/HU")
            test_error4_markdown = create_markdown_str("HU", "iso3166-2-flags/ZZ")

    # @unittest.skip("")
    def test_create_readme(self):
        """ Testing the function that generates the full markdown file per country subfolder. """
        test_markdown_az = "AZ"
        test_markdown_ca = "CA"
        test_markdown_fi = "FI"
        test_markdown_ke = "KE"
#1.)
        create_readme(self.test_input_flag_folder, test_markdown_az, self.test_markdown_output_folder)
        self.assertTrue(os.path.isfile(os.path.join(self.test_markdown_output_folder, test_markdown_az, "README.md")))
#2.)
        create_readme(self.test_input_flag_folder, test_markdown_ca, self.test_markdown_output_folder)
        self.assertTrue(os.path.isfile(os.path.join(self.test_markdown_output_folder, test_markdown_ca, "README.md")))
#3.)
        create_readme(self.test_input_flag_folder, test_markdown_fi, self.test_markdown_output_folder)
        self.assertTrue(os.path.isfile(os.path.join(self.test_markdown_output_folder, test_markdown_fi, "README.md")))
#4.)
        create_readme(self.test_input_flag_folder, test_markdown_ke, self.test_markdown_output_folder)
        self.assertTrue(os.path.isfile(os.path.join(self.test_markdown_output_folder, test_markdown_ke, "README.md")))
#5.)
        with self.assertRaises(ValueError):
            create_readme(self.test_input_flag_folder, "ABC")
            create_readme(self.test_input_flag_folder, "123")
#6.)
        with self.assertRaises(OSError):
            create_readme("invalid_folder_path")

    @classmethod
    def tearDown(self):
        """ Delete any temp export folder. """
        shutil.rmtree(self.test_output_dir)

if __name__ == '__main__':  
    #run all unit tests
    unittest.main(verbosity=2)    