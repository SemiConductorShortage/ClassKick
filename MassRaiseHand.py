import ast
import requests


code = input ("Class Code:  ")

classcode = "https://services.classkick.com/v1/class-codes/"+code+"/usernames"
e = requests.get(classcode)
print(e)
e = e.content
print(e)
e = e.decode()
print(e)
e = e.split(',"hide_student_work"')
e = e[0]
e = e.split('"names":')
e = e[1]
e=str(e)
e = ast.literal_eval(e)

for i in range(0,len(e)):
    studentname = e[i]
    print(studentname)
    data={
       "class_code":code,
       "name":studentname
       }
    Hook = requests.post("https://services.classkick.com/v1/users/login/anonymous-student", json={"class_code":code, "name":studentname})
    token = Hook.text.split("token\":\"")[1].split("\"}")[0]
    print("Hook Token:  "+token)
    headers = {
    "authorization": "Bearer "+token
    }
    rosterid = Hook.text.split("roster_id\":\"")[1].split("\"")[0]
    assignmentid = Hook.text.split("assignment_id\":\"")[1].split("\"")[0]



    
    
    CodeTitle = requests.post("https://services.classkick.com/v1/assignment-works", json={"assignment_id":assignmentid, "roster_id":rosterid}, headers=headers)


    idAssignmentWorks = CodeTitle.text.split("id\":\"")[1].split("\"")[0]

    assignment = CodeTitle.text
    print(assignment)
    question_id = assignment.split("chat_id")[1]
    print(question_id)
    question_id = question_id.split("}")[1]
    print("QID: "+question_id)
    question_id = question_id.split("\":{\"element_list")[0]
    question_id = question_id.split(",\"")[1]
    print("NEW QID:  "+question_id)

    

    

    


    requests.post("https://services.classkick.com/v1/help-requests", json={"roster_id":rosterid,"assignment_id":assignmentid,"question_id":question_id,"request_type":"help"}, headers=headers)