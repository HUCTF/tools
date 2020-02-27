var operator=""
var typed=""
var text=""
var dic=[]
var Dict={}
var num_of_button //按钮数量
var num_of_other_input //其他输入框数量

var eval_str=''
$(document).ready(function(){
    //获取Dict
    get_Dict()
   // 侧边栏伸缩控制
     span_slide()
    //点击选项修改按钮和输入框标题
    span_click()
    //点击按钮时进行的运算操作，通信操作在这里完成
    button_click()
    //复制
    click_copy()

});

// 侧边栏伸缩控制
function span_slide() {
   $("b").click(function () {

       var idd=$(this).attr('id')
       idd=idd.substring(0,idd.length-3)
        eval_str= '$("#'+idd+'").slideToggle();\n'
      // alert(eval_str)
       eval(eval_str)
   })
}
//点击按钮事件
function button_click() {
    //alert(num_of_button)
    $("button").click(function () {
       //获取输入字符串、获取按钮操作
      text=$("#text").val()
      operator=$(this).val()
      for(id in Dict){
          if(typed.search(id)!=-1){
              var strr=''
              var dataa=''
              var subString=Dict[id]['substring']
              var other_input_value_text= Dict[id]['other_input_value_text']
              var other_input_code=Dict[id]['other_input_code']

              for(var i=0;i<num_of_other_input;i++){
                   //alert('2')
                  if(other_input_code[i]==1){
                      strr+='this.'+other_input_value_text[i][0]+'=$("#'+other_input_value_text[i][0]+'").val();\n'
                      dataa+=other_input_value_text[i][0]+':this.'+other_input_value_text[i][0]+',\n'
                  }
              }
             // alert(strr)
              strr= '   this.text=text\n' +
                    '   this.typed=typed\n' +
                    '   this.url= "/'+id+'"\n' +
                    '   this.operator=operator\n' +strr+
                    '   this.data={\n' +
                    '       text:this.text,\n' +
                    '       typed:this.typed.substring('+subString+'),\n' +
                    '       operator:this.operator,\n' +dataa+
                    '   }\n' +
                    '   var TR = new transport(this.url ,this.data)\n' +
                    '   TR.transport()\n'

              //alert('4')
              //alert(strr)
              eval(strr)
               break
          }
    }

  })
}
//侧边栏点击事件
function span_click(){
    $("span").click(function (){
      //a中的value为非标准属性，不能使用$(this).val()
      typed=$(this).attr('value')
     $("#inputTop").text($(this).text()+" 工具");//在淡入淡出之间来回切换

      //a中的value为非标准属性，不能使用$(this).val()
      typed=$(this).attr('value')

        var flag=0
     //这里用来删除多余按钮,并且更改其他输入框的信息
      for(id in Dict){

            if(typed.search(id)!=-1){
               $("#text").attr('placeholder',Dict[id]['input_placeholder']);
               $ ('#hintt').text('hint:'+Dict[id]['hint'])
             btn_control_str=''
             btn_control_arr=Dict[id]['btn_code']
             otherInput_control_arr=Dict[id]['other_input_code']
             otherInput_control_str=''
             other_input_value_text=Dict[id]['other_input_value_text']
              //alert(other_input_value_text[1][0])
             for(i=0;i<num_of_button;i++ ){
                 if(btn_control_arr[i]==0){
                     btn_control_str+='$("#option'+String(i+1)+'").hide(100);'
                 }else{
                     btn_control_str+='$("#option'+String(i+1)+'").show(100);'
                 }
             }
             eval(btn_control_str)
              for(i=0;i<num_of_other_input;i++ ){
                 if(otherInput_control_arr[i]==0){
                     otherInput_control_str+='$("#other'+String(i+1)+'").hide(100);\n'
                 }else{
                     flag++ //记录其他输入的数量
                     otherInput_control_str+='$("#other'+String(i+1)+'").show(100);\n'
                     otherInput_control_str+='$("#other'+String(i+1)+'_span").text('+'"'+other_input_value_text[i][1]+'"'+');\n' //修改其他输入的名字
                    otherInput_control_str+='$("#other'+String(i+1)+' input:first").attr("id",'+'"'+other_input_value_text[i][0]+'"'+');\n' //修改其他输入的value
                 }
             }
             //alert(otherInput_control_str)
             eval(otherInput_control_str)
                //界面高度控制
             height_control(flag)
          }
      }

  });
}
//主体部分高度控制
function height_control(num) {
         num=680+num*40
        $("#main-div").css("height",String(num+'px'));
        $("#main-container1").css("height",String(num+'px'));
        $("#main-container2").css("height",String(num+'px'));
}
//ajax通信代码
function transport(url,data) {
    this.url=url
    this.data=data
    this.transport=function() {
             $.ajax({
            //请求方式
            type : "POST",
            //请求的媒体类型
            contentType: "application/json;charset=UTF-8",
            //请求地址
            url : this.url,
            //数据，json字符串
            data:JSON.stringify(this.data),
            //请求成功
            success : function(result) {
                result=JSON.parse(result)
                //if(typeof (result["result"])!='object')
                    $("#result").text(result["result"])
                // else {
                //     var strr=""
                //     result=result["result"]
                //     for (key in result){
                //         strr+=result[key]+'      '
                //     }
                //     $("#result").text(strr)
                // }

            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("通信失败")

            }
        });
    }

}
//获得字典Dict
function get_Dict() {
    $.ajax({
            type : "POST",
            contentType: "application/json;charset=UTF-8",
            url : '/get_Dict',
            data:JSON.stringify({'passwd':'123456'}),
            success : function(result) {
                   Dict=result['Dict']
                   num_of_button=result['num_of_button']
                   num_of_other_input=result['num_of_other_input']

            },
            //请求失败，包含具体的错误信息
            error : function(e){
                alert("未知错误")

            }
        });

}
//按钮复制功能
function click_copy() {
        // var content = $("#result").text();
        var content = $("#result").html();  
    var clipboard = new Clipboard('.btn-warning', {  
        text: function() {  
            return content;  
        }  
    });  
    clipboard.on('success', function(e) {  
        alert("复制成功");  
    });  


}
