import numpy as np
import matplotlib.pyplot as plt

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