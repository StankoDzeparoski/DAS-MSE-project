package mk.ukim.finki.wp.homework2das.web.controller;

import mk.ukim.finki.wp.homework2das.model.Issuer;
import mk.ukim.finki.wp.homework2das.model.Ticker;
import mk.ukim.finki.wp.homework2das.service.IssuerService;
import mk.ukim.finki.wp.homework2das.service.TickerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
//@RequestMapping("/issuers")
public class IssuerWebController {

    private final IssuerService issuerService;
    private final TickerService tickerService;

    @Autowired
    public IssuerWebController(IssuerService issuerService, TickerService tickerService) {
        this.issuerService = issuerService;
        this.tickerService = tickerService;
    }

    // Mapping to home page
    @GetMapping("/")
    public String showHomePage(Model model) {
//        List<Ticker> tickers = tickerService.findAll();
//        model.addAttribute("tickers", tickers);
        return "home"; // Name of the Thymeleaf template (issuers.html)
    }

    // Mapping to show all issuers in a Thymeleaf template
    @GetMapping("/issuers")
    public String showAllIssuersPage(Model model) {
        List<Ticker> tickers = tickerService.findAll();
        model.addAttribute("tickers", tickers);
        return "issuers_list"; // Name of the Thymeleaf template (issuers.html)
    }

    // Mapping to show a single issuer by tickerCode and date
    @GetMapping("/issuers/{tickerCode}/{date}")
    public String showIssuerDetailsPage(@PathVariable String tickerCode, @PathVariable String date, Model model) {
        List<Issuer> issuers = issuerService.getIssuersByTickerCode(tickerCode);
        model.addAttribute("issuers", issuers);
        return "issuer-details"; // Another Thymeleaf template for details
    }

}
