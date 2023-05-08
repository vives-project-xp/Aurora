var redSlider = document.getElementById("red-slider");
var redValue = document.getElementById("red-value");
var greenSlider = document.getElementById("green-slider");
var greenValue = document.getElementById("green-value");
var blueSlider = document.getElementById("blue-slider");
var blueValue = document.getElementById("blue-value");
var hexInput = document.getElementById("hex-input");
var decimalInput = document.getElementById("decimal-input");
var colorBox = document.getElementById("color-box");

function Loop() {
  timeout = setInterval(function () {
    Sensors();
  }, 1000);
}

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
  var hex = Number(c).toString(16);
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
redSlider.addEventListener("mousemove", function () {
  var x = redSlider.value;
  var color =
    "linear-gradient(90deg,red " +
    (x / 255) * 100 +
    "%,grey " +
    (x / 255) * 100 +
    "%)";

  redSlider.style.background = color;
});

greenSlider.addEventListener("mousemove", function () {
  var x = greenSlider.value;
  var color =
    "linear-gradient(90deg,#00ff00 " +
    (x / 255) * 100 +
    "%,grey " +
    (x / 255) * 100 +
    "%)";

  greenSlider.style.background = color;
});

blueSlider.addEventListener("mousemove", function () {
  var x = blueSlider.value;
  var color =
    "linear-gradient(90deg,blue " +
    (x / 255) * 100 +
    "%,grey " +
    (x / 255) * 100 +
    "%)";

  blueSlider.style.background = color;
});

init();

function Color() {
  let data = {
    red: redSlider.value,
    green: greenSlider.value,
    blue: blueSlider.value,
  };
  Post("color", data);
}

function Toggle() {
  Post("toggle", "");
}

async function Sensors() {
  sensors = JSON.parse(await Post("sensors"));

  //clearing sensor list
  //document.getElementById("sensors").textContent = "";
  if (sensors) {
    for (sensor of sensors) {
      AddSensor(sensor);
    }
  }
}

function AddSensor(sensor) {
  const sensors = document.getElementById("sensors");
  if (sensors.querySelector("#" + sensor["name"]) == null) {
    const node = document.createElement("li");
    const name = document.createElement("p");
    name.innerHTML = sensor["name"];
    name.setAttribute("id", sensor["name"]);
    const id = document.createElement("input");
    id.setAttribute("type", "text");
    id.setAttribute("value", sensor["id"]);
    id.setAttribute(
      "onchange",
      'UpdateSensor("' + sensor["name"] + '",this.value)'
    );
    //const time = document.createElement("p");
    //time.innerHTML = sensor["lastseen"];
    node.appendChild(name);
    node.appendChild(id);
    //node.appendChild(time);

    document.getElementById("sensors").appendChild(node);
  }
}

function UpdateSensor(name, id) {
  console.log("update " + name + " to " + id);
  let data = {
    name: name,
    id: id,
  };
  Post("updatesensor", data);
}

/*Form()

test test
{
    
        const form = document.getElementById("preset-form");
        form.addEventListener("submit", function(event) {
            event.preventDefault(); 
      // Prevent the form from submitting and refreshing the page

            const input = document.getElementById("preset-input");
            const preset = input.value;
            console.log("You gave a preset: " + preset);

            // You can now use the value of `preset` to do whatever you need to do, such as sending it to a server or updating the UI
        });
	
}*/

function Preset(val) {
  let data = { ps: val };
  Post("preset", data);
}

async function Post(page, data) {
  //fetch("http://" + document.getElementById("api").value + "/" + page, {
  let response = await fetch("http://10.11.0.2:5500/" + page, {
    method: "post",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  });
  msg = await response.text();
  return msg;
}
