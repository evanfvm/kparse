#Streamlit app main file

import streamlit as st
import pandas as pd
import numpy as np
import datetime
from myfunc import split_block_frmstr, parse_block, toexcel, saveexcel
from gsheet import gsheet
import re

with st.container():

    uploaded_files = st.file_uploader(
        "Upload log file(s)", accept_multiple_files=True, type="log"
    )

    # outfile = st.text_input("outfile", value="", placeholder="Export File Name, eg. Export", label_visibility="collapsed")
    gmail = st.text_input("gmail", value="", placeholder="Your gmail | abc@gmail.com", label_visibility="collapsed")

    export = st.button("Export",use_container_width=True)

    if export and uploaded_files is not None:

        my_bar = st.progress(0, text="Loading MO data...")
        blocks = [split_block_frmstr(file.read().decode()) for file in uploaded_files]
        #array of all MO block (id, MO, block data)
        Blocks = np.concatenate(blocks)

        my_bar.progress(10, text="Parsing MO data...")
        #parse block into dict of param: value, with MOCLass as first array column
        # Blocks = np.array([parse_block(block) for block in Blocks])
        # print (Blocks[0])
        # TABNAMES = sorted(np.unique(Blocks[:,0]))
        # WORKBOOKS = {tab: pd.DataFrame(list(Blocks[Blocks[:,0]==tab, 1])) for tab in TABNAMES}
        # for tab in TABNAMES:
        #     values = WORKBOOKS[tab].to_numpy().tolist()
        #     print (values)
        #     break
        # print (WORKBOOKS['VlanPort'])
        # my_bar.progress(60, text="Converting to excel ...")
        # ggsheet = gsheet(st.secrets["gsheets"], gmail)
        # ggsheet.export(Blocks)
        # OUTFILE = "Export_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create excel data buffer stream for download button
        # BUFFER = toexcel(Blocks)

        # Save data to excel file in local directory
        # saveexcel(OUTFILE, Blocks)

        # my_bar.progress(100, text=f"Complete. Export file {OUTFILE} is saved.")
        # my_bar.empty()
        st.success("Completed")

        # st.download_button(
        #         label="Download Excel worksheets",
        #         data=BUFFER,
        #         file_name="Export.xlsx" if outfile == "" else f"{outfile}.xlsx",
        #         mime="application/vnd.ms-excel"
        #     )
