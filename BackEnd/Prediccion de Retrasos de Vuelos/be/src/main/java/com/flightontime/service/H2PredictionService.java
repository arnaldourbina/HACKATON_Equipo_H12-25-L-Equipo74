package com.flightontime.service;

import com.flightontime.dto.FlightInput;
import com.flightontime.dto.PredictionOutput;
import com.flightontime.entity.H2Prediction;
import com.flightontime.repository.H2PredictionRepository;

import java.time.LocalDateTime;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class H2PredictionService {

    @Autowired
    private H2PredictionRepository repository;

    // Guarda predicción en H2
    public void savePrediction(FlightInput input, PredictionOutput prediction) {
        LocalDateTime fechaParsed = LocalDateTime.parse(input.getFechaPartida());

        H2Prediction h2Pred = new H2Prediction(
                input.getAerolinea(),
                input.getOrigen(),
                input.getDestino(),
                fechaParsed,
                input.getDistanciaKm(),
                prediction.getPrevision(),
                prediction.getProbabilidad());
        repository.save(h2Pred);
    }
}
