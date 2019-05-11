$(document).ready(function() {
  $(".list-group > a").hover(function() {
    $(this).toggleClass("active");
  })

  $(".click-action").click(function() {
    $(this).find(":radio").prop("checked", true);
  })
});
