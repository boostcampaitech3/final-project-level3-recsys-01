var imageUrl = localStorage.getItem("rec_key");
var image_link=localStorage.getItem("rec_value");
var arr=JSON.parse(imageUrl);
var arr_link=JSON.parse(image_link);
console.log(arr_link[0].url[0]);

for(i=1; i<=10; i++){
    const image1=document.getElementById('image'+i);
    const video1=document.getElementById('video'+i);
    if(arr_link[i-1].extension=='jpg'||arr_link[i-1].extension=='png'||arr_link[i-1].extension=='gif'){
        video1.style.display='none';
        image1.style.display='block';
        image1.style.backgroundImage= "url('" + arr[i-1] + "')";
    }else{
        image1.style.display='none';
        video1.style.height='300px'
        video1.style.width='240px'
        video1.style.display='block';
        video1.setAttribute('src',arr[i-1]);
    }
    document.getElementById('image'+i+'_link').setAttribute('href',arr_link[i-1].url[0]);
    document.getElementById("likes"+i).innerHTML="❤ "+arr_link[i-1].likes;
}