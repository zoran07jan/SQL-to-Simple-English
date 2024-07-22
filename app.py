import re
from flask import Flask, request, render_template, send_from_directory
from tkinter.filedialog import askopenfilename
import xlwt
from xlwt import Workbook
import nltk
import os

nltk.download('punkt')

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_file(file_path):
    output_text_file = os.path.join(app.config['UPLOAD_FOLDER'], "output_file.txt")
    excel_file = os.path.join(app.config['UPLOAD_FOLDER'], "xlwt_example2.xls")

    with open(file_path, "rt") as f:
        read_data = f.read()
        SQL_dict = {
            "SELECT": "(SELECT)fetch from",
            "TOP" : "(TOP) the top value",
                "*" : "(*)the entire table",
                "AS" : "(AS) rename",
                "AND" : "(AND) combining (all conditions met)",
                "OR" : "(OR) combining (only one condition met)",
                "BETWEEN" : "(BETWEEN) between a range",
                "LIKE" : "(LIKE) search for a pattern where",
                "NULL" : "(NULL) returning null values",
                "NOT NULL" : "(NOT NULL) return values that aren't null",
                "VIEW" : "(VIEW) create virtual database",
                "COUNT" : "(COUNT) Creating number of rows with the criteria",
                "SUM" : "(SUM) returns the total sum",
                "AVG" : "(AVG) returns the average value",
                "MIN" : "(MIN) returns the minimum value",
                "MAX" : "(MAX) returns the maximum value",
                "GROUP BY" : "(GROUP BY) grouping rowa with same value into summary rows",
                "HAVING" : "(HAVING) where the condition",
                "ORDER BY" : "(ORDER BY) getting results in ascending order of",
                "DESC" : "but changing to descending order",
                "OFFSET" : "(OFFSET) specify to skip",
                "FETCH" : "(FETCH) and then return",
                "INNER JOIN" : "(INNER JOIN) matching value from both tables",
                "LEFT JOIN" : "(LEFT JOIN) matching rows from left to right",
                "RIGHT JOIN" : "(RIGHT JOIN) matching rows from right to left",
                "FULL JOIN" : "(FULL JOIN) matching rows from left OR right",
                "EXISTS" : "(EXISTS) testing the existence of the record",
                "GRANT" : "(GRANT) giving access to",
                "REVOKE" : "(REVOKE) removing permission to",
                "SAVEPONT" : "(SAVEPOINT) creating a backup for",
                "COMMIT" : "(COMMIT) saving the transaction",
                "ROLLBACK" : "(ROLLBACK) undo the transaction",
                "TRUNCATE" : "(TRUNCATE) removing the data entries from",
                "UNION" : "(UNION) combining datasets",
                "CREATE" : "(CREATE)create",
                "INSERT" : "(INSERT)insert the data to",
                "WHERE" : "(WHERE)on the condition",
                "UPDATE":"(UPDATE)updating the database",
                "DELETE":"(DELETE)Delete the",
                "INTO":"(INTO) specific data into the databse",
                "ALTER":"(ALTER)modify this",
                "TABLE":"(TABLE)Table in the selected databse",
                "DROP":"(DROP)delete the",
                "INDEX":"(INDEX)a search key",
                "SET": "(SET)update the data where",
                "=":"(=)is",
                "WHILE": "(WHILE)Loop Statement",
                "BEGIN": "(BEGIN) Beginning of a loop statement",
                "END": "(END) MArks the end of the loop statement",
                "BREAK": "(BREAK) Causes the flow to exit from the innermost WHILE loop",
                "CONTINUE": "(CONTINUE) Causes the WHILE loop to restart"
        }
        for word in SQL_dict:
            read_data = read_data.replace(word, SQL_dict[word])
        with open(output_text_file, "wt") as file2:
            file2.write(read_data)
    
    with open(file_path, "rt") as f2:
        lines = sum(1 for line in f2)
    
    with open(file_path, "rt") as f3:
        read2 = f3.read()
        comment_lines = re.findall(r'--.*', read2)
        count = len(comment_lines)
    
    with open(file_path, "rt") as f4:
        read3 = f4.read()
        counter1 = read3.count("WHILE") + read3.count("END")
        counter12 = counter1 / 2
        counter3 = read3.count("BREAK") + read3.count("CONTINUE")
        counter34 = counter3 + counter12
    
    with open(file_path, "rt") as f5:
        read4 = f5.read()
        select_statements = re.findall(r'SELECT.*?FROM.*?(?=(?:WHERE|GROUP BY|HAVING|ORDER BY|;|$))', read4, re.IGNORECASE | re.DOTALL)
        counter45 = 0
        for statement in select_statements:
            tables = re.findall(r'FROM\s+(\w+)', statement, re.IGNORECASE)
            counter45 += len(tables)
    
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0, 0, 'Parameter')
    sheet1.write(0, 1, 'value')
    sheet1.write(1, 0, 'number of lines')
    sheet1.write(1, 1, lines)
    sheet1.write(2, 0, 'number of comment lines')
    sheet1.write(2, 1, count)
    sheet1.write(3, 0, 'number of loops')
    sheet1.write(3, 1, counter34)
    sheet1.write(4, 0, 'number of tables in SELECT statement')
    sheet1.write(4, 1, counter45)
    wb.save(excel_file)
    
    return {
        "lines": lines,
        "comments": count,
        "loops": counter34,
        "tables_in_select": counter45,
        "output_file": "output_file.txt",
        "excel_file": "xlwt_example2.xls"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        result = process_file(file_path)
        return render_template('result.html', result=result)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)