if(localStorage.getItem("ID")==null){
    document.getElementById('title').innerHTML='환영합니다';
}else{
    document.getElementById('title').innerHTML='환영합니다<br>'+localStorage.getItem("ID")+'님!';
    const txt=document.getElementById("text");
    if(localStorage.getItem("over30")=="false"){
        txt.innerHTML="<br>NFT 구매 내역이 부족해요!<br>그렇다면 가장 인기가 많은 NFT 10개는 어떠신가요?";
        txt.style.textAlign="center";
        txt.style.fontSize="17px";
    }else{
        txt.innerHTML="<br>NFT를 구매하신 적이 있네요!<br>그렇다면 이러한 비슷한 상품들은 어떠신가요?";
        txt.style.textAlign="center";
        txt.style.fontSize="17px";
    }
    var imageUrl = localStorage.getItem("rec_key");
    var image_link=localStorage.getItem("rec_value");
    var arr=JSON.parse(imageUrl);
    var arr_link=JSON.parse(image_link);

    for(i=1; i<=10; i++){
        const image1=document.getElementById('image'+i);
        const video1=document.getElementById('video'+i);
        if(arr_link[i-1].extension=='jpg'||arr_link[i-1].extension=='png'||arr_link[i-1].extension=='gif'){
            video1.style.display='none';
            image1.style.display='block';
            image1.style.backgroundImage= "url('" + arr[i-1] + "')";
            document.getElementById("likes"+i).innerHTML="❤ "+arr_link[i-1].likes;
            document.getElementById('image'+i+'_link').setAttribute('href',arr_link[i-1].url);
            document.getElementById('image'+i+'_link_').style.display='none'
        }else{
            image1.style.display='none';
            video1.style.height='300px'
            video1.style.width='240px'
            video1.style.display='block';
            video1.setAttribute('src',arr[i-1]);
            document.getElementById("likes"+i+"_1").innerHTML="❤ "+arr_link[i-1].likes;
            document.getElementById('image'+i+'_link_').setAttribute('href',arr_link[i-1].url);
        }
    }
}