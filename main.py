import threading
import time
import random as r # is used only to assign random time for teaching

mutex = 1 # will handle whether the teacher is free or not i.e binary semaphore
semaphore = 3 # will handle no of chairs i.e counting semaphore

chairs = []
n = 10 # total no. of students that will visit teacher on that day

students = [x for x in range(1,n+1)]

count = 0
turn = None # which student is the teacher currently teaching

def wait(x):
    "function for synchronization"
    if(x == 0):
        return x
    else:
        return x - 1
    
def signal(x):
    "function for synchronization"
    return x+1

def teacher_teaching_or_sleeping():
    global mutex, semaphore, chairs, students, turn
    i = 0
    while(i < n): # while(True): replace if infinite looping is needed
#         print(chairs)
        if(mutex == 0):
            duration = r.randint(2,5) # teacher will teach each student for some random time
            print('*'*100)
            print()
            print(f"Teacher is teaching Student {turn} for {duration} secs ||| mutex = {mutex} semaphore = {semaphore} ||| students on chair = {chairs}")
            print()
            print('*'*100)
            
            time.sleep(duration) # else duration = 2
            # mutex = 1
            mutex = signal(mutex)
            
            print(f"Student {turn} left....")
            
            i += 1
            
            
            try:
                if(chairs[0]):
                    turn = chairs[0]
                    # mutex = 0
                    mutex = wait(mutex)
                    
            except Exception:
                turn = None
            else:
                del chairs[0]
                semaphore += 1
            
        else:
            print(f"Teacher is sleeping because mutex = {mutex} and semaphore = {semaphore}")
        
        time.sleep(2)
    
    print(f"Teacher is sleeping because mutex = {mutex} and semaphore = {semaphore}")

def student_enters():
    global mutex, semaphore, count, turn
    
    while(count < n): # while(count < n) # replace if infinite loop is not required
        try:
            print(f"Student {students[count]} enters")
        except Exception:
            pass
        
        
            
        if(mutex == 1 and semaphore == 3):
            # mutex = 0
            mutex = wait(mutex)
            
            turn = students[count]
            count += 1
            print(f"Student {turn} woke teacher".upper().center(100,'-'))
            
        elif(mutex == 0 and semaphore <=3 and semaphore != 0):
            semaphore -= 1
            
            chairs.append(students[count])
            
            count += 1
#           
#             print(f"students on chairs = {chairs}")
        elif(semaphore == 0):
            try:
                print(f"\nStudent {students[count]} please come after sometime as there is no place to sit. Chairs are occupied by students = ", chairs)
            except Exception:
                pass
        time.sleep(1)
        
        
t1 = threading.Thread(target=teacher_teaching_or_sleeping)
t2 = threading.Thread(target=student_enters)

t1.start()
t2.start()