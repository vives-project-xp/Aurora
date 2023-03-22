function Color(){
    let data = {
        red: document.getElementById("red").value,
        green: document.getElementById("green").value,
        blue: document.getElementById("blue").value,
    }
    Post("color", data);
}

function Connect(){
    let data = {
        wled: document.getElementById("wled").value
    }
    Post("connect", data);
}

function Post(page, data){
    fetch("/" + page, {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })  .then(response => {
        //handle response
        info = response.headers.get("info")
        state = document.getElementById("state");
        console.log(response);
        if(info != null && info == "wrong_url"){
            state.innerText = "Unable to connect\nWrong url";
            state.style.color = "red";
        }
        if(info != null && info == "connected"){
            state.innerText = "Connect to " + data["wled"];
            state.style.color = "green";
        }
      })      
}