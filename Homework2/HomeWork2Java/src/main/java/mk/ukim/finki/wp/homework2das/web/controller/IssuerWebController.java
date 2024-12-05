package mk.ukim.finki.wp.homework2das.web.controller;

import mk.ukim.finki.wp.homework2das.model.Issuer;
import mk.ukim.finki.wp.homework2das.model.Ticker;
import mk.ukim.finki.wp.homework2das.service.IssuerService;
import mk.ukim.finki.wp.homework2das.service.TickerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

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
        List<Ticker> tickers = tickerService.findAll();
        model.addAttribute("tickers", tickers);
        List<Issuer> TickerData = issuerService.getAllIssuers();
        Issuer latestIssuer = TickerData.stream()
                .max(Comparator.comparing(Issuer::getDate))
                .orElse(null);
//        System.out.println(latestIssuer);
        TickerData = TickerData.stream()
                .filter(i -> i.getDate().isEqual(latestIssuer.getDate()))
                .collect(Collectors.toList());
        TickerData.sort(Comparator.comparing(Issuer::getVolumeInMoney).reversed());
        Set<String> distinct = new HashSet<>();
        TickerData = TickerData.stream().filter(i -> distinct.add(i.getTickerCode())).limit(10).collect(Collectors.toList());
//        System.out.println(TickerData);
        model.addAttribute("TickerData", TickerData);
        return "home"; // Name of the Thymeleaf template (issuers.html)
    }

    // Mapping to show all issuers in a Thymeleaf template
    @GetMapping("/issuers")
    public String showAllIssuersPage(@RequestParam(required = false) String error, Model model) {
        if (error != null && !error.isEmpty()) {
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

        List<Ticker> tickers = tickerService.findAll();
        model.addAttribute("tickers", tickers);

        if (tickerCode.equals("NONE")) {

            return "issuer_by_ticker";
        }
        if (!this.issuerService.getIssuersByTickerCode(tickerCode).isEmpty()) {
            List<Issuer> TickerData = issuerService.getIssuersByTickerCode(tickerCode);
            TickerData.sort(Comparator.comparing(Issuer::getDate).reversed());
            model.addAttribute("TickerData", TickerData);
            return "issuer_by_ticker";
        }

        return "redirect:/issuers?error=tickerCodeNotFound";

    }

    // Mapping to show a single issuer by tickerCode including date
    @PostMapping("/issuers/{tickerCode}")
    public String showIssuerDetailsPageDateTicker(@PathVariable String tickerCode,
                                                  @RequestParam(required = false) String dateFrom,
                                                  @RequestParam(required = false) String dateTo,
                                                  Model model) {

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("M/d/yyyy");

        List<Ticker> tickers = tickerService.findAll();
        model.addAttribute("tickers", tickers);

        if (!this.issuerService.getIssuersByTickerCode(tickerCode).isEmpty()) {
            List<Issuer> TickerData = issuerService.getIssuersByTickerCode(tickerCode);
            TickerData.sort(Comparator.comparing(Issuer::getDate).reversed());
            TickerData = TickerData.stream().
                    filter(ticker -> ticker.getDate().isAfter(LocalDate.parse(dateFrom, formatter))
                            && ticker.getDate().isBefore(LocalDate.parse(dateTo, formatter))).collect(Collectors.toList());
            model.addAttribute("TickerData", TickerData);
            if (TickerData.isEmpty()) {
                return "redirect:/issuers?error=NoDataFrom" + dateFrom + "TILL" + dateTo;
            }
            return "issuer_by_ticker";
        }

        return "redirect:/issuers?error=tickerCodeNotFound";

    }

    @GetMapping("/report")
    public String getReport(@RequestParam(value = "period", defaultValue = "day") String period, Model model) {
        LocalDate today = LocalDate.now();
        LocalDate startOfWeek = today.minusDays(today.getDayOfWeek().getValue() - 1);
        LocalDate startOfMonth = today.withDayOfMonth(1);

        List<Issuer> issuers = issuerService.getAllIssuers();


        switch (period.toLowerCase()) {
            case "week":
                issuers = issuers.stream()
                        .filter(issuer -> !issuer.getDate().isBefore(startOfWeek) && !issuer.getDate().isAfter(today))
                        .collect(Collectors.toList());
                model.addAttribute("period", "Weekly Report");
                break;

            case "month":
                issuers = issuers.stream()
                        .filter(issuer -> !issuer.getDate().isBefore(startOfMonth) && !issuer.getDate().isAfter(today))
                        .collect(Collectors.toList());
                model.addAttribute("period", "Monthly Report");
                break;

            default: // "day"
                issuers = issuers.stream()
                        .filter(issuer -> issuer.getDate().isEqual(today))
                        .collect(Collectors.toList());
                model.addAttribute("period", "Daily Report");
                break;
        }

        model.addAttribute("issuers", issuers);
        return "report";
    }

}