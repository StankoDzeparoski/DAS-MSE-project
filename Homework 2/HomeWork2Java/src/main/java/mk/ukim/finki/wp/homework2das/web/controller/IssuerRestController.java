//package mk.ukim.finki.wp.homework2das.web.controller;
//
//import mk.ukim.finki.wp.homework2das.model.Issuer;
//import mk.ukim.finki.wp.homework2das.service.IssuerService;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.web.bind.annotation.*;
//
//import java.time.LocalDate;
//import java.util.List;
//import java.util.Optional;
//
//@RestController
//@RequestMapping("/api/issuers")
//public class IssuerRestController {
//
//    private final IssuerService issuerService;
//
//    @Autowired
//    public IssuerRestController(IssuerService issuerService) {
//        this.issuerService = issuerService;
//    }
//
//    // Endpoint to get all issuers
//    @GetMapping
//    public List<Issuer> getAllIssuers() {
//        return issuerService.getAllIssuers();
//    }
//
//    // Endpoint to get issuer by tickerCode and date
//    @GetMapping("/{tickerCode}/{date}")
//    public Optional<Issuer> getIssuerByTickerCodeAndDate(@PathVariable String tickerCode, @PathVariable String date) {
//        return issuerService.getIssuerByTickerCodeAndDate(tickerCode, LocalDate.parse(date));
//    }
//
//    // Endpoint to save an issuer
//    @PostMapping
//    public Issuer saveIssuer(@RequestBody Issuer issuer) {
//        return issuerService.saveIssuer(issuer);
//    }
//
//    // Endpoint to delete an issuer by ID
//    @DeleteMapping("/{id}")
//    public void deleteIssuer(@PathVariable Long id) {
//        issuerService.deleteIssuer(id);
//    }
//}
