import flask, json,urllib,gmpy2
from flask import render_template
import base64,base58,base91,base36,base62
#62->pip install pybase62
from flask import request




'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
登录接口，需要传url、username、passwd
'''
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)

@server.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')


#aaa  = flask.Flask(__name__)

# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式
@server.route('/login', methods=['get', 'post'])
def login():
    # 获取通过url请求传参的数据
    username = request.values.get('name')
    # 获取url请求传的密码，明文
    pwd = request.values.get('pwd')
    # 判断用户名、密码都不为空，如果不传用户名、密码则username和pwd为None
    if username and pwd:
        if username == 'xiaoming' and pwd == '111':
            resu = {'code': 200, 'message': '登录成功'}
            return json.dumps(resu, ensure_ascii=False)  # 将字典转换为json串, json是字符串
        else:
            resu = {'code': -1, 'message': '账号密码错误'}
            return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {'code': 10001, 'message': '参数不能为空！'}
        return json.dumps(resu, ensure_ascii=False)

@server.route('/base_all', methods=['get', 'post'])
#函数功能：base全家桶
#路径：/base_all
#输入：
#   text = 输入字符串
#   num_of_base = 需要加解密的类型      [64，32，58，91，36，62，85]
#   encode_or_decode = 选择加密或者解密 [encode,decode]
#返回：
#   成功：
#       加密{'code': 200, 'result':加密结果,'lenth':长度 }
#       解密{'code': 200, 'result':解密结果 ，'lenth':长度 }
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       字符集错误{'code': 10000, 'message':'输入字符集错误。' }
def base_all():
    cypher_text=''
    plain_text=''
    text=request.values.get('text')              #输入字符串
    num_of_base=request.values.get('num_of_base')   #输入base（num），即base的类型
    encode_or_decode=request.values.get('encode_or_decode')   #加密或者解密
    try:
        if text and num_of_base and encode_or_decode:
            if encode_or_decode == 'encode': #加密算法
                plain_text=text.encode(encoding='utf-8')
                if num_of_base == '64':
                    cypher_text=base64.b64encode(plain_text)
                elif num_of_base == '32':
                    cypher_text=base64.b32encode(plain_text)
                elif num_of_base == '58':
                    cypher_text=base58.b58encode(plain_text)
                elif num_of_base == '91':
                    cypher_text = base91.encode(plain_text)
                # elif num_of_base == '92':
                #     cypher_text = base92.encode(plain_text)
                elif num_of_base=='36':
                    cypher_text = base36.loads(plain_text)
                # elif num_of_base=='16':
                #     cypher_text = hex(plain_text)
                elif num_of_base=='62':
                    cypher_text=base62.encodebytes(plain_text)
                elif num_of_base=='85':
                    cypher_text=base64.a85encode(plain_text)
                if type(cypher_text) == bytes:
                    resu = {'code': 200, 'result':cypher_text.decode('utf-8') ,'length':len(cypher_text.decode('utf-8'))}#如果输出是字节流格式
                else:
                    resu = {'code': 200, 'result': cypher_text,'length':len(cypher_text)}  #如果输出是字符串形式
                return json.dumps(resu, ensure_ascii=False)
            elif encode_or_decode=='decode': #解密算法
                cypher_text=text
                if num_of_base == '64':
                    plain_text=base64.b64decode(cypher_text)
                elif num_of_base == '32':
                    plain_text=base64.b32decode(cypher_text)
                elif num_of_base == '58':
                    plain_text=base58.b58decode(cypher_text)
                elif num_of_base == '91':
                    plain_text = base91.decode(cypher_text)
                # elif num_of_base == '92':
                #     plain_text = base92.decode(cypher_text)
                elif num_of_base=='36':
                    plain_text= base36.dumps(cypher_text)
                # elif num_of_base=='16':
                #     plain_text = int(cypher_text)
                elif num_of_base=='62':
                    plain_text=base62.decodebytes(cypher_text)
                elif num_of_base=='85':
                    plain_text=base64.a85decode(cypher_text)
                if type(plain_text) == bytes:
                    resu = {'code': 200, 'result': plain_text.decode('utf-8'),'length':len(plain_text.decode('utf-8'))}  # 如果输出是字节流格式
                else:
                    resu = {'code': 200, 'result': plain_text,'length':len(plain_text)}  # 如果输出是字符串形式
                #resu = {'code': 200, 'cypher_text':plain_text.decode('utf-8') }
                return json.dumps(resu, ensure_ascii=False)

        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except :
        resu = {'code': 10000, 'message':'输入字符集错误。' }
        return json.dumps(resu, ensure_ascii=False)
#函数功能：进制转化
#路径：/base_change_all
#输入：
#   begin_text = 输入字符串
#   begin_base = 原进制     [2，8，16，10]
#   destination = 结果进制 [2，8，16，10]
#返回：
#   成功：
#       {'code': 200, 'destination_text': 结果,'length':结果长度}
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       字符集错误{'code': 10000, 'message':'输入字符不符合当前进制字符集。' }
@server.route('/base_change_all',methods=['get','post'])
def base_change_all():
    begin_base = request.values.get('begin_base')
    destination_base=request.values.get('destination_base')
    begin_text = request.values.get('begin_text')
    destination_text=''
    try:
        if begin_base and destination_base and begin_text:
                if begin_base == '10':
                    begin_text=int(begin_text)
                    if destination_base=='2':
                        destination_text=bin(begin_text)
                        destination_text=destination_text[2:]
                    elif destination_base=='8':
                        destination_text=oct(begin_text)
                        destination_text = destination_text[2:]
                    elif destination_base=='16':
                        destination_text=hex(begin_text)
                        destination_text = destination_text[2:]
                elif begin_base =='8':
                    if destination_base=='10':
                        destination_text=int(begin_text,8)
                    elif destination_base=='2':
                        destination_text = bin(int(begin_text, 8))[2:]
                    elif destination_base=='16':
                        destination_text=hex(int(begin_text,8))[2:]
                elif begin_base =='2':
                    if destination_base=='10':
                        destination_text=int(begin_text,2)
                    elif destination_base=='8':
                        destination_text = oct(int(begin_text, 2))[2:]
                    elif destination_base=='16':
                        destination_text=hex(int(begin_text,2))[2:]
                elif begin_base == '16':
                    if destination_base=='10':
                        destination_text=int(begin_text,16)
                    elif destination_base=='8':
                        destination_text = oct(int(begin_text, 16))[2:]
                    elif destination_base=='2':
                        destination_text=bin(int(begin_text,16))[2:]
                resu = {'code': 200, 'destination_text': destination_text,'length':len(destination_text)}
                return json.dumps(resu, ensure_ascii=False)

        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10000, 'message': '输入字符不符合当前进制字符集。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：ascii与str互转
#注意十六进制或十进制转str时输入格式为12 34 56 78 ，每个参数中间用空格隔开
#路径：/ascii_str
#输入：
#   text = 输入字符串
#   operator =你想要执行的操作[16进制的ascii转字符串：hex_ascii_to_str,10进制ascii转字符串：dec_ascii_to_str,字符串转16进制ascii：str_to_hex_ascii,字符串转16进制ascii:str_to_hex_ascii]
#返回：
#   成功：
#       {'code': 200, 'result': 结果}
#   失败：
#       输入不可见字符集{'code': 10000, 'message': '请输入可见字符。'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/ascii_str',methods=['get','post'])
def ascii_str():
    text=request.values.get('text')
    operator=request.values.get('operator')
    result=''
    s=[]
    try:
        if text and operator:
            if operator == 'hex_ascii_to_str':
                for i in text:
                    if ord(i) not in range(32, 255):
                        resu = {'code': 10000, 'message': '请输入可见字符。'}
                        return json.dumps(resu, ensure_ascii=False)
                    result+=hex(ord(i))[2:]+' '
            elif operator == 'dec_ascii_to_str':
                for i in text:
                    if ord(i) not in range(32, 255):
                        resu = {'code': 10000, 'message': '请输入可见字符。'}
                        return json.dumps(resu, ensure_ascii=False)
                    result+=str(ord(i))+' '
            elif operator == 'str_to_hex_ascii':   #输入格式为12 34 56 78
                s=text.split(' ')
                for i in s:
                    i='0x'+i
                    if int(i,16) not in range(32, 255):
                        resu = {'code': 10000, 'message': '请输入可见字符。'}
                        return json.dumps(resu, ensure_ascii=False)
                    result+= chr(int(i,16))
            elif operator == 'str_to_dec_ascii':
                s=text.split(' ')
                for i in s:
                    if int(i) not in range(32, 255):
                        resu = {'code': 10000, 'message': '请输入可见字符。'}
                        return json.dumps(resu, ensure_ascii=False)
                    result += chr(int(i))
            resu = {'code': 200, 'result': result}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：凯撒密码加解密
#注意：加密解密过程是一样的
#路径：/caesar_cipher
#输入：
#   text = 输入字符串 （对非字母进行操作，只显示原字符累加操作）
#返回：
#   成功：
#       {'code': 200, 'result_arr': {"0": "位移0位的结果：liyiyi1"，"1": "位移1位的结果：mjzjzj2"}}
#   失败：
#       输入不可见字符集{'code': 10000, 'message': '请输入可见字符。'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/caesar_cipher',methods=['get','post'])
def caesar_cipher():
    text=request.values.get('text')
    result={}
    for i in text:
        if ord(i) not in range(32, 255):
            resu = {'code': 10000, 'message': '请输入可见字符。'}
            return json.dumps(resu, ensure_ascii=False)
    try:
        if text :
            for i in range(0,26):
                result[i] = '位移' + str(i) + '位的结果：'
                for each in text:
                    if each>='a' and each<='z':
                        result[i]+=chr((ord(each)-ord('a')+i)%26+ord('a'))
                    elif each>='A' and each<='Z':
                        result[i]+=chr((ord(each)-ord('A')+i)%26+ord('A'))
                    else:
                        result[i] += chr((ord(each)+i))

            resu = {'code': 200, 'result_arr':result}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)

    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：栅栏密码解密
#注意：无
#路径：/fence
#输入：
#   text = 输入字符串 （对非字母进行操作，只显示原字符累加操作）
#返回：
#   成功：
#       {"code": 200, "result": {"分2栏:": "flag{nideyangzi}", "分4栏:": "fa{ieagilgndynz}", "分8栏:": "f{eglnyzaiaigdn}"}}
#   失败：
#       输入不可见字符集{'code': 10000, 'message': '请输入可见字符。'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/fence',methods=['get','post'])
def fence():
    text = request.values.get('text')
    key = 0
    result={}
    # 小于间隔继续
    try:
        if text :
            for i in text:
                if ord(i) not in range(32, 255):
                    resu = {'code': 10000, 'message': '请输入可见字符。'}
                    return json.dumps(resu, ensure_ascii=False)
            for space in range(2,len(text)):
                if len(text) % space ==0:
                    key=0
                    strr=''
                    print(space)
                    while key < space:
                        for i in range(0, len(text), space):
                            # 不能越界
                            #j='分'+str(space)+'栏：'
                            if (i + key) < len(text):
                                strr+=text[i+key]
                        index='分'+str(space)+'栏:'
                        result[index]=strr
                        key = key + 1
            resu = {'code': 200, 'result': result}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)
#函数功能：培根密码解密
#注意：明文默认为小写
#路径：/bacon
#输入：
#   text = 输入字符串 （只对ab进行操作）
#返回：
#   成功：
#       {"code": 200, "result": "flag"}
#   失败：
#       参数错误{'code': 10003, 'message': '参数错误（不能输入AB（ab）以外的值）'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/bacon',methods=['get','post'])
def bacon():
    text = request.values.get('text')
    new=''
    lists = []
    # 分割，五个一组
    result = ''
    try:
        if text :
            letters2 = [
                'a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z',
            ]

            cipher2 = [
                "AAAAA", "AAAAB", "AAABA", "AAABB", "AABAA", "AABAB", "AABBA",
                "AABBB", "ABAAA", "ABAAA", "ABAAB", "ABABA", "ABABB", "ABBAA",
                "ABBAB", "ABBBA", "ABBBB", "BAAAA", "BAAAB", "BAABA",
                "BAABB", "BAABB", "BABAA", "BABAB", "BABBA", "BABBB",
            ]

            for i in text:
                if i != 'a' and i != 'b' and i!='A' and i!='B':
                    resu = {'code': 10003, 'message': '参数错误（不能输入AB（ab）以外的值）'}
                    return json.dumps(resu, ensure_ascii=False)
                elif i == 'a':
                    i = 'A'
                elif i == 'b':
                    i = 'B'

                new += i
                text = new

            for i in range(0, len(text), 5):
                lists.append(text[i:i + 5])
            # print(lists)
            # 循环匹配，得到下标，对应下标即可
            for i in range(0, len(lists)):
                for j in range(0, 26):
                    if lists[i] == cipher2[j]:
                        result += letters2[j]
            resu = {'code': 200, 'result': result,'length':len(result)}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：摩尔斯密码加解密
#注意：密文默认大写输出
#路径：/bacon
#输入：
#   text = 输入字符串
#   operator=执行操作 [encode,decode]
#返回：
#   成功：
#       {"code": 200, "result": result,'length':结果长度}
#   失败：
#       参数错误{'code': 9999, 'message': '输入字符不符合当前解密字符集。'}
#       参数错误{'code': 10000, 'message': '输入字符不符合当前加密字符集。'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/morse',methods=['get','post'])
def morse():
    text = request.values.get('text')
    result = ''
    operator = request.values.get('operator')
    try:
        if text and operator:
            dict1 = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
                    '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
                    '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
                    '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
                    '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0', '..--..': '?', '-..-.': '/',
                    '-.--.-': '()', '-....-': '-', '.-.-.-': '.'};
            dict2 = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                     'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                     'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                     'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
                     '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', '?': '..--..', '/': '-..-.',
                     '()': '-.--.-', '-': '-....-', '.': '.-.-.-'};
            if operator == 'decode':
                for i in text:
                    if i != '.' and i != '-' and i != ' ':
                        resu = {'code': 9999, 'message': '输入字符不符合当前解密字符集。'}
                        return json.dumps(resu, ensure_ascii=False)
                s = text.split(" ")
                for item in s:
                    result += dict1[item]
            elif operator == 'encode':
                for i in text:
                    if i not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
                                 '8', '9', '?', '/', '()', '-', '.']:
                        resu = {'code': 10000, 'message': '输入字符不符合当前加密字符集。'}
                        return json.dumps(resu, ensure_ascii=False)
                for item in text:
                    if i>='a' and i<='z':
                        i=chr(ord(item-32))
                    result+=dict2[item]+' '
            resu = {'code': 200, 'result':result,'length':len(result)}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：字符串反转
#注意：
#路径：/reverse
#输入：
#   text = 输入字符串
#返回：
#   成功：
#       {'code': 200, 'result': result,'length':结果字符串长度}
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/reverse',methods=['get','post'])
def reverse():
    text = request.values.get('text')
    result=''
    try:
        if text:
            result=text[::-1]
            resu = {'code': 200, 'result': result,'length':len(text)}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：Url编码加解密
#注意：
#路径：/url_code
#输入：
#   text = 输入字符串
#   operator=执行操作 [encode,decode]
#返回：
#   成功：
#       {'code': 200, 'result': result,'length':结果字符串长度}
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常,可能是输入字符集错误造成的。。' }
@server.route('/url_code',methods=['get','post'])
def url_code():
    text = request.values.get('text')
    operator=request.values.get('operator')
    result=''
    try:
        if text and operator:
            if operator == 'encode':
                result = urllib.quote(text)
            elif operator == 'decode':
                result = urllib.unquote(text)
            resu = {'code': 200, 'result': result,'length':len(result)}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常,可能是输入字符集错误造成的。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：rsa加解密
#注意：
#路径：/rsa
#输入：
#   p = 素数参数1
#   q = 素数参数2
#   e = 公钥
#   operator=执行操作 [encode,decode]：
#          encode情况下额外输入m = 明文
#          decode情况下额外输入c = 密文
#返回：
#   成功：
#       decode{'code': 200, 'm': 明文,'d':私钥}
#       encode{'code': 201, 'c': 密文}
#   失败：
#       素数{'code': 9999, 'message':'p和q必须是素数'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常,可能是输入字符集错误造成的。。' }
@server.route('/rsa',methods=['get','post'])
def rsa():

    p = gmpy2.mpz(int(request.values.get('p')))
   # print(p)
    q =  gmpy2.mpz(int(request.values.get('q')))
    e =  gmpy2.mpz(int(request.values.get('e')))
    operator=request.values.get('operator')
    try:
        if p and q and e and operator:
            if not gmpy2.is_prime(p) or not gmpy2.is_prime(q):
                resu = {'code': 9999, 'message':'p和q必须是素数'}
                return json.dumps(resu, ensure_ascii=False)
            n=gmpy2.mul(p,q)
            if operator == 'decode':
                c = gmpy2.mpz(int(request.values.get('c')))
                phi_n=gmpy2.mul(gmpy2.sub(p,1),gmpy2.sub(q,1))
                d = gmpy2.invert(e, phi_n)  # private key
                m = gmpy2.powmod(c, d, n)
                print(m)
                print(d)
                resu = {'code': 200, 'm': str(m),'d':str(d)}
                return json.dumps(resu, ensure_ascii=False)
            elif operator=='encode':
                m=gmpy2.mpz(int(request.values.get('m')))
                c=gmpy2.powmod(m,e,n)
                resu = {'code': 201, 'c': str(c)}
                return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：大整数运算
#注意：
#路径：/big_num
#输入：
#    p=第一个参数
#    q=第二个参数
#    n=第三个参数
#    operator=选择的操作 [isPrime,FACT,MULMN,POWMN,ADD,SUB,MUL,DIV,MOD,POW,GCD,LCM,OR,AND,XOR,SHL,SHR]
#返回：
#   成功：
#       {'code': 200, 'result':结果}
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常！' }
@server.route('/big_num',methods=['get','post'])
def big_num():
    operator = request.values.get('operator')
    result='1'

    try:
        if operator == 'FACT'or operator =='isPrime':
            p = gmpy2.mpz(int(request.values.get('p')))
            if not p:
                resu = {'code': 10001, 'message': '参数不能为空！'}
                return json.dumps(resu, ensure_ascii=False)
            if operator=='FACT':  #p的阶层
                result=gmpy2.fac(p)
            elif operator=='isPrime': #判断p是否是素数
                result=gmpy2.is_prime(p)
        elif operator =='MULMN' or operator =='POWMN':
            p = gmpy2.mpz(int(request.values.get('p')))
            q = gmpy2.mpz(int(request.values.get('q')))
            n = gmpy2.mpz(int(request.values.get('n')))
            if not p and not q and not n:
                resu = {'code': 10001, 'message': '参数不能为空！'}
                return json.dumps(resu, ensure_ascii=False)
            if operator == 'POWMN': #计算p**q mod n
                result=gmpy2.powmod(p,q,n)
            elif operator == 'MULMN':#计算p*q mod n
                result=gmpy2.modf(gmpy2.mul(p,q),n)
        else:
            p = gmpy2.mpz(int(request.values.get('p')))
            q = gmpy2.mpz(int(request.values.get('q')))
            if not p and not q :
                resu = {'code': 10001, 'message': '参数不能为空！'}
                return json.dumps(resu, ensure_ascii=False)
            if operator == 'ADD':#相加
                print('good')
                result=gmpy2.add(p,q)
            elif operator=='SUB':#相减
                result=gmpy2.sub(p,q)
            elif operator=='MUL':#相乘
                result=gmpy2.mul(p,q)
            elif operator=='DIV':#相除
                result=gmpy2.div(p,q)
            elif operator=='MOD':#取余
                result=gmpy2.f_mod(p,q)
            elif operator=='POW':
                result=gmpy2.powmod(p,q)
            elif operator=='GCD':#最大公因数
                result=gmpy2.gcd(p,q)
            elif operator=='LCM':
                result=gmpy2.lcm(p,q)
            elif operator=='OR':#或
                result=p | q
            elif operator=='AND':#与
                result=p & q
            elif operator=='XOR':#抑或
                result=p ^ q
            elif operator=='SHL':#左移
                result=p<<q
            elif operator=='SHR':#右移
                result=p>>q
        resu = {'code': 200, 'result': str(result)}
        return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)

#函数功能：键盘密码加解密Qwerty
#注意：密文默认大写输出,使用键盘qwerty..分别映射abcdef..
#路径：/Keyboard_A
#输入：
#   text = 输入字符串
#   operator=执行操作 [encode,decode]
#返回：
#   成功：
#       {"code": 200, "result": result,'length':结果长度}
#   失败：
#       参数错误{'code': 9999, 'message': '输入字符不符合当前解密字符集。'}
#       参数错误{'code': 10000, 'message': '输入字符不符合当前加密字符集。'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/Keyboard_A',methods=['get','post'])
def Keyboard_A():
    text = request.values.get('text')
    result = ''
    operator = request.values.get('operator')
    try:
        if text and operator:
            letter1 = {
            'q': 'a', 'w': 'b', 'e': 'c', 'r': 'd', 't': 'e', 'y': 'f', 'u': 'g',
            'i': 'h', 'o': 'i', 'p': 'j', 'a': 'k', 's': 'l', 'd': 'm', 'f': 'n',
            'g': 'o', 'h': 'p', 'j': 'q', 'k': 'r', 'l': 's', 'z': 't',
            'x': 'u', 'c': 'v', 'v': 'w', 'b': 'x', 'n': 'y', 'm': 'z',
            'Q': 'A', 'W': 'B', 'E': 'C', 'R': 'D', 'T': 'E', 'Y': 'F', 'U': 'G',
            'I': 'H', 'O': 'I', 'P': 'J', 'A': 'K', 'S': 'L', 'D': 'M', 'F': 'N',
            'G': 'O', 'H': 'P', 'J': 'Q', 'K': 'R', 'L': 'S', 'Z': 'T',
            'X': 'U', 'C': 'V', 'V': 'W', 'B': 'X', 'N': 'Y', 'M': 'Z',
            }
            letter2 = {
            'A': 'Q', 'C': 'E', 'B': 'W', 'E': 'T', 'D': 'R', 'G': 'U', 'F': 'Y', 'I': 'O',
            'H': 'I', 'K': 'A', 'J': 'P', 'M': 'D', 'L': 'S', 'O': 'G', 'N': 'F', 'Q': 'J',
            'P': 'H', 'S': 'L', 'R': 'K', 'U': 'X', 'T': 'Z', 'W': 'V', 'V': 'C', 'Y': 'N',
            'X': 'B', 'Z': 'M', 'a': 'q', 'c': 'e', 'b': 'w', 'e': 't', 'd': 'r', 'g': 'u',
            'f': 'y', 'i': 'o', 'h': 'i', 'k': 'a', 'j': 'p', 'm': 'd', 'l': 's', 'o': 'g',
            'n': 'f', 'q': 'j', 'p': 'h', 's': 'l', 'r': 'k', 'u': 'x', 't': 'z', 'w': 'v',
            'v': 'c', 'y': 'n', 'x': 'b', 'z': 'm'}
            if operator == 'decode':
                for i in text:
                    if (i<'a' or i>'z') and (i<'A' or i>'z')and i !=' ':
                        resu = {'code': 9999, 'message': '输入字符不符合当前解密字符集。'}
                        return json.dumps(resu, ensure_ascii=False)
                s = text.split(" ")
                for item in s:
                    result += letter1[item]
            elif operator == 'encode':
                for i in text:
                    if (i<'a' or i>'z') and (i<'A' or i>'z') :
                        resu = {'code': 10000, 'message': '输入字符不符合当前加密字符集。'}
                        return json.dumps(resu, ensure_ascii=False)
                for item in text:
                    result+=letter2[item]+' '
            resu = {'code': 200, 'result':result,'length':len(result)}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)


#函数功能：键盘密码加解密B
#注意：WERTYUIO分别映射到9键键盘的数字键 密文重复次数及9键键盘对应按键的第几个字母 默认输出小写
#路径：/Keyboard_B
#输入：
#   text = 输入字符串
#   operator=执行操作 [encode,decode]
#返回：
#   成功：
#       {"code": 200, "result": result,'length':结果长度}
#   失败：
#       参数错误{'code': 9999, 'message': '输入字符不符合当前解密字符集。'}
#       参数错误{'code': 10000, 'message': '输入字符不符合当前加密字符集。'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/Keyboard_B',methods=['get','post'])
def Keyboard_B():
    text = request.values.get('text')
    result = ''
    operator = request.values.get('operator')
    try:
        if text and operator:
            letter2 = {
	        'a':'w','b':'ww','c':'www','d':'e','e':'ee','f':'eee',
		'g':'r','h':'rr','i':'rrr','j':'t','k':'tt','l':'ttt','m':'y',
		'n':'yy','o':'yyy','p':'u','q':'uu','r':'uuu','s':'uuuu',
		't':'i','u':'ii','v':'iii','w':'o','x':'oo','y':'ooo','z':'oooo',
		'A':'w','B':'ww','C':'www','D':'e','E':'ee','F':'eee',
		'G':'r','H':'rr','I':'rrr','J':'t','K':'tt','L':'ttt',
		'M':'y','N':'yy','O':'yyy','P':'u','Q':'uu','R':'uuu',
		'S':'uuuu','T':'i','U':'ii','V':'iii','W':'o','X':'oo','Y':'ooo','Z':'oooo',
		
            }
            letter1 = {
		'w':'a','ww':'b','www':'c','e':'d','ee':'e','eee':'f',
		'r':'g','rr':'h','rrr':'i','t':'j','tt':'k','ttt':'l',
		'y':'m','yy':'n','yyy':'o','u':'p','uu':'q','uuu':'r',
		'uuuu':'s','i':'t','ii':'u','iii':'v','o':'w','oo':'x','ooo':'y','oooo':'z',
            }
            if operator == 'decode':
                for i in text:
                    if (i<'a' or i>'z') and i !=' ':
                        resu = {'code': 9999, 'message': '输入字符不符合当前解密字符集。'}

                        return json.dumps(resu, ensure_ascii=False)
                s = text.split(" ")
                for item in s:
                    result += letter1[item]
            elif operator == 'encode':
                for i in text:
                    if (i<'a' or i>'z') and (i<'A' or i>'z') :
                        resu = {'code': 10000, 'message': '输入字符不符合当前加密字符集。'}
                        return json.dumps(resu, ensure_ascii=False)
                for item in text:
                    result+=letter2[item]+' '
            resu = {'code': 200, 'result':result,'length':len(result)}
            return json.dumps(resu, ensure_ascii=False)
        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return json.dumps(resu, ensure_ascii=False)
    except:
        resu = {'code': 10002, 'message': '异常。'}
        return json.dumps(resu, ensure_ascii=False)


#函数功能：字符串各字符数量统计
#注意：输出区分到每种字符
#路径：/Letter_frequence
#输入：
#   text = 输入字符串
#返回：
#   成功：
#       {"code": 200, "result": cnt_dict,'length':lenth}
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/Letter_frequence',methods=['get','post'])
def Letter_frequence():
    text = request.values.get('text')
    try:
        if text:
		cnt_dict = {}
		for c in text:
			if c in cnt_dict:
				cnt_dict[c] = cnt_dict[c] + 1
			else:
				cnt_dict[c] = 1
		resu = {'code': 200, 'result':cnt_dict,'length':len(cnt_dict)}
		return json.dumps(resu, ensure_ascii=False)
        else:
		resu = {'code': 10001, 'message': '参数不能为空！'}
		return json.dumps(resu, ensure_ascii=False)
    except:
	resu = {'code': 10002, 'message': '异常。'}
	return json.dumps(resu, ensure_ascii=False)


#函数功能：社会主义核心价值观编码的加密与解密
#注意：
#路径：/Socialist_code
#输入：
#   text = 输入字符串 operator = 加密/解密
#返回：
#   成功：
#       {"code": 200, "result": result,'length':lenth}
#   失败：
#	输入错误{'code': 10000, 'message': '输入错误'}
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       异常{'code': 10002, 'message':'异常。' }
@server.route('/Socialist_code',methods=['get','post'])
def Socialist_code():
    text = request.values.get('text')
    result = ''
    operator = request.values.get('operator')
    try:
        if text and operator:
		#print '1'
		ENSTRS = ("富强", "民主", "文明", "和谐", "自由", "平等","公正", "法治", "爱国", "敬业", "诚信", "友善")
		#print '1'
		if operator == 'decode':
			#print 1
			len_str = len(text)
			if len_str % 16 == 0:
				resu={'code': 10000, 'message': '输入错误'}
				return json.dumps(resu, ensure_ascii=False)
			for x in range(0, len_str, 16):
				decode_char = text[x:x+16]
				temp_int = [ENSTRS.index(decode_char[y:y+2]) for y in range(0, 16, 2)]
				int_list = [temp_int[x]+temp_int[x+1] for x in range(0, 8, 2)]
				bin_temp = [bin(i).replace('0b', '') for i in int_list]
				binstr_list = []
				for b in bin_temp:
					if len(b) < 4:
						binstr_list.append(b.zfill(4))
					else:
						binstr_list.append(b)
				binstr = ''.join(binstr_list)
				result = result + chr(int(binstr, 2))
			resu = {'code': 200, 'result':result,'length':len(result)}
			#print 'aaaa'+resu
			return json.dumps(resu, ensure_ascii=False)
		elif operator == 'encode':
			#print 2
			binstr_list=[]
#			binstr_list = [b.replace('0b', '') for b in [bin(ord(c)) for c in text]]
			for c in text:
				binstr_list.append(bin(ord(c))[2:])
			#print binstr_list
#			print 4
			for binstr in binstr_list:
				#print 3
				len_binstr = len(binstr)
				if len_binstr < 16:
					binstr = binstr.zfill(16)
				temp_list = [binstr[start:start+4] for start in range(0, 16, 4)]
				int_list = []
				for i in temp_list:
					i = int(i, 2)
					if i >= 11:
						int_list.append(11)
						int_list.append(i - 11)
					else:
						int_list.append(0)
						int_list.append(i)
				#print aaaaaaa
				result = result + ''.join([ENSTRS[index] for index in int_list])
		resu = {'code': 200, 'result':result,'length':len(result)}
		#print 'aaaa'+resu
		return json.dumps(resu, ensure_ascii=True)
        else:
		resu = {'code': 10001, 'message': '参数不能为空！'}
		return json.dumps(resu, ensure_ascii=False)
    except:
	resu = {'code': 10002, 'message': '异常。'}
	return json.dumps(resu, ensure_ascii=False)

def des():
    return
if __name__ == '__main__':
    server.run(debug=True, port=8887, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
