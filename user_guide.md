# Salesforce ETL (User Guide)

This guide explains how to use the **Salesforce ETL** app step by step.  

---

## What this app is good at

- Combining multiple Salesforce exports (CSV / Excel)
- Looking up values from reference tables
- Creating new columns based on logic
- Cleaning and reshaping data
- Producing a final table ready for reporting or re-upload

---

## How the app works (in plain terms)

1. You upload files  
2. Each file gets a short **alias** (like a table name)
3. You define what columns you want in the output
4. You optionally connect files together (lookup / join)
5. The app builds the result for you

---

## Example used throughout this guide

We will use **two files**, which is very common in Salesforce work.

### File 1 (Main data)
**Accounts.csv**

| AccountId | Name          | IndustryCode |
|----------|---------------|--------------|
| A001     | Acme Ltd      | TEC          |
| A002     | Blue Corp     | FIN          |

### File 2 (Lookup table)
**Industry_Lookup.xlsx**

| Code | IndustryName |
|------|--------------|
| TEC  | Technology   |
| FIN  | Finance      |

Goal:
- Keep AccountId and Name
- Replace IndustryCode with the full Industry name

Final output:

| AccountId | AccountName | Industry |
|----------|-------------|----------|
| A001     | Acme Ltd    | Technology |
| A002     | Blue Corp   | Finance    |

---

## 1) Source File (Upload your files)

### Upload files
1. Go to **1) Source File**
2. Click **📂 Upload Source File**
3. Upload:
   - `Accounts.csv`
   - `Industry_Lookup.xlsx`

You can upload one or many files.

---

## Alias (Think of this as a sheet name)

After upload, you’ll see **🏷️ Alias for Source Files**.

Each file gets an alias automatically.

Example:
- Accounts.csv → `accounts`
- Industry_Lookup.xlsx → `industry_lookup`

You can edit these.

### Why alias matters
Aliases are how the app knows **which file a column comes from**.

If you know Excel formulas, this is similar to:
```text
SheetName!ColumnName
```

Here it becomes:
```text
alias.ColumnName
```

---

## 2) Transformation (Create a workspace)

At the top of **2) Transformation**:

1. Click the dropdown
2. Type a new name, for example:
   ```
   accounts_with_industry
   ```
3. Press **Enter**

The app creates a new configuration automatically.

---

## 2.1) Mapping (Choose your output columns)

This section defines **what the final table looks like**.

Each row = **one output column**.

### Columns explained simply

| Column | Meaning |
|------|--------|
| Target | Name of the column in the final result |
| Source | Original column (for reference) |
| Expression | How the value is calculated (optional) |

---

## Example 1 (Simple copy)

### Add AccountId
- Target: `AccountId`
- Source: `accounts.AccountId`
- Expression: *(leave empty)*

### Add AccountName
- Target: `AccountName`
- Source: `accounts.Name`
- Expression: *(leave empty)*

This is like saying:
> “Just copy this column as-is.”

---

## 2.2) Join (Connect files - lookup logic)

This step is like **VLOOKUP / XLOOKUP**, but for whole tables.

We want:
- `accounts.IndustryCode`
- matched to
- `industry_lookup.Code`

### Join Clause
Paste this into **2.2) Join**:

```sql
accounts
LEFT JOIN industry_lookup
  ON accounts.IndustryCode = industry_lookup.Code
```

What this means:
- Start from Accounts
- Look up matching rows in Industry Lookup
- Keep all accounts, even if lookup is missing

---

## Example 2 (Lookup value from another file)

### Add Industry name
- Target: `Industry`
- Source: `industry_lookup.IndustryName`
- Expression: *(leave empty)*

Now the app knows where to fetch the value from.

---

## Example 3 (Map values - replace codes)

Sometimes you don’t have a lookup table and just want rules.

Example:
- `Y` → `Yes`
- `N` → `No`

### Expression example
```sql
CASE
  WHEN accounts.ActiveFlag = 'Y' THEN 'Yes'
  WHEN accounts.ActiveFlag = 'N' THEN 'No'
  ELSE 'Unknown'
END
```

This works like nested IFs in Excel.

---

## Example 4 (Computed column - simple logic)

### Combine text
Target: `DisplayName`

Expression:
```sql
accounts.Name || ' (' || accounts.AccountId || ')'
```

Result:
```
Acme Ltd (A001)
```

---

## Example 5 (Numbers and calculations)

Salesforce exports numbers as text.  
You can still calculate.

### Total with tax
Target: `AmountWithTax`

Expression:
```sql
CAST(accounts.Amount AS REAL) * 1.2
```

Think of `CAST` as:
> “Treat this like a number.”

---

## 2.3) Filter (Limit rows - WHERE)

This is similar to filtering rows in Excel.

### Example: only Technology accounts
```sql
industry_lookup.IndustryName = 'Technology'
```

Important:
- Do **not** type `WHERE`
- Only the condition

---

## 2.4) Group By (Summaries and totals)

Use this when you want totals, counts, or rollups.

### Example: count accounts per industry

Mapping:
- Target: `Industry`
  - Expression: `industry_lookup.IndustryName`
- Target: `AccountCount`
  - Expression:
    ```sql
    COUNT(accounts.AccountId)
    ```

Group By:
```sql
industry_lookup.IndustryName
```

This is similar to a Pivot Table.

---

## 3) Export (Generate the result)

Click **Generate**.

You will see:
- Final table
- SQL used (for transparency)

You don’t need to understand the SQL, it’s there if you’re curious 🙂

---

## Common questions (non-technical)

### “Do I need to know SQL?”
No. You can copy examples and adjust names.

### “What if I make a mistake?”
- Fix the text
- Click **Save**
- Generate again

Configs are backed up automatically.

### “Why does nothing happen?”
Usually one of these:
- No mapping rows added
- No files uploaded
- Join refers to a wrong alias or column

---

## Best tips from real usage

- Start simple, then add logic
- Always check column names in the preview
- Use lookup tables when possible (cleaner than long rules)
- Keep aliases short and readable
- Save often

---

## Final thought

If you’re comfortable with:
- Salesforce exports
- Excel formulas
- Basic reporting logic