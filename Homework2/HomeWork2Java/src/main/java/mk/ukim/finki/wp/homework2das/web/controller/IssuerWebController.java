package mk.ukim.finki.wp.homework2das.web.controller;

import mk.ukim.finki.wp.homework2das.model.Issuer;
import mk.ukim.finki.wp.homework2das.model.Ticker;
import mk.ukim.finki.wp.homework2das.service.IssuerService;
import mk.ukim.finki.wp.homework2das.service.TickerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.Comparator;
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
    public String showAllIssuersPage(@RequestParam(required = false) String error,Model model) {
        if(error != null && !error.isEmpty()) {
            model.addAttribute("hasError", true);
            model.addAttribute("error", error);
        }
        List<Ticker> tickers = tickerService.findAll();
        model.addAttribute("tickers", tickers);
        return "issuers_list";
    }

    // Mapping to show a single issuer by tickerCode
    @GetMapping("/issuers/{tickerCode}")
    public String showIssuerDetailsPage(@PathVariable String tickerCode, Model model) {
        if(!this.issuerService.getIssuersByTickerCode(tickerCode).isEmpty()){
            List<Issuer> TickerData = issuerService.getIssuersByTickerCode(tickerCode);
            TickerData.sort(Comparator.comparing(Issuer::getDate).reversed());
            model.addAttribute("TickerData", TickerData);
            System.out.println(TickerData.get(0));
            return "issuer_by_ticker";
        }

        return "redirect:/issuers?error=tickerCodeNotFound";

    }

}
