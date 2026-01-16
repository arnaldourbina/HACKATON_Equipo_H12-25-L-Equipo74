@PostMapping
public PredictionOutput predict(@Valid @RequestBody FlightInput input) {
    RestTemplate restTemplate = new RestTemplate();

    // Llamada al microservicio Python
    ResponseEntity<Map> response = restTemplate.postForEntity(
        "http://localhost:5000/predict", input, Map.class);

    Map<String, Object> result = response.getBody();

    PredictionOutput output = new PredictionOutput();
    output.setAerolinea(input.getAerolinea());
    output.setNumeroVuelo(input.getNumeroVuelo());
    output.setOrigen(input.getOrigen());
    output.setDestino(input.getDestino());
    output.setFechaPartida(input.getFechaPartida().toString());
    output.setDistanciaKm(input.getDistanciaKm());

    // Valores devueltos por Python
    int delayMinutes = (Integer) result.get("delayMinutes");
    String status = (String) result.get("status");

    output.setDelayMinutes(delayMinutes);
    output.setStatus(status);

    return output;
}