(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substring(1).match(reg);
        if (r != null) return decodeURI(r[2]);
        return null;
    };
})(jQuery);
var chapter = $.getUrlParam("chapter");
var cid = $.getUrlParam("cid");
var chapterid = chapter - 1;
var cidnum = cid - 1;
console.log(chapter);
console.log(chapterid);
console.log(cid);
console.log(cidnum);
$(document).ready(function () {
    charter();
});

function charter() {
    //   var chart = $("#id");
    $.ajax({
        url: "./recodeContent.json",
        method: "GET",
        dataType: "json",
        success: function (res) {

            $("#content").html(res[chapterid]["data"][cidnum]["ctext"]);
            console.log(res);
            // console.log(res[chapterid]["data"][cid]);
            console.log(res[chapterid]["data"][cidnum]['ctext']);
        },
        error: function (res) {
            console.log("no");
        },
    });
    // for (var i = 1;i<)
}

