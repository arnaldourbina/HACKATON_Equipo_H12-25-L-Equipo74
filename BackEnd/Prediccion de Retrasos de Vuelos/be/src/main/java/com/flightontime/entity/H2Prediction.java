package com.flightontime.entity; // Tu paquete

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "FOT_HISTORICO_PREDICCIONES")
public class H2Prediction {

    @Id
    @GeneratedValue()
    @Column(name = "ID")
    private Long id;

    @Column(name = "FECHA&HORA_REGISTRO")
    private LocalDateTime timestamp;

    @Column(name = "AEROLINEA")
    private String aerolinea;

    @Column(name = "ORIGEN")
    private String origen;

    @Column(name = "DESTINO")
    private String destino;

    @Column(name = "FECHA_PARTIDA")
    private LocalDateTime fechaPartida;

    @Column(name = "DISTANCIA_KM")
    private Integer distanciaKm;

    @Column(name = "PREVISION")
    private String prevision;

    @Column(name = "PROBABILIDAD")
    private Double probabilidad;

    // Constructor
    public H2Prediction() {
    }

    // Constructor completo
    public H2Prediction(String aerolinea, String origen, String destino,
            LocalDateTime fechaPartida, Integer distanciaKm,
            String prevision, Double probabilidad) {
        this.timestamp = LocalDateTime.now();
        this.aerolinea = aerolinea;
        this.origen = origen;
        this.destino = destino;
        this.fechaPartida = fechaPartida;
        this.distanciaKm = distanciaKm;
        this.prevision = prevision;
        this.probabilidad = probabilidad;
    }

    // GETTERS & SETTERS
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }

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

    public LocalDateTime getFechaPartida() {
        return fechaPartida;
    }

    public void setFechaPartida(LocalDateTime fechaPartida) {
        this.fechaPartida = fechaPartida;
    }

    public Integer getDistanciaKm() {
        return distanciaKm;
    }

    public void setDistanciaKm(Integer distanciaKm) {
        this.distanciaKm = distanciaKm;
    }

    public String getPrevision() {
        return prevision;
    }

    public void setPrevision(String prevision) {
        this.prevision = prevision;
    }

    public Double getProbabilidad() {
        return probabilidad;
    }

    public void setProbabilidad(Double probabilidad) {
        this.probabilidad = probabilidad;
    }
}
