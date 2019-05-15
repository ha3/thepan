$(document).ready(function() {
  $(".list-group > a").hover(function() {
    $(this).toggleClass("active");
  });

  $(".click-action").click(function() {
    $(this).find(":radio").prop("checked", true);
  });

  $('#example-css').barrating({
    theme: 'css-stars',
    showSelectedRating: false,
    onSelect: function(value, text, event) {
      console.log(value);
    }
  });
});
