import flask, json,urllib,gmpy2
from flask import render_template
import base64,base58,base91,base36,base62
#62->pip install pybase62
from flask import request

server = flask.Flask(__name__)

@server.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')  #跳入主页

@server.route('/to_base64', methods=['get', 'post'])
def to_base64():
    return render_template('base64.html',result='') #主页中的链接跳到base64.html，注意index.html中不能直接跳转到别的网页，需要借助flask里的render_template函数。所以index.html里面的href都需要修改成相应函数名行跳转，比如这里是to_base64.
										#这里给result赋初值，不至于报错
@server.route('/base_all', methods=['get', 'post']) #
#函数功能：base全家桶
#路径：/base_all
#输入：
#   text = 输入字符串
#   num_of_base = 需要加解密的类型      [64，32，58，91，36，62，85]
#   encode_or_decode = 选择加密或者解密 [encode,decode]
#返回：
#   成功：
#       加密{'code': 200, 'cypher_text':加密结果,'lenth' }
#       解密{'code': 200, 'plain_text':解密结果 }
#   失败：
#       参数为空{'code': 10001, 'message': '参数不能为空！'}
#       字符集错误{'code': 10000, 'message':'输入字符集错误。' }
def base_all():                                                    #注意，这里返回的时候返回原来的网页，并把结果写在上面。
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
                return render_template('base64.html', result=resu)
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
                return render_template('base64.html',result=resu)

        else:
            resu = {'code': 10001, 'message': '参数不能为空！'}
            return render_template('base64.html', result=resu)
    except :
        resu = {'code': 10000, 'message':'输入字符集错误。' }
        return render_template('base64.html', result=resu)        
if __name__ == '__main__':
    server.run(debug=True, port=8887, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
