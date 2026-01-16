package com.flightontime.controller;

import com.flightontime.dto.FlightInput;
import com.flightontime.dto.PredictionOutput;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class WebController {

    @GetMapping("/form")
    public String showForm(Model model) {
        model.addAttribute("flightInput", new FlightInput());
        return "form"; // busca form.html en templates
    }

    @PostMapping("/form")
    public String processForm(@ModelAttribute FlightInput input, Model model) {
        PredictionOutput output = new PredictionOutput();
        output.setAerolinea(input.getAerolinea());
        output.setNumeroVuelo(input.getNumeroVuelo());
        output.setOrigen(input.getOrigen());
        output.setDestino(input.getDestino());
        output.setFecha_partida(input.getFecha_partida());
        output.setDistancia_km(input.getDistancia_km());
        output.setDelayMinutes(30);
        output.setStatus("Predicted delay");

        model.addAttribute("prediction", output);
        return "result"; // busca result.html en templates
    }
}
