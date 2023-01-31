## Data
column_names = ['name', 'salary', 'job']
db_rows = [('Alice', 180000, 'data scientist'),
 ('Bob', 99000, 'mid-level manager'),
 ('Frank', 87000, 'CEO')]
## One-Liner
db = [dict(zip(column_names, row)) for row in db_rows]
## Result
print(db)
