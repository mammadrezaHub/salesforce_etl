import consts as c
import streamlit as st
import pandas as pd


def file_picker(caption=""):
    return st.file_uploader(
        caption,
        type=c.supported_ext,
        accept_multiple_files=True,
        width="stretch"
    )

def header(caption="", sub=False):
    if sub:
        st.subheader(caption)
    else:
        st.header(caption, divider=True)

def mapping_table(mapping_dict):
    rows = []

    for target_col, inner in mapping_dict.items():
        for source_col, expr in inner.items():
            rows.append([target_col, source_col, expr])

    return pd.DataFrame(rows, columns=["Target", "Source", "Expression"])

def alias_table():
    st.write(c.caption_alias)
    st.session_state[c.session_files_df] = st.data_editor(
        st.session_state[c.session_files_df],
        hide_index=True,
        column_config={
            "File": st.column_config.TextColumn(disabled=True),
            "Alias": st.column_config.TextColumn()
        }
    )

def preview_df(df, filename, alias):
    with st.expander(
        f"{c.icon_file} {filename} ({df.shape[0]:,}×{df.shape[1]:,}) → [`{alias}`]",
        expanded=False
    ):
        st.dataframe(df, hide_index=True)


def sql_block(sql):
    st.code(sql, language="sql")