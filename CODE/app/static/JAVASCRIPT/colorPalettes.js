function color()
{
    // FUNCTIONAL!!!!
    
    var color = document.getElementById("color").innerText
    document.getElementById("colorDiv").style.backgroundColor = color
    if(color == "rgb(0,0,0)")
    {
        document.getElementById("color").style.color = "white"
    }
    if(color == "#000000")
    {
        document.getElementById("color").style.color = "white"
    }
}


// colorPicker.addEventListener("input", updateFirst);
// colorPicker.addEventListener("change", watchColorPicker);

// function watchColorPicker(event) 
// {
//   document.querySelectorAll("p").forEach((p) => 
//     {
//     p.style.color = event.target.value;
//   });
// }
