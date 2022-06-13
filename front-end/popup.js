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
