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

// emInput.addEventListener('blur', (e)=>{
//     if(emInput.value === ''){
//         e.target.parentElement.children[1].style = ph_style_set;
//     }
// });

ph_email.addEventListener('click', (e)=>{
    e.target.parentElement.children[0].focus();
});

function getJsonFile(id){
    var url="http://115.85.181.5:30001/"+id;
    fetch(url)
        .then((response) => {
        return response.json();
        })
        .then((json) => {
            console.log(json);
            // localStorage.setItem("recommendation",json["recommendation"]);
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
    document.getElementById('ids').textContent = '현재 ID: '+id;
    document.getElementById('input').value=id;
    document.getElementById('title').textContent='환영합니다\n'+id+'님!';
    // var url="http://118.67.128.97:30001/"+emInput.value;
    // var url="http://115.85.181.5:30001/"+id;
    // fetch(url)
    //     .then((response) => {
    //     return response.json();
    //     })
    //     .then((json) => {
    //         console.log(json);
    //     })
    //     .catch((err) => {
    //         console.log(err);
    //     });
    
    getJsonFile(id)
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
    if(document.getElementById("change_id").classList.contains("hide")){
        document.getElementById("change_id").classList.toggle("show");
    }else{
        document.getElementById("change_id").classList.toggle("show");
    }
    document.getElementById("change_id_input").classList.toggle("show");

    localStorage.setItem("Full-ID",document.getElementById('input').value);
    localStorage.setItem("ID",document.getElementById('input').value.split("@")[0]);
    // getJsonFile(document.getElementById('input').value.split("@")[0])
    console.log(3);
});

cancelIDBtn.addEventListener('click', (e)=>{
    document.getElementById("change_id_input").classList.toggle("show");
});
