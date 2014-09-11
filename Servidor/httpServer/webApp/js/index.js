/*

	Verificar Sistema de Busca
	Implementar Sistema de
	Implementar FollowCamera
	Implementar AirLine NameList
	Implementar Airplane Remover
	
*/

var map;
var marcadores = [];
var error = false;
var routes = [];
var websocket;
var flightPlanCoordinates = [];

$(document).ready(function(){

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
	
	$('#sidr-trigger').sidr();
	
	var wsUri = "ws://" + document.location.host + ":9999/Radar-Livre/websocket";
	try{
		websocket = new WebSocket(wsUri);
	}
	catch(err){
		createLoadingScreenError("Erro ao Conectar ao Servidor de Dados ADS-B...");
		error = true;
	}
	
	websocket.onerror = function(event) { 
		//verifica se o elemento do loading existe
	    //identifica o typo de erro
		error = true;
		$(".msgAlerta").hide();
		$(".msgErro").show();
		
	};
	
	websocket.onopen = function(event) { onOpen(event); };
	websocket.onmessage = function(event) { onMessage(event); };
	
	if(error == false)
		removeLoadingScreen();
		generateAiportPoints();
		
	var timer = setInterval(function(){myTimer();}, 10000);

	function myTimer() {
		websocket.send("GET");
		
		$.each(marcadores, function (key, val){
			if(toTimestamp(val.hora) < ($.now() - 120000)){
				console.log("Removendo");
				val.setMap(null);
				marcadores.remove(val);
			}
		});
		
	}
	
});
	
function generateAiportPoints(){
  var image = 'img/airport-terminal.png';
  var myLatLng = new google.maps.LatLng(-3.776945,-38.533119);
  var beachMarker = new google.maps.Marker({
      position: myLatLng,
      map: map,
	  title: 'Aeroporto Internacional Pinto Martins - FOR',
      icon: image
  });
}
	
function timestamp2timedate(time){
    var theDate = new Date(time * 1000);
    return theDate.toGMTString();
}
	
function erropos(error){
	console.log("Erro");
}

function removeLoadingScreen(){
	$(".loading").fadeOut('slow');
}

function createLoadingScreenError(Message){
    $(".msgAlerta").hide();
	$('.exceptionMessage').append(Message+"<br>");
}

function createErrorMessageBox(Message){

}

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
	
    map = new google.maps.Map(document.getElementById("mapa"),
        mapOptions);
    
	//google.maps.event.addListener(map,'click', function(){
	//	$.sidr('close', 'sidr');
	//});
}

function onOpen(event){}

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
	var returndata = event.data;
	
	if(returndata.search("getroute_return:") != -1){
		returndata = returndata.replace("getroute_return:", "");
		var rota = JSON.parse(returndata);
		$.each(rota, function (key, val){
			flightPlanCoordinates.push([val.latitude, val.longitude]);
		});
	}
	
	if(returndata.search("search_return:") != -1){
		returndata = returndata.replace("search_return:", "");
		alert(returndata);
		var aeronave = JSON.parse(returndata);
		$.each(aeronave, function (key, val){
			var auxlat = flightPlanCoordinates[i][0];
			var auxlon = flightPlanCoordinates[i][1];
			var pantoLatLong=new google.maps.LatLng(auxlat, auxlon);
			var cameraView = new google.maps.panTo(pantoLatLong);
		});
	}
	
	if(returndata.search("get_return:") != -1){
		returndata = returndata.replace("get_return:", "");
		var aeronave = JSON.parse(returndata);
		$.each(aeronave, function(key, val){
			if(jaExiste(val)){
				console.log("Atualizando");
				atualizarMarcador(val);
			}else{
				$(".msgAlerta").fadeOut("slow");
				console.log("Adicionando");
				adicionarMarcador(val);
			}
		});
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
		$("#altitudeft").text(aeronave.altitude+' ft');
		$("#altitudemt").text((aeronave.altitude*0.3048).toFixed(2)+' m');
		$("#grau").text(aeronave.head+'°');
		$("#velocidade").text(aeronave.velocidadegnd + ' knots');
		
		if(aeronave.velocidadegnd != null){
			velocidade = aeronave.velocidadegnd * 1.852;
		}
		
		$("#velocidadekmh").text(velocidade.toFixed(2) + ' km/h');
		$("#hora").text(aeronave.hora);
		
		websocket.send("getroute("+aeronave.hex+")");
		
		$("#datahora").text(timestamp2timedate(aeronave.timestamp));
		
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
			if(aeronave.head != null){
				val.setIcon(new google.maps.MarkerImage('img/aeronaves/rotacionado'+ aeronave.head +'.png',new google.maps.Size(25,25),new google.maps.Point(0,0),new google.maps.Point(13,12)));
			}
			google.maps.event.addListener(val, 'click', function() {
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
					$("#velocidade").text(aeronave.velocidadegnd+' knots');
					velocidade = aeronave.velocidadegnd * 1.852;
					$("#velocidadekmh").text(velocidade.toFixed(2)+' km/h');
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
		return this.splice(idx, 1); // The second parameter is the number of elements to remove.
	}
	return false;
};