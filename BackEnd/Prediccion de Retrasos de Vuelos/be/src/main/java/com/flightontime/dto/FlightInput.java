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

    @Override
    public String toString() {
        return String.format(
                "FlightInput{aerolinea='%s', origen='%s', destino='%s', fecha_partida=%s, distancia_km=%d}",
                aerolinea, origen, destino, fecha_partida, distancia_km);
    }

    public FlightInput() {
    }

}
