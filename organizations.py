# -*- coding: utf-8 -*-
__author__ = 'Evgeny'
from lxml import html
import csv
import re


class MkHouseOrg(object):

    def __init__(self):
        self.sub_name = None
        self.main_name = None
        self.address = None
        self.phone = None
        self.boss_name = None
        self.service_area = None

    def to_string(self, s):
        return html.tostring(s, method='text', encoding='unicode')

    def try_get(self, s):
        try:
            return self.to_string(s[1][0])
        except IndexError:
            return self.to_string(s[0][0])

    def get_sub_name(self, name):
        sub_name_regex = "(Д|Ж|д)[А-ЯІЇЄҐа-яіїєґ]+\s?-?№?\s?\d+(\s\(ЖЕК-\d\))?"
        try:
            self.sub_name = re.search(sub_name_regex, self.to_string(name)).group()
        except AttributeError:
            self.sub_name = self.try_get(name)

    def get_main_name(self, name):
        self.main_name = self.try_get(name)

    def get_address(self, address):
        address_regex = '(вул.|пр\.)\s?[.А-ЯІЇЄҐа-яіїєґ]+,?\s?\d*-?[а-яіїєґ]?'
        try:
            self.address = re.search(address_regex, self.to_string(address)).group()
        except AttributeError:
            self.address = "None"

    def get_phone(self, phone):
        phone_regex = "(\d+[-]\d+[-]\d+)"
        self.phone = ",".join(re.findall(phone_regex, self.to_string(phone)))

    def get_boss_name(self, boss_name):
        boss_regex = "[А-ЯІЇЄҐ][а-яіїєґ]+\s[А-ЯІЇЄҐ][а-яіїєґ]+\s[А-ЯІЇЄҐ][а-яіїєґ]+"
        self.boss_name = re.search(boss_regex, self.to_string(boss_name)).group()

    def get_service_area(self, address_list):
        self.service_area = ";".join([self.to_string(j) for j in address_list])

    def retrieve_elements(self):
        return "(%s, %s, %s, %s, %s, %s)" % (self.sub_name, self.main_name,
                                             self.address, self.phone,
                                             self.boss_name, self.service_area)


def write_to_csv(data):
    with open("/home/death/PycharmProjects/cityscale/orgs.csv", "w") as csv_file:
        for row in data:
            writer = csv.writer(csv_file, delimiter=";", quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow([row.sub_name, row.main_name, row.address,
                             row.phone, row.boss_name, row.service_area])
        csv_file.write(url)

url = "http://www.gorsovet.mk.ua/services/zhek.ua"
page = html.parse(url)
all_elements = page.getroot().find_class('top_list').pop()
main_elements = all_elements.xpath('.//table[@class="st"]')
sub_elements = all_elements.xpath('.//b')
area_elements = all_elements.xpath('.//ul')

mk_house_org_list = []

for i in range(len(area_elements)-1):   # -1 last area without organization
    obj = MkHouseOrg()
    obj.get_service_area(area_elements[i])
    mk_house_org_list.append(obj)

obj = MkHouseOrg()
obj.get_service_area(area_elements[31])
mk_house_org_list[30].service_area += obj.service_area

main_rel = [3, 3, 4, 5, 6, 6, 6, 7, 8, 9, 9,
            10, 11, 12, 12, 12, 12, 13, 13,
            13, 13, 13, 13, 13, 13, 14, 15,
            16, 17, 18, 19]

sub_rel_sub = [0, 1, 4, 5, 6, 9, 10] + [i for i in range(12, 25)]
sub_rel_main = [2, 3, 7, 8, 11] + [i for i in range(25, 31)]
sub_rel_main2 = [4, 5, 7, 8, 10] + [i for i in range(14, 20)]

for i in range(len(mk_house_org_list)):
    mk_house_org_list[i].get_main_name(main_elements[main_rel[i]])

for i in range(20):
    mk_house_org_list[sub_rel_sub[i]].get_sub_name(sub_elements[i+2])
    mk_house_org_list[sub_rel_sub[i]].get_phone(sub_elements[i+2])
    mk_house_org_list[sub_rel_sub[i]].get_boss_name(sub_elements[i+2])
    mk_house_org_list[sub_rel_sub[i]].get_address(sub_elements[i+2])

for i, j in zip(sub_rel_main, sub_rel_main2):
    mk_house_org_list[i].get_sub_name(main_elements[j])
    mk_house_org_list[i].get_phone(main_elements[j])
    mk_house_org_list[i].get_boss_name(main_elements[j])
    mk_house_org_list[i].get_address(main_elements[j])

write_to_csv(mk_house_org_list)

