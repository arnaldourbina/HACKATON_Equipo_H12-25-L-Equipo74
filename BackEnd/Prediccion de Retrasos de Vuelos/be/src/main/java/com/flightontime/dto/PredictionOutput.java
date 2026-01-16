package com.flightontime.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class PredictionOutput {
    private String aerolinea;
    private String numeroVuelo;
    private String origen;
    private String destino;

    @JsonProperty("fecha_partida") // mantiene compatibilidad con el JSON
    private String fechaPartida;

    @JsonProperty("distancia_km") // mantiene compatibilidad con el JSON
    private double distanciaKm;

    private int delayMinutes;
    private String status;

    // Getters y setters
    public String getAerolinea() { return aerolinea; }
    public void setAerolinea(String aerolinea) { this.aerolinea = aerolinea; }

    public String getNumeroVuelo() { return numeroVuelo; }
    public void setNumeroVuelo(String numeroVuelo) { this.numeroVuelo = numeroVuelo; }

    public String getOrigen() { return origen; }
    public void setOrigen(String origen) { this.origen = origen; }

    public String getDestino() { return destino; }
    public void setDestino(String destino) { this.destino = destino; }

    public String getFechaPartida() { return fechaPartida; }
    public void setFechaPartida(String fechaPartida) { this.fechaPartida = fechaPartida; }

    public double getDistanciaKm() { return distanciaKm; }
    public void setDistanciaKm(double distanciaKm) { this.distanciaKm = distanciaKm; }

    public int getDelayMinutes() { return delayMinutes; }
    public void setDelayMinutes(int delayMinutes) { this.delayMinutes = delayMinutes; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}