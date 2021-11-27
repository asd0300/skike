$(".icon_plus{{loop.index}}").click(function () {
  var form_data = new FormData();
  var icon_plus2 = document.getElementsByClassName("icon_plus{{loop.index}}");
  form_data.append("want_time_start", $("#want_time_start").text());
  form_data.append("want_time_end", $("#want_time_end").text());
  form_data.append("the_name", $("#theName{{loop.index}}").text());
  form_data.append(
    "hotel_detail",
    $("#hotel_detail{{loop.index}}").attr("href")
  );
  form_data.append("hotel_img", $("#hotel_img{{loop.index}}").attr("src"));
  form_data.append("location", $("#location_seletor option:selected").text());
  form_data.append("price", $("#price_hotel{{loop.index}}").text());
  form_data.append("status", "delete");
  $(".icon_empty{{loop.index}}").show();
  $(".icon_plus{{loop.index}}").hide();
  $.ajax({
    type: "POST",
    url: $SCRIPT_ROOT + "/route_function",
    data: form_data,
    success: function (data) {},
    contentType: false,
    processData: false,
    // dataType: "json"
  });
});
