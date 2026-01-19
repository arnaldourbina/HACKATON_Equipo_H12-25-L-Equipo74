package com.flightontime.controller;

import com.flightontime.dto.FlightInput;
import com.flightontime.dto.PredictionOutput;
import com.flightontime.service.DsClientService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class PredictController {
    @Autowired
    private DsClientService dsClient;

    @PostMapping("/predict")
    public ResponseEntity<PredictionOutput> predict(@Valid @RequestBody FlightInput input) {
        PredictionOutput result = dsClient.predict(input);
        return ResponseEntity.ok(result);
    }
}
