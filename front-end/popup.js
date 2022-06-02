// localStorage.clear();
function getCurrentTabUrl(callback) {
  var queryInfo = {
    active: true,
    currentWindow: true
  };
  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;
    callback(url);
  });
}

function renderURL(statusText) {
  document.getElementById('urls').textContent = statusText;
}

document.addEventListener('DOMContentLoaded', function() {
  var link = document.getElementById('getUrl');
  getCurrentTabUrl(function(url) {
    renderURL(url);
    console.log(url);
  });
});

// window.onload=function(event){ //페이지 추가 전
//   document.getElementById('ids').textContent = localStorage.getItem("ID");
//   if(localStorage.length==0){
//     function loadPopup(event){
//       if(document.getElementById("popup-overlay").classList.contains("popup-hide")){
//         document.getElementById("popup-overlay").classList.remove("popup-hide");
//        }else{
//         document.getElementById("popup-overlay").classList.add("popup-show");
//       }
//     }
//     setTimeout(loadPopup, 3000);
//   }else{
//     id=localStorage.getItem("ID");
//     document.getElementById('title').textContent='환영합니다\n'+id+'님!';
//     // var url="http://115.85.181.5:30001/"+id;
//     var url='./hugom.json'
//     fetch(url)
//         .then((response) => {
//         return response.json();
//         })
//         .then((json) => {
//             console.log(json);
//             console.log(json["recommendation"]);
//             // keys=Object.keys(json.recommendation);
//             console.log(Object.keys(json.recommendation));
//             localStorage.setItem("rec_key",JSON.stringify(Object.keys(json.recommendation)));
//             // values=Object.values(json.recommendation);
//             console.log(Object.values(json.recommendation));
//             localStorage.setItem("rec_value",JSON.stringify(Object.values(json.recommendation)));
//         })
//         .catch((err) => {
//             console.log(err);
//         });
    
//   }
// };
window.onload=function(event){ //페이지 추가 전 json 파일 수정
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
    // var url="http://115.85.181.5:30001/"+id;
    // var url='./hugom.json'
    // var url='./output_hugom.json'
    var url='./output_artsdesign.json'
    fetch(url)
        .then((response) => {
        return response.json();
        })
        .then((json) => {
            console.log(json);
            console.log(json["recommendation"]);
            // console.log(Object.keys(json.recommendation));
            // console.log(Object.values(json.recommendation));
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
};
