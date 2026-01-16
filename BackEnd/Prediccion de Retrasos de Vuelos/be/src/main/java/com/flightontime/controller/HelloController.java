package com.flightontime.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HelloController {

    @GetMapping("/")
    public String redirectToForm() {
        return "redirect:/form";
    }
}