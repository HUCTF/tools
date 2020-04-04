$(document).ready(function(){
   do_once()

  // $("#BASE_bt").click(function(){
  //   $("#BASE").slideToggle();//在淡入淡出之间来回切换
  // });
  //
  // $("#Change_B_bt").click(function(){
  //   $("#Change_B").slideToggle();//在淡入淡出之间来回切换
  // });
  // $("#Ascii_str_bt").click(function(){
  //   $("#Ascii_str").slideToggle();//在淡入淡出之间来回切换
  // });
  //  $("#Caesar_bt").click(function(){
  //   $("#Caesar").slideToggle();//在淡入淡出之间来回切换
  // });

   $(window).resize(function () {          //当浏览器大小变化时

    if($(document.body).width()<=500){
            $("span").addClass("change_font_size");
             $("button").addClass("change_font_size");
             $("#option4").addClass("change_font_size")
        $("b").addClass("change_font_size")
       }else{
          $("span").removeClass("change_font_size");
          $("button").removeClass("change_font_size");
           $("#option4").removeClass("change_font_size")
        $("b").removClass("change_font_size")
    } //浏览器时下窗口文档body的高度

});

});


function do_once(){
  if($(document.body).width()<=500){
            $("span").addClass("change_font_size");
             $("button").addClass("change_font_size");
             $("#option4").addClass("change_font_size")
      $("b").addClass("change_font_size")
       }else{
          $("span").removeClass("change_font_size");
          $("button").removeClass("change_font_size");
           $("#option4").removeClass("change_font_size")
      $("b").removeClass("change_font_size")
    }


}