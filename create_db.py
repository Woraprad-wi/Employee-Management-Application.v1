# create_db.py
import sqlite3

# เชื่อมต่อกับฐานข้อมูล
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# สร้างตาราง Employee
cursor.execute('''
CREATE TABLE IF NOT EXISTS Employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    manager BOOLEAN,
    status TEXT,
    position TEXT,
    salary REAL,
    department TEXT,
    image TEXT
)
''')

# ใส่ข้อมูลตัวอย่าง 20 คน
employees = [
    ('Nattawut Srisang', '123 Sukhumvit Rd, Bangkok', 1, 'Active', 'Software Engineer', 75000, 'IT', 'nattawut.jpg'),
    ('Chutimon Srisai', '456 Phahonyothin Rd, Bangkok', 0, 'Active', 'Data Analyst', 65000, 'Analytics', 'chutimon.jpg'),
    ('Poomjai Thongthip', '789 Rama IX Rd, Bangkok', 1, 'Active', 'Project Manager', 80000, 'Management', 'poomjai.jpg'),
    ('Anon Kittipong', '135 Sathorn Rd, Bangkok', 1, 'Active', 'HR Specialist', 60000, 'HR', 'anon.jpg'),
    ('Supachai Panpradit', '246 Ratchadapisek Rd, Bangkok', 0, 'Inactive', 'Marketing Officer', 55000, 'Marketing', 'supachai.jpg'),
    ('Wattanapong Mungmee', '357 Silom Rd, Bangkok', 1, 'Active', 'UX Designer', 70000, 'Design', 'wattanapong.jpg'),
    ('Kanya Jiranan', '468 Vibhavadi Rangsit Rd, Bangkok', 1, 'Active', 'Frontend Developer', 72000, 'IT', 'kanya.jpg'),
    ('Poonnapha Chumchit', '579 Lat Phrao Rd, Bangkok', 0, 'Active', 'Backend Developer', 74000, 'IT', 'poonnapha.jpg'),
    ('Ratanakorn Suwannakham', '680 Phetchaburi Rd, Bangkok', 1, 'Active', 'Sales Executive', 65000, 'Sales', 'ratanakorn.jpg'),
    ('Rachakorn Chokpa', '791 Ekkamai Rd, Bangkok', 0, 'Active', 'Accountant', 62000, 'Finance', 'rachakorn.jpg'),
    ('Wipavadi Lertwong', '902 Sukhumvit Soi 22, Bangkok', 1, 'Active', 'System Analyst', 70000, 'IT', 'wipavadi.jpg'),
    ('Chaisiri Pongpetch', '123 Ramkhamhaeng Rd, Bangkok', 0, 'Inactive', 'QA Engineer', 58000, 'IT', 'chaisiri.jpg'),
    ('Tanaporn Jitnawan', '234 Sukhothai Rd, Bangkok', 1, 'Active', 'Content Writer', 50000, 'Content', 'tanaporn.jpg'),
    ('Kanokwan Suwanne', '345 Rajdamri Rd, Bangkok', 1, 'Active', 'Graphic Designer', 65000, 'Design', 'kanokwan.jpg'),
    ('Suthida Sawangwong', '456 Chao Phraya Rd, Bangkok', 1, 'Active', 'Network Engineer', 75000, 'IT', 'suthida.jpg'),
    ('Pichaya Sakulthong', '567 Narathiwat Rd, Bangkok', 1, 'Active', 'Business Analyst', 68000, 'Analytics', 'pichaya.jpg'),
    ('Pannicha Suwanpim', '678 Praram 9 Rd, Bangkok', 1, 'Active', 'Operations Manager', 80000, 'Management', 'pannicha.jpg'),
    ('Chakkrit Prakob', '789 Thonglor Rd, Bangkok', 0, 'Inactive', 'Procurement Officer', 60000, 'Procurement', 'chakkrit.jpg'),
    ('Phongchai Srisang', '890 Ratchaprasong Rd, Bangkok', 1, 'Active', 'Legal Advisor', 72000, 'Legal', 'phongchai.jpg'),
    ('Chutikan Kasemsap', '901 Asoke Rd, Bangkok', 1, 'Active', 'IT Support', 50000, 'IT', 'chutikan.jpg')
]

# ใส่ข้อมูลลงในตาราง Employee
cursor.executemany('''
INSERT INTO Employee (name, address, manager, status, position, salary, department, image)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', employees)

# บันทึกการเปลี่ยนแปลงและปิดการเชื่อมต่อ
conn.commit()
conn.close()
