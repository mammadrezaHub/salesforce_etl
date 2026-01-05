## Mapping
### 1. String Functions

| Function | Example | Description |
|---------|---------|-------------|
| LOWER() | `LOWER(col)` | Converts text to lowercase |
| UPPER() | `UPPER(col)` | Converts text to uppercase |
| TRIM() | `TRIM(col)` | Removes leading and trailing spaces |
| LTRIM() | `LTRIM(col)` | Removes spaces on the left |
| RTRIM() | `RTRIM(col)` | Removes spaces on the right |
| LENGTH() | `LENGTH(col)` | Returns number of characters |
| REPLACE() | `REPLACE(col, 'a', 'b')` | Replaces text |
| SUBSTR() | `SUBSTR(col, start, length)` | Extracts substring |
| INSTR() | `INSTR(col, 'x')` | Finds position of substring |
| HEX() | `HEX(col)` | Converts value to hex text |
| PRINTF() | `PRINTF('%s-%s', col1, col2)` | String formatting |

---

### 2. Numeric Functions

| Function | Example | Description |
|---------|---------|-------------|
| ABS() | `ABS(col)` | Absolute value |
| ROUND() | `ROUND(col, 2)` | Rounds numeric value |
| COALESCE() | `COALESCE(col, 'default')` | First non-null value |
| NULLIF() | `NULLIF(a, b)` | Returns NULL if equal |
| IFNULL() | `IFNULL(col, 'x')` | Replace NULL |
| RANDOM() | `RANDOM()` | Generates random integer |

---

### 3. Date & Time Functions

| Function | Example | Description |
|---------|---------|-------------|
| DATE() | `DATE('now')` | Current date |
| TIME() | `TIME('now')` | Current time |
| DATETIME() | `DATETIME('now')` | Current date/time |
| STRFTIME() | `STRFTIME('%Y-%m-%d', datecol)` | Formats a date string |
| JULIANDAY() | `JULIANDAY('now')` | Days since base date |

---

### 4. Conditional Expressions

| Expression | Example | Description |
|-----------|---------|-------------|
| CASE WHEN | `CASE WHEN amount > 0 THEN 'POS' ELSE 'NEG' END` | SQL conditional logic |
| IFNULL() | `IFNULL(col, 'N/A')` | Replace NULL values |
| NULLIF() | `NULLIF(a, b)` | NULL if equal |
| COALESCE() | `COALESCE(a, b, c)` | First non-null expression |

## Join

Use JOINs to combine multiple source files using their aliases.

| Type | Example | Description |
|------|--------|-------------|
| INNER JOIN | `a INNER JOIN b ON a.id = b.id` | Matching rows only |
| JOIN (same as INNER) | `a JOIN b ON a.id = b.id` | Shorthand for INNER JOIN |
| LEFT JOIN | `a LEFT JOIN b ON a.id = b.id` | Keeps all rows from the left source |
| CROSS JOIN | `a CROSS JOIN b` | Every combination of rows |
| Multiple JOINs | `a JOIN b ON ... LEFT JOIN c ON ...` | Join more than two sources |

**Tips**
- Does **not** support `RIGHT JOIN` or `FULL OUTER JOIN`
- Always use file aliases (defined in Step 1)
- The first source acts as the base table

---

## Filter

Use filters to limit which rows are included in the result.

| Expression | Example | Description |
|-----------|---------|-------------|
| Comparison | `amount > 100` | Numeric comparison |
| Text match | `status = 'Active'` | Exact text match |
| Pattern match | `name LIKE '%test%'` | Partial text match |
| IN list | `country IN ('UK', 'US')` | Match multiple values |
| AND | `a = 1 AND b = 2` | Combine conditions |
| OR | `a = 1 OR b = 2` | Alternative conditions |

---

## Group By

Use grouping when applying aggregations.

| Function | Example | Description |
|---------|---------|-------------|
| COUNT() | `COUNT(*)` | Number of rows |
| SUM() | `SUM(amount)` | Total value |
| AVG() | `AVG(score)` | Average value |
| MIN() | `MIN(date)` | Minimum value |
| MAX() | `MAX(date)` | Maximum value |

**Example**
```sql
country, status
```

**Note**
> Do **not** include the `JOIN` or `WHERE` or `GROUP BY` keywords.