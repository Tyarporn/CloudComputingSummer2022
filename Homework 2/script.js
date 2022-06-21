var apigClient = apigClientFactory.newClient({
  apiKey: 'jW0CsfblTC6JJVnFhETfCZAbwhMOEH95i9hTItZd'
});

function enterPost(){
  apigClient.GET();
}
function showPost(){
  apigClient.POST();
}

var btn1 = document.getElementById("enterbtn");
var btn2 = document.getElementById("showbtn");
btn1.addEventListener("click", enterPost);
btn2.addEventListener("click", showPost);


//api key jW0CsfblTC6JJVnFhETfCZAbwhMOEH95i9hTItZd
