from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
import tempfile
import mimetypes, xlsxwriter
from werkzeug.datastructures import Headers
from datetime import datetime

#  get path
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  set sqlite3 as default database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data_register.sqlite')
app.config['SECRET_KEY']='hello world'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def register():
    from model import UserRegister
    from form import FormRegister
    form =FormRegister()
    if form.validate_on_submit():
        visitor = UserRegister(
            username = form.username.data,
            email = form.email.data,
            phone = form.phone.data,
            hostname = form.hostname.data
        )
        db.session.add(visitor)
        db.session.commit()
        return 'Success Thank You!'
    return render_template('login.html', form=form)

@app.route('/list')
def show_list():
    from model import UserRegister
    return render_template('list.html', visitors=UserRegister.query.all())

@app.route("/getcsv")
def getcsv():
    from model import UserRegister
    csv = 'name,email,phone,hostname\n'
    for instances in UserRegister.query.all():
        csv = csv + instances.username + ',' + instances.email + ',' + instances.phone+',' + instances.hostname + '\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=Visitor_List.csv"})

@app.route("/exceldownload")
def xlsx_export():
    from model import UserRegister
    try:
        # Flask response
        response = Response()
        response.status_code = 200

        output = tempfile.TemporaryFile()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('VisitorSheet1')

        #Write data into the sheet
        columns = ['username', 'email', 'phone', 'hostname']
        row_num = 0

        for col_num in range(len(columns)):
            worksheet.write(row_num, col_num, columns[col_num])

        for users in UserRegister.query.all():
            row_num += 1
            row = [users.username, users.email, users.phone, users.hostname]
            for col_num in range(len(columns)):
                worksheet.write(row_num, col_num, row[col_num])

        # Close the workbook before streaming the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Add output to response
        response.data = output.read()

        # Set filname and mimetype
        file_name = '{}_{}.xlsx'.format('Visitor_List', datetime.now())
        mimetype_tuple = mimetypes.guess_type(file_name)

        # HTTP headers for forcing file download
        response_headers = Headers({
                'Pragma': "public",  # required,
                'Expires': '0',
                'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
                'Cache-Control': 'private',  # required for certain browsers,
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'Content-Disposition': 'attachment; filename=\"%s\";' % file_name,
                'Content-Transfer-Encoding': 'binary',
                'Content-Length': len(response.data)
            })

        if not mimetype_tuple[1] is None:
            response.update({
                    'Content-Encoding': mimetype_tuple[1]
                })

        # Add headers
        response.headers = response_headers

        #jquery.fileDownload.js requirements
        response.set_cookie('fileDownload', 'true', path='/')

        # Return the response
        return response

    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.debug = True
    app.run()

