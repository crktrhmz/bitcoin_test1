import hashlib
import re

log = 'start*'
def add_answer(log,str):
	mas=re.findall('(\d+)', str)
	mas=list(set(mas))#set mnogestvo v kotorom elementy ne mogut povtor
	for i in mas:
	    log+=(i+'-')
	log+='*'
	return log

print "Hello, my name is BitcoinTester !"
answer=raw_input("Are you Ready to Travel? ")
print answer
f = open('test.txt')
ques_counter=0
for line in f:
	line=line[0:-1]
	if len(line) == 0:#if empty answer suda
		ques_counter=0
		answer=raw_input ("Your answer: ")
		log=add_answer(log,answer)
		print "----------------------------"
		continue
	if ques_counter==0:		
		if line[0].isdigit():#if txt pered questins stoyat digital
			line=line[2:]#chto by eta tema raspoznavala ih as questions, pridumat' kak
		print line
	else:
		if line[0]=="\t":#in varyant we use tab
			line=line[1:]
		print str(ques_counter)+". "+line#counter is variant otveta
	ques_counter+=1



b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(n):
    l = []
    while n > 0:
        n, r = divmod(n, 58)
        l.insert(0,(b58_digits[r]))
    return ''.join(l)

def base58_decode(s):
    n = 0
    for ch in s:
        n *= 58
        digit = b58_digits.index(ch)
        n += digit
    return n

def base58_encode_padded(s):
    res = base58_encode(int('0x' + s.encode('hex'), 16))
    pad = 0
    for c in s:
        if c == chr(0):
            pad += 1
        else:
            break
    return b58_digits[0] * pad + res

def base58_decode_padded(s):
    pad = 0
    for c in s:
        if c == b58_digits[0]:
            pad += 1
        else:
            break
    h = '%x' % base58_decode(s)
    if len(h) % 2:
        h = '0' + h
    res = h.decode('hex')
    return chr(0) * pad + res

def dhash(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def base58_check_encode(s):
    check = dhash(s)[:4]
    return base58_encode_padded(s + check)

def base58_check_decode(s):
    k = base58_decode_padded(s)
    data, check0 = k[0:-4], k[-4:]
    check1 = dhash(data)[:4]
    if check0 != check1:
        raise BaseException('checksum error')
    return data


log+='end'
res=base58_check_encode(log)
print res
ans=base58_check_decode(res)
print ans


size=8
correct_all=0
correct_mas=size*[[]]
answers_mas=size*[[]]

f = open('correct_test.txt')

i=0
mas=[]
for line in f:
    line=line[0:-1]
    if len(line)==0 or line[0]=='#':
    	if len(mas)<1:
        	continue#IF EMPTY OR # WE CONTINUE LOOPING
        i+=1
        correct_mas[i]=mas
        mas=[]
        correct_mas[i].sort()
        continue
    if(line.isdigit()):
        mas+=line
        correct_all+=1#ANSWERS SORT v array do znaka #

pos=ans.find('start')#begin
if pos==-1:
    print 'Error'#if smestilos'
else:
    ans=ans[pos:]   
i=0
while len(ans)>0:
    pos=ans.find('*')+1
    ans=ans[pos:]
    print ans
    if ans.find('end')==0:
        break
    i+=1
    mas=[]
    if ans[0]=='*':
        continue
    while True:
        pos=ans.find('-')
        if ans[0:pos].isdigit():
            mas+=ans[0:pos]
        pos=ans.find('-')+1#loop through answers, if digit -> mas
        ans=ans[pos:]
        if ans[0]=='*':
            break
    answers_mas[i]=mas
    answers_mas[i].sort()

q = 0
print "YOUR ANSWER"
while q < len(answers_mas):
    print answers_mas[q]
    q+=1
q = 0
print "CORRECT ANSWER"
while q < len(correct_mas):
    print correct_mas[q]
    q+=1


correct_counter=0
for i in xrange(len(correct_mas)):
    for j in xrange(len(answers_mas[i])):
        if answers_mas[i][j] in correct_mas[i]:
            correct_counter+=1
        else:
            correct_counter-=2

print str(correct_counter)+'/'+str(correct_all)
print "Your Result is "+str((correct_counter*100)/correct_all)+'%'
