เข้าใจแล้ว!
ฉันจะเขียน SQL Command สำหรับสร้างตารางในรูปแบบ Markdown ให้เลย

---

### ✅ **SQL Command สำหรับสร้างตาราง (Copy & Paste)**

```sql
-- สร้างตาราง users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

-- สร้างตาราง bookings
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

---

### ✅ **การใช้งาน:**

1. เปิด SQLite:

```bash
sqlite3 database/database.db
```

2. คัดลอกและวางคำสั่ง SQL:

```sql
-- วางคำสั่งที่นี่
```

3. ตรวจสอบการสร้างตาราง:

```sql
.tables
```

---

### ✅ **SQL Command สำหรับลบตาราง (Drop Table) และลบคอลัมน์ (Drop Column)**

---

### 🛠️ **ลบตาราง (Drop Table)**

**คำสั่งนี้จะลบทั้งตารางและข้อมูลทั้งหมดในตารางนั้น:**

```sql
-- ลบตาราง users
DROP TABLE IF EXISTS users;

-- ลบตาราง bookings
DROP TABLE IF EXISTS bookings;
```

---

### 🛠️ **ลบคอลัมน์ (Drop Column)**

SQLite **ไม่รองรับคำสั่ง `DROP COLUMN`** โดยตรง
แต่เราสามารถใช้วิธีการแก้ไขโครงสร้างตาราง (Rebuild Table) ดังนี้:

---

### ✅ **ตัวอย่าง: ลบคอลัมน์ `password` ในตาราง `users`**

1. **สร้างตารางใหม่โดยไม่รวมคอลัมน์ `password`:**

```sql
CREATE TABLE users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
);
```

2. **ย้ายข้อมูลจากตารางเก่าไปตารางใหม่:**

```sql
INSERT INTO users_new (id, username)
SELECT id, username FROM users;
```

3. **ลบตารางเก่า:**

```sql
DROP TABLE users;
```

4. **เปลี่ยนชื่อตารางใหม่กลับไปเป็น `users`:**

```sql
ALTER TABLE users_new RENAME TO users;
```

---

### ✅ **การเพิ่มคอลัมน์ใหม่ (Add Column):**

```sql
ALTER TABLE users ADD COLUMN email TEXT;
```

---

### ✅ **สรุปคำสั่ง:**

| **คำสั่ง**   | **รูปแบบ**                                                 |
| ------------ | ---------------------------------------------------------- |
| ลบตาราง      | `DROP TABLE IF EXISTS table_name;`                         |
| ลบคอลัมน์    | ต้องใช้การสร้างตารางใหม่แล้วคัดลอกข้อมูล                   |
| เพิ่มคอลัมน์ | `ALTER TABLE table_name ADD COLUMN column_name data_type;` |

---



