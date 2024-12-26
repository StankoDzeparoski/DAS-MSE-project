package mk.ukim.finki.wp.homework2das.service.impl;

import mk.ukim.finki.wp.homework2das.model.Issuer;
import mk.ukim.finki.wp.homework2das.repository.IssuerRepository;
import mk.ukim.finki.wp.homework2das.service.IssuerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class IssuerServiceImpl implements IssuerService {

    private final IssuerRepository issuerRepository;

    @Autowired
    public IssuerServiceImpl(IssuerRepository issuerRepository) {
        this.issuerRepository = issuerRepository;
    }

    // Method to get all issuers
    public List<Issuer> getAllIssuers() {
        return issuerRepository.findAll();
    }

    // Method to find an issuer by ticker code and date
    public Optional<Issuer> getIssuerByTickerCodeAndDate(String tickerCode, LocalDate date) {
        return issuerRepository.findByTickerCodeAndDate(tickerCode, date);
    }

    // Method to get issuers by ticker code
    public List<Issuer> getIssuersByTickerCode(String tickerCode) {
        return issuerRepository.findByTickerCode(tickerCode);
    }

}

