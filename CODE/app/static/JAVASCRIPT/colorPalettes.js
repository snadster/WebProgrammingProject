function showColors()
{   // not functional for some fucking reason
    var colors = document.getElementsByClassName("color");
    for(let color of colors)
    {
        color.style.backgroundColor = color.innerText
        if(color == "rgb(0,0,0)")
        {
            color.style.color = "white";
        }
        if(color == "#000000")
        {
            color.style.color = "white";
        }
    }
}

showColors();


// colorPicker.addEventListener("input", updateFirst);
// colorPicker.addEventListener("change", watchColorPicker);

// function watchColorPicker(event) 
// {
//   document.querySelectorAll("p").forEach((p) => 
//     {
//     p.style.color = event.target.value;
//   });
// }
