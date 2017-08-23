//此JS代码必须放到body结束之前才有效
function $(id){return document.getElementById(id);}
$("submit_job").onclick = function(){
    var obj = document.getElementById("from_add_job");
    form = obj.getElementsByTagName("input")
    url = "/Job/add_job?"
    url = url+form[0].placeholder+"="+form[0].value
    for (var i=1;i<form.length;i++){
        if (form[i].value!=""){
            url = url+"&"+form[i].placeholder+"="+form[i].value
        }
    }
    add_job(url)
}

function add_job(url){
    jQuery.get(url, function(data, status){
        alert(data, status)
    })
}