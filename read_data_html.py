import six
import os.path as op
import codecs
from bs4 import BeautifulSoup
import pandas as pd

file_path = op.expanduser("~/Downloads/wirelessUsage.html")
#file_path2 = op.expanduser("~/Downloads/wirelessUsage2.html")

usage_results = []
for file in [file_path, ]:
    f = codecs.open(file, 'r')
    bill = BeautifulSoup(f.read(), 'html.parser')
    usage_results.extend(bill.find_all(
        "div",
        attrs={"ng-repeat": "ctnData in tableData"}
    ))

person_example = usage_results[-1]

person_name = person_example.find(
    "div", attrs={"class": "CTNTruncate dataUserName ng-binding"}
)
person_amount = person_example.find(
    "strong", attrs={"class": "ng-binding"}
)

bill_items = []

for result in usage_results[:]:
    name = result.find(
        "div",
        attrs={"class": "CTNTruncate dataUserName ng-binding"}
    ).text

    data = result.find(
        "strong", attrs={"class": "ng-binding"}
    ).text

    record_dict = {'name': name, 'data': data}

    bill_items.append(record_dict)

bill_df = pd.DataFrame(bill_items)
#
#alert = bill.find_all("i", attrs={"class": "icon-alert ng-scope",
#                                  "ng-if": "usageDet.showAlert"})
#
#if len(alert) == 0:
#    data_overaged = False
#elif len(alert) == 1:
#    data_overaged = True
#else:
#    raise ValueError("Two alerts detected. 1st might be data overage. 2nd "
#                     "alert is unkown.")
#
#if data_overaged:
#    bill_details = bill.find_all("span", attrs={"class":"ng-binding"})
#    for num, detail in enumerate(bill_details):
#        if detail.contents:
#            if isinstance(detail.contents[0], six.string_types):
#                if detail.contents[0].startswith("Overage"):
#                    overage_msg = detail.contents[0]
#                    overage_amount = bill_details[num + 1].contents[0]
#                    break
