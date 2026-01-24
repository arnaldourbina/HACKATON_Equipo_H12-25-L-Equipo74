package com.flightontime.service;

import com.flightontime.dto.ExplainOutput;
import com.flightontime.dto.FlightEmail;
import com.flightontime.dto.FlightInput;
import com.flightontime.dto.PredictionOutput;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class DsClientService {
    private final RestTemplate restTemplate;
    private final String dsUrl;

    public DsClientService(RestTemplate restTemplate,
            @Value("${ds.service.url:http://localhost:5000}") String dsUrl) {
        this.restTemplate = restTemplate;
        this.dsUrl = dsUrl;
        System.out.println("DS URL configurada: " + dsUrl);
    }

    public PredictionOutput predict(FlightInput input) {
        System.out.println("enviando a DS: " + input);
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

            String url = dsUrl + "/predict";
            PredictionOutput result = restTemplate.postForObject(url, request, PredictionOutput.class);
            System.out.println("Servicio DS Ok: " + result);
            return result;
        } catch (Exception e) {
            System.err.println("Servicio DS Error: " + e.getMessage());
            e.printStackTrace();
            throw new RestClientException("Proxy DS falló", e);
        }
    }

    public List<PredictionOutput> predictBatch(List<FlightInput> vuelos) {
        List<PredictionOutput> resultados = new ArrayList<>();
        for (FlightInput vuelo : vuelos) {
            resultados.add(predict(vuelo));
        }
        return resultados;
    }

    public ExplainOutput explain(FlightInput input) {
        System.out.println("Enviando a DS /explain: " + input);
        try {
            FlightInput isoInput = new FlightInput();
            isoInput.aerolinea = input.aerolinea;
            isoInput.origen = input.origen;
            isoInput.destino = input.destino;
            isoInput.distancia_km = input.distancia_km;
            isoInput.fecha_partida = input.fecha_partida;

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<FlightInput> request = new HttpEntity<>(isoInput, headers);

            String url = dsUrl + "/explain";
            ExplainOutput result = restTemplate.postForObject(url, request, ExplainOutput.class);
            return result;
        } catch (Exception e) {
            throw new RestClientException("Proxy DS /explain falló", e);
        }
    }

    public Map<String, Object> sendAlert(FlightEmail input) {
        System.out.println("Enviando a DS /send-alert: " + input);
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<FlightEmail> request = new HttpEntity<>(input, headers);

            String url = dsUrl + "/send-alert";
            @SuppressWarnings("unchecked")
            Map<String, Object> resp = restTemplate.postForObject(url, request, Map.class);
            return resp;
        } catch (Exception e) {
            throw new RestClientException("Proxy DS /send-alert falló", e);
        }
    }
}