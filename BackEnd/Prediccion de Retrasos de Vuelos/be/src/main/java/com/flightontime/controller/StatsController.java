package com.flightontime.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/stats")
public class StatsController {
  private final RestTemplate restTemplate = new RestTemplate();
  @Value("${ds.baseUrl}") private String baseUrl;

  @GetMapping
  public ResponseEntity<Map> stats() {
    Map resp = restTemplate.getForObject(baseUrl + "/stats", Map.class);
    return ResponseEntity.ok(resp);
  }
}
