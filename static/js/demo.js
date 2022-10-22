$(document).ready(function () {
  charter();
});

function charter() {
  $.ajax({
    url: "./recodeContent.json",
    method: "GET",
    dataType: "json",
    success: function (res) {
      console.log(res);
      for (var i = 0; i < res.length; i++) {
        var Chart = $("<div>");
        Chart.addClass("row");
        var Chartid = $("<div>");
        Chartid.addClass("Chartid chart-space");
        Chartid.html("第" + res[i]["chapter"]+"章");
        Chart.append(Chartid);
        for (var j = 0; j < res[i]["data"].length; j++) {
          var Cid = $("<a>");
          Cid.addClass("col-3 chart-cid btn btn-outline-secondary");
          Cid.attr(
              "href",
              `/question?chapter=${res[i]["chapter"]}&cid=${res[i]["data"][j]["cid"]}`
          );
          Cid.html("第"+res[i]["data"][j]["cid"]+"節");
          Chart.append(Cid);
          // console.log(i + "." + res[i]["data"][j]["cid"]);
        }
        $("#charter").append(Chart);
      }
    },
    error: function (res) {
      console.log("no");
    },
  });
}
