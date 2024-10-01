from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = '5678'

# เก็บข้อมูลผู้ใช้และรหัสผ่านใน
users = {
    'user1@example.com': '123',
    'user2@example.com': '456',
    'user3@example.com': '789'
}

# ฟังก์ชันเพื่อดึงข้อมูลจากฐานข้อมูล SQLite
def get_employees():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rowid, name, address, manager, status, position, salary, department, image FROM Employee')
    employees = cursor.fetchall()
    conn.close()
    return employees

# ฟังก์ชันเพื่อดึงข้อมูลพนักงานรายบุคคล
def get_employee_by_id(emp_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, address, manager, status, position, salary, department, image FROM Employees WHERE rowid = ?', (emp_id,))
    employee = cursor.fetchone()
    conn.close()
    return employee

# ฟังก์ชันเพื่ออัพเดทข้อมูลพนักงานในฐานข้อมูล
def update_employee(emp_id, name, address, manager, status, position, salary, department, image):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE Employee 
                      SET name = ?, address = ?, manager = ?, status = ?, position = ?, salary = ?, department = ?, image = ?
                      WHERE rowid = ?''', (name, address, manager, status, position, salary, department, image, emp_id))
    conn.commit()
    conn.close()

# ฟังก์ชันเพื่อลบข้อมูลพนักงาน
def delete_employee(emp_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Employee WHERE rowid = ?', (emp_id,))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # ตรวจสอบว่าอีเมลอยู่ใน dict และรหัสผ่านถูกต้อง
        if email in users and users[email] == password:
            employees = get_employees()
            return render_template('employee_table.html', employees=employees)
    
    return render_template('login.html')

@app.route('/employee_table', methods=['GET', 'POST'])
def employee_list():
    employees = get_employees()
    return render_template('employee_table.html', employees=employees)

@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # รับข้อมูลจากแบบฟอร์ม
        name = request.form['name']
        address = request.form['address']
        manager = 1 if 'manager' in request.form else 0  # แก้ไขตรงนี้เพื่อจัดการกับ checkbox
        status = request.form['status']
        position = request.form['position']
        salary = request.form['salary']
        department = request.form['department']
        image = request.form['image']
        
        # อัปเดตข้อมูลในฐานข้อมูล
        cursor.execute('''UPDATE Employee SET name=?, address=?, manager=?, status=?, position=?, salary=?, department=?, image=? WHERE rowid=?''',
                       (name, address, manager, status, position, salary, department, image, employee_id))
        conn.commit()
        conn.close()
        return redirect(url_for('employee_list'))  # เปลี่ยนเส้นทางกลับไปที่หน้าแสดงข้อมูลพนักงาน
    
    # ดึงข้อมูลพนักงานที่จะแก้ไข
    cursor.execute('SELECT * FROM Employee WHERE rowid=?', (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    
    return render_template('edit_employee.html', employee=employee, employee_id=employee_id)


@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Employee WHERE rowid=?', (employee_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('employee_list'))  # เปลี่ยนเส้นทางกลับไปที่หน้าแสดงข้อมูลพนักงาน

# เส้นทางสำหรับเพิ่มข้อมูลพนักงาน
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        manager = int(request.form.get('manager', 0))  # ใช้ 0 ถ้าไม่มีการเลือก
        status = request.form['status']
        position = request.form['position']
        salary = request.form['salary']
        department = request.form['department']
        image = request.form['image']
        
        # เพิ่มข้อมูลพนักงานในฐานข้อมูล 
        add_employee_to_db(name, address, manager, status, position, salary, department, image)
        return redirect(url_for('employee_list'))

    return render_template('add_employee.html')

@app.route('/search_employee', methods=['POST'])
def search_employee():
    search_query = request.form.get('query', '')
    search_field = request.form.get('field', 'name').strip()  # Get the selected field and strip any whitespace

    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
  
    if search_field == 'salary':
        try:
            salary_value = int(search_query)
            cursor.execute("SELECT rowid, name, address, manager, status, position, salary, department, image FROM Employee WHERE salary = ?", (salary_value,))
            employees = cursor.fetchall()
        except ValueError:
            employees = []
    elif search_field == 'name':
        cursor.execute("SELECT rowid, name, address, manager, status, position, salary, department, image FROM Employee WHERE name LIKE ?", ('%' + search_query + '%',))
        employees = cursor.fetchall()
    elif search_field == 'position':
        cursor.execute("SELECT rowid, name, address, manager, status, position, salary, department, image FROM Employee WHERE position LIKE ?", ('%' + search_query + '%',))
        employees = cursor.fetchall()
    elif search_field == 'department':
        cursor.execute("SELECT rowid, name, address, manager, status, position, salary, department, image FROM Employee WHERE department LIKE ?", ('%' + search_query + '%',))
        employees = cursor.fetchall()
    else:
        employees = []  # Default to empty if field is not recognized

    conn.close()

    return render_template('search_results.html', employees=employees)  # เปลี่ยนเส้นทางไปยัง search_results.html



# ฟังก์ชันสำหรับเพิ่มข้อมูลพนักงานในฐานข้อมูล
def add_employee_to_db(name, address, manager, status, position, salary, department, image):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Employee (name, address, manager, status, position, salary, department, image)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (name, address, manager, status, position, salary, department, image))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
