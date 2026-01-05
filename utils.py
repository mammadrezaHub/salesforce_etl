from pathlib import Path
import consts as c
import pandas as pd
import json
import shutil
from datetime import datetime
import streamlit as st
import sqlparse
import re


@st.cache_data(show_spinner=False)
def get_df_from_file(file):
    if file:
        ext = file.name.lower()

        if ext.endswith(".csv"):
            return pd.read_csv(file, dtype=str)

        elif ext.endswith(".xls") or ext.endswith(".xlsx"):
            return pd.read_excel(file, dtype=str)


def get_full_config_path(config_name):
    return Path(c.folder_configs) / f"{config_name}{c.ext_config}"


def load_config(config_name):
    path = get_full_config_path(config_name)
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)
        return (
            config.get("mapping", {}),
            config.get("where", ""),
            config.get("join", ""),
            config.get("group_by", "")
        )



def create_config(df_mapping, where_clause, join_clause, group_by_clause):
    config = {}

    for _, row in df_mapping.iterrows():
        target = row["Target"] or ""
        source = row["Source"] or ""
        expr   = row["Expression"] or ""

        if target == "" and source == "" and expr == "":
            continue

        if target not in config:
            config[target] = {}

        config[target][source] = expr

    config = {
        "mapping": config,
        "where": where_clause,
        "join": join_clause,
        "group_by": group_by_clause
    }

    return config


def backup_config(config_path: Path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = config_path.with_suffix(
        config_path.suffix + f".{timestamp}.bak"
    )

    if config_path.exists():
        shutil.copy2(config_path, backup_file)


def replace_none(obj):
    if isinstance(obj, dict):
        return {k: replace_none(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [replace_none(v) for v in obj]
    return "" if obj is None else obj


def save_config(config_name, config, backup=True):
    config_path = get_full_config_path(config_name)  # must return Path

    if backup:
        backup_config(config_path)

    config = replace_none(json.loads(json.dumps(config)))

    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_select(config, base_alias):
    sql_cols = []

    for target_col, inner in config.get("mapping", {}).items():
        for source, expr in inner.items():
            if not isinstance(expr, str) or expr.strip() == "":
                sql_cols.append(f'{source} AS "{target_col}"')
            else:
                sql_cols.append(f'{expr} AS "{target_col}"')

    select_sql = ",\n       ".join(sql_cols)
    join = (config.get("join") or "").strip() or base_alias
    where = f"WHERE {config.get('where').strip()}" if config.get("where") else ""
    group_by = f"GROUP BY {config.get('group_by').strip()}" if config.get("group_by") else ""

    sql = f"""
    SELECT
        {select_sql}
    FROM
        {join}
    {where}
    {group_by}
    """

    sql = format_sql(sql)

    return sql


def create_default_config(config_name):
    config_name = config_name + c.ext_config
    path = get_full_config_path(config_name.replace(c.ext_config, ""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(c.default_config)


def get_list_configs():
    files = sorted(
        (
            f for f in Path(c.folder_configs).iterdir()
            if f.is_file() and f.suffix == c.ext_config
        ),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    return [f.stem for f in files] or [""]


def format_sql(sql: str) -> str:
    return sqlparse.format(
        sql,
        reindent=True,
        keyword_case="upper",
        identifier_case=None,
        strip_comments=False
    )


def normalize_alias(text: str) -> str:
    if not text:
        return ""

    alias = (
        str(text)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("@", "_")
        .replace("#", "_")
        .replace("$", "_")
        .replace("%", "_")
        .replace("&", "_")
        .replace("+", "_")
        .replace("=", "_")
        .replace("!", "_")
        .replace("?", "_")
        .replace(",", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace("[", "_")
        .replace("]", "_")
        .replace("{", "_")
        .replace("}", "_")
        .replace("'", "_")
        .replace('"', "_")
    )

    alias = re.sub(r"_+", "_", alias).strip("_")

    # Ensure valid SQLite identifier (must not start with a digit)
    if not re.match(r"^[a-z_]", alias):
        alias = f"t_{alias}"

    return alias

def create_folder(folder_name):
    Path(folder_name).mkdir(parents=True, exist_ok=True)