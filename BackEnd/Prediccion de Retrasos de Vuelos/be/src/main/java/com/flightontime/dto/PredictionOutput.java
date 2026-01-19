package com.flightontime.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class PredictionOutput {
    @JsonProperty("prevision")
    public String prevision;

    @JsonProperty("probabilidad")
    public Double probabilidad;

    // Constructor vacío OBLIGATORIO
    public PredictionOutput() {
    }

    // Constructor completo
    public PredictionOutput(String prevision, Double probabilidad) {
        this.prevision = prevision;
        this.probabilidad = probabilidad;
    }
}
