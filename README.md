Turso migration of local data

```bash
turso db shell command-center < migrations/001_create_tables.sql
```

```bash
turso db shell command-center < migrations/002_populate_data.sql
```
