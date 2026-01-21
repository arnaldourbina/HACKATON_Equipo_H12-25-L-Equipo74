package com.flightontime.repository;

import com.flightontime.entity.H2Prediction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface H2PredictionRepository extends JpaRepository<H2Prediction, Long> {
    // Últimas predicciones
    @Query("SELECT p FROM H2Prediction p ORDER BY p.timestamp DESC")
    List<H2Prediction> buscaTopPrediccionesPorTimestampDesc();

    // Conteo de predicciones por rango de tiempo
    @Query("SELECT COUNT(p) FROM H2Prediction p " +
            "WHERE p.timestamp >= :start AND p.timestamp < :end")
    long cuentaPorTimestamp(@Param("start") LocalDateTime start, @Param("end") LocalDateTime end);

    // Conteo de predicciones por prevision
    @Query("SELECT COUNT(p) FROM H2Prediction p " +
            "WHERE p.timestamp >= :start AND p.timestamp < :end " +
            "AND p.prevision = :prevision")
    long cuentaPorTiemstampPrevision(@Param("start") LocalDateTime start,
            @Param("end") LocalDateTime end,
            @Param("prevision") String prevision);

    // Aerolínea con más retrasos
    @Query("SELECT p.aerolinea FROM H2Prediction p " +
            "WHERE p.timestamp >= :start AND p.timestamp < :end " +
            "AND p.prevision = 'Retrasado' " +
            "GROUP BY p.aerolinea " +
            "ORDER BY COUNT(p) DESC LIMIT 1")
    String buscaTopAerolineaRetrasos(@Param("start") LocalDateTime start,
            @Param("end") LocalDateTime end);
}