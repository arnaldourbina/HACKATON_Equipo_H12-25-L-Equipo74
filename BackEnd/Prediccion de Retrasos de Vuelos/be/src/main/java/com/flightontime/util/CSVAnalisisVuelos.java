package com.flightontime.util;

import com.flightontime.dto.FlightInput;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import com.opencsv.exceptions.CsvException;
import org.springframework.stereotype.Component;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class CSVAnalisisVuelos {

    public List<FlightInput> parseCSV(org.springframework.web.multipart.MultipartFile csvFile)
            throws IOException, CsvException {
        try (Reader reader = new InputStreamReader(csvFile.getInputStream());
                CSVReader csvReader = new CSVReaderBuilder(reader).withSkipLines(1).build()) { // Skip header

            List<String[]> rows = csvReader.readAll();
            return rows.stream()
                    .map(row -> new FlightInput(
                            row[0], // aerolinea
                            row[1], // origen
                            row[2], // destino
                            row[3], // fecha_partida
                            Integer.parseInt(row[4]) // distancia_km
                    ))
                    .collect(Collectors.toList());
        }
    }

}