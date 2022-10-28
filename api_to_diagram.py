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
    count_list = [-1, 0, 3, 7, 12, 18, 25, 33, 42, 52, 63, 75, 88, 102, 117, 133, 200, float("inf")]
    for i in range(len(count_list)-1):
        data_range = IntInterval.open_closed(count_list[i], count_list[i+1])  # open_closed → (,]
        interval_list.append(data_range)

    color_table_str = {
        "certificate":      ["FFFFFF", "FFF7FB", "FFECF5", "FFD9EC", "FFC1E0", "FFAAD5", "FF95CA", "FF79BC", "FF60AF", "FF359A", "FF0080", "F00078", "D9006C", "BF0060", "9F0050", "820041", "600030"],
        "crypto":           ["FFFFFF", "FFF7FF", "FFE6FF", "FFD0FF", "FFBFFF", "FFA6FF", "FF8EFF", "FF77FF", "FF44FF", "FF00FF", "E800E8", "D200D2", "AE00AE", "930093", "750075", "5E005E", "460046"],
        "exception":        ["FFFFFF", "FFF3EE", "FFE6D9", "FFDAC8", "FFCBB3", "FFBD9D", "FFAD86", "FF9D6F", "FF8F59", "FF8040", "FF5809", "F75000", "D94600", "BB3D00", "A23400", "842B00", "642100"],
        "file":             ["FFFFFF", "F5FFE8", "EFFFD7", "E8FFC4", "DEFFAC", "D3FF93", "CCFF80", "C2FF68", "B7FF4A", "A8FF24", "9AFF02", "8CEA00", "82D900", "73BF00", "64A600", "548C00", "467500"],
        "iexplore":         ["FFFFFF", "FDFFFF", "ECFFFF", "D9FFFF", "CAFFFF", "BBFFFF", "A6FFFF", "80FFFF", "4DFFFF", "00FFFF", "00E3E3", "00CACA", "00AEAE", "009393", "007979", "005757", "006000"],
        "process":          ["FFFFFF", "FBFFFD", "E8FFF5", "D7FFEE", "C1FFE4", "ADFEDC", "96FED1", "7AFEC6", "4EFEB3", "1AFD9C", "02F78E", "02DF82", "02C874", "01B468", "019858", "01814A", "006030"],
        "misc":             ["FFFFFF", "E8E8D0", "DEDEBE", "D6D6AD", "CDCD9A", "C2C287", "B9B973", "AFAF61", "A5A552", "949449", "808040", "707038", "616130", "D4CF6E", "B3AD17", "918C00", "787200"],
        "netapi":           ["FFFFFF", "FAF4FF", "F1E1FF", "E6CAFF", "DCB5FF", "D3A4FF", "CA8EFF", "BE77FF", "B15BFF", "9F35FF", "921AFF", "8600FF", "6F00D2", "5B00AE", "4B0091", "3A006F", "28004D"],
        "network":          ["FFFFFF", "FFFFF4", "FFFFDF", "FFFFCE", "FFFFB9", "FFFFAA", "FFFF93", "FFFF6F", "FFFF37", "F9F900", "E1E100", "C4C400", "A6A600", "8C8C00", "737300", "5B5B00", "424200"],
        "office":           ["FFFFFF", "FFFCEC", "FFF8D7", "FFF4C1", "FFF0AC", "FFED97", "FFE66F", "FFE153", "FFDC35", "FFD306", "EAC100", "D9B300", "C6A300", "AE8F00", "977C00", "796400", "5B4B00"],
        "ole":              ["FFFFFF", "F3F3FA", "E6E6F2", "D8D8EB", "C7C7E2", "B8B8DC", "A6A6D2", "9999CC", "8080C0", "7373B9", "5A5AAD", "5151A2", "484891", "919EFF", "5357CF", "4E4373", "270020"],
        "registry":         ["FFFFFF", "ECF5FF", "D2E9FF", "C4E1FF", "ACD6FF", "97CBFF", "84C1FF", "66B3FF", "46A3FF", "2894FF", "0080FF", "0072E3", "0066CC", "005AB5", "004B97", "003D79", "003060"],
        "resource":         ["FFFFFF", "FBFBFF", "ECECFF", "DDDDFF", "CECEFF", "B9B9FF", "AAAAFF", "9393FF", "7D7DFF", "6A6AFF", "4A4AFF", "2828FF", "0000E3", "0000C6", "0000C6", "000093", "000079"],
        "services":         ["FFFFFF", "FFFAF4", "FFEEDD", "FFE4CA", "FFDCB9", "FFD1A4", "FFC78E", "FFBB77", "FFAF60", "FFA042", "FF9224", "FF8000", "EA7500", "D26900", "BB5E00", "9F5000", "844200"],
        "synchronisation":  ["FFFFFF", "FFECEC", "FFD2D2", "FFB5B5", "FF9797", "FF7575", "FF5151", "FF2D2D", "FF0000", "EA0000", "CE0000", "AE0000", "930000", "750000", "600000", "4D0000", "2F0000"],
        "ui":               ["FFFFFF", "F0FFF0", "DFFFDF", "CEFFCE", "BBFFBB", "A6FFA6", "93FF93", "79FF79", "53FF53", "28FF28", "00EC00", "00DB00", "00BB00", "00A600", "009100", "007500", "006000"],
        "system":           ["FFFFFF", "D1E9E9", "C4E1E1", "B3D9D9", "A3D1D1", "95CACA", "81C0C0", "6FB7B7", "5CADAD", "4F9D9D", "408080", "3D7878", "336666", "38B8FF", "00A5B8", "007A99", "1C778C"]
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

    row = 17
    col = 17
    img = np.zeros((row, col, 3), np.uint8)
    img.fill(255)
    for y, category in enumerate(category_list):
        x = get_x(category_dict[category])
        for _x in range(x):
            img[y, _x] = color_table[category][_x]

    # cv2.imshow('3 Channel Window', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print("image shape: ", img.shape)
    cv2.imwrite(REPORT_PICTURE_DIR_PATH + report.split('.')[0] + '.jpg', img)


