var map;
var marcadores = [];
var error = false;
var routes = [];
var websocket;
var flightPlanCoordinates = [];
var mapShow = false;
var wsUri = "ws://" + document.location.host + ":9999/Radar-Livre/websocket";
var listaaeroportos = [];
var marker = [];
var fullLoaded = false;

/*
 vooorigem
 voodestino
 aircraftcatandtype
 aircraftsk

 
 formatTypeCode = [
  [None],
  [
    "D - Reservado" ,
  ],
  [
    "C",
    [
      "No aircraft category information",
      "Surface vehicle - emergency vehicle",
      "Surface vehicle - service vehicle",
      "Fixed ground or tethered obstruction",
      "Reserved",
      "Reserved",
      "Reserved",
      "Reserved"
    ]
  ],
  [
    "B",
    [
      "No aircraft category information",
      "Glider/sailplane",
      "Lighter-than-air",
      "Parachutist/skydiver",
      "Ultralight/hang-glider/paraglider",
      "Reserved",
      "Unmanned aerial vehicle",
      "Space/transatmospheric vehicle"
    ]
  ],
  [
    "A",
    [
      "No aircraft category information",
      "Light (< 15 500 lbs or 7 031 kg)",
      "Medium 1 (>15 500 to 75 000 lbs, or 7 031 to 34 019 kg)",
      "Medium 2 (>75 000 to 300 000 lbs, or 34 019 to 136 078 kg)",
      "High vortex aircraft",
      "Heavy (> 300 000 lbs or 136 078 kg)",
      "High performance (> 5g acceleration) and high speed (> 400 kt)",
      "Rotorcraft"
    ]
  ]
]
 
 
*/

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

function myTimer() {
	websocket.send("GET");
	$.each(marcadores, function (key, val){
		if(toTimestamp(val.hora) < ($.now() - 60)){
			console.log("Removendo");
			val.setMap(null);
			marcadores.remove(val);
		}
	});
	
	if(mapShow == false && error == false){
		$('.progress-bar').css( "width", "100%" );
		$(".loading").fadeOut('slow');
		mapShow = true;
		startTips();
	}
}

var airportsshow = false;

function getAirports(){
	var image = 'img/airport-terminal.png';
	$.each(listaaeroportos, function (key, val){
		i++;
		marker = new google.maps.Marker({
			position: new google.maps.LatLng((val.latitude), (val.longitude)),
			map: map,
			icon: image,
			title: val.name + " - " + val.state + " - " + val.latitude
		});
		i++;
	});
	marker.setMap(map);
	airportsshow = true
}

function removeAirports(){

   /* for (i in marker) {
        marker[i].setMap(null);
    }
	alert(); */
  
  airportsshow = false;
  
}

/* Funções de Socket */

function onOpen(event){
	$('.progress-bar').css( "width", "20%" );
	var timer = setInterval(function(){myTimer();}, 1000);
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
		
		var flightPath = new google.maps.Polyline({
			path: flightPlanCoordinatesZ,
			geodesic: true,
			strokeColor: '#FF0000',
			strokeOpacity: 1.0,
			strokeWeight: 2
		});

		flightPath.setMap(map); 
		flightPlanCoordinatesZ = [];
		flightPlanCoordinates = [];
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
		var aeronave = JSON.parse(returndata);
		i = 0;
		$.each(aeronave, function(key, val){
			if(mapShow == false){
				$('.progress-bar').css( "width", "60%" );
			}
			userLoadMessage('Obtendo lista de voos... ' + i);
			i++;
		
			if(jaExiste(val)){
				console.log("Atualizando");
				atualizarMarcador(val);
			}else{
				$(".msgAlerta").fadeOut("slow");
				console.log("Adicionando");
				adicionarMarcador(val);
			}
		});
		if(mapShow == false){
			$('.progress-bar').css( "width", "80%" );
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

function createErrorMessageBox(Message){}

/* Funções do GMaps */

function toTimestamp(strDate){
	var datum = Date.parse(strDate);
	return datum;
}

function inicializarMapa() {
	var appLat = -14.239424;
	var appLon = -53.186502;

    var mapOptions = {
      center: new google.maps.LatLng(appLat, appLon),
      zoom: 4, 
      disableDefaultUI: true,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
	
    map = new google.maps.Map(document.getElementById("mapa"), mapOptions);
	//getAirports();
	
	google.maps.event.addListener(map,'zoom_changed',function(){
	  if(map.getZoom() == 7){
		getAirports();
	  }else{
	    //if(airportsshow == true){
			removeAirports();
		//}
	  }
	  
	});

}

function MoveCameraTo(lat, lon){
	var pantoLatLong=new google.maps.LatLng(lat, lon);
    var cameraView = new google.maps.panTo(pantoLatLong);
}

/* Funções de Marcadores */

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
		velocidade: aeronave.velocidadegnd,
		timestamp: aeronave.timestamp
	});
	marcadores.push(marcador);
	google.maps.event.addListener(marcador, 'click', function() {
		
		$.sidr('open', 'sidr');
		$("#hex").text(aeronave.hex);
		$("#idvoo").text(aeronave.id);
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
		
		websocket.send("getroute("+aeronave.hex+")");
		
	});
}

function removerMarcador(aeronave){
	return 0;
//	$.each(marcadores, function (key, val){
//		if(val.title == aeronave.hex){
//			val.setMap(null);
//		}
//	});
//	marcadores.remove(aeronave);
}

function atualizarMarcador(aeronave){ 
	$.each(marcadores, function (key, val){
		
		if(val.title == aeronave.hex){
			if(aeronave.latitude != null){
				val.setPosition(new google.maps.LatLng(aeronave.latitude, aeronave.longitude));
			}
			if(aeronave.head != null){
				val.setIcon(new google.maps.MarkerImage('img/aeronaves/rotacionado'+ aeronave.head +'.png',new google.maps.Size(25,25),new google.maps.Point(0,0),new google.maps.Point(13,12)));
			}
			google.maps.event.addListener(val, 'click', function() {
				websocket.send("getroute("+aeronave.hex+")");
				$.sidr('open', 'sidr');
				$("#hex").text(aeronave.hex);
				
				if(aeronave.id != null){
					airLineData = identifyAirLineInformations(aeronave.id);
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
			val.hora = aeronave.hora;
			console.log(val.hora);
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