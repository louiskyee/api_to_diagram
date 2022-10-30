import os
import json
import shutil

REPORT_DIR_PATH = "./report/"
report_file_list = os.listdir(REPORT_DIR_PATH)

for report_dir in report_file_list:
    report_path = os.getcwd() + REPORT_DIR_PATH[1:] + report_dir
    print(report_path)
    dir_file_list = os.listdir(report_path)    
    for file in dir_file_list:
        if not (file == "files.json" or file == "reports"):
            if os.path.isfile(report_path+'/'+file):
                os.remove(report_path+'/'+file)
            else:
                shutil.rmtree(report_path+'/'+file)
            # print(report_path+file)
