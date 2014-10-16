var map;
var error = false;
var mapShow = false;
var fullLoaded = false;
var airportsshow = false;

var websocket;
var wsUri = "ws://" + document.location.host + ":9999/Radar-Livre/websocket";

var voos = [];
var rota = [];
var aeroportos = [];

//Auxiliares
var listaaeroportos = [];
var flightPlanCoordinates = [];

var routes = [];
var flightPath;

var planeDataConnection;

var AiPlaneSelected;
var getAirPlaneRouteRealTime = false;

$(document).ready(function(){

	$('#sidr-trigger').sidr();
	$( "#target" ).submit(function( event ) {
	  event.preventDefault();
	  var nomevoo = $(".buscavoo").val();
	  websocket.send("buscar("+nomevoo+")");
	});

	$(".close").click(function(){
		$.sidr('close', 'sidr');
	});
	
	try{
		inicializarMapa();
		$(".msgAlerta").show();
	}
	catch(err){
		createLoadingScreenError("Erro ao Inicializar Mapa...");
		error = true;
	}
	
	try{
		websocket = new WebSocket(wsUri);
	}
	catch(err){
		createLoadingScreenError("Erro ao Conectar ao Servidor...");
		error = true;
	}
	
	websocket.onerror = function(event) { 
		error = true;
		if(mapShow == false){
			ohSnap('A conexão com o servidor caiu! :(', 'red');
		}		
	};
	
	websocket.onopen = function(event) { onOpen(event); };
	websocket.onmessage = function(event) { onMessage(event); };
});


function AtualizarRota(){
	//websocket.send("getroute("+aeronave.hex+")");
}

function myTimer() {
	websocket.send("GET");
	if(getAirPlaneRouteRealTime)
		AtualizarRota();

	$.each(voos, function (key, val){
		if(toTimestamp(val.hora) < ($.now() - 60)){
			val.setMap(null);
			voos.remove(val);
		}
	});
	
	if(mapShow == false && error == false){
		$('.progress-bar').css( "width", "100%" );
		$(".loading").fadeOut('slow');
		mapShow = true;
		startTips();
	}
}

function getAirports(){
	var image = 'img/airport-dot.png';
	$.each(listaaeroportos, function (key, val){
		var aeroporto = new google.maps.Marker({
			position: new google.maps.LatLng((val.latitude), (val.longitude)),
			map: map,
			icon: image,
			title: val.icao + " -> " + val.name + " - " + val.city + "/" + val.state
		});
		aeroportos.push(aeroporto);
	});
	airportsshow = true
}

function removeAirports(){ 
	$.each(aeroportos, function (key, val){
		val.setMap(null);
	});
}

/* Funções de Socket */

function onOpen(event){
	$('.progress-bar').css( "width", "20%" );
	var timer = setInterval(function(){myTimer();}, 800);
	websocket.send("GETAirports");
	userLoadMessage('Obtendo lista de aeroportos... ');
	$('.progress-bar').css( "width", "40%" );
}

