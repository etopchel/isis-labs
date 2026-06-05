the general description of the project is in the PROBLEM.md file

it actually consists of three parts
part 1 (lab 12) 
    - create scripts db/create_tables.sql and db/seed_data.sql for creating a new DB and tables insided and populating with the test data (invent around 20 students, 10 teachers, 10 styles, 5 groups, 7 programs, 20 lessons in the past + future)
    
    - write docs/project-vision.txt with "сформулировать цели ИС" in Russian, in a sort of bit more free style, not super neural, like a student's work

    - using `generate_usecase.py` make a diagram using the simplified PlantUML wrapper in the script according to the use cases described in this document later
    write the modified generate_usecase.py (you should only modify the generating part in the if __name__ == __main__ clause) as
    db/generate_usecase.py

    - similary to the previous point use generate_er.py to generate the ER diagram

    - create a flask rest API client similar to the one provided in `app.py` file that will be sufficient for working with our database and implementing all the use cases provided later in this document

    - test all the endpoints using curl (or other similar tool), ensure that it works properly and write curl prompts into tests/api-requests.txt or maybe api-requests.ps1 if it's convenient


postgres credentials:
    localhost, default port
    user: postgres
    password: 123


FLASK / other python modules:
    create a local virtual environment via venv
    and install any necessary modules via pip inside it

    prioritize the once given in the problem description
    Установите: pip install flask psycopg2-binary flask-cors
    if anything else is needed, don't hesitate to install it as well

general considerations:
    - don't write perfect code, stay as close as possible to the provided examples
    - write simple comments in russian
    - document any major step you make in PROGRESS.md
    - commit at each major step
    

my topic would be a system for a dance studio like
- teachers
- students
- dance programs
- lessons

So i've came up with the following Relational DB structure:

(use surrogate PKs everywhere)

user
    login
    password
    userType (student/teacher)

teacher
    name
    phone
    e-mail
    sex
    age
    userId (fk)

student
    name
    phone
    e-mail
    sex
    age
    userId (fk)

style
    name

group
    name
    ageFrom (may be null if it's for 0-18)
    ageTo (may be null if it's for 18+)
    style

student_group (many to many)

program
    name
    style
    track
    duration (mm:ss)

lesson (group - program many to many)
    groupid
    programid
    datetimeStart
    datetimeEnd



use case 1
    new user sign up
use case 2
    teacher signs in and edits her profile
use case 3
    student signs in and edits her profile
use case 4
    signed in teacher edits style table
use case 5
    signed in teacher creates a new group / edits existing group / deletes group / checks the group list 
use case 6
    signed in teacher adds/removes students from groups 
use case 7
    signed in student checks her group list and her group information
use case 8
    signed in teacher adds/removes/edits a program or checks the program list
use case 9
    signed in teacher adds/removes/edits a lesson or checks the lesson list, can implementet it as a calendar / or just a list filtered by the date
use case 10
    a signed in student checks their future/past lessons similarly to the teacher (based on the groups they're in)

so basically just CRUD operations on the described tables where
a student can only edit their personal information whereas teacher is more like teacher / administrator that can edit everything













