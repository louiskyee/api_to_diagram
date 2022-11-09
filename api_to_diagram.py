# %%
from collections import Counter
import os
from tqdm import tqdm
import numpy as np
from intervals import IntInterval
from PIL import Image
import re
import ijson

REPORT_DIR_PATH = "./analyses/"
REPORT_PICTURE_DIR_PATH = "./report_diagram_dir/"
VIRUS_FAMILY_FILE_PATH = "./VirusShare3_Family.txt"
VIRUS_LIST_FILE_PATH = "./VirusShare3_list2.txt"

trigger = {
    "create_file": False,
    "color_table": True,
    "diagram": True
}

def get_color(count:int, interval_list):
    for i, interval in enumerate(interval_list):
        if count in interval:
            return i

def hex_to_rgb(hex):
    rgb = list()
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)

def get_time_range(timestamp_interval, _time):
    for i, time in enumerate(timestamp_interval):
        if _time <= time:
            return i
    return len(timestamp_interval)

def reset_category_dict():
    _dict = {
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
        "ui": 0,
        "system": 0
    }
    return _dict

with open(VIRUS_FAMILY_FILE_PATH, encoding="utf-8") as file:
    virus_family = file.readlines()
    virus_family_dict = dict()
    for virus in virus_family:
        virus_list = virus.split()
        if len(virus_list) >= 3 and len(re.findall('FAM:', virus_list[2])) == 1:
            family =  virus_list[2]
            family = family[family.index("FAM:")+4:family.index("|", family.index("FAM:"))]
            virus_family_dict["VirusShare_"+virus_list[0]] = family
virus_family_cnt = Counter(virus_family_dict.values())
number = 16
virus_list = list(word for word, word_count in virus_family_cnt.most_common(number))
virus_dict = dict.fromkeys(virus_list, 0)

for family in virus_list:
    if not os.path.exists(os.getcwd()+REPORT_DIR_PATH[1:]+family):
        os.makedirs(os.getcwd()+REPORT_DIR_PATH[1:]+family)
    if not os.path.exists(os.getcwd()+REPORT_PICTURE_DIR_PATH[1:]+family):
        os.makedirs(os.getcwd()+REPORT_PICTURE_DIR_PATH[1:]+family)

if trigger["create_file"]:
    with open(VIRUS_LIST_FILE_PATH, encoding="utf-8", mode='w') as file:
        for virus, family in virus_family_dict.items():
            if family in virus_dict and virus_dict[family] < 100:
                file.write(f"{virus} {family}\n")
                virus_dict[family] += 1
else:
    with open(VIRUS_LIST_FILE_PATH, encoding="utf-8") as file:
        virus_file_list = file.read().split()
