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
        api: document.getElementById("api").value,
        wled: document.getElementById("wled").value
    }
    Post("connect", data);
}

function Post(page, data){
    fetch("http://" + document.getElementById("api").value + "/" + page, {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })    
}