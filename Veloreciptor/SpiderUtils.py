import re


def add_space_before_unit(ingredient):
    return re.sub(r'([0-9/\-,]+)([A-Za-zĄąĆćĘęŃńŚśŻżŹźÓóŁł]+)', r'\1 \2', ingredient)