function onMessage(event){
	var returndata = event.data;

	if(returndata.search("getroute_return:") != -1){
		returndata = returndata.replace("getroute_return:", "");
		var rota = JSON.parse(returndata);
		$.each(rota, function (key, val){
			flightPlanCoordinates.push([val.latitude, val.longitude]);
		});
		
		var flightPlanCoordinatesZ = [];
		for (i = 0; i < flightPlanCoordinates.length; ++i) {
		    var auxlat = flightPlanCoordinates[i][0];
			var auxlon = flightPlanCoordinates[i][1];
			flightPlanCoordinatesZ.push(new google.maps.LatLng(auxlat, auxlon));
		}
		
		flightPath = new google.maps.Polyline({
			path: flightPlanCoordinatesZ,
			geodesic: true,
			strokeColor: '#FF0000',
			strokeOpacity: 0.3,
			strokeWeight: 1.5
		});

		flightPath.setMap(map); 
		flightPlanCoordinatesZ = [];
		flightPlanCoordinates = [];
		flightPath = [];
		
		
		
	}
	
	if(returndata.search("search_return:") != -1){
		returndata = returndata.replace("search_return:", "");
		alert(returndata);
		var aeronave = JSON.parse(returndata);
		$.each(aeronave, function (key, val){
			var auxlat = flightPlanCoordinates[i][0];
			var auxlon = flightPlanCoordinates[i][1];
			var pantoLatLong = new google.maps.LatLng(auxlat, auxlon);
			var cameraView = new google.maps.panTo(pantoLatLong);
		});
	}
	
	if(returndata.search("get_return:") != -1){
		returndata = returndata.replace("get_return:", "");
		//console.log(returndata);
		if(returndata != "None"){
			var aeronave = JSON.parse(returndata);
			i = 0;
			$.each(aeronave, function(key, val){
				if(mapShow == false){
					$('.progress-bar').css( "width", "60%" );
				}
				userLoadMessage('Obtendo lista de voos... ' + i);
				i++;
			
				if(jaExiste(val)){
					atualizarMarcador(val);
				}else{
					$(".msgAlerta").fadeOut("slow");
					adicionarMarcador(val);
				}
			});
			if(mapShow == false){
				$('.progress-bar').css( "width", "80%" );
			}
		}
	}

	if(returndata.search("return_airport:") != -1){
		returndata = returndata.replace("return_airport:", "");
		listaaeroportos = JSON.parse(returndata);
	}

}
	
function timestamp2timedate(time){
    var theDate = new Date(time * 1000);
    return theDate.toGMTString();
}

/* Funções de Interface de Usuario */

function userLoadMessage(Message){
	$('.userLoadMessage').text(Message);
}

function createLoadingScreenError(Message){
	$('.progress-bar').css( "width", "0%" );
	$('.exceptionMessage').append(Message+"<br>");
	$('.progress-bar').hide();
	while(true){
		event.preventDefault();
	}
}

function toTimestamp(strDate){
	var datum = Date.parse(strDate);
	return datum;
}

/* Funções do GMaps */
function inicializarMapa() {
	var appLat = -14.239424;
	var appLon = -53.186502;

	
	var color = [
		{
			"featureType": "road",
			"elementType": "geometry",
			"stylers": [
				{
					"visibility": "off"
				}
			]
		},
		{
			"featureType": "poi",
			"elementType": "geometry",
			"stylers": [
				{
					"visibility": "off"
				}
			]
		},
		{
			"featureType": "landscape",
			"elementType": "geometry",
			"stylers": [
				{
					"color": "#fffffa"
				}
			]
		},
		{
			"featureType": "water",
			"stylers": [
				{
					"lightness": 50
				}
			]
		},
		{
			"featureType": "road",
			"elementType": "labels",
			"stylers": [
				{
					"visibility": "off"
				}
			]
		},
		{
			"featureType": "transit",
			"stylers": [
				{
					"visibility": "off"
				}
			]
		},
		{
			"featureType": "administrative",
			"elementType": "geometry",
			"stylers": [
				{
					"lightness": 40
				}
			]
		}
	];
	
    var mapOptions = {
      center: new google.maps.LatLng(appLat, appLon),
      zoom: 4, 
      disableDefaultUI: true,
	  zoomControl: true,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
	  styles: color
    };
	
    map = new google.maps.Map(document.getElementById("mapa"), mapOptions);
	google.maps.event.addListener(map,'zoom_changed',function(){
	  if(map.getZoom() > 5){
		if(airportsshow == false){
			getAirports();
		}
	  }else{
	    if(airportsshow == true){
			removeAirports();
		}
	  }
	});

	
	//getAirPlaneRouteRealTime = true;
	
}

function MoveCameraTo(lat, lon){
	var pantoLatLong=new google.maps.LatLng(lat, lon);
    var cameraView = new google.maps.panTo(pantoLatLong);
}

/* Funções de voos */

