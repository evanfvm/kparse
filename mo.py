import re
import numpy as np
from numpy.typing import NDArray


def split_block(file:str)->None:
    #regrex pattern
    pattern_block = r"=+\nProxy Id\s+(\d+)\nMO\s+(.+)\n=+"
    pattern_end = r"\n+Total:\s+(\d+) MOs\n"

    blocks = re.split(pattern_block, file)[1:]
    print (blocks[0])
    # blocks[-1], total, _ = re.split(pattern_end, blocks[-1])

    # if int(total)*3 == len(blocks):
    #     blocks = np.reshape(blocks, (int(total),3))
    #     return blocks

    # print ("not align")
    # blocks = np.reshape(blocks, (len(blocks)//3,3))
    # return blocks
