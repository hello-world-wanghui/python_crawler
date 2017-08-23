function get_job_list(){
    jQuery.get("/Job/get_jobs", function(data,status){
        var data = eval('(' + data + ')');
        if (parseInt(data.errcode) == 0){
            data = data.data
            job_lsit = document.getElementById("job_lists")
        if (data.length>0){
            tablestr = "<tbody>"
            for(var i=0;i<data.length;i++){
                tablestr = tablestr + '<tr class="success">\n '
                job_id = data[i].job_id;
                tablestr = tablestr + '<td> \n ' + job_id + '\n' + '</td>'
                next_run_time = data[i].next_run_time;
                tablestr = tablestr + '<td> \n ' + next_run_time + '\n' + '</td>'
                project_name = data[i].project_name;
                tablestr = tablestr + '<td> \n ' + project_name + '\n' + '</td>'
                start_date = data[i].start_date;
                tablestr = tablestr + '<td> \n ' + start_date + '\n' + '</td>'
            }
            tablestr = tablestr + "</tbody>"
            job_lists.innerHTML = job_lists.innerHTML + tablestr
        }
        }
    })
    }