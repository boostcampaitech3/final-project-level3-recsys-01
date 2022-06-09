const emInput = document.querySelector("#email-input");
const loginBtn = document.querySelector("#loginBtn");

const ph_email = document.querySelector(".phTxt_email");
const ph_style_set = ph_email.style;

const showidtxt=document.querySelector("#open")
const changeidBtn = document.querySelector("#changeIDBtn");
const saveIDBtn = document.querySelector("#saveIDBtn");
const cancelIDBtn = document.querySelector("#cancelIDBtn");


emInput.addEventListener('focus', (e)=>{
    e.target.parentElement.children[1].style.fontSize = '15px';
    e.target.parentElement.children[1].style.top = '12px';
    e.target.parentElement.children[1].style.left = '7px';
});

emInput.addEventListener('blur', (e)=>{
    if(emInput.value === ''){
        e.target.parentElement.children[1].style = ph_style_set;
    }
});

ph_email.addEventListener('click', (e)=>{
    e.target.parentElement.children[0].focus();
});

function getJsonFile(id){
    // var url="http://115.85.181.5:30001/"+id;
    var url="http://118.67.128.97:30001/"+id;
    fetch(url)
        .then((response) => {
        return response.json();
        })
        .then((json) => {
            console.log(json);
            keys=Object.keys(json.recommendation);
            console.log(Object.keys(json.recommendation));
            localStorage.setItem("rec_key",JSON.stringify(Object.keys(json.recommendation)));
            values=Object.values(json.recommendation);
            console.log(Object.values(json.recommendation));
            localStorage.setItem("rec_value",JSON.stringify(Object.values(json.recommendation)));
        })
        .catch((err) => {
            console.log(err);
        });
}

loginBtn.addEventListener('click', (e)=>{
    document.getElementById('popup-overlay').classList.add("popup-hide");
    document.getElementById("change_id").classList.add("hide");
    document.getElementById("change_id_input").classList.add("hide");
    e.preventDefault();
    localStorage.setItem("Full-ID",emInput.value);
    id=emInput.value.split("@")[0];
    console.log(id);
    localStorage.setItem("ID",id);
    load();
    setTimeout(() => window.location.reload(), 300);
});

showidtxt.addEventListener('click', (e)=>{
    if(document.getElementById("change_id_input").classList.contains("show"))
        document.getElementById("change_id_input").classList.toggle("show");
    else{
        document.getElementById("change_id").classList.toggle("show");
        document.getElementById('ids').textContent ='현재 ID: '+localStorage.getItem("Full-ID");
        console.log(1);
    }
    console.log(localStorage.getItem("Full-ID"));
});

changeidBtn.addEventListener('click', (e)=>{
    if(document.getElementById("change_id_input").classList.contains("hide")){
        document.getElementById("change_id_input").classList.toggle("show");
    }else{
        document.getElementById("change_id_input").classList.toggle("show");
    }
    document.getElementById("change_id").classList.toggle("show");
    document.getElementById('input').value=localStorage.getItem("Full-ID");

    console.log(2);
});

saveIDBtn.addEventListener('click', (e)=>{
    e.preventDefault();
    localStorage.clear();
    localStorage.setItem("Full-ID",document.getElementById('input').value);
    localStorage.setItem("ID",document.getElementById('input').value.split("@")[0]);
    console.log(3);
    if(document.getElementById("change_id").classList.contains("hide")){
        document.getElementById("change_id").classList.toggle("show");
    }else{
        document.getElementById("change_id").classList.toggle("show");
    }
    document.getElementById("change_id_input").classList.toggle("show");
    document.getElementById('ids').textContent ='현재 ID: '+localStorage.getItem("Full-ID");
    load();
    setTimeout(() => window.location.reload(), 300);
});

cancelIDBtn.addEventListener('click', (e)=>{
    document.getElementById("change_id_input").classList.toggle("show");
});


function load(event){
    document.getElementById('ids').textContent = localStorage.getItem("ID");
    if(localStorage.length==0){
      function loadPopup(event){
        if(document.getElementById("popup-overlay").classList.contains("popup-hide")){
          document.getElementById("popup-overlay").classList.remove("popup-hide");
         }else{
          document.getElementById("popup-overlay").classList.add("popup-show");
        }
      }
      setTimeout(loadPopup, 3000);
    }else{
      id=localStorage.getItem("ID");
      document.getElementById('title').textContent='환영합니다\n'+id+'님!';
    getJsonFile(id);
    }
  };