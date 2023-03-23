function Color(){
    let data = {
        red: document.getElementById("red").value,
        green: document.getElementById("green").value,
        blue: document.getElementById("blue").value,
    }
    Post("color", data);
}

function Toggle(){
    Post("toggle", "");
}

function Preset() {
    let data = {ps: document.getElementById("preset").value}
    Post("preset", data)
}

function Post(page, data){
    //fetch("http://" + document.getElementById("api").value + "/" + page, {
    fetch("http://localhost:5500/" + page, {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })    
}