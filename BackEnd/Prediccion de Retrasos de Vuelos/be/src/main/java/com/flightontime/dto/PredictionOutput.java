package com.flightontime.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class PredictionOutput {
    @JsonProperty("prevision")
    public String prevision;

    @JsonProperty("probabilidad")
    public Double probabilidad;

    // Constructor
    public PredictionOutput() {
    }

    // Constructor
    public PredictionOutput(String prevision, Double probabilidad) {
        this.prevision = prevision;
        this.probabilidad = probabilidad;
    }

    // GETTERS Y SETTERS
    public String getPrevision() {
        return prevision;
    }

    public Double getProbabilidad() {
        return probabilidad;
    }

    public void setPrevision(String prevision) {
        this.prevision = prevision;
    }

    public void setProbabilidad(Double probabilidad) {
        this.probabilidad = probabilidad;
    }
}
