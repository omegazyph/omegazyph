'''this is a secunity risk because a
a person can input a malicious script
and it will get executed'''


print('\n')
expression = input('Enter an arithmetic expression: ')

result = eval(expression)
print("Result is: ", result)