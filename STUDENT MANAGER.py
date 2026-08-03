student = {}


while True:
    print("\n-----STUDENT MANGER APP -----")
    print("1.ADD Students")
    print("2.View Students")
    print("3.Check Result")
    print("4.Exit")


    choice = int(input("Enter your choice : "))

    # Add students
    if choice == 1:
        name = input ("Enter Your name: ")
        marks = int(input("Enter marks: "))
        student[name] = marks 
        print(f"{name} Successfully added!")


    #View students 
    elif choice == 2:
        if not student:
            print("No student found!")
        else :
            for name, marks in student.items():
                print(name,":",marks)
    #check result 
    elif choice == 3:
        name = input ("Enter Student name :")

        if name in student:
            name = student[name]


            if marks >= 40 :
                print("PASS")
            else:
                print("FAIL")
        else:
            print("Student not fount! ") 

    #Exit               
    elif choice == 4:
        print("Exiting......!")
        break

    else :
        print("Tnvalid Input...!")


    print("-----ALL SET-----")
          

    


