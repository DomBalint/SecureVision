"""Dataloader and dataset statistics for the SIXRay dataset, currently parses all the xml files in the selected
folder and creates a quick statistic, just to check if annotations are correct"""

import os
import os.path
import xml.etree.ElementTree as ET
from collections import Counter
from typing import List, Dict


def get_xml_data_recursive(element, counter) -> Dict:
    """
    Parses the xml file from the root
    :param counter: count the objects
    :param element: root of the xml
    :return: dictionary of the parsed xml
    """
    # To count each elements in annotations and not to overwrite the keys
    key = str(element.tag)
    if key == 'object':
        key = key + str(counter)

    rec_dict = {key: None}
    # only end-of-line elements have important text, at least in this example
    if len(element) == 0:
        if element.text is not None:
            rec_dict[element.tag] = element.text
    # otherwise, go deeper and add to the current tag
    else:
        rec_dict[key] = {}
        for el in element:
            if el.tag == 'object':
                counter += 1
            within = get_xml_data_recursive(el, counter)
            for i, (k, v) in enumerate(within.items()):
                rec_dict[key].update({k: v})

    return rec_dict


def extract(obj: List, arr: List, key: str) -> None:
    """Recursively search for values of key in nested dict.
    :param obj: the list to search
    :param arr: fills up the array with the values
    :param key: search a specific key and grab all values
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                arr.append(v)

            if isinstance(v, (dict, list)):
                extract(v, arr, key)

    elif isinstance(obj, list):
        for item in obj:
            extract(item, arr, key)


def parse_annotations(annotation_folder: str) -> List[Dict]:
    """
    Creates a list from the parsed annotations, could be expanded to create a pandas df and write to .csv
    :param annotation_folder: path to the SIXRay annotations
    :return: a list from the parsed annotations
    """
    files_all = os.listdir(annotation_folder)
    all_annotations = []

    for xml_file in files_all:
        root = ET.parse(os.path.join(annotation_folder, xml_file)).getroot()
        counter = 0
        parsed_dict = get_xml_data_recursive(root, counter)
        # Drop unnecessary data like folder, source, owner
        parsed_dict['annotation'].pop('folder')
        parsed_dict['annotation'].pop('owner')
        parsed_dict['annotation'].pop('source')
        all_annotations.append(parsed_dict)
    return all_annotations


def statistics(list_all_annotations):
    """
    Creates a quick statistic of the annotations folder, see the searched keys in the stat list
    :param list_all_annotations: a List of all the annotations
    """
    stat_list = ['segmented', 'name', 'pose', 'truncated', 'difficult']
    for key_stat in stat_list:
        types = []
        extract(list_all_annotations, types, key_stat)
        key_stat_values = list(Counter(types).keys())
        key_stat_values_count = list(Counter(types).values())
        print(f'{key_stat} has values: {key_stat_values}, counting: {key_stat_values_count}')


root_path = 'path/to/SIXRay/dataset/Annotations_Folder/containing_htmls'
all_annotations = parse_annotations(root_path)
statistics(all_annotations)
