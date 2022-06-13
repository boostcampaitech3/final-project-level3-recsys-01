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

const fetchUser=(id)=>{
    let url="http://118.67.128.97:30001/"+id;
    return fetch(url).then(res=>res.json());
}
const Asynchronous=async()=>{
    let user=await fetchUser(id);
    keys=Object.keys(user.recommendation);
    localStorage.setItem("rec_key",JSON.stringify(Object.keys(user.recommendation)));
    values=Object.values(user.recommendation);
    localStorage.setItem("rec_value",JSON.stringify(Object.values(user.recommendation)));
    localStorage.setItem("over30",user.over30);
    window.location.reload();
}

loginBtn.addEventListener('click', (e)=>{
    document.getElementById('popup-overlay').classList.add("popup-hide");
    document.getElementById("change_id").classList.add("hide");
    document.getElementById("change_id_input").classList.add("hide");
    e.preventDefault();
    localStorage.setItem("Full-ID",emInput.value);
    id=emInput.value.split("@")[0];
    localStorage.setItem("ID",id);
    load();
});

showidtxt.addEventListener('click', (e)=>{
    if(document.getElementById("change_id_input").classList.contains("show"))
        document.getElementById("change_id_input").classList.toggle("show");
    else{
        document.getElementById("change_id").classList.toggle("show");
        document.getElementById('ids').textContent ='현재 ID: '+localStorage.getItem("Full-ID");
    }
});

changeidBtn.addEventListener('click', (e)=>{
    if(document.getElementById("change_id_input").classList.contains("hide")){
        document.getElementById("change_id_input").classList.toggle("show");
    }else{
        document.getElementById("change_id_input").classList.toggle("show");
    }
    document.getElementById("change_id").classList.toggle("show");
    document.getElementById('input').value=localStorage.getItem("Full-ID");
});

saveIDBtn.addEventListener('click', (e)=>{
    e.preventDefault();
    localStorage.clear();
    full_id=document.getElementById('input').value;
    id=full_id.split("@")[0];
    localStorage.setItem("Full-ID",full_id);
    localStorage.setItem("ID",id);
    load();
    
    if(document.getElementById("change_id").classList.contains("hide")){
        document.getElementById("change_id").classList.toggle("show");
    }else{
        document.getElementById("change_id").classList.toggle("show");
    }
    document.getElementById("change_id_input").classList.toggle("show");
    document.getElementById('ids').textContent ='현재 ID: '+localStorage.getItem("Full-ID");
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
    Asynchronous();
    document.getElementById('title').innerHTML='환영합니다<br>'+id+'님!';
  }
};

window.onload=function(event){
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
    }
  };
