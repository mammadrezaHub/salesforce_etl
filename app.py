import re
import streamlit as st
from pandasql import sqldf
import consts as c
import ui
import utils
import pandas as pd
from pathlib import Path

utils.create_folder(c.folder_configs)


st.set_page_config(page_title=c.caption_app, layout="wide")
st.title(c.caption_app)

with st.expander(c.caption_user_guide, expanded=False):
    try:
        with open(c.filename_user_guide, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.info("User guide not found.")


########## Step 1
ui.header(c.caption_load)

col_source_picker, col_source_alias = st.columns([1, 2])

with col_source_picker:
    with st.form("load_files"):
        source_files = ui.file_picker(c.caption_source_file)
        st.form_submit_button("Load files")

if source_files:
    current_files = {f.name for f in source_files}

    if (
        c.session_files_df not in st.session_state
        or set(st.session_state[c.session_files_df]["File"]) != current_files
    ):
        st.session_state[c.session_files_df] = pd.DataFrame({
            "File": [f.name for f in source_files],
            "Alias": [utils.normalize_alias(Path(f.name).stem.lower()) for f in source_files]
        })

    with col_source_alias:
        ui.alias_table()

    new_source_dfs = {}

    for file in source_files:
        alias = st.session_state[c.session_files_df].loc[
            st.session_state[c.session_files_df]["File"] == file.name,
            "Alias"
        ].values[0]

        if not alias:
            continue

        df = utils.get_df_from_file(file)
        if df is not None:
            new_source_dfs[alias] = df
            ui.preview_df(df, file.name, alias)

    st.session_state[c.session_source_dfs] = new_source_dfs

########## Step 2
ui.header(c.caption_transform)


with st.expander(c.caption_instructions):
    with open(c.filename_instructions, "r", encoding="utf-8") as f:
        st.markdown(f.read())

col_config_list, col_config_refresh, col_config_save = st.columns([25, 1, 3])
col_mapping, col_join = st.columns([1, 1])
col_filter, col_groupby = st.columns([1, 1])

with col_config_list:
    json_files = utils.get_list_configs()

    selected_config = st.selectbox(
        "",
        json_files,
        key="selected_config",
        label_visibility="collapsed",
        accept_new_options=True
    )
    selected_config = re.sub(r"[^a-zA-Z0-9_\- ]", "_", str(selected_config))

if not selected_config:
    with col_config_list:
        st.warning(c.hint_transformation)
    st.stop()


with col_config_refresh:
    if st.button(" ", icon=c.icon_refresh):
        st.session_state.pop("selected_config", None)


########## Step 2.1
with col_mapping:
    ui.header(c.caption_mapping, True)

    mapping_dict = {}
    current_where = ""

    if selected_config:
        try:
            mapping_dict, current_where, current_join, current_group_by = utils.load_config(selected_config)
            st.session_state["join_clause"] = current_join
            st.session_state["group_by_clause"] = current_group_by
        except FileNotFoundError:
            utils.create_default_config(selected_config)
            mapping_dict, current_where, current_join, current_group_by = utils.load_config(selected_config)
            st.session_state["join_clause"] = current_join
            st.session_state["group_by_clause"] = current_group_by
            with col_config_list:
                st.info(f"Created: {selected_config}")
        except Exception as e:
            with col_config_list:
                st.error(f"Failed to load {selected_config}: {e}")

        edited_df = st.data_editor(
            ui.mapping_table(mapping_dict),
            num_rows="dynamic",
            disabled=not selected_config
        )


########## Step 2.2
with col_join:
    ui.header(c.caption_join, True)

    if selected_config:
        join_clause = st.text_area(
            "JOIN Clause",
            value=st.session_state.get("join_clause", "")
        )

        st.session_state["join_clause"] = join_clause
        ui.sql_block(join_clause)


########## Step 2.3
with col_filter:
    ui.header(c.caption_filter, True)

    if selected_config:
        where_clause = st.text_area(
            "WHERE Clause",
            value=current_where
        )

    st.session_state["where_clause"] = where_clause
    ui.sql_block(where_clause)

    config = utils.create_config(
        edited_df,
        st.session_state.get("where_clause", ""),
        st.session_state.get("join_clause", ""),
        st.session_state.get("group_by_clause", "")
    )

    with col_config_save:
        if st.button(
            c.caption_config_save,
            disabled=edited_df.empty,
            icon=c.icon_config_save,
            shortcut=c.shortcut_config_save
        ):
            try:
                utils.save_config(selected_config, config)
                with col_config_list:
                    st.success(f"Saved: {selected_config}")
            except Exception as e:
                st.error(f"Failed to save file: {e}")

########## Step 2.4
with col_groupby:
    ui.header(c.caption_groupby, True)

    if selected_config:
        group_by_clause = st.text_area(
            "GROUP BY Clause",
            value=st.session_state.get("group_by_clause", "")
        )

        st.session_state["group_by_clause"] = group_by_clause
        ui.sql_block(group_by_clause)


########## Step 3
ui.header(c.caption_export)

source_dfs = st.session_state.get(c.session_source_dfs, {})

can_transform = (selected_config and source_dfs and not edited_df.empty)

if st.button(
    c.caption_generate,
    icon=c.icon_generate,
    shortcut=c.shortcut_generate,
    disabled=not can_transform
):
    try:
        base_alias = next(iter(source_dfs.keys()))

        sql = utils.get_select(config, base_alias)

        df_target = sqldf(sql, source_dfs)

        st.dataframe(df_target, hide_index=True)
        with st.expander(c.caption_full_script, expanded=False):
            ui.sql_block(sql)

    except Exception as e:
        st.error(f"SQL Error: {e}")

