$(document).ready(function() {
    $("#sub").on("click", function() {
        window.location = "results.html";
    });
});
$(".resultSingle").each(function(e) {
    e = e * 100;
    $(this).css("animation-delay", e + "ms");
});