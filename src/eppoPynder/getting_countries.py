import numpy as np

def getting_countries(acronym):
    """
    Function to translate the acronyms of the Regional Plant Protection Organizations used in the EPPO database to the corresponding member countries.

    Parameters
    ----------
    acronym : str
        The acronym of the Regional Plant Protection Organization.

    Returns
    -------
    countries : str
        All the member countries.

    Examples
    --------
    getting_countries('OIRSA')
    """
    assert isinstance(acronym, str), "acronym must be a string!"

    if acronym == 'EPPO':
        countries = ", ".join([
            'Albania', 'Algeria', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 
            'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 
            'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 
            'Guernsey', 'Hungary', 'Ireland', 'Israel', 'Italy', 'Jersey', 'Jordan', 
            'Kazakhstan', 'Kyrgyzstan', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 
            'Moldova', 'Montenegro', 'Morocco', 'Netherlands', 'North Macedonia', 'Norway', 
            'Poland', 'Portugal', 'Romania', 'Russia', 'Serbia', 'Slovakia', 'Slovenia', 
            'Spain', 'Sweden', 'Switzerland', 'Tunisia', 'Türkiye', 'Ukraine', 'United Kingdom', 
            'Uzbekistan'
        ])
    elif acronym == 'OIRSA':
        countries = ", ".join([
            'Belize', 'Costa Rica', 'Dominican Republic', 'El Salvador', 'Guatemala', 
            'Honduras', 'Mexico', 'Nicaragua', 'Panama'
        ])
    elif acronym == 'EAEU':
        countries = ", ".join([
            'Armenia', 'Belarus', 'Kazakhstan', 'Kyrgyzstan', 'Russia'
        ])
    elif acronym == 'COSAVE':
        countries = ", ".join([
            'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Paraguay', 'Peru', 'Uruguay'
        ])
    elif acronym == 'EU':
        countries = ", ".join([
            'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 
            'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 
            'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 
            'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden'
        ])
    elif acronym == 'APPPC':
        countries = ", ".join([
            'Australia', 'Bangladesh', 'Cambodia', 'China', 'East Timor', 'Fiji', 
            'French Polynesia', 'India', 'Indonesia', "Korea Dem. People's Republic", 
            'Korea, Republic', 'Laos', 'Malaysia', 'Myanmar', 'Nepal', 'New Zealand', 
            'Pakistan', 'Papua New Guinea', 'Philippines', 'Samoa', 'Solomon Islands', 
            'Sri Lanka', 'Thailand', 'Tonga', 'Vietnam'
        ])
    elif acronym == 'CAHFSA':
        countries = ", ".join([
            'Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Dominica', 'Grenada', 
            'Guyana', 'Haiti', 'Jamaica', 'Montserrat', 'Saint Lucia', 'St Kitts-Nevis', 
            'St Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago'
        ])
    elif acronym == 'CAN':
        countries = ", ".join([
            'Bolivia', 'Colombia', 'Ecuador', 'Peru', 'Venezuela'
        ])
    elif acronym == 'IAPSC':
        countries = ", ".join([
            'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 
            'Cape Verde', 'Central African Republic', 'Chad', 'Comoros', 'Congo', 
            'Congo, Democratic Republic of the', "Cote d'Ivoire", 'Djibouti', 'Egypt', 
            'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 
            'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 
            'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 
            'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome & Principe', 'Senegal', 
            'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 
            'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zaire', 'Zambia', 'Zimbabwe'
        ])
    elif acronym == 'NAPPO':
        countries = ", ".join([
            'Canada', 'Mexico', 'United States of America'
        ])
    elif acronym == 'NEPPO':
        countries = ", ".join([
            'Algeria', 'Egypt', 'Jordan', 'Libya', 'Malta', 'Morocco', 'Pakistan', 
            'South Sudan', 'Sudan', 'Syria', 'Tunisia'
        ])
    elif acronym == 'PPPO':
        countries = ", ".join([
            'American Samoa', 'Australia', 'Cook Islands', 'Fiji', 'French Polynesia', 
            'Guam', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Caledonia', 
            'New Zealand', 'Niue', 'Northern Mariana Islands', 'Palau', 'Papua New Guinea', 
            'Pitcairn', 'Samoa', 'Solomon Islands', 'Tokelau', 'Tonga', 'Tuvalu', 'Vanuatu', 
            'Wallis and Futuna Islands'
        ])
    else:
        countries = np.nan
        print("Unknown acronym")

    return countries
