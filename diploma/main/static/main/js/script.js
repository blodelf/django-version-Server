$('#datepicker-example').datepicker({
    calendarWeeks: true,
    autoclose: true,
    todayHighlight: true
});
var form = document.querySelector('.formWithValidation')
var fields = form.querySelectorAll('#crit')
count = 0
for (var i = 0; i < fields.length; i++) {
    console.log(fields[i].value)
    if (!fields[i].value) {
      $(".form-add-part2").hide();
      break;
    }
    else{
        count++;
    }
    if(count == fields.length){
      $(".form-add-part1").hide();
    }
}

$(".next").click(function(){
    $(".form-add-part1").hide();
    $(".form-add-part2").show();
})
$(".prev").click(function(){
    $(".form-add-part1").show();
    $(".form-add-part2").hide();
})