package com.flightontime.dto;

import java.util.Map;

public class FlightEmail {
    private String to_email;
    private Map<String, Object> vuelo_data;
    private Double probabilidad;
    // GETTERS Y SETTERS

    public String getTo_email() {
        return to_email;
    }

    public void setTo_email(String to_email) {
        this.to_email = to_email;
    }

    public Map<String, Object> getVuelo_data() {
        return vuelo_data;
    }

    public void setVuelo_data(Map<String, Object> vuelo_data) {
        this.vuelo_data = vuelo_data;
    }

    public Double getProbabilidad() {
        return probabilidad;
    }

    public void setProbabilidad(Double probabilidad) {
        this.probabilidad = probabilidad;
    }
}