package com.flightontime.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDate;

public class StatsDto {
    private LocalDate fecha;
    private int totalPredicciones;
    private int retrasados;
    @JsonProperty("porcentajeRetraso")
    private double porcentajeRetraso;
    private String aerolineaTop;

    // Constructor, getters/setters
    public StatsDto(LocalDate fecha, int total_predicciones, int retrasados,
            @JsonProperty("porcentajeRetraso") double porc_retrasos,
            String top_aerolinea) {
        this.fecha = fecha;
        this.totalPredicciones = total_predicciones;
        this.retrasados = retrasados;
        this.porcentajeRetraso = porc_retrasos;
        this.aerolineaTop = top_aerolinea;
    }
    // GETTERS Y SETTERS

    public LocalDate getFecha() {
        return fecha;
    }

    public void setFecha(LocalDate fecha) {
        this.fecha = fecha;
    }

    public int getTotalPredicciones() {
        return totalPredicciones;
    }

    public void setTotalPredicciones(int totalPredicciones) {
        this.totalPredicciones = totalPredicciones;
    }

    public int getRetrasados() {
        return retrasados;
    }

    public void setRetrasados(int retrasados) {
        this.retrasados = retrasados;
    }

    public double getPorcentajeRetraso() {
        return porcentajeRetraso;
    }

    public void setPorcentajeRetraso(double porcentajeRetraso) {
        this.porcentajeRetraso = porcentajeRetraso;
    }

    public String getAerolineaTop() {
        return aerolineaTop;
    }

    public void setAerolineaTop(String top_aerolinea) {
        this.aerolineaTop = top_aerolinea;
    }
}
