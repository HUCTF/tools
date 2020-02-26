num_of_button =4 #按钮数量
num_of_other_input=4 #其他输入框数量
Dict={    'BASE'    #唯一标识，必须和函数、接口名保持一致
                    :{'name':"BASE全家桶",   #该函数的名字
                     'typed_value_text':{'BASE32':'BASE32', #执行的类型：类型的名字
                                           'BASE36':'BASE36',
                                           'BASE58':'BASE58',
                                           'BASE62':'BASE62',
                                           'BASE58':'BASE58',
                                           'BASE64':'BASE64',
                                           'BASE85':'BASE85'},
                     'substring':5,                     # 'id'的长度+1
                     'input_placeholder':'未输入:',    #输入框主界面的默认提示值
                     'btn_code':[0,1,1,1],         #预留四个按钮，0代表消失，1代表显示，四个按钮分别是[none,encode,decode,copy]
                     'other_input_code':[1,1,0,0],#预留了四个其他输入框，0代表消失，1代表显示
                     'other_input_value_text':{'0':['test','test'], #其他输入框的 元素：名字 （如rsa中的e为额外输入，则填写 e:参数e）
                                                  '1':['none','none'],
                                                  '2':['none','none'],
                                                  '3':['none','none'],
                                                },
                     'hint':'base解密还不能实现自动补齐',  #对于该功能的描述及提示
                    },
         'Change_B'  :{'name':"进制转换",
                       'typed_value_text':{ '10_2':'10进制→2进制',
                                             '10_8':'10进制→8进制',
                                             '10_16':'10进制→16进制',
                                             '16_2':'16进制→2进制',
                                             '16_8':'16进制→8进制',
                                             '16_10':'16进制→10进制',
                                             '8_2':'8进制→2进制',
                                             "8_10":'8进制→10进制',
                                             "8_16":'8进制→16进制',
                                             '2_8':'2进制→8进制',
                                             '2_10':'2进制→10进制',
                                             '2_16':'2进制→10进制'},
                     'substring':9,
                     'input_placeholder':'未输入:',
                     'btn_code':[1,0,0,1],
                     'other_input_code':[0,0,0,0],
                     'other_input_value_text':{'none':'none',
                                                  'none':'none',
                                                  'none':'none',
                                                  'none':'none'
                                                },
                     'hint':'无',
                    },

      'Ascii_str'  :{'name':"字符串⇌ascii",
                       'typed_value_text':{'hex_ascii_to_str':'Hex→字符串',
                                           'dec_ascii_to_str':'Dec→字符串',
                                           'str_to_Dec_ascii':'字符串→Dec',
                                           'str_to_hex_ascii':'字符串→Hex',
                                            },
                       'substring':10,
                       'input_placeholder':'未输入:',
                       'btn_code':[1,0,0,1],
                       'other_input_code':[0,0,0,0],
                       'other_input_value_text':{'none':'none',
                                                  'none':'none',
                                                  'none':'none',
                                                  'none':'none'
                                                },
                       'hint':'注意，数字转字符串时格式为 65 66 67 68，中间必须有空格+',
                         },
      'Caesar':      {'name':"凯撒密码",
                       'typed_value_text':{
                           'encode_or_decode':'Caesar加解密',
                                          },
                       'substring':7,
                       'input_placeholder':'未输入:',
                       'btn_code':[1,0,0,1],
                       'other_input_code':[0,0,0,0],
                       'other_input_value_text':{'none':'none',
                                                  'none':'none',
                                                  'none':'none',
                                                  'none':'none'
                                                },
                       'hint':'对于凯撒密码，加密解密过程是一样的',
                      },
      }