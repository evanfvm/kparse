#Streamlit app main file

import streamlit as st
import pandas as pd
import numpy as np
import datetime
# from myfunc import parse_block, toexcel, saveexcel
from mo import split_block, parse_block
from gsheet import gsheet
import re

with st.container():
    file = st.file_uploader(
        "Upload the log file", accept_multiple_files=False, type="log"
    )

    gmail = st.text_input("gmail", value="", placeholder="Your gmail | abc@gmail.com", label_visibility="collapsed")

    export = st.button("Parse to gsheet",use_container_width=True)

    if export and file is not None:

        my_bar = st.progress(0, text="Loading MO data...")
        BLOCKS = split_block(file.read().decode())
        if BLOCKS is None:
            st.error("Incomplete log. Upload a different log!")

        st.write (BLOCKS[0])
        # my_bar.progress(10, text="Parsing MO data...")
        # if BLOCKS is not None:
        #     block = parse_block(BLOCKS[0])
        #     st.write(block)
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
