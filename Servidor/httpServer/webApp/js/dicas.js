var tip = ["Você pode visualizar aeroportos de uma determinada <br> área dando zoom em sua direção.", 
		   "Você poderá ver informações sobre a aeronave,<br> rota e voo clicando nos icones dos aviões."];

var t = 0;
function tipRemove(){
	$('.tipbox').fadeOut('slow'); //trocar isso por um slide lateral 
}

function nextTip(){
    //implementar um slide lateral
	ohSnap(tip[t], 'blue');
	//$(".messagetip").text(tip[i]);
	t++;
	tipRemove();
}

function startTips(){
	var tipTime = setTimeout("nextTip()", 4000);
	var tipTime2 = setTimeout("nextTip()", 10000);
}