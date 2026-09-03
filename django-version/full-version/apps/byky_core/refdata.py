"""Reference lists shared by every module's dropdowns and filters."""

from apps.byky_core import seed
from apps.byky_cms import data as cms
from apps.byky_hrms import data as hrms
from apps.byky_ims import data as ims


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
    }
