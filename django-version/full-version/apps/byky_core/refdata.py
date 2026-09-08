"""Reference lists shared by every module's dropdowns and filters."""

from apps.byky_core import seed
from apps.byky_cms import data as cms
from apps.byky_hrms import data as hrms
from apps.byky_ims import data as ims

# A standard nationality/demonym reference list -- not employee data (no
# employee's actual nationality is known, per CLAUDE.md 12), just the options
# a Nationality dropdown offers to choose from, the same category of reference
# list as countries_list below.
NATIONALITIES = [
    "Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan",
    "Argentine", "Armenian", "Australian", "Austrian", "Azerbaijani",
    "Bahamian", "Bahraini", "Bangladeshi", "Barbadian", "Belarusian",
    "Belgian", "Belizean", "Beninese", "Bhutanese", "Bolivian",
    "Bosnian", "Motswana", "Brazilian", "British", "Bruneian",
    "Bulgarian", "Burkinabe", "Burmese", "Burundian", "Cambodian",
    "Cameroonian", "Canadian", "Cape Verdean", "Central African", "Chadian",
    "Chilean", "Chinese", "Colombian", "Comoran", "Congolese",
    "Costa Rican", "Croatian", "Cuban", "Cypriot", "Czech",
    "Danish", "Djiboutian", "Dominican", "Dutch", "Timorese",
    "Ecuadorian", "Egyptian", "Emirati", "Salvadoran", "Equatorial Guinean",
    "Eritrean", "Estonian", "Ethiopian", "Fijian", "Filipino",
    "Finnish", "French", "Gabonese", "Gambian", "Georgian",
    "German", "Ghanaian", "Greek", "Grenadian", "Guatemalan",
    "Guinean", "Guyanese", "Haitian", "Honduran", "Hungarian",
    "Icelandic", "Indian", "Indonesian", "Iranian", "Iraqi",
    "Irish", "Israeli", "Italian", "Ivorian", "Jamaican",
    "Japanese", "Jordanian", "Kazakhstani", "Kenyan", "Kittitian",
    "Kuwaiti", "Kyrgyz", "Lao", "Latvian", "Lebanese",
    "Basotho", "Liberian", "Libyan", "Liechtensteiner", "Lithuanian",
    "Luxembourgish", "Macedonian", "Malagasy", "Malawian", "Malaysian",
    "Maldivian", "Malian", "Maltese", "Marshallese", "Mauritanian",
    "Mauritian", "Mexican", "Micronesian", "Moldovan", "Monacan",
    "Mongolian", "Montenegrin", "Moroccan", "Mozambican", "Namibian",
    "Nauruan", "Nepali", "New Zealander", "Nicaraguan", "Nigerien",
    "Nigerian", "North Korean", "Norwegian", "Omani", "Pakistani",
    "Palauan", "Palestinian", "Panamanian", "Papua New Guinean", "Paraguayan",
    "Peruvian", "Polish", "Portuguese", "Qatari", "Romanian",
    "Russian", "Rwandan", "Saudi", "Senegalese", "Serbian",
    "Seychellois", "Sierra Leonean", "Singaporean", "Slovak", "Slovenian",
    "Solomon Islander", "Somali", "South African", "South Korean", "South Sudanese",
    "Spanish", "Sri Lankan", "Sudanese", "Surinamese", "Swazi",
    "Swedish", "Swiss", "Syrian", "Taiwanese", "Tajik",
    "Tanzanian", "Thai", "Togolese", "Tongan", "Trinidadian",
    "Tunisian", "Turkish", "Turkmen", "Tuvaluan", "Ugandan",
    "Ukrainian", "Uruguayan", "Uzbek", "Vanuatuan", "Venezuelan",
    "Vietnamese", "Yemeni", "Zambian", "Zimbabwean",
]


def lists():
    return {
        "branches_list": cms.branches(),
        "states_list": cms.states(),
        "countries_list": cms.countries(),
        "categories_list": ims.categories(),
        "subcategories_list": ims.subcategories(),
        "designations_list": hrms.designations(),
        "employees_list": seed.EMPLOYEES,
        "stations_list": seed.STATIONS,
        "nationalities_list": NATIONALITIES,
    }
