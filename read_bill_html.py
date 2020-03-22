import os.path as op
import six
import codecs
from bs4 import BeautifulSoup
import pandas as pd

file_path = op.expanduser("~/Downloads/My bill.htm")
f = codecs.open(file_path, 'r')

bill = BeautifulSoup(f.read(), 'html.parser')
person_results = bill.find_all("div", attrs={"class":"row visible-phone"})

bill_items = []

# 2 for starting from shared fees
for result in person_results[2:]:
    name = result.find("span", attrs={"class": "font-14"}).text

    phone = result.find("span",
                        attrs={"class": ["span8 pull-left col1BlockBV",
                                         "span8 pull-left col1Block"]}).text
    phone_cleaned = phone[:-len(name)]
    amount = result.find(
                # sometimes it is col2BlockBV
                "span", attrs={"class": "span2 pull-right col2Block"}
             ).text
    amount = float(amount[1:])
    record_dict = {'phone':phone_cleaned, 'name':name, 'amount':amount}
    bill_items.append(record_dict)

bill_df = pd.DataFrame(bill_items)

alert = bill.find_all("i", attrs={"class": "icon-alert ng-scope",
                                  "ng-if": "usageDet.showAlert"})
if len(alert) == 0:
    data_overaged = False
elif len(alert) == 1:
    data_overaged = True
else:
    raise ValueError("Two alerts detected. 1st might be data overage. 2nd "
                     "alert is unkown.")

if data_overaged:
    bill_details = bill.find_all("span", attrs={"class":"ng-binding"})
    for num, detail in enumerate(bill_details):
        if detail.contents:
            if isinstance(detail.contents[0], six.string_types):
                if detail.contents[0].startswith("Overage"):
                    overage_msg = detail.contents[0]
                    overage_amount = bill_details[num + 1].contents[0]
                    break

if not data_overaged:
    shared_amount = bill_df.loc[0, 'amount']
    averaged_shared = round(shared_amount / (len(bill_df) - 1), 2)
    bill_df['total'] = bill_df['amount'] + averaged_shared

export = bill_df[['name', 'total']]
export = export.drop(0, axis=0)
export.to_csv("result.csv", index=False)
