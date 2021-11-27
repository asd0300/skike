$("#btn_2").click(function () {
  var checkbox_value = "";
  $(":checkbox").each(function () {
    var ischecked = $(this).is(":checked");
    if (ischecked) {
      checkbox_value += $(this).val() + "|";
    }
  });
  var form_data = new FormData();
  form_data.append("checkbox", checkbox_value);
  form_data.append(
    "agency_selected",
    $("#agency_selected option:selected").text()
  );
  form_data.append("start_date", "{{start_date}}");
  form_data.append("id", "{{id}}");
  form_data.append("agency_result", "{{agency}}");
  $.ajax({
    type: "POST",
    url: $SCRIPT_ROOT + "/route_function/hotel_detail",
    data: form_data,
    success: function (data) {
      $(".product_item").hide();
      $(".list_number_result2").hide();
      var html_data =
        '<h3 class="list_number_result2">為您找到' +
        data["result_count_of_agency"] +
        "個結果</h3>";
      $.each(data["newlist"], function (index, value) {
        html_data +=
          "<div class='product_details'" +
          index +
          "><div class= 'product_colors'></div><div class='product_item'><div class='hotel_item'><a href=" +
          value["hotel_url"] +
          " class='hotel_img'><img  src=" +
          value["agency_logo"] +
          " border='0px' width='80' height='30'/></a><i class=''></i><div class=\"hotel_name\"></div></div><i class=\"\"></i><div class=\"hotel_detail_feature\">" +
          value["hotel_feature"] +
          "</div><div class='hotel_detail_price'>NT" +
          value["price"] +
          "$/每晚</div></div><a></a></div></div>";
        $(".after_query").html(html_data);
      });
    },
    contentType: false,
    processData: false,
    // dataType: "json"
  });
});
