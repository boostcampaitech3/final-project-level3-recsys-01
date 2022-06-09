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
    document.getElementById('title').textContent='환영합니다\n'+id+'님!';
  }
};