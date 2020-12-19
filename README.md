
# languages and frameworks and techniques:
Python3, HTML5, CSS3, ES6, Flask, Flask SQLAlchemy, Jinja2, AJAX(Fetch)

# Functions Count:
16 Functions

# Main Functions:
* add_employee(employee_code,employee_name)
* checkin()
* checkout()
* get_attendance(employee_code, date)
* get_history(employee_code)


# Routes Count:
13

## Index Route: 
localhost:5000/

## Routes Accept Get Request and Return JSON result None AJAX:
*
/add_employee/<string:employee_code>/<string:employee_name>
localhost:5000/add_employee/emp01/mahmoud

*
/get_history/<string:employee_code>
localhost:5000/get_history/emp01

*
/get_attendance/<string:employee_code>/<string:date>
localhost:5000//get_attendance/emp01/2020-12-19

*
/get_history_normal/<string:employee_code>
localhost:5000/get_history_normal/emp01


##### localhost:5000/api/employess
* return all Employess in the Database (backup and endpoit)

##### localhost:5000/api/atttendance
* return all atttendancein the Database (backup and endpoit)


##### localhost:5000/api/atttendance_actions
* return all atttendance_actions the Database (backup and endpoit)





##### Routes Accept POST Request Only AJAX IT work Via dashboar only:
/checkin
/checkout

handle all errors with AJAX and Fetch

* Cannot create checkout before check in and vice versa
* It is not possible to create 2Checkout or 2Checkout records without clicking Checkout or Check-in
* Each checkout record or check in is connected to attendance request
* Check In will create 2 records 1 Attendance record with open = True status and 1 Attendance Actions record with type check in (date in egypt format)
* Checkout will accept 1 parameter which is the employee code then it will search for the record with that code where type is open 
* and create checkout record in Attendance Actions table with date
* calculate the duration and update the Attendance record for that with open = False  and update The duration in the attendance record

