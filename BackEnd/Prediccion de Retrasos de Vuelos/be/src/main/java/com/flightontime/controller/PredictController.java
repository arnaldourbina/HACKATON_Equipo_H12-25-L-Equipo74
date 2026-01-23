package com.flightontime.controller;

import com.flightontime.dto.FlightInput;
import com.flightontime.dto.PredictionOutput;
import com.flightontime.dto.StatsDto;
import com.flightontime.entity.H2Prediction;
import com.flightontime.service.DsClientService;
import com.flightontime.service.H2PredictionService;
import com.flightontime.service.H2StatsService;
import com.flightontime.util.CSVAnalisisVuelos;
import com.flightontime.repository.H2PredictionRepository;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.MediaType;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.util.ArrayList;
import com.opencsv.exceptions.CsvException;

@RestController
@RequestMapping("/api")
public class PredictController {
    @Autowired
    private DsClientService dsClientService;

    @Autowired
    private H2PredictionService H2PredictionService;

    @Autowired
    private H2StatsService H2statsService;

    @Autowired
    private H2PredictionRepository H2PredictionRepository;

    @Autowired
    private CSVAnalisisVuelos csvParser;

    @PostMapping("/predict")
    public ResponseEntity<PredictionOutput> predict(@Valid @RequestBody FlightInput input) {
        PredictionOutput result = dsClientService.predict(input);
        H2PredictionService.savePrediction(input, result);
        return ResponseEntity.ok(result);
    }

    @PostMapping(value = "/predict/batch", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<byte[]> predictBatch(@RequestParam("file") MultipartFile csvFile)
            throws IOException, CsvException {
        List<FlightInput> vuelos = csvParser.parseCSV(csvFile);

        List<PredictionOutput> resultados = new ArrayList<>();
        for (FlightInput vuelo : vuelos) {
            resultados.add(dsClientService.predict(vuelo));
        }

        StringBuilder csv = new StringBuilder("aerolinea,origen,destino,prevision,probabilidad\n");
        for (int i = 0; i < resultados.size(); i++) {
            csv.append(String.format("%s,%s,%s,%s,%.2f\n",
                    vuelos.get(i).getAerolinea(),
                    vuelos.get(i).getOrigen(),
                    vuelos.get(i).getDestino(),
                    resultados.get(i).getPrevision(),
                    resultados.get(i).getProbabilidad()));
        }

        return ResponseEntity.ok()
                .header("Content-Disposition", "attachment; filename=predicciones_batch.csv")
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(csv.toString().getBytes());
    }

    @GetMapping("/stats")
    public ResponseEntity<StatsDto> stats() {
        return ResponseEntity.ok(H2statsService.stadisticasHoy());
    }

    @GetMapping("/history")
    public ResponseEntity<List<H2Prediction>> history() {
        List<H2Prediction> recientes = H2PredictionRepository.buscaTopPrediccionesPorTimestampDesc();
        return ResponseEntity.ok(recientes);
    }
}
