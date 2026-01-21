package com.flightontime.controller;

import com.flightontime.dto.FlightInput;
import com.flightontime.dto.PredictionOutput;
import com.flightontime.dto.StatsDto;
import com.flightontime.entity.H2Prediction;
import com.flightontime.service.DsClientService;
import com.flightontime.service.H2PredictionService;
import com.flightontime.service.H2StatsService;
import com.flightontime.repository.H2PredictionRepository;

import jakarta.validation.Valid;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class PredictController {
    @Autowired
    private DsClientService dsClient;

    @Autowired
    private H2PredictionService h2Service;

    @Autowired
    private H2StatsService H2statsService;

    @Autowired
    private H2PredictionRepository repo;

    @PostMapping("/predict")
    public ResponseEntity<PredictionOutput> predict(@Valid @RequestBody FlightInput input) {
        PredictionOutput result = dsClient.predict(input);
        h2Service.savePrediction(input, result);
        return ResponseEntity.ok(result);
    }

    @GetMapping("/stats")
    public ResponseEntity<StatsDto> stats() {
        return ResponseEntity.ok(H2statsService.stadisticasHoy());
    }

    @GetMapping("/history")
    public ResponseEntity<List<H2Prediction>> history() {
        List<H2Prediction> recientes = repo.buscaTopPrediccionesPorTimestampDesc();
        return ResponseEntity.ok(recientes);
    }
}
