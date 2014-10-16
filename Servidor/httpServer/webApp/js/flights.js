var flightData = [
	["ONE6370",  "GRU(São Paulo)",  		"FOR(Fortaleza)"],
	["GLO1828",  "GRU(São Paulo)",  		"FOR(Fortaleza)"],
	["TAM3324",  "GRU(São Paulo)",  		"FOR(Fortaleza)"],
	["TAM8084",  "GRU(São Paulo)", 		 "LHR(Londres)"],
	["ONE6271",  "GIG(Rio de Janeiro)",  "FOR(Fortaleza)"],
	["TAM8063",  "MXP(Milão)",      	 "GRU(São Paulo)"],
	["TAM8065",  "MAD(Madri)",      	 "GRU(São Paulo)"],
	["BAW247",   "LHR(Londres)",    "GRU(São Paulo)"],
	["GOL1821",  "FOR(Fortaleza)",  "GRU(São Paulo)"],
	["TAM3858",  "SSA(Salvador)",  	"FOR(Fortaleza)"],
	["GOL1242",  "NAT(Natal)",      "FOR(Fortaleza)"],
	["GLO1096",  "SSA(Salvador)",   "FOR(Fortaleza)"],
	["TAM3742",  "FOR(Fortaleza)",  "BEL(Belem)"],
	["GOL1650",  "FOR(Fortaleza)",  "REC(Recife)"],
	["TAM3062",  "BSB(Bralisia)",   "FOR(Fortaleza)"],
	["ONE6390",  "GRU(São Paulo)",  "FOR(Fortaleza)"],
	["ONE6374",  "BSB(Bralisia)",   "FOR(Fortaleza)"],
	["GLO1912",  "SLZ(Sao Luis)",   "FOR(Fortaleza)"],
	["TAM3840",  "THE(Teresina)",   "FOR(Fortaleza)"],
	["TAM3835",  "FOR(Fortaleza)",  "SSA(Salvador)"],
	["TAM3879",  "FOR(Fortaleza)",  "GRU(São Paulo)"],
	["GOL1900",  "GRU(Sao Paulo)",  "FOR(Fortaleza)"],
	["KLM791",   "AMS(Amsterdam)",  "GRU(São Paulo)"],
	["TAP67",    "OPO(Porto)",      "GIG(Rio de Janeiro)"],
	["DLH500",   "FRA(Frankfurt)",  "GIG(Rio de Janeiro)"],
];

function identifyFlightInformations(airCode){
	if (airCode != null){
		airCode = airCode.replace(/\s/g, '');
		var dest;
		var orin;
		var ret = ['-', '-'];
		
		for (var i = 0; i < flightData.length; i++) {
			if(airCode == flightData[i][0]){
				console.log("Bateu");
				dest = flightData[i][1];
				orin = flightData[i][2];
			}
		}
		ret = [dest, orin];
		return ret;
	}
}