# %%
if trigger["color_table"]:
    interval_list = list()

    # count_list = [-1, 0, 3, 7, 12, 18, 25, 33, 42, 52, 63, 75, 88, 102, 117, 133, 200, float("inf")]
    count_list = [-1, 0, 3, 7, 12, 18, 25, 33, 42, 100, 200, float("inf")]
    for i in range(len(count_list)-1):
        data_range = IntInterval.open_closed(count_list[i], count_list[i+1])  # open_closed → (,]
        interval_list.append(data_range)

    # color_table_str = {
    #     "certificate":      ["FFFFFF", "FFF7FB", "FFECF5", "FFD9EC", "FFC1E0", "FFAAD5", "FF95CA", "FF79BC", "FF60AF", "FF359A", "FF0080", "F00078", "D9006C", "BF0060", "9F0050", "820041", "600030"],
    #     "crypto":           ["FFFFFF", "FFF7FF", "FFE6FF", "FFD0FF", "FFBFFF", "FFA6FF", "FF8EFF", "FF77FF", "FF44FF", "FF00FF", "E800E8", "D200D2", "AE00AE", "930093", "750075", "5E005E", "460046"],
    #     "exception":        ["FFFFFF", "FFF3EE", "FFE6D9", "FFDAC8", "FFCBB3", "FFBD9D", "FFAD86", "FF9D6F", "FF8F59", "FF8040", "FF5809", "F75000", "D94600", "BB3D00", "A23400", "842B00", "642100"],
    #     "file":             ["FFFFFF", "F5FFE8", "EFFFD7", "E8FFC4", "DEFFAC", "D3FF93", "CCFF80", "C2FF68", "B7FF4A", "A8FF24", "9AFF02", "8CEA00", "82D900", "73BF00", "64A600", "548C00", "467500"],
    #     "iexplore":         ["FFFFFF", "FDFFFF", "ECFFFF", "D9FFFF", "CAFFFF", "BBFFFF", "A6FFFF", "80FFFF", "4DFFFF", "00FFFF", "00E3E3", "00CACA", "00AEAE", "009393", "007979", "005757", "006000"],
    #     "process":          ["FFFFFF", "FBFFFD", "E8FFF5", "D7FFEE", "C1FFE4", "ADFEDC", "96FED1", "7AFEC6", "4EFEB3", "1AFD9C", "02F78E", "02DF82", "02C874", "01B468", "019858", "01814A", "006030"],
    #     "misc":             ["FFFFFF", "E8E8D0", "DEDEBE", "D6D6AD", "CDCD9A", "C2C287", "B9B973", "AFAF61", "A5A552", "949449", "808040", "707038", "616130", "D4CF6E", "B3AD17", "918C00", "787200"],
    #     "netapi":           ["FFFFFF", "FAF4FF", "F1E1FF", "E6CAFF", "DCB5FF", "D3A4FF", "CA8EFF", "BE77FF", "B15BFF", "9F35FF", "921AFF", "8600FF", "6F00D2", "5B00AE", "4B0091", "3A006F", "28004D"],
    #     "network":          ["FFFFFF", "FFFFF4", "FFFFDF", "FFFFCE", "FFFFB9", "FFFFAA", "FFFF93", "FFFF6F", "FFFF37", "F9F900", "E1E100", "C4C400", "A6A600", "8C8C00", "737300", "5B5B00", "424200"],
    #     "office":           ["FFFFFF", "FFFCEC", "FFF8D7", "FFF4C1", "FFF0AC", "FFED97", "FFE66F", "FFE153", "FFDC35", "FFD306", "EAC100", "D9B300", "C6A300", "AE8F00", "977C00", "796400", "5B4B00"],
    #     "ole":              ["FFFFFF", "F3F3FA", "E6E6F2", "D8D8EB", "C7C7E2", "B8B8DC", "A6A6D2", "9999CC", "8080C0", "7373B9", "5A5AAD", "5151A2", "484891", "919EFF", "5357CF", "4E4373", "270020"],
    #     "registry":         ["FFFFFF", "ECF5FF", "D2E9FF", "C4E1FF", "ACD6FF", "97CBFF", "84C1FF", "66B3FF", "46A3FF", "2894FF", "0080FF", "0072E3", "0066CC", "005AB5", "004B97", "003D79", "003060"],
    #     "resource":         ["FFFFFF", "FBFBFF", "ECECFF", "DDDDFF", "CECEFF", "B9B9FF", "AAAAFF", "9393FF", "7D7DFF", "6A6AFF", "4A4AFF", "2828FF", "0000E3", "0000C6", "0000C6", "000093", "000079"],
    #     "services":         ["FFFFFF", "FFFAF4", "FFEEDD", "FFE4CA", "FFDCB9", "FFD1A4", "FFC78E", "FFBB77", "FFAF60", "FFA042", "FF9224", "FF8000", "EA7500", "D26900", "BB5E00", "9F5000", "844200"],
    #     "synchronisation":  ["FFFFFF", "FFECEC", "FFD2D2", "FFB5B5", "FF9797", "FF7575", "FF5151", "FF2D2D", "FF0000", "EA0000", "CE0000", "AE0000", "930000", "750000", "600000", "4D0000", "2F0000"],
    #     "ui":               ["FFFFFF", "F0FFF0", "DFFFDF", "CEFFCE", "BBFFBB", "A6FFA6", "93FF93", "79FF79", "53FF53", "28FF28", "00EC00", "00DB00", "00BB00", "00A600", "009100", "007500", "006000"],
    #     "system":           ["FFFFFF", "D1E9E9", "C4E1E1", "B3D9D9", "A3D1D1", "95CACA", "81C0C0", "6FB7B7", "5CADAD", "4F9D9D", "408080", "3D7878", "336666", "38B8FF", "00A5B8", "007A99", "1C778C"]
    # }
    color_table_str = {
        "certificate":      ["FFFFFF", "FFD9EC", "FFC1E0", "FFAAD5", "FF95CA", "FF79BC", "FF60AF", "FF359A", "FF0080", "F00078", "D9006C"],
        "crypto":           ["FFFFFF", "FFD0FF", "FFBFFF", "FFA6FF", "FF8EFF", "FF77FF", "FF44FF", "FF00FF", "E800E8", "D200D2", "AE00AE"],
        "exception":        ["FFFFFF", "FFDAC8", "FFCBB3", "FFBD9D", "FFAD86", "FF9D6F", "FF8F59", "FF8040", "FF5809", "F75000", "D94600"],
        "file":             ["FFFFFF", "E8FFC4", "DEFFAC", "D3FF93", "CCFF80", "C2FF68", "B7FF4A", "A8FF24", "9AFF02", "8CEA00", "82D900"],
        "iexplore":         ["FFFFFF", "D9FFFF", "CAFFFF", "BBFFFF", "A6FFFF", "80FFFF", "4DFFFF", "00FFFF", "00E3E3", "00CACA", "00AEAE"],
        "process":          ["FFFFFF", "D7FFEE", "C1FFE4", "ADFEDC", "96FED1", "7AFEC6", "4EFEB3", "1AFD9C", "02F78E", "02DF82", "02C874"],
        "misc":             ["FFFFFF", "D6D6AD", "CDCD9A", "C2C287", "B9B973", "AFAF61", "A5A552", "949449", "808040", "707038", "616130"],
        "netapi":           ["FFFFFF", "E6CAFF", "DCB5FF", "D3A4FF", "CA8EFF", "BE77FF", "B15BFF", "9F35FF", "921AFF", "8600FF", "6F00D2"],
        "network":          ["FFFFFF", "FFFFCE", "FFFFB9", "FFFFAA", "FFFF93", "FFFF6F", "FFFF37", "F9F900", "E1E100", "C4C400", "A6A600"],
        "office":           ["FFFFFF", "FFF4C1", "FFF0AC", "FFED97", "FFE66F", "FFE153", "FFDC35", "FFD306", "EAC100", "D9B300", "C6A300"],
        "ole":              ["FFFFFF", "D8D8EB", "C7C7E2", "B8B8DC", "A6A6D2", "9999CC", "8080C0", "7373B9", "5A5AAD", "5151A2", "484891"],
        "registry":         ["FFFFFF", "C4E1FF", "ACD6FF", "97CBFF", "84C1FF", "66B3FF", "46A3FF", "2894FF", "0080FF", "0072E3", "0066CC"],
        "resource":         ["FFFFFF", "DDDDFF", "CECEFF", "B9B9FF", "AAAAFF", "9393FF", "7D7DFF", "6A6AFF", "4A4AFF", "2828FF", "0000E3"],
        "services":         ["FFFFFF", "FFE4CA", "FFDCB9", "FFD1A4", "FFC78E", "FFBB77", "FFAF60", "FFA042", "FF9224", "FF8000", "EA7500"],
        "synchronisation":  ["FFFFFF", "FFB5B5", "FF9797", "FF7575", "FF5151", "FF2D2D", "FF0000", "EA0000", "CE0000", "AE0000", "930000"],
        "ui":               ["FFFFFF", "CEFFCE", "BBFFBB", "A6FFA6", "93FF93", "79FF79", "53FF53", "28FF28", "00EC00", "00DB00", "00BB00"],
        "system":           ["FFFFFF", "B3D9D9", "A3D1D1", "95CACA", "81C0C0", "6FB7B7", "5CADAD", "4F9D9D", "408080", "3D7878", "336666"]
    }

    color_table = dict()
    for key, value_list in color_table_str.items():
        color_table[key] = list()
        for value in value_list:
            color_table[key].append(hex_to_rgb(value))
    # print(json.dumps(color_table, indent=4))

