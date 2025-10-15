function toggle_menu() {
  with(document.getElementById("menu-box").style) {
    if(display=="block") { 
      display = "none"; 
    }
    else { 
      display = "block"; 
    }
  } 
}