
var text = document.getElementById('{{url_username}}').value;
$.ajax({
    type: 'POST',
    url: {{url_for('course.getnode')}},
    data: JSON.stringify(text), 
    contentType: 'application/json; charset=UTF-8',
    dataType: 'json', 
    success: function(data) { 
    },
    error: function(xhr, type) {
    }
});