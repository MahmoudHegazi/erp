#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from database_setup import Base, Employees, Atttendance, AtttendanceActions
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from flask import make_response
import random
import json
import string
import requests
from io import BytesIO
from flask import send_file
from openpyxl import Workbook
import getpass
from datetime import datetime
from sqlalchemy import desc
import uuid
import sys
import datetime
from time import gmtime, strftime
import time
import pytz
from datetime import timedelta

app = Flask(__name__)

engine = create_engine('sqlite:///erp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def test(x1, x2):
    #x1 = '2020-12-18 5:00:00 pm'
    #x2 = '2020-12-19 09:00:32 AM'
    FMT1 = '%Y-%m-%d %I:%M:%S %p'
    tdelta1 = datetime.datetime.strptime(x2, FMT1) - datetime.datetime.strptime(x1, FMT1)
    speical = '%Y-%m-%d %I:%M:%S %p'
    def days_hours_minutes(td):
        return td.days, td.seconds//3600, (td.seconds//60)%60
    x = days_hours_minutes(tdelta1)

    if x[0] == 0 and x[1] >= 10 and x[2] >= 10:
        duration_string = str(x[1]) +  ':' + str(x[2])
        return duration_string
    elif x[0] == 0 and x[1] <= 9 and x[2] <= 9:
        duration_string = '0' + str(x[1]) +  ':0' + str(x[2])
        return duration_string

    elif x[0] == 0 and x[1] >= 10 and x[2] <= 9:
        duration_string = str(x[1]) +  ':0' + str(x[2])
        return duration_string

    elif x[0] == 0 and x[1] <= 9 and x[2] >= 10:
        duration_string = '0' + str(x[1]) +  ':' + str(x[2])
        return duration_string

    else:
        duration_string = str(x[0]) + ':' + str(x[1]) +  ':' + str(x[2])
        return duration_string

# 01 Check day attendance for employee
@app.route('/get_attendance/<string:employee_code>/<string:date>')
def get_attendance(employee_code, date):
    error = False
    try:
         duration_object = session.query(Atttendance).filter_by(employee_code=employee_code).filter_by(date=date).first()
         duration_string = duration_object.duration
         attended = duration_object.attended
         answer = {'duration':duration_string,'attended':attended}
    except:
        print(sys.exc_info())
        error = True
        message = 'Can not Return duration for that Employee'
        answer = {'message':message}
    finally:
        session.close()
    if not error:
        return jsonify(answer)
    else:
        return jsonify(answer)


# 02 Retrieve attendance history for employee
# this normal Function return the history in ISO Format
@app.route('/get_history/<string:employee_code>')
def get_history(employee_code):
    error = False
    data = {'days':[]}
    try:
        atttendance_object = session.query(Atttendance).filter_by(employee_code=employee_code).all()
    except:
        print(sys.exc_info())
        error = True
    finally:
        session.close()
    if not error:
        for day in atttendance_object:
            actions = []
            date = day.date
            atttendance_actions_object  = session.query(AtttendanceActions).filter_by(atttendance_id=day.id).all()
            for action in atttendance_actions_object:
                time_zone = pytz.timezone("Africa/Cairo")
                iso_format = datetime.datetime.strptime(action.date, "%Y-%m-%d %H:%M:%S %p")
                d = iso_format.replace(tzinfo=datetime.timezone.utc)
                actions.append({'action':action.type, 'time':d.isoformat()})
            data['days'].append([date, actions])
        return jsonify(data)
    else:
        data['error'] = True
        return jsonify(data)


# 02 Retrieve attendance history for employee
# this normal Function return the history in Egypt Time
@app.route('/get_history_normal/<string:employee_code>')
def get_history_normal(employee_code):
    error = False
    data = {'days':[]}
    try:
        atttendance_object = session.query(Atttendance).filter_by(employee_code=employee_code).all()
    except:
        print(sys.exc_info())
        error = True
    finally:
        session.close()
    if not error:
        for day in atttendance_object:
            actions = []
            date = day.date
            atttendance_actions_object  = session.query(AtttendanceActions).filter_by(atttendance_id=day.id).all()
            for action in atttendance_actions_object:
                actions.append({'action':action.type, 'time':action.date})
            data['days'].append([date, actions])
        return jsonify(data)
    else:
        data['error'] = True
        return jsonify(data)


# EndPoint1 return all the employess from the database in JSON format
@app.route('/api/employess')
def json_employess():
    employees = session.query(Employees).all()
    session.close()
    return jsonify(employees=[r.serialize for r in employees])

# EndPoint2 return all the atttendance records from the database in JSON format
@app.route('/api/atttendance')
def json_attendance():
    attendance = session.query(Atttendance).all()
    session.close()
    return jsonify(atttendance=[r.serialize for r in attendance])

# EndPoint3 return all the atttendance_actions records from the database in JSON format
@app.route('/api/atttendance_actions')
def json_atttendance_actions():
    atttendance_actions = session.query(AtttendanceActions).all()
    session.close()
    return jsonify(atttendance_actions=[r.serialize for r in atttendance_actions])

#‘2020-04-01’)
#“duration”: “12:00”

def time_maker():
    time_dict = {'gmt_timestring':str(),'gmt_datetime':str(),'gmt_date':str(),'egypt_datetime':str(), 'egypt_date':str()}
    date_string = datetime.datetime.now()
    date_and_time = datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S: %p')
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    egypt_time0 = datetime.datetime.now(pytz.timezone('Africa/Cairo'))
    egypt_datetime = egypt_time0.strftime('%Y-%m-%d %I:%M:%S %p')
    egypt_date = egypt_time0.strftime('%Y-%m-%d')
    #Thu, 17 Dec 2020 01:04:52 GMT
    time_dict['gmt_timestring'] = date_string
    time_dict['gmt_datetime'] = date_and_time
    time_dict['gmt_date'] = date
    time_dict['egypt_datetime'] = egypt_datetime
    time_dict['egypt_date'] = egypt_date
    return time_dict


@app.route('/')
def index():
    the_time_dict = time_maker()
    error = False
    try:
        employees = session.query(Employees).all()
    except:
        error = True
        print(sys.exc_info())
    finally:
        session.close()
    if not error:
        return render_template('index.html', employees=employees)
    else:
        flash('Error In Employee query {}')
        return render_template('index.html')


# this function to add new employee to the database
@app.route('/add_employee/<string:employee_code>/<string:employee_name>')
def add_employee(employee_code,employee_name):
    error = False
    try:
        new_employee = Employees(employee_code=employee_code,name=employee_name)
        session.add(new_employee)
        session.commit()
        empid = new_employee.id
    except:
        error = True
        print(sys.exc_info())
        session.rollback()
        message = 'Employee With Not Added'
    finally:
        session.close()

    if not error:
        message = 'New Employee Added id: %s' % empid
        return jsonify({'message':message})
    return jsonify({'message':'unkown_error'})




@app.route('/checkin', methods=['POST'])
def checkin():
    error = False
    accepted = False
    if request.method == 'POST':
        employee_code = '%s' % request.get_json()['code']
        try:
            # check if there is an open attendance request To Stop the adding process if found
            open_request = session.query(Atttendance).filter_by(employee_code=employee_code).filter_by(open=True).first()
            accepted = False
            print(open_request)
        except:
            accepted = True
            print('Accepted Value')
        finally:
            session.close()
        # if we did not found open request for that employee code so continue else return error
        if open_request == None:
            accepted = True
        else:
            return jsonify({'message':'You Already Checked In Please Check out Before Try again', 'status':'request duplicated'})

        try:
            employee = session.query(Employees).filter_by(employee_code=employee_code).first()
            employeeid = employee.id
            type = 'checkin'
            checkin_date = time_maker()['egypt_date']
            checkin_datetime = time_maker()['egypt_datetime']
            attended = True
        except:
            error = True
            print(sys.exc_info())
        finally:
            session.close()
        # add new attendance record if system found that employee
        if not error:
            try:
                new_atttendance = Atttendance(employee_code=employee_code,date=checkin_date,attended=attended,employee_id=employeeid)
                session.add(new_atttendance)
                session.commit()
                attend_id = new_atttendance.id
                print('New Attendance created %s ' % attend_id)
            except:
                print(sys.exc_info())
                session.rollback()
                error = True
            finally:
                session.close()
        else:
            return render_template('index.html', error='Could Not Add new Atttendance record For Employee ID: %s' % employee_code)
        # add new AtttendanceActions record if no errors found in adding attendance record

        if not error:
            try:
                new_actions = AtttendanceActions(date=checkin_datetime,type=type,atttendance_id=attend_id)
                session.add(new_actions)
                session.commit()
                action_id = new_actions.id
            except:
                print(sys.exc_info())
                session.rollback()
                error = True
                # if any errors in adding AtttendanceActions record rollback the session and Remove the attendance record
                # then return error message in JSOn format to AJAX client Side Function
                try:
                    record_to_remove = session.query(Atttendance).filter_by(id=attend_id).first().delete()
                    session.commit()
                except:
                    print(sys.exc_info())
                    session.rollback()
                    error = True
                finally:
                    session.close()
            finally:
                session.close()
        # to make sure 0 errors and not leave an open if
        else:
            return render_template('index.html', error='Could Not Add new Atttendance record For Employee ID: %s' % employee_code)
    # if no errors found Return Successfull Message to the AJAX Client Side Function in JSON format then Render it To User status = ok
    if not error:
        message = 'New Record Added In Atttendance: %s and New Record Added in AtttendanceActions: %s' %(attend_id, action_id)
        return jsonify({'message':message, 'status':'ok'})
    # if an error pass all the steps Will return an error Message and Status != ok
    else:
        message = 'Request Not Added After Click Checkin Or Out Please Wait Until system save the Recoreds'
        return jsonify({'message':message, 'status':'blocked 1 second'})


@app.route('/checkout', methods=['GET','POST'])
def checkout():
    error = False
    if request.method == 'POST':
        employee_code = '%s' % request.get_json()['code']
        try:
            open_request = session.query(Atttendance).filter_by(employee_code=employee_code).filter_by(open=True).first()
            attendance_id = open_request.id
            checkin_datetime = time_maker()['egypt_datetime']
            type = 'checkout'
            #y = test('2020-12-18 5:00:00 pm','2020-12-19 01:45:25 AM')
        except:
            error = True
            message = 'Please Check In First Before Check Out'
            print(sys.exc_info())
        finally:
            session.close()
        if error:
            return jsonify({'message':message, 'error':'No attendance request found'})
        else:
            try:
                new_actions = AtttendanceActions(date=checkin_datetime,type=type,atttendance_id=attendance_id)
                session.add(new_actions)
                session.commit()
                attendance_action_id = new_actions.id
                message = 'Successfull Created Checkout record.'
            except:
                error = True
                session.rollback()
                print(sys.exc_info())
                message = 'Could Not Create Record in AtttendanceActions'
            finally:
                session.close()
        if not error:
            try:
                open_request = session.query(Atttendance).filter_by(employee_code=employee_code).filter_by(open=True).first()

                mycheckin = session.query(AtttendanceActions).filter_by(atttendance_id=attendance_id).filter_by(type='checkin').first()
                mycheckout = session.query(AtttendanceActions).filter_by(atttendance_id=attendance_id).filter_by(type='checkout').first()
                x = str(mycheckin.date)
                y = str(mycheckout.date)
                the_duration = test(x, y)
                open_request.duration = the_duration
                open_request.open = False
                session.commit()
            except:
                error = True
                message = 'Can not update the open request'
            finally:
                session.close()
        if not error:
            return jsonify({'message':message, 'status':'ok'})
        else:
            return jsonify({'message':message, 'status':'error in update Atttendance  request'})

    return jsonify({'message':'Many Requests sent in less than a second', 'error':'blocked for 2 seconds'})


# --------------- Addon ---------------
# this normal Function return the history in ISO Format
@app.route('/get_history_ajax', methods=['POST','GET'])
def get_history_ajax():
    if request.method == 'POST':
        employee_code = '%s' % request.form.get('employee_code_history')
        error = False
        data = {'days':[]}
        try:
            atttendance_object = session.query(Atttendance).filter_by(employee_code=employee_code).all()
        except:
            print(sys.exc_info())
            error = True
        finally:
            session.close()
        if not error:
            for day in atttendance_object:
                actions = []
                date = day.date
                atttendance_actions_object  = session.query(AtttendanceActions).filter_by(atttendance_id=day.id).all()
                for action in atttendance_actions_object:
                    time_zone = pytz.timezone("Africa/Cairo")
                    iso_format = datetime.datetime.strptime(action.date, "%Y-%m-%d %H:%M:%S %p")
                    d = iso_format.replace(tzinfo=datetime.timezone.utc)
                    actions.append({'action':action.type, 'time':d.isoformat()})
                data['days'].append([date, actions])
            return jsonify(data)
        else:
            data['error'] = True
            return jsonify(data)



@app.route('/get_history_ajax1', methods=['POST','GET'])
def get_history_ajax1():
    if request.method == 'POST':
        employee_code = '%s' % request.form.get('employee_code_history1')
        error = False
        data = {'days':[]}
        try:
            atttendance_object = session.query(Atttendance).filter_by(employee_code=employee_code).all()
        except:
            print(sys.exc_info())
            error = True
        finally:
            session.close()
        if not error:
            for day in atttendance_object:
                actions = []
                date = day.date
                atttendance_actions_object  = session.query(AtttendanceActions).filter_by(atttendance_id=day.id).all()
                for action in atttendance_actions_object:
                    actions.append({'action':action.type, 'time':action.date})
                data['days'].append([date, actions])
            return jsonify(data)
        else:
            data['error'] = True
            return jsonify(data)



@app.route('/get_attendance1', methods=['POST','GET'])
def get_attendance1():
    if request.method == 'POST':
        employee_code = '%s' % request.form.get('employee_code_attendance')
        the_date = '%s' % request.form.get('the_date')
        error = False
        try:
             duration_object = session.query(Atttendance).filter_by(employee_code=employee_code).filter_by(date=the_date).first()
             duration_string = duration_object.duration
             attended = duration_object.attended
             answer = {'duration':duration_string,'attended':attended}
        except:
            print(sys.exc_info())
            error = True
            message = 'Can not Return duration for that Employee'
            answer = {'message':message}
        finally:
            session.close()
        if not error:
            return jsonify(answer)
        else:
            return jsonify(answer)


# this function to add new employee to the database
@app.route('/add_employee_normal', methods=['GET', 'POST'])
def add_employee_normal():
    if request.method == 'POST':
        employee_code = '%s' % request.form.get('employee_code_employee')
        employee_name = '%s' % request.form.get('employee_name')
        error = False
        try:
            check_employee_code = session.query(Employees).filter_by(employee_code=employee_code).first()
        except:
            message = 'Error In Query '
            error = True
        finally:
            session.close()
        if not error and check_employee_code == None:
            try:
                new_employee = Employees(employee_code=employee_code,name=employee_name)
                session.add(new_employee)
                session.commit()
                empid = new_employee.id
            except:
                error = True
                print(sys.exc_info())
                session.rollback()
                message = 'Employee With Not Added'
            finally:
                session.close()

            if not error:
                message = 'New Employee Added id: %s' % empid
                return jsonify({'message':message})
            return jsonify({'message':'unkown_error'})
        else:
            return jsonify({'message':'duplicated Employee Code %s' % employee_code})



if __name__ == '__main__':
    app.secret_key = 'S&Djry636qyye21777346%%^&&&#^$^^y___'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
