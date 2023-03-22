function Color(){
    let date = new Date(Date.now());
    console.debug("color: " + date.getHours() + ":" +date.getMinutes() + ":" + date.getSeconds() + ":" + date.getMilliseconds());
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
    let date = new Date(Date.now());
    console.debug("post: " + date.getHours() + ":" +date.getMinutes() + ":" + date.getSeconds() + ":" + date.getMilliseconds());
    //fetch("http://" + document.getElementById("api").value + "/" + page, {
    fetch("http://aurora.local:5500/" + page, {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })    
}