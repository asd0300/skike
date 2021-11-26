let isClick = true;
$("button").on("click", function () {
  if (isClick) {
    isClick = false;
    console.log("我被點擊了");
    setTimeout(function () {
      isClick = true;
    }, 1000); //
  } else {
    console.log("過快");
  }
});

let isClick = true;
$("a").on("click", function () {
  if (isClick) {
    isClick = false;
    console.log("我被點擊了");
    setTimeout(function () {
      isClick = true;
    }, 1000); //
  } else {
    console.log("過快");
  }
});
