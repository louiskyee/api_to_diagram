import os
import json
import shutil

VIRUS_FAMILY_PATH = r"/home/user/Documents/virus/VirusShare3_list2.txt"
REPORT_DIR_PATH = r"/home/user/.cuckoo/storage/analyses/"
SAVE_DIR_PATH = r"/home/user/Documents/virus/analyses/"

def makdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_virus_family(file_name):
    with open(file_name, encoding="utf-8") as f:
        virus_dict = dict()
        virus_list = f.readlines()
        for virus_info in virus_list:
            name, family = virus_info.split()
            virus_dict[name] = family
    return virus_dict


if __name__ == "__main__":
    if not os.path.exists(REPORT_DIR_PATH):
        os.makedirs(SAVE_DIR_PATH)
    virus_dict = load_virus_family(VIRUS_FAMILY_PATH)
    report_dir_list = os.listdir(REPORT_DIR_PATH)
    for report_dir_name in report_dir_list:
        report_file_path = REPORT_DIR_PATH + report_dir_name + "/"
        print(report_file_path)
        task_file = report_file_path + "task.json"
        old_virus_report = report_file_path + "reports/report.json"
        with open(task_file, encoding="utf-8") as f:
            file_json = json.load(f)
            virus_file_path = file_json["target"]
            virus_file_name = virus_file_path[virus_file_path.index("VirusShare_"):]
            makdir(SAVE_DIR_PATH + virus_dict[virus_file_name])
            new_virus_report = SAVE_DIR_PATH + virus_dict[virus_file_name] + "/" + virus_file_name
            if not os.path.exists(new_virus_report):
                shutil.copy(old_virus_report, new_virus_report)
            else:
                os.remove(new_virus_report)
                shutil.copy(old_virus_report, new_virus_report)
    # dir_file_list = os.listdir(report_file_path)
    # for file in dir_file_list:
    #     if file == "task.json":
    #         if not os.path.exists(SAVE_DIR_PATH + report_dir_name):
    #             os.makedirs(SAVE_DIR_PATH + report_dir_name)
    #         new_file_name = SAVE_DIR_PATH + report_dir_name + "/" + file
    #         old_file_name = REPORT_DIR_PATH + report_dir_name + "/" + file
    #         if not os.path.exists(new_file_name):
    #             shutil.copy(old_file_name, new_file_name)
    #         else:
    #             os.remove(new_file_name)
    #             shutil.copy(old_file_name, new_file_name)
    #     elif file == "reports":
    #         if not os.path.exists(SAVE_DIR_PATH + report_dir_name):
    #             os.makedirs(SAVE_DIR_PATH + report_dir_name)
    #         new_file_name = SAVE_DIR_PATH + report_dir_name + "/" + file + "/"
    #         old_file_name = REPORT_DIR_PATH + report_dir_name + "/" + file + "/"
    #         if not os.path.exists(new_file_name):
    #             shutil.copytree(old_file_name, new_file_name)
    #         else:
    #             shutil.rmtree(new_file_name)
    #             shutil.copytree(old_file_name, new_file_name)
