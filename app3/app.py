from flask import Flask
from flask_restful import Api,Resource,reqparse
from models.student import STUDENT,DEPARTMENT


app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


@app.before_first_request
def createdatabse():
    db.create_all()


class StudentResource(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('dept_id',required=True,help="Please pass the departmnet ")

    def get(self,name):
        stu=STUDENT.getStudent(name)
        if stu :
            return stu
        return{"status":"Student not found!!"}
        
    def post(self,name):
        data=StudentResource.parser.parse_args()
        data['name']=name
        s=STUDENT(data['name'],data['dept_id'])
        stu=s.postStudent()
        return stu

    def delete(self,name):
        s=STUDENT.deleteStudent(name)
        return s

class DepartmentResource(Resource):
    def get(self,name):
        dept=DEPARTMENT.getDepartment(name)
        if dept:
            return dept
        return{"status":"Department not found!!"}
    def post(self,name):
        dept=DEPARTMENT(name)
        x=dept.insertDepartment(name)
        return x

class studentList(Resource):
      def get(self):
        return STUDENT.getStudentList()

class DepartmentList(Resource):
    def get(self):
        x= DEPARTMENT.DeptList()
        if x:
            return x
        return {"items":"No data found!!"}


api.add_resource(StudentResource,"/student/<string:name>")
api.add_resource(DepartmentResource,"/department/<string:name>")
api.add_resource(studentList,'/students')
api.add_resource(DepartmentList,'/depts')


if __name__=="__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)

