import re
from typing import Dict, List, Any
from numpy.typing import NDArray

import pandas as pd
import numpy as np
import io


def split_block(path:str)->NDArray:
    #regrex pattern
    pattern_block = r"=+\s+Proxy Id\s+(\d+)\s+MO\s+(.+)\s+=+\s+"
    pattern_end = r"=+\s+Total:\s+(\d+) MOs\s+"

    file = open(path, 'r', encoding='utf-8')
    file = file.read()
    blocks = re.split(pattern_block, file)[1:]
    blocks[-1], total, _ = re.split(pattern_end, blocks[-1])

    if int(total)*3 == len(blocks):
        blocks = np.reshape(blocks, (int(total),3))
        return blocks

    print ("not align")
    blocks = np.reshape(blocks, (len(blocks)//3,3))
    return blocks

def split_block_frmstr(file:str)->NDArray:
    #regrex pattern
    pattern_block = r"=+\s+Proxy Id\s+(\d+)\s+MO\s+(.+)\s+=+\s+"
    pattern_end = r"=+\s+Total:\s+(\d+) MOs\s+"

    blocks = re.split(pattern_block, file)[1:]
    blocks[-1], total, _ = re.split(pattern_end, blocks[-1])

    if int(total)*3 == len(blocks):
        blocks = np.reshape(blocks, (int(total),3))
        return blocks

    print ("not align")
    blocks = np.reshape(blocks, (len(blocks)//3,3))
    return blocks

def parse_block(block:NDArray[Any])->NDArray:
    #regrex pattern
    pattern_nodeid = r"MeContext=(\w+)"
    pattern_param = r"^(\S+)(.+)"
    pattern_struct = r"^Struct (\S+) has (\d+) members:"
    pattern_subStruct = r"^ >>> \d+.(\S+) =(.+)"
    pattern_arr = r"^(\S+)\[(\d+)\](.+)"

    #metadata
    ProxyID = int(block[0])
    MOCLASS = block[1].split(",")[-1]
    MOCLASS = MOCLASS.split("=")[0]
    ROW = {
        "NodeID": re.split(pattern_nodeid,block[1])[1],
        "MO": str(block[1])
    }
    Lines = block[2].splitlines()
    StructCounter = 0
    StructID = ""
    ArrCounter = 0
    ArrayID = ""

    for line in Lines:
        '''Struct Pattern'''
        struct = re.match(pattern_struct, line)
        if struct:
            StructID = struct.group(1)
            StructCounter = int(struct.group(2))
            #Struct has 0 member
            if StructCounter == 0:
                ROW[StructID] = ""
            continue

        #sub struct
        if StructCounter != 0 and ArrCounter == 0 :
            substruct = re.match(pattern_subStruct, line)
            if substruct:
                subid = substruct.group(1)
                subvalue = substruct.group(2).strip()
                ROW[f"{StructID}__{subid}"] = subvalue

            StructCounter -= 1
            if StructCounter == 0: StructID = "" #reset struct
            continue

        '''Array Pattern'''
        arr = re.match(pattern_arr, line)
        if arr:
            ArrayID = arr.group(1)
            ArrCounter = int(arr.group(2))
            arrval = arr.group(3).strip()
            # print (arr.groups())

            # Size 0 array OR Inline array
            if (ArrCounter == 0) or (arrval != ""):
                ROW[ArrayID] = arrval
                ArrCounter = 0
            continue

        #Sub Array
        if ArrCounter != 0:
            line = line.lstrip(" >")

            #Struct under array
            struct = re.match(r"Struct\[\d+\]\s+has (\d+) members", line)
            if struct:
                StructID = ArrayID
                StructCounter = int(struct.group(1))
                continue

            #Array of substruct
            if StructCounter != 0:
                substruct = line.split(".")[1].split(" = ")
                subid = substruct[0]
                subval = substruct[1].strip()
                if f"{StructID}__{subid}" in ROW.keys():
                    ROW[f"{StructID}__{subid}"] = f"{ROW[f"{StructID}__{subid}"]};{subval}"
                else:
                    ROW[f"{StructID}__{subid}"] = subval
                StructCounter -=1
                if StructCounter == 0: ArrCounter -=1
                if ArrCounter == 0: #reset array & struct ID
                    ArrayID = ""
                    StructID = ""
                continue

            #no struct, multi-line array
            if StructCounter == 0:
                subarr = re.match(r"^\S+ = (.+)", line)
                if subarr:
                    ROW[ArrayID] = f"{ROW[ArrayID]};{subarr.group(1)}" if ArrayID in ROW.keys() else subarr.group(1)
                    ArrCounter -=1
                    if ArrCounter==0: ArrayID="" #reset array ID
                continue

        #Regular parameters
        param = re.match(pattern_param, line)
        if param:
            ROW[param.group(1)] = param.group(2).strip()

    return np.array([MOCLASS, ROW])

def toexcel (Blocks):
    TABNAMES = sorted(np.unique(Blocks[:,0]))
    WORKBOOKS = {tab: pd.DataFrame(list(Blocks[Blocks[:,0]==tab, 1])) for tab in TABNAMES}

    BUFFER = io.BytesIO()

    writer = pd.ExcelWriter(BUFFER, engine="openpyxl")
    [WORKBOOKS[tab].to_excel(writer, sheet_name=tab[:31], index=False) for tab in TABNAMES]
    writer.close()

    return BUFFER

if __name__=="__main__":
    path = ["Kget_NOM5317_1.log", "Kget_NOM5317_2.log"]
    OUTFILE = "Kget_NOM5317.xlsx"

    blocks = [split_block(p) for p in path]
    Blocks = np.concatenate(blocks)

    # print (Blocks.shape)
    Blocks = np.array([parse_block(block) for block in Blocks])
    # print (Blocks.shape)

    TABNAMES = sorted(np.unique(Blocks[:,0]))
    WORKBOOKS = {tab: pd.DataFrame(list(Blocks[Blocks[:,0]==tab, 1])) for tab in TABNAMES}

    writer = pd.ExcelWriter(OUTFILE, engine="openpyxl")
    [WORKBOOKS[tab].to_excel(writer, sheet_name=tab[:31], index=False) for tab in TABNAMES]
    writer.close()
