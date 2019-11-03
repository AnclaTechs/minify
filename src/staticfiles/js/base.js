$(document).ready(function() {
  $("#postarea").on("keyup", function() {
    var postLength = $("#postarea").val();
    var btn = document.querySelector(".post-bbtn");
    if (postLength.length >= 1) {
      btn.removeAttribute("disabled");
    } else {
      btn.setAttribute("disabled", "true");
    }
  });
});
