import unittest
import numpy as np
from io import StringIO
import sys

from eppoPynder.getting_countries import getting_countries

class TestGettingCountries(unittest.TestCase):

    def test_EPPO(self):
        """Test if a concatenation of countries corresponding to the acronym 'EPPO' is returned."""
        result = getting_countries("EPPO")
        expected = "Albania, Algeria, Austria, Azerbaijan, Belarus, Belgium, Bosnia and Herzegovina, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Georgia, Germany, Greece, Guernsey, Hungary, Ireland, Israel, Italy, Jersey, Jordan, Kazakhstan, Kyrgyzstan, Latvia, Lithuania, Luxembourg, Malta, Moldova, Montenegro, Morocco, Netherlands, North Macedonia, Norway, Poland, Portugal, Romania, Russia, Serbia, Slovakia, Slovenia, Spain, Sweden, Switzerland, Tunisia, Türkiye, Ukraine, United Kingdom, Uzbekistan"
        self.assertEqual(result, expected)

    def test_OIRSA(self):
        """Test if a concatenation of countries corresponding to the acronym 'OIRSA' is returned."""
        result = getting_countries("OIRSA")
        expected = "Belize, Costa Rica, Dominican Republic, El Salvador, Guatemala, Honduras, Mexico, Nicaragua, Panama"
        self.assertEqual(result, expected)

    def test_EAEU(self):
        """Test if a concatenation of countries corresponding to the acronym 'EAEU' is returned."""
        result = getting_countries("EAEU")
        expected = "Armenia, Belarus, Kazakhstan, Kyrgyzstan, Russia"
        self.assertEqual(result, expected)

    def test_COSAVE(self):
        """Test if a concatenation of countries corresponding to the acronym 'COSAVE' is returned."""
        result = getting_countries("COSAVE")
        expected = "Argentina, Bolivia, Brazil, Chile, Paraguay, Peru, Uruguay"
        self.assertEqual(result, expected)

    def test_EU(self):
        """Test if a concatenation of countries corresponding to the acronym 'EU' is returned."""
        result = getting_countries("EU")
        expected = "Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden"
        self.assertEqual(result, expected)

    def test_APPPC(self):
        """Test if a concatenation of countries corresponding to the acronym 'APPPC' is returned."""
        result = getting_countries("APPPC")
        expected = "Australia, Bangladesh, Cambodia, China, East Timor, Fiji, French Polynesia, India, Indonesia, Korea Dem. People's Republic, Korea, Republic, Laos, Malaysia, Myanmar, Nepal, New Zealand, Pakistan, Papua New Guinea, Philippines, Samoa, Solomon Islands, Sri Lanka, Thailand, Tonga, Vietnam"
        self.assertEqual(result, expected)

    def test_CAHFSA(self):
        """Test if a concatenation of countries corresponding to the acronym 'CAHFSA' is returned."""
        result = getting_countries("CAHFSA")
        expected = "Antigua and Barbuda, Bahamas, Barbados, Belize, Dominica, Grenada, Guyana, Haiti, Jamaica, Montserrat, Saint Lucia, St Kitts-Nevis, St Vincent and the Grenadines, Suriname, Trinidad and Tobago"
        self.assertEqual(result, expected)

    def test_CAN(self):
        """Test if a concatenation of countries corresponding to the acronym 'CAN' is returned."""
        result = getting_countries("CAN")
        expected = "Bolivia, Colombia, Ecuador, Peru, Venezuela"
        self.assertEqual(result, expected)

    def test_IAPSC(self):
        """Test if a concatenation of countries corresponding to the acronym 'IAPSC' is returned."""
        result = getting_countries("IAPSC")
        expected = "Algeria, Angola, Benin, Botswana, Burkina Faso, Burundi, Cameroon, Cape Verde, Central African Republic, Chad, Comoros, Congo, Congo, Democratic Republic of the, Cote d'Ivoire, Djibouti, Egypt, Equatorial Guinea, Eritrea, Eswatini, Ethiopia, Gabon, Gambia, Ghana, Guinea, Guinea-Bissau, Kenya, Lesotho, Liberia, Libya, Madagascar, Malawi, Mali, Mauritania, Mauritius, Morocco, Mozambique, Namibia, Niger, Nigeria, Rwanda, Sao Tome & Principe, Senegal, Seychelles, Sierra Leone, Somalia, South Africa, South Sudan, Sudan, Tanzania, Togo, Tunisia, Uganda, Zaire, Zambia, Zimbabwe"
        self.assertEqual(result, expected)

    def test_NAPPO(self):
        """Test if a concatenation of countries corresponding to the acronym 'NAPPO' is returned."""
        result = getting_countries("NAPPO")
        expected = "Canada, Mexico, United States of America"
        self.assertEqual(result, expected)

    def test_NEPPO(self):
        """Test if a concatenation of countries corresponding to the acronym 'NEPPO' is returned."""
        result = getting_countries("NEPPO")
        expected = "Algeria, Egypt, Jordan, Libya, Malta, Morocco, Pakistan, South Sudan, Sudan, Syria, Tunisia"
        self.assertEqual(result, expected)

    def test_PPPO(self):
        """Test if a concatenation of countries corresponding to the acronym 'PPPO' is returned."""
        result = getting_countries("PPPO")
        expected = "American Samoa, Australia, Cook Islands, Fiji, French Polynesia, Guam, Kiribati, Marshall Islands, Micronesia, Nauru, New Caledonia, New Zealand, Niue, Northern Mariana Islands, Palau, Papua New Guinea, Pitcairn, Samoa, Solomon Islands, Tokelau, Tonga, Tuvalu, Vanuatu, Wallis and Futuna Islands"
        self.assertEqual(result, expected)

    def test_unknown_acronym(self):
        """Test if np.nan and print message are returned for unknown acronyms."""
        # Capture print output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Test unknown acronym
        result = getting_countries("XYZ")
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify results
        self.assertTrue(np.isnan(result))
        self.assertEqual(captured_output.getvalue().strip(), "Unknown acronym")
