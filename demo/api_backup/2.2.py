#函数功能：域名解析查询
#注意：新增模块引用 dns.resolver  （pip install dnspython）
#路径：/Domain_name
#输入：
#   text = 输入域名 operator = 查询记录类别 A/CNAME/MX/TXT/NS
#返回：
#   成功：
#       {"code": 200, "result": result,'length':lenth}
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/Domain_name',methods=['get','post'])
def Domain_name():
	text = request.values.get('text')
	print text
	result = ''
	operator = request.values.get('operator')
	try:
		if(text and operator):
			if(operator=='A'):
				result0=dns.resolver.query(text,"A")
			elif(operator=='CNAME'):
				result0=dns.resolver.query(text,"CNAME")
			elif(operator=='MX'):
				result0=dns.resolver.query(text,"MX")
			elif(operator=='TXT'):
				result0=dns.resolver.query(text,"TXT")
			elif(operator=='NS'):
				result0=dns.resolver.query(text,"NS")
			for i in result0.response.answer:
				for j in i.items:
					result+=' '+j.to_text()
				print result
			resu = {'code': 200, 'result':result,'length':len(result)}
			return json.dumps(resu, ensure_ascii=False)
		else:
			resu = {'code': 10001, 'message': '参数不能为空！'}
			return json.dumps(resu, ensure_ascii=False)
	except:
		resu = {'code': 200, 'result':result,'length':len(result)}
		return json.dumps(resu, ensure_ascii=False)

#函数功能：各类rot编码的加解密
#注意：新增模块引用 string
#注意:ROT5：只对数字进行编码，将数字往前数的第5个数字替换当前数字，例如当前为0，编码后变成5，当前为1，编码后变成6。
#ROT13：只对字母进行编码，将字母往前数的第13个字母替换当前字母，例如当前为A，编码后变成N，当前为B，编码后变成O。
#ROT18：将ROT5和ROT13组合在一起，命名为ROT18。
#ROT47：对数字、字母、常用符号进行编码，按ASCII值进行位置替换，将字符ASCII值往前数的第47位对应字符替换当前字符，例如当前为小写字母z，编码后变成大写字母K，当前为数字0，编码后变成符号_。用于ROT47编码的字符其ASCII值范围是33－126，具体参考ASCII编码。
#路径：/Rot_ALL
#输入：
#   text = 输入字符串
#   operator=执行操作 [rot5encode,rot5decode,rot13encode,rot13decode,rot18encode,rot18decode,rot47encode,rot47decode]
#返回：
#   成功：
#       {"code": 200, "result": result,'length':结果长度}
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
def Rot5decode(strings):
	text=strings
	digits_dict = {}
	result=''
	digits = string.digits
	for i in range(len(digits)):
		digits_dict[digits[i]] = digits[i-5]  #建立字典
	for i in text:
		a=i
		if a.isdigit():
			a=digits_dict[i]
		result+=a
	return result		
def Rot13decode(strings):
	ascii_lowercase = string.ascii_lowercase   
	ascii_uppercase = string.ascii_uppercase  
	text=strings
	result=''
	lookup_dict = {}
	for i in range(len(ascii_uppercase)):
		lookup_dict[ascii_uppercase[i]] = ascii_uppercase[i-13]
	for i in range(len(ascii_lowercase)):
		lookup_dict[ascii_lowercase[i]] = ascii_lowercase[i-13]  #建立字典
	for i in text:
		a=i
		if a.isalpha():
			a=lookup_dict[a]
		result+=a
	return result

def Rot18decode(strings):
	text=strings
	text=Rot5decode(text)
	text=Rot13decode(text)
	return text

def Rot47decode(strings):
	text=strings
	result=''
	for i in text:
		a=i
		j=ord(i)
		if(j>=33 and j <=126):
			a=chr(33+((j+14)%94))
		result+=a
	return result	
@server.route('/Rot_ALL',methods=['get','post'])
def Rot_ALL():
	text = request.values.get('text')
	print text
	result = ''
	operator = request.values.get('operator')
	try:
		if(text and operator):
			print operator
			if(operator=='rot5encode' or operator=='rot5decode'):
				result=Rot5decode(text)
			elif(operator=='rot13encode' or operator=='rot13decode'):
				result=Rot13decode(text)
			elif(operator=='rot18encode' or operator=='rot18decode'):
				result=Rot18decode(text)
			elif(operator=='rot47encode' or operator=='rot47decode'):
				result=Rot47decode(text)
			resu = {'code': 200, 'result':result,'length':len(result)}
			return json.dumps(resu, ensure_ascii=False)
		else:
			resu = {'code': 10001, 'message': '参数不能为空！'}
			return json.dumps(resu, ensure_ascii=False)
	except:
		resu = {'code': 200, 'result':result,'length':len(result)}
		return json.dumps(resu, ensure_ascii=False)