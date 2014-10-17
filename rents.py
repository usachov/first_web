# -*- coding: utf-8 -*-
__author__ = 'Evgeny'
from lxml import html
import csv
import re


def write_to_csv(data):
    """
    write data to file
    in csv format
    """
    with open("/home/death/PycharmProjects/cityscale/rent.csv", "w") as csv_file:
        for row in data:
            writer = csv.writer(csv_file, delimiter=";", quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(row)
        csv_file.write(url)



def to_s(obj):
    """
    lxml element to string
    """
    return html.tostring(obj, method='text', encoding='unicode', pretty_print=True)


def get_name(name):
    """
    get organization name from string
    """
    s = to_s(name)
    if s.find('.', 5) == -1:
        return s[5:]
    else:
        return s[7:].replace('.', '').replace(' ', '', 1).replace('\xa0','')


def from_list(my_list):
    """
    get elements from list of elements
    and remove the excess
    return clean list for export
    """
    list_1 = []
    list_2 = []
    regex = '[А-ЯІЇЄҐа-яіїєґ0-9%]'
    for el in my_list.iterchildren():
        list_1.append(el.getchildren()[1:])
    for i in list_1[2:]:
        s = ""
        for j in i:
            if re.search(regex, to_s(j)):
                s += to_s(j)
            else:
                s += " 0"
        list_2.append(s.replace(",", ".").replace("  ", " "))
    return list_2


url = "http://www.gorsovet.mk.ua/services/flat.ua"
page = html.parse(url)
all_elements = page.getroot().find_class('top_list').pop()
data_elements = all_elements.xpath('.//table[@class="st"]')
name_elements = all_elements.xpath('.//h1')

name_range = [i for i in range(3, 10)] + [i for i in range(12, 36)]
data_rage = [i for i in range(1, 8)] + [i for i in range(10, 34)]

all_rents = []
for el in range(len(name_range)):
    rent = []
    rent.append(get_name(name_elements[name_range[el]]))
    for i in from_list(data_elements[data_rage[el]]):
        rent.append(i)
    all_rents.append(rent)

write_to_csv(all_rents)

