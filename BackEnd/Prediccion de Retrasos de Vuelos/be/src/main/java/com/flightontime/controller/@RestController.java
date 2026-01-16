@RestController
public class RootController {
    @GetMapping("/")
    public String home() {
        return "API FlightOnTime activa";
    }
}