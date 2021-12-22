document.addEventListener("click", function(thenew)

{
  if_id = thenew . target. id;
  the_class = thenew . target.className;
  if(the_class == "click_me")
  {
    if_id = document.getElementById(if_id);
    if(if_id .style . background == "red")
    {
      if_id .style . background = "#efefef";
    }
    else
    {
      var links = document.querySelectorAll(".click_me");
      links.forEach(link => {
        link.setAttribute("style", "background:#efefef");
      })
      if_id .style . background = "red";
    }
    }
    if(the_class == "click_me_2")
  {
    if_id = document.getElementById(if_id);
    if(if_id .style . background == "green")
    {
      if_id .style . background = "#efefef";
    }
    else
    {
      var links = document.querySelectorAll(".click_me");
      links.forEach(link => {
        link.setAttribute("style", "background:#efefef");
      })
      if_id .style . background = "green";
    }
  }
});