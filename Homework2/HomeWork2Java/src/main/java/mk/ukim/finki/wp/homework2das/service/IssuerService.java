package mk.ukim.finki.wp.homework2das.service;

import mk.ukim.finki.wp.homework2das.model.Issuer;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

public interface IssuerService {
    // Method to get all issuers
    List<Issuer> getAllIssuers();
    // Method to find an issuer by ticker code and date
    Optional<Issuer> getIssuerByTickerCodeAndDate(String tickerCode, LocalDate date);
    // Method to get issuers by ticker code
    List<Issuer> getIssuersByTickerCode(String tickerCode);

}

