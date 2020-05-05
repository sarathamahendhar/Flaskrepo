from db import db
from sqlalchemy import Column, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import relationship



class DEPARTMENT(db.Model):
    __tablename__ = 'DEPARTMENTS'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    students=relationship('STUDENT',lazy="dynamic")

    def __init__(self,name):
        self.name=name

    def json(self):
        return {"name":self.name,"id":self.id,"students":[i.stujson() for i in self.students.all()]}


    @classmethod
    def DeptList(cls):
        arr=DEPARTMENT.query.all()
        return {"items":[i.json() for i in arr]}


    @classmethod
    def getDepartment(cls,name):
        x=DEPARTMENT.query.filter_by(name=name).first()
        if x:
            return x.json()
        return None

    @classmethod
    def insertDepartment(cls,name):
        val=cls.getDepartment(name)
        if val:
            return {"status":"department Alredy exists please try other !!"}
        d=DEPARTMENT(name=name)
        db.session.add(d)
        db.session.commit()
        return {"status":"department inserted successfully !!"}
        


class STUDENT(db.Model):
    __tablename__ = 'STUDENTS'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    dept_id = Column(ForeignKey('DEPARTMENTS.id'))
    department = relationship('DEPARTMENT')

    def __init__(self,name,dept_id):
        self.name=name
        self.dept_id=dept_id
    
    def stujson(self):
        return {"name":self.name,"dept":self.dept_id}

    @classmethod
    def getStudent(cls,name):
        x= cls.query.filter_by(name=name).first()
        if x:
            return x.stujson()
        else:
            return None
        
    @classmethod
    def getStudentList(cls):
        print(cls.query.all())
        for i in cls.query.all():
            print (i.name)

        return list(map(lambda i: i.stujson() ,cls.query.all()))
        
    
    def postStudent(self):
        val=self.getStudent(self.name)
        db.session.add(self)
        db.session.commit()
        if val:
            return {"status":"updated successfully!!"}
        return {"status":"Inserted  successfully!!"}

    @classmethod
    def deleteStudent(cls,name):
        val=cls.query.filter_by(name=name).first()
        if val:
            db.session.delete(val)
            db.session.commit()
            return {"status":"deleted successfully!!"}
        return {"status":"No student to delete!!"}



    





    
