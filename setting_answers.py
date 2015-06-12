import re

######################GLOBAL
answer = ''

f = open('test.txt')
f2 = open('correct_test.txt', 'wb')
ques_counter=0
for line in f:
    line=line[0:-1]
    if len(line) == 0:#if empty answer suda
        ques_counter=0
        answer = raw_input("Your answer:")
        mas = re.findall('(\d+)',answer)
        for i in mas:
            f2.writelines(i+'\n')
        print "----------------------------"
        continue
    if ques_counter == 0:
        if line[0].isdigit():
            f2.writelines('#'+line+'\n')
            line = line[2:]
        print line
    else:
        if line[0]=="\t":
            line=line[1:]
        print str(ques_counter)+". "+line
    ques_counter+=1
f.close()
f2.close()