package com.flightontime.dto;

import jakarta.validation.constraints.*;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDateTime;

public class FlightInput {
    @NotBlank 
    private String aerolinea;

    @NotBlank 
    private String numeroVuelo;

    @NotBlank 
    @Size(min=3, max=4) 
    private String origen;

    @NotBlank 
    @Size(min=3, max=4) 
    private String destino;

    @NotBlank
    @JsonProperty("fecha_partida") // mantiene compatibilidad con el JSON
    private LocalDateTime fechaPartida;

    @Positive
    @JsonProperty("distancia_km") // mantiene compatibilidad con el JSON
    private double distanciaKm;

    // Getters y setters
    public String getAerolinea() { return aerolinea; }
    public void setAerolinea(String aerolinea) { this.aerolinea = aerolinea; }

    public String getNumeroVuelo() { return numeroVuelo; }
    public void setNumeroVuelo(String numeroVuelo) { this.numeroVuelo = numeroVuelo; }

    public String getOrigen() { return origen; }
    public void setOrigen(String origen) { this.origen = origen; }

    public String getDestino() { return destino; }
    public void setDestino(String destino) { this.destino = destino; }

    public LocalDateTime getFechaPartida() { return fechaPartida; }
    public void setFechaPartida(LocalDateTime fechaPartida) { this.fechaPartida = fechaPartida; }

    public double getDistanciaKm() { return distanciaKm; }
    public void setDistanciaKm(double distanciaKm) { this.distanciaKm = distanciaKm; }
}