# %%
if trigger["diagram"]:
    virus_category_dirs = os.listdir(REPORT_DIR_PATH)

    # other_category = list()
    all_category_dict = dict()
    time_frequency_setting = 17
    lower_bound = 300
    for virus_category_dir in virus_category_dirs:
        report_file_list = os.listdir(os.getcwd() + REPORT_DIR_PATH[1:] + virus_category_dir)
        for report in tqdm(report_file_list):
            report_path = os.getcwd() + REPORT_DIR_PATH[1:] + virus_category_dir + '/' + report
            # print(report_path)
            with open(report_path, encoding="utf-8", errors='ignore') as file:
                category_dict = reset_category_dict()
                report_json = ijson.items(file, 'behavior.processes.item')
                try:
                    process_list = [processes for processes in report_json]
                except Exception as e:
                    pass
                if process_list:
                    timestamp_list = list()
                    for process in process_list:
                        for call in process["calls"]:  # get api call time
                            if call is not None:
                                timestamp_list.append(float(call["time"]))
                    if timestamp_list and len(timestamp_list) > lower_bound:
                        timestamp_list.sort()
                        frequency = (timestamp_list[-1] - timestamp_list[0])/time_frequency_setting
                        if frequency:
                            timestamp_interval = [float('%.5f'%(time+0.00005)) for time in np.arange(timestamp_list[0]+frequency, timestamp_list[-1], frequency)]
                        else:
                            timestamp_interval = [timestamp_list[0] for i in range(time_frequency_setting)]
                        # if len(timestamp_interval) < time_frequency_setting-1:
                        #     timestamp_interval.append(timestamp_list[-1]+frequency)
                        category_dict_of_time = [reset_category_dict() for i in range(time_frequency_setting)]
                        for process in process_list:
                            for call in process["calls"]:  # get api call category
                                if call is not None:
                                    category = call["category"]
                                    # print(datetime.datetime.fromtimestamp(call["time"]))
                                    category_dict_index = get_time_range(timestamp_interval, float(str(call["time"])[:str(call["time"]).find('.')+5]))
                                    if category in category_dict_of_time[category_dict_index]:
                                        category_dict_of_time[category_dict_index][category] += 1

                        row = 17
                        col = 17
                        img = np.zeros((row, col, 3), np.uint8)
                        img.fill(255)
                        for x, category_dict in enumerate(category_dict_of_time):
                            category_list = [*category_dict]
                            category_list.sort()    # make sure the order is consistent
                            for y, category in enumerate(category_list):
                                count = get_color(category_dict[category], interval_list)
                                img[y, x] = color_table[category][count]
                        report_name = report.split('.')[0]
                        img = Image.fromarray(img)
                        img.save(REPORT_PICTURE_DIR_PATH + virus_category_dir + '/' + report_name + '.png')
                        # cv2.imwrite(REPORT_PICTURE_DIR_PATH + virus_category_dir + '/' + report_name + '.png', img)