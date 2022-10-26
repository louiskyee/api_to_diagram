# %%
import os
import json
import numpy as np
from intervals import IntInterval
import cv2

def hex_to_rgb(hex):
    rgb = list()
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)
def get_x(count:int):
    for i, interval in enumerate(interval_list):
        if count in interval:
            return i

REPORT_DIR_PATH = "./report_dir/"
REPORT_PICTURE_DIR_PATH = "./report_diagram_dir/"
report_file_list = os.listdir(REPORT_DIR_PATH)

other_category = list()
for report in report_file_list:
    report_path = os.getcwd() + REPORT_DIR_PATH + report
    with open(report_path, encoding="utf-8") as file:
        category_dict = {
            "certificate": 0,
            "crypto": 0,
            "exception": 0,
            "file": 0,
            "iexplore": 0,
            "process": 0,
            "misc": 0,
            "netapi": 0,
            "network": 0,
            "office": 0,
            "ole": 0,
            "registry": 0,
            "resource": 0,
            "services": 0,
            "synchronisation": 0,
            "ui": 0
        }
        report_json = json.load(file)
        process_list = report_json["behavior"]["processes"]
        for process in process_list:
            for call in process["calls"]:  # get api call category
                if call is not None:
                    category = call["category"]
                    if category in category_dict:
                        category_dict[category] += 1
        #             elif category not in other_category:
        #                 other_category.append(category)
        # print(other_category)
        # print(json.dumps(category_dict, indent=4))

# %%
    interval_list = list()
    count_list = [-1, 0, 3, 7, 12, 18, 25, 33, 42, 100, 200, float("inf")]
    for i in range(len(count_list)-1):
        data_range = IntInterval.open_closed(count_list[i], count_list[i+1])  # open_closed → (,]
        interval_list.append(data_range)

    color_table_str = {
        "certificate":      ["FFFFFF", "FFC1E0", "FFAAD5", "FF95CA", "FF79BC", "FF60AF", "FF359A", "FF0080", "F00078", "D9006C", "BF0060"],
        "crypto":           ["FFFFFF", "FFBFFF", "FFA6FF", "FF8EFF", "FF77FF", "FF44FF", "FF00FF", "E800E8", "D200D2", "AE00AE", "930093"],
        "exception":        ["FFFFFF", "FFDAC8", "FFCBB3", "FFBD9D", "FFAD86", "FF9D6F", "FF8F59", "FF8040", "FF5809", "F75000", "D94600"],
        "file":             ["FFFFFF", "D3FF93", "CCFF80", "B7FF4A", "A8FF24", "9AFF02", "8CEA00", "82D900", "73BF00", "64A600", "548C00"],
        "iexplore":         ["FFFFFF", "CAFFFF", "BBFFFF", "A6FFFF", "4DFFFF", "00FFFF", "00E3E3", "00CACA", "00AEAE", "009393", "005757"],
        "process":          ["FFFFFF", "C1FFE4", "ADFEDC", "96FED1", "4EFEB3", "1AFD9C", "02F78E", "02DF82", "01B468", "019858", "01814A"],
        "misc":             ["FFFFFF", "D6D6AD", "CDCD9A", "C2C287", "B9B973", "AFAF61", "A5A552", "949449", "808040", "707038", "616130"],
        "netapi":           ["FFFFFF", "DCB5FF", "D3A4FF", "CA8EFF", "BE77FF", "B15BFF", "9F35FF", "921AFF", "8600FF", "6E00FF", "5B00AE"],
        "network":          ["FFFFFF", "FFFF6F", "FFFF37", "F9F900", "E1E100", "C4C400", "A6A600", "8C8C00", "737300", "5B5B00", "5B5B00"],
        "office":           ["FFFFFF", "FFE66F", "FFE153", "FFDC35", "FFD306", "EAC100", "D9B300", "C6A300", "AE8F00", "977C00", "796400"],
        "ole":              ["FFFFFF", "D8D8EB", "C7C7E2", "B8B8DC", "A6A6D2", "9999CC", "8080C0", "7373B9", "5A5AAD", "5151A2", "484891"],
        "registry":         ["FFFFFF", "97CBFF", "84C1FF", "66B3FF", "46A3FF", "2894FF", "0080FF", "0072E3", "0066CC", "005AB5", "004B97"],
        "resource":         ["FFFFFF", "B9B9FF", "AAAAFF", "9393FF", "7D7DFF", "6A6AFF", "4A4AFF", "2828FF", "0000E3", "0000C6", "0000C6"],
        "services":         ["FFFFFF", "FFD1A4", "FFC78E", "FFBB77", "FFAF60", "FFA042", "FF9224", "FF8000", "EA7500", "D26900", "BB5E00"],
        "synchronisation":  ["FFFFFF", "FF9797", "FF7575", "FF5151", "FF2D2D", "FF0000", "EA0000", "CE0000", "AE0000", "930000", "750000"],
        "ui":               ["FFFFFF", "93FF93", "79FF79", "53FF53", "28FF28", "00EC00", "00DB00", "00BB00", "00A600", "009100", "007500"]
    }

    color_table = dict()
    for key, value_list in color_table_str.items():
        color_table[key] = list()
        for value in value_list:
            color_table[key].append(hex_to_rgb(value))
    # print(json.dumps(color_table, indent=4))

    # %%

    category_list = [*category_dict]
    category_list.sort()    # make sure the order is consistent
    # print(category_list)

    row = 16
    col = 16
    img = np.zeros((row, col, 3), np.uint8)
    img.fill(255)
    for y, category in enumerate(category_list):
        x = get_x(category_dict[category])
        img[y, x] = color_table[category][x]

    # cv2.imshow('3 Channel Window', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print("image shape: ", img.shape)
    cv2.imwrite(REPORT_PICTURE_DIR_PATH + report.split('.')[0] + '.jpg', img)


