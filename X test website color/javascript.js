var redSlider = document.getElementById("red-slider");
var redValue = document.getElementById("red-value");
var greenSlider = document.getElementById("green-slider");
var greenValue = document.getElementById("green-value");
var blueSlider = document.getElementById("blue-slider");
var blueValue = document.getElementById("blue-value");
var hexInput = document.getElementById("hex-input");
var decimalInput = document.getElementById("decimal-input");
var colorBox = document.getElementById("color-box");

function updateColor() {
  var red = redSlider.value;
  var green = greenSlider.value;
  var blue = blueSlider.value;
  var color = "rgb(" + red + "," + green + "," + blue + ")";
  colorBox.style.backgroundColor = color;
  redValue.innerText = red;
  greenValue.innerText = green;
  blueValue.innerText = blue;
  hexInput.value = "#" + rgbToHex(red, green, blue);
  decimalInput.value = rgbToDecimal(red, green, blue);
}

function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
  return componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function rgbToDecimal(r, g, b) {
  return r + ", " + g + ", " + b;
}

redSlider.addEventListener("input", updateColor);
greenSlider.addEventListener("input", updateColor);
blueSlider.addEventListener("input", updateColor);

function init() {
  updateColor();
}

init();

Form()
{
    
		const form = document.getElementById("preset-form");
		form.addEventListener("submit", function(event) {
			event.preventDefault(); // Prevent the form from submitting and refreshing the page

			const input = document.getElementById("preset-input");
			const preset = input.value;
			console.log("You gave a preset: " + preset);

			// You can now use the value of `preset` to do whatever you need to do, such as sending it to a server or updating the UI
		});
	
}

