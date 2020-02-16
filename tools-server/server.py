import flask, json,urllib,gmpy2
from flask import render_template
from flask_
import base64,base58,base91,base36,base62
#62->pip install pybase62
from flask_bootstrap import Bootstrap
from flask import request

server = flask.Flask(__name__)

Bootstrap.init_app(server)

@server.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html') 

@server.route('/to_base64', methods=['get', 'post'])
def to_base64():
    return render_template('base64.html',result='')
@server.route('/base_all', methods=['get', 'post'])

def base_all():                       
    cypher_text=''
    plain_text=''
    text=request.values.get('text')           
    num_of_base=request.values.get('num_of_base')
    encode_or_decode=request.values.get('encode_or_decode')
    try:
        if text and num_of_base and encode_or_decode:
            if encode_or_decode == 'encode': 
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
                    resu = {'code': 200, 'result':cypher_text.decode('utf-8') ,'length':len(cypher_text.decode('utf-8'))}
                else:
                    resu = {'code': 200, 'result': cypher_text,'length':len(cypher_text)}  
                return render_template('base64.html', result=resu)
            elif encode_or_decode=='decode': 
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
                    resu = {'code': 200, 'result': plain_text.decode('utf-8'),'length':len(plain_text.decode('utf-8'))}  
                else:
                    resu = {'code': 200, 'result': plain_text,'length':len(plain_text)}  
                #resu = {'code': 200, 'cypher_text':plain_text.decode('utf-8') }
                return render_template('base64.html',result=resu)
        else:
            resu = {'code': 10001, 'message': 'args can not be blank!'}
            return render_template('base64.html', result=resu)
    except :
        resu = {'code': 10000, 'message':'input error' }
        return render_template('base64.html', result=resu)        
if __name__ == '__main__':
    server.run(debug=True, port=8887, host='0.0.0.0')