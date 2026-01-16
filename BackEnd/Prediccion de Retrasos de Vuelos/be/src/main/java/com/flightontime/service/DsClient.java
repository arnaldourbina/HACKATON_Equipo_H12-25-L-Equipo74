package com.flightontime.service;

import com.flightontime.dto.FlightInput;
import com.flightontime.dto.PredictionOutput;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
public class DsClient {
  private final RestTemplate restTemplate = new RestTemplate();

  @Value("${ds.baseUrl}")
  private String baseUrl;

  public PredictionOutput predict(FlightInput input) {
    try {
      String url = baseUrl + "/predict";
      HttpHeaders headers = new HttpHeaders();
      headers.setContentType(MediaType.APPLICATION_JSON);
      HttpEntity<FlightInput> entity = new HttpEntity<>(input, headers);
      ResponseEntity<PredictionOutput> resp = restTemplate.postForEntity(url, entity, PredictionOutput.class);
      return resp.getBody();
    } catch (RestClientException ex) {
      throw new RuntimeException("Error consultando servicio DS: " + ex.getMessage());
    }
  }
}
