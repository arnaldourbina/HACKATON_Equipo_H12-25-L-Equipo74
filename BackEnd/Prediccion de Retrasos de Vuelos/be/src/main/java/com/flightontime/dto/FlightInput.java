package com.flightontime.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class FlightInput {
    @NotBlank(message = "Aerolinea requerida")
    @JsonProperty("aerolinea")
    public String aerolinea;

    @NotBlank(message = "Origen requerido")
    @JsonProperty("origen")
    public String origen;

    @NotBlank(message = "Destino requerido")
    @JsonProperty("destino")
    public String destino;

    @NotNull(message = "Fecha partida requerida")
    @JsonProperty("fecha_partida")
    public String fecha_partida;

    @NotNull(message = "Distancia requerida")
    @JsonProperty("distancia_km")
    public Integer distancia_km;

    public FlightInput(String aerolinea, String origen, String destino,
            String fecha_partida, Integer distancia_km) {
        this.aerolinea = aerolinea;
        this.origen = origen;
        this.destino = destino;
        this.fecha_partida = fecha_partida;
        this.distancia_km = distancia_km;
    }

    public FlightInput() {
    }

    // GETTERS Y SETTERS
    public String getAerolinea() {
        return aerolinea;
    }

    public void setAerolinea(String aerolinea) {
        this.aerolinea = aerolinea;
    }

    public String getOrigen() {
        return origen;
    }

    public void setOrigen(String origen) {
        this.origen = origen;
    }

    public String getDestino() {
        return destino;
    }

    public void setDestino(String destino) {
        this.destino = destino;
    }

    public String getFechaPartida() {
        return fecha_partida;
    }

    public void setFecha_partida(String fecha_partida) {
        this.fecha_partida = fecha_partida;
    }

    public Integer getDistanciaKm() {
        return distancia_km;
    }

    public void setDistancia_km(Integer distancia_km) {
        this.distancia_km = distancia_km;
    }

    @Override
    public String toString() {
        return String.format(
                "FlightInput{aerolinea='%s', origen='%s', destino='%s', fecha_partida=%s, distancia_km=%d}",
                aerolinea, origen, destino, fecha_partida, distancia_km);
    }
}
