
const dbParam = JSON.stringify({
        table:"characters", limit:200
    });

const xmlhttp = new XMLHttpRequest();

xmlhttp.onload = function() {
    myObj = JSON.parse(this.responseText);
    
    let text = "<table border='1'>"

    for (let x in myObj) {
    text += "<tr><td>" + myObj[x].name + "</td></tr>";
    }

    text += "</table>"
    document.getElementById("demo").innerHTML = text;
}

$(function() {

    var people = [];
 
    $.getJSON('people.json', function(data) {
        $.each(data.person, function(i, f) {
           var tblRow = "<tr>" + "<td>" + f.firstName + "</td>" +
            "<td>" + f.lastName + "</td>" + "<td>" + f.job + "</td>" + "<td>" + f.roll + "</td>" + "</tr>"
            $(tblRow).appendTo("#userdata tbody");
      });
 
    });
 
 });

xmlhttp.open("POST", "json_demo_html_table.php");
xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
xmlhttp.send("x=" + dbParam);

