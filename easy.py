#I.	Write a Python statement that reads an exam score from the user, converts it to an integer, and stores it in a variable called score.
#II.	Write an if-elif-else block that assigns a letter grade based on the score:  90–100 = 'A'  |  80–89 = 'B'  |  70–79 = 'C'  |  60–69 = 'D'  |  below 60 = 'F' Also print: 'Pass' if grade is A, B, or C, otherwise print 'Fail'.
#III.	Explain what would happen if the elif score >= 60 condition was placed BEFORE the elif score >= 90 condition in your chain. Why does ordering matter in an if-elif-else structure?
#IV.	Explain the concept of inheritance in object-oriented programming. Give a real-world analogy and a Python code example showing a parent class Animal and a subclass Dog that inherits from it. The Dog subclass must override at least one method.
#V.	Explain polymorphism >in object-oriented programming. Write a code example showing a function process_shape(shape) that works correctly with both a Circle and a Rectangle through polymorphism, without using isinstance() or type() checks inside the function.

        
    
score = int(input("What did you get in your last exam?:"))
if score > 100 or score < 0:
    print("Please enter a valid score ")
    else score => 90:
        
