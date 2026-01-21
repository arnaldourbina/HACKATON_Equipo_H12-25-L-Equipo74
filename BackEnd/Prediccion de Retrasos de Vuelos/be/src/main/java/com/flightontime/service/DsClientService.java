package com.flightontime.service;

import com.flightontime.dto.FlightInput;
import com.flightontime.dto.PredictionOutput;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
public class DsClientService {
    private final RestTemplate restTemplate;
    private final String dsUrl;

    public DsClientService(RestTemplate restTemplate,
            @Value("${ds.service.url:http://localhost:5000/predict}") String dsUrl) {
        this.restTemplate = restTemplate;
        this.dsUrl = dsUrl;
        System.out.println("DS URL configurada: " + dsUrl);
    }

    public PredictionOutput predict(FlightInput input) {
        System.out.println("nviando a DS: " + input);
        try {

            FlightInput isoInput = new FlightInput();
            isoInput.aerolinea = input.aerolinea;
            isoInput.origen = input.origen;
            isoInput.destino = input.destino;
            isoInput.distancia_km = input.distancia_km;
            isoInput.fecha_partida = input.fecha_partida != null ? input.fecha_partida.toString() : null; // ISO-8601
                                                                                                          // string

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<FlightInput> request = new HttpEntity<>(isoInput, headers);

            PredictionOutput result = restTemplate.postForObject(dsUrl, request, PredictionOutput.class);
            System.out.println("Servicio DS Ok: " + result);
            return result;
        } catch (Exception e) {
            System.err.println("Servicio DS Error: " + e.getMessage());
            e.printStackTrace();
            throw new RestClientException("Proxy DS falló", e);
        }
    }
}