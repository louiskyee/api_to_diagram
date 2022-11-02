import numpy as np
import matplotlib.pyplot as plt
import os

VIRUS_FAMILY_PATH = r"/home/user/Documents/virus/VirusShare3_list2.txt"
VIRUS_DIR_PATH = r"/home/user/Documents/virus/temp_virus/"
SAVE_VIRUS_DIR_PATH = r"/home/user/Documents/virus/entropy_graph/"

def shannon_entropy(segment):
    '''
        return the entropy of input segment
    '''
    _, counts = np.unique(segment, return_counts=True)
    p = counts / len(segment)
    return - (p * np.log2(p)).sum()

def entropy_graph(file_name:str, segment_len, saveAs:str = 'output.png'):
    '''
        file to entropy graph
    '''
    with open(file_name, 'rb') as binaryFile:
        content  = binaryFile.read() # binary
        content = np.array(list(content)) # to byte list

        n_segment = len(content) // segment_len

        result_list = []
        for i in range(n_segment):
            segment = content[segment_len * i : segment_len * i + segment_len]
            result_list.append(shannon_entropy(segment))

        plt.ylim(0, np.log2(segment_len))
        plt.plot(result_list,c='b')
        plt.savefig(saveAs)

def load_virus_family(file_name):
    with open(file_name, encoding="utf-8") as f:
        virus_dict = dict()
        virus_list = f.readlines()
        for virus_info in virus_list:
            name, family = virus_info.split()
            virus_dict[name] = family
    return virus_dict

def makdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    virus_family_dict = load_virus_family(VIRUS_FAMILY_PATH)
    virus_list = os.listdir(VIRUS_DIR_PATH)
    makdir(SAVE_VIRUS_DIR_PATH)
    segment_len = 200
    for segment_len in range(200, 501, 100):
        print(f"segment_len = {segment_len}")
        makdir(SAVE_VIRUS_DIR_PATH + str(segment_len))
        for virus in virus_list:
            if virus_family_dict[virus] == "bancos" or virus_family_dict[virus] == "banload":
                makdir(SAVE_VIRUS_DIR_PATH + str(segment_len) + '/' + virus_family_dict[virus])
                entropy_graph(file_name=VIRUS_DIR_PATH + virus, segment_len=segment_len, saveAs=SAVE_VIRUS_DIR_PATH + str(segment_len) + '/' + virus_family_dict[virus] + '/'+ virus)