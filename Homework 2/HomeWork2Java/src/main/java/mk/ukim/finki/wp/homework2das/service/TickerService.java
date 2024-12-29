package mk.ukim.finki.wp.homework2das.service;

import mk.ukim.finki.wp.homework2das.model.Ticker;

import java.util.List;
import java.util.Optional;

public interface TickerService {
    // Fetch all tickers
    List<Ticker> findAll();
    // Custom logic (e.g., find by symbol)
    public Optional<Ticker> findBySymbol(String symbol);
    public Optional<Ticker> findByCompanyName(String companyName);
}
