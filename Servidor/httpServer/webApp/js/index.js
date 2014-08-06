var map;
var marcadores = [];

var appLat, appLon; 
appLat = -14.239424;
appLon = -53.186502;

var error = false;

$(document).ready(function(){
	
	if (navigator.geolocation) {
	  navigator.geolocation.getCurrentPosition(showpos,erropos);
	}

	$(".close").click(function(){
		$.sidr('close', 'sidr');
	});
	
	try{
		inicializarMapa();
	}
	catch(err){
		createLoadingScreenError("Erro ao Inicializar Mapa...");
		error = true;
	}
	
	$('#sidr-trigger').sidr();
	
	var wsUri = "ws://" + document.location.host + ":9999/Radar-Livre/websocket";
	try{
		var websocket = new WebSocket(wsUri);
	}
	catch(err){
		createLoadingScreenError("Erro ao Conectar ao Servidor de Dados ADS-B...");
		error = true;
	}
	
	websocket.onerror = function(event) { 
		//verifica se o elemento do loading existe
		error = true;
	};
	websocket.onopen = function(event) { onOpen(event); };
	websocket.onmessage = function(event) { onMessage(event); };
	
	if(error == false)
			removeLoadingScreen();
	
	var timer = setInterval(function(){myTimer();},1000);

	function myTimer() {
		console.log("Timer passando");
		websocket.send("GET");
		$.each(marcadores, function (key, val){
			if(toTimestamp(val.hora) < ($.now() - 120000)){
				console.log("Removendo")
				val.setMap(null);
				marcadores.remove(val);
			}
		});
		
	}
	
});

function showpos(position){
  appLat=position.coords.latitude;
  appLon=position.coords.longitude;
 
  try{
		inicializarMapa();
	}
	catch(err){
		createLoadingScreenError("Erro ao Inicializar Mapa...");
		error = true;
	}
	
}

function erropos(error){
	console.log("Erro");
}

function removeLoadingScreen(){
	$(".loading").fadeOut('slow');
}

function createLoadingScreenError(Message){
	$('.exceptionMessage').append(Message);
}

function createErrorMessageBox(Message){

}

function toTimestamp(strDate){
	var datum = Date.parse(strDate);
	return datum;
}

function inicializarMapa() {

    var mapOptions = {
      center: new google.maps.LatLng(appLat, appLon),
      zoom: 4, 
      disableDefaultUI: true,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
	
    map = new google.maps.Map(document.getElementById("mapa"),
        mapOptions);
    
	google.maps.event.addListener(map,'click', function(){
		$.sidr('close', 'sidr');
	});
}

function onOpen(event){

}

function jaExiste(aeronave){
	var aux = 0;
	$.each(marcadores, function (key, val){
		if(val.title == aeronave.hex){
			aux++;
		}
	});
	if(aux == 0){
		return false;
	}else{
		return true;
	}
}

function onMessage(event){
	var aeronave = JSON.parse(event.data);
	
	$.each(aeronave, function(key, val){
		if(jaExiste(val)){
			console.log("Atualizando");
			atualizarMarcador(val);
		}else{
			console.log("Adicionando");
			adicionarMarcador(val);
		}
	});
	
/*	switch(aeronave.status){
	case "ADD":
		adicionarMarcador(aeronave);
		break;
	case "REMOVE":
		removerMarcador(aeronave);
		break;
	case "UPDATE":
		atualizarMarcador(aeronave);
		break;
	}*/
}

function adicionarMarcador(aeronave){
	if(aeronave.grau == null){
		aeronave.grau = 1;
	}
	var image = new google.maps.MarkerImage('img/aeronaves/rotacionado'+ aeronave.grau +'.png',new google.maps.Size(25,25),new google.maps.Point(0,0),new google.maps.Point(13,12));
	var marcador = new google.maps.Marker({
		position: new google.maps.LatLng(aeronave.latitude, aeronave.longitude),
        map: map,
        icon: image,
        title: aeronave.hex,
        hora: aeronave.hora
	});
	marcadores.push(marcador);
	google.maps.event.addListener(marcador, 'click', function() {
		$.sidr('open', 'sidr');
		$("#hex").text(aeronave.hex);
		$("#latitude").text(aeronave.latitude);
		$("#longitude").text(aeronave.longitude);
		$("#altitude").text(aeronave.altitude);
		$("#grau").text(aeronave.grau);
		$("#velocidade").text(aeronave.velocidade);
		$("#hora").text(aeronave.hora);
	});
}

//function removerMarcador(aeronave){
//	$.each(marcadores, function (key, val){
//		if(val.title == aeronave.hex){
//			val.setMap(null);
//		}
//	});
//	marcadores.remove(aeronave);
//}

function atualizarMarcador(aeronave){ 
	$.each(marcadores, function (key, val){
		if(val.title == aeronave.hex){
			if(aeronave.latitude != null){
				val.setPosition(new google.maps.LatLng(aeronave.latitude, aeronave.longitude));
			}
			if(aeronave.grau != null){
				if(aeronave.grau != null){
					aeronave.grau = 1;
				}
				val.setIcon(new google.maps.MarkerImage('img/aeronaves/rotacionado'+ aeronave.grau +'.png',new google.maps.Size(25,25),new google.maps.Point(0,0),new google.maps.Point(13,12)));
			}
			google.maps.event.addListener(val, 'click', function() {
				$.sidr('open', 'sidr');
				$("#hex").text(aeronave.hex);
				if(aeronave.latitude != null){
					$("#latitude").text(aeronave.latitude);
					$("#longitude").text(aeronave.longitude);
				}
				if(aeronave.altitude != null){
					$("#altitude").text(aeronave.altitude);
				}
				if(aeronave.grau != null){
					$("#grau").text(aeronave.grau);
				}
				if(aeronave.velocidade != null){
					$("#velocidade").text(aeronave.velocidade);
				}
				$("#hora").text(aeronave.hora);
			});
			val.hora = aeronave.hora;
			console.log(val.hora);
		}
	});
}
//Removes an element from an array.
//String value: the value to search and remove.
//return: an array with the removed element; false otherwise.
Array.prototype.remove = function(value) {
	var idx = this.indexOf(value);
	if (idx != -1) {
		return this.splice(idx, 1); // The second parameter is the number of elements to remove.
	}
	return false;
};

//$.sidr('open', 'sidr');
//$.sidr('close', 'sidr');