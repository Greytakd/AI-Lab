


print('Hello World')
print('What is your name?') #This is asking the name of the person if you can believe it
my_name = input('>')
"""
Multi Line Comment 
about my_name variable taking the users input
"""
print('Nice to meet you ' + my_name)

print('The length of your name is: ')
print(len(my_name))
print('What is your age?')
age = int(input('>'))
if age > 21:
     print('You stopped having fun ' + str(age - 21) + ' years ago.')
else:
     print("You can't have fun for another "+ str(21 - age) + ' years.')