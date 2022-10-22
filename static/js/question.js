(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substring(1).match(reg);
        if (r != null) return decodeURI(r[2]);
        return null;
    };
})(jQuery);
<<<<<<< HEAD

var chapter = $.getUrlParam("chapter"); //url後面的當下章數值
var cid = $.getUrlParam("cid"); //url後面的當下節數值
var chapterid = chapter - 1; //先減1是為了，for迴圈時，第一章是陣列編號0
var cidnum = cid - 1; //先減1是為了，for迴圈時，第一節是陣列編號0

$(document).ready(function(){
    charter();
    $("#submit").click(function () {
        let question = $("#question").val();
        console.log(ctext);
        console.log(question);

        $.ajax({
            url: "/question",
            method: "POST",
            dataType: "json",
            data: { content: ctext, question: question },
            success: function (res) {
                $("#answer").text(res["output"]);
            },
            error: function (res) {
                console.log("no");
            },
        });
    });
});

var ctext = "";
function charter() {
=======
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
>>>>>>> origin/xinci
    $.ajax({
        url: "./recodeContent.json",
        method: "GET",
        dataType: "json",
        success: function (res) {
<<<<<<< HEAD
            $(".table-text").html(
                "第" +
                    res[chapterid]["chapter"] +
                    "章" +
                    " - 第" +
                    res[chapterid]["data"][cidnum]["cid"] +
                    "節"
            );
            $("#content").html(res[chapterid]["data"][cidnum]["ctext"]);
            ctext = res[chapterid]["data"][cidnum]["ctext"]; //文字暫存要傳出去的
            var datacid = res[chapterid]["data"][cidnum]["cid"]; //當下文章第幾節
            var last = cid - 1; //用於判斷是否第一節，先減 1
            var allcid = res[chapterid]["data"].length; //當下章數的總 cid
            var next = allcid - cid; //用於判斷是否第一節，全部減掉當下章節
            var Clast = $("#last");
            var Cnext = $("#next");
            if (last == 0) { //當是第一節時
                if (chapter == 1) { //當又是第一章時，將按鈕消失、線消失、a連結不可按
                    Clast.attr(
                        "style",
                        "background-color:transparent; !important; border:none !important; pointer-events:none;"
                    );
                } else { //切換成上一章最後一節
                    var lcid = res[chapterid - 1]["data"].length;
                    Clast.html(
                        "第" +
                            res[chapterid - 1]["chapter"] +
                            "章" +
                            " - 第" +
                            lcid +
                            "節"
                    );
                    Clast.attr(
                        "href",
                        `./question?chapter=${
                            res[chapterid - 1]["chapter"]
                        }&cid=${lcid}`
                    );
                }
            } else { //同一章，切換成上一節
                Clast.html(
                    "第" +
                        res[chapterid]["chapter"] +
                        "章" +
                        " - 第" +
                        last +
                        "節"
                );
                Clast.attr(
                    "href",
                    `./question?chapter=${
                        res[chapterid]["chapter"]
                    }&cid=${last}`
                );
            }
            if (next == 0) { //當是第一節時，判斷是否要換下一章
                var allcharter = res.length; //總章數
                var ncharter = allcharter - chapter; //用於判斷是否最後一章
                var Cnext = $("#next");
                if (ncharter == 0) { //當又是最後一章時，將按鈕消失、線消失、a連結不可按
                    Cnext.attr(
                        "style",
                        "background-color:transparent; !important; border:none !important; pointer-events:none;"
                    );
                } else { //切換成下一章第一節
                    Cnext.html(
                        "第" +
                            res[chapterid + 1]["chapter"] +
                            "章" +
                            " - 第" +
                            1 +
                            "節"
                    );
                    Cnext.attr(
                        "href",
                        `./question?chapter=${
                            res[chapterid + 1]["chapter"]
                        }&cid=${1}`
                    );
                }
            } else { //同一章，切換成下一節
                datacid = datacid + 1;
                console.log(datacid);
                Cnext.html(
                    "第" +
                        res[chapterid]["chapter"] +
                        "章" +
                        " - 第" +
                        datacid +
                        "節"
                );
                console.log(datacid);
                Cnext.attr(
                    "href",
                    `./question?chapter=${res[chapterid]["chapter"]}&cid=${datacid}`
                );
            }
=======

            $("#content").html(res[chapterid]["data"][cidnum]["ctext"]);
            console.log(res);
            // console.log(res[chapterid]["data"][cid]);
            console.log(res[chapterid]["data"][cidnum]['ctext']);
>>>>>>> origin/xinci
        },
        error: function (res) {
            console.log("no");
        },
    });
<<<<<<< HEAD
}
=======
    // for (var i = 1;i<)
}

>>>>>>> origin/xinci
