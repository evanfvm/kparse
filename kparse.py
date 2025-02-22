#Streamlit app main file

from pandas.core.generic import WriteExcelBuffer
from pandas.core.internals.managers import Block
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from myfunc import split_block_frmstr, parse_block, toexcel, saveexcel

with st.container():
    uploaded_files = st.file_uploader(
        "Upload log file(s)", accept_multiple_files=True, type="log"
    )

    outfile = st.text_input("outfile", value="", placeholder="Export File Name, eg. Export", label_visibility="collapsed")

    export = st.button("Export",use_container_width=True)

    if export and uploaded_files is not None:
        my_bar = st.progress(0, text="Loading MO data...")
        blocks = [split_block_frmstr(file.read().decode()) for file in uploaded_files]
        #array of all MO block (id, MO, block data)
        Blocks = np.concatenate(blocks)

        my_bar.progress(10, text="Parsing MO data...")
        #parse block into dict of param: value, with MOCLass as first array column
        Blocks = np.array([parse_block(block) for block in Blocks])

        my_bar.progress(60, text="Converting to excel ...")

        BUFFER = toexcel(Blocks)
        # OUTFILE="Export.xlsx" if outfile == "" else f"{outfile}.xlsx"
        # saveexcel(OUTFILE, Blocks)

        # my_bar.progress(100, text=f"Complete. Export file {OUTFILE} is saved.")
        my_bar.empty()
        st.success("Completed")

        st.download_button(
                label="Download Excel worksheets",
                data=BUFFER,
                file_name="Export.xlsx" if outfile == "" else f"{outfile}.xlsx",
                mime="application/vnd.ms-excel"
            )
