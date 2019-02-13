#animals = open('animals.txt', 'r')

#animals.write('elephant\n')
#text = animals.read()
#print text
#animals.seek(0)

#for animal in animals:
#	if animal[0] in 'AEIOUaeiou':
#		print '{} starts with a vowel'.format(animal)
#		print animal[0]
#	else:
#		print '{} starts with a consonant'.format(animal)
#		print animal[0]


#animals.close()


list3 = [1,2,[3,4,'hello']]

print(list3)

list3[2][2] = 'goodbye'
print(list3)