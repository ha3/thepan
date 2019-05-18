function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Rounds numbers to nearest 0.5
function roundHalf(num) {
    return Math.round(parseFloat(num)*2)/2;
}


$(document).ready(function() {
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  var options = {
    max_value: 5,
    step_size: 1,
    cursor: 'pointer',
    ajax_method: 'POST',
    url: '../../' + $("#recipe-id").val() + '/rate/',
    initial_value: roundHalf($("#current-rating").val()),
  }

  $(".rate").rate(options);

  $(".rate").on("updateSuccess", function(ev, data){
    $(".rate").rate("setValue", roundHalf(data), 1);
  });

  $(".rate").on("updateError", function(ev, jxhr, msg, err){
    alert("Bir hata oluştu; lütfen daha sonra tekrar deneyin!");
  });

});
