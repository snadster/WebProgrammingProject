
function displayPalette()
{
    var paletteName = document.getElementById('pOption').innerText

    document.getElementById('pTitle').innerText = paletteName
}

// function displayColor()
// {
//     var colors = document.getElementsByClassName("color");
//     for(let color of colors)
//     {
//         color.style.backgroundColor = color.innerText
//         if(color == "rgb(0,0,0)")
//         {
//             color.style.color = "white";
//         }
//         if(color == "#000000")
//         {
//             color.style.color = "white";
//         }
//     }
// }

displayPalette();
// displayColor();