package com.flightontime.service;

import com.flightontime.dto.StatsDto;
import com.flightontime.repository.H2PredictionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Service
public class H2StatsService {
    @Autowired
    private H2PredictionRepository repo;

    public StatsDto stadisticasHoy() {
        LocalDate hoy = LocalDate.now();
        LocalDateTime inicio = hoy.atStartOfDay();
        LocalDateTime fin = hoy.plusDays(1).atStartOfDay();

        long conteoHoy = repo.cuentaPorTimestamp(inicio, fin);
        long conteoRetraso = repo.cuentaPorTiemstampPrevision(inicio, fin, "Retrasado");
        String topAerolineas = repo.buscaTopAerolineaRetrasos(inicio, fin);

        double porc = conteoHoy > 0 ? (double) conteoRetraso / conteoHoy * 100.0 : 0.0;

        return new StatsDto(hoy, (int) conteoHoy, (int) conteoRetraso, porc, topAerolineas);
    }
}
