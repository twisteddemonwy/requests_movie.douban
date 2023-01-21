import csv
import os
from selenium.webdriver.common.by import By
from typing import Tuple


class Bot:
    # Selenium: get element attributes
    def _get_attrs(self, elements, attr):
        if type(elements) == list:
            attrs = [element.get_attribute(attr) for element in elements]
            return attrs
        else:
            attrs = elements.get_attribute(attr)
            return attrs

    # Selenium: get the element or get the attribute of the element
    def operational_elements(self, driver, locator: str, index: Tuple[bool, int], attr: Tuple[bool, str]):
        """
        locator: Element locators
        index: The elements we get are stored in the list by default.
               We can pass in [Ture, <index>] for index to get the only element we want.
               Or pass in [False, 0] for index to directly return the elements list.
        attr: Sometimes what we want to get is the attribute of the element.
              We can pass in [Ture, <attribute name>] for attr to get the attribute.
              Or pass in [False, ""] for index to directly return the elements list.

        pay attention to: The index parameter has higher priority than attr parameter.
                          This means that when we set index and attr to True at the same time, an attribute will be returned.
                          When index is False and attr is True, a list of attributes will be returned.
        """
        try:
            elements = driver.find_elements(by=By.CSS_SELECTOR, value=locator)
        except IndexError:
            print("## 未找到期望元素")
            return None

        if not index[0]:
            if not attr[0]:
                return elements
            attrs = self._get_attrs(elements, attr[1])
            return attrs

        element = elements[index[1]]
        if not attr[0]:
            return element
        attrs = self._get_attrs(element, attr[1])
        return attrs

    # Save the data to the specified csv file
    def save_data_to_csv(self, path: str, fieldnames: list, data: dict):
        with open(path, 'a') as f:
            csvw = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
            if not os.path.getsize(path):
                csvw.writeheader()
            csvw.writerows([data])