function jaExiste(aeronave){
	var aux = 0;
	$.each(voos, function (key, val){
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

function adicionarMarcador(aeronave){
	if(aeronave.head == null){
		aeronave.head = 1;
	}
	var image = new google.maps.MarkerImage('img/aeronaves/rotacionado'+ aeronave.head +'.png',new google.maps.Size(25,25),new google.maps.Point(0,0),new google.maps.Point(13,12));
	var marcador = new google.maps.Marker({
		position: new google.maps.LatLng(aeronave.latitude, aeronave.longitude),
        map: map,
        icon: image,
        title: aeronave.hex,
        hora: aeronave.hora,
		id: aeronave.id,
		timestamp: aeronave.timestamp
	});
	voos.push(marcador);
	google.maps.event.addListener(marcador, 'click', function() {
		
		$.sidr('open', 'sidr');
		$("#hex").text(aeronave.hex);
		AiPlaneSelected = aeronave.hex;
		getAirPlaneRouteRealTime = true;
		$("#idvoo").text(aeronave.id);
		var w = identifyFlightInformations(aeronave.id);
		if(!w[0]){
			var w = ['-', '-'];
		}
		$("#origem").text(w[0]);
		$("#destino").text(w[1]);
		$("#latitude").text(aeronave.latitude);
		$("#longitude").text(aeronave.longitude);
		$("#altitude").text(aeronave.altitude+' ft / '+ (aeronave.altitude*0.3048).toFixed(2)+' m');
		$("#grau").text(aeronave.head+'°');
		
		if(aeronave.velocidadegnd != null){
			velocidade = aeronave.velocidadegnd * 1.852;
		}
		
		$("#velocidade").text(aeronave.velocidadegnd + ' knots / '+ velocidade.toFixed(2) + ' km/h');
		$("#hora").text(aeronave.hora);
		$("#datahora").text(timestamp2timedate(aeronave.timestamp));
		
		removerRota();
		websocket.send("getroute("+aeronave.hex+")");
		
	});
	
}

function removerVoo(){
	$.each(voos, function (key, val){
		val.setMap(null);
	});
	voos.remove(aeronave);
}

function removerRota(){
	$.each(rota, function (key, val){
		val.setMap(null);
		rota = [];
	});
}

function atualizarMarcador(aeronave){ 
	$.each(voos, function (key, val){
		
		if(val.title == aeronave.hex){
			if(aeronave.latitude != null){
				val.setPosition(new google.maps.LatLng(aeronave.latitude, aeronave.longitude));
			}
			if(aeronave.head != null){
				val.setIcon(new google.maps.MarkerImage('img/aeronaves/rotacionado'+ aeronave.head +'.png',new google.maps.Size(25,25),new google.maps.Point(0,0),new google.maps.Point(13,12)));
			}
			google.maps.event.addListener(val, 'click', function() {
				console.log('atualizando');
				$.sidr('open', 'sidr');
				$("#hex").text(aeronave.hex);
				
				if(aeronave.id != null){
					airLineData = identifyAirLineInformations(aeronave.id);
					var d = identifyFlightInformations(aeronave.id);
					if(!d[0]){
						var d = ['-', '-'];
						
					};
					$("#origem").text(d[0]);
					$("#destino").text(d[1]);
					$("#idvoo").text(airLineData[0]+" / "+aeronave.id);
					$("#linha").text(airLineData[1]+" - "+airLineData[2]);
				}
				
				if(aeronave.latitude != null){
					$("#latitude").text(aeronave.latitude);
					$("#longitude").text(aeronave.longitude);
				}
				if(aeronave.altitude != null){
					$("#altitudeft").text(aeronave.altitude+' ft');
					$("#altitudemt").text((aeronave.altitude*0.3048).toFixed(2)+' m');
				}
				if(aeronave.head != null){
					$("#grau").text(aeronave.head+'°');
				}
				if(aeronave.velocidadegnd != null){
					velocidade = aeronave.velocidadegnd * 1.852;
					$("#velocidade").text(aeronave.velocidadegnd+' knots / '+velocidade.toFixed(2)+' km/h');
				}
				$("#datahora").text(timestamp2timedate(aeronave.timestamp));
			});
			
		}
	});
}

Array.prototype.remove = function(value) {
	var idx = this.indexOf(value);
	if (idx != -1) {
		return this.splice(idx, 1); 
	}
	return false;
};