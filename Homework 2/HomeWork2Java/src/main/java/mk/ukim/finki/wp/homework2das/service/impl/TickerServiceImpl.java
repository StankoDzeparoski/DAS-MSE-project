package mk.ukim.finki.wp.homework2das.service.impl;

import jakarta.transaction.Transactional;
import mk.ukim.finki.wp.homework2das.model.Ticker;
import mk.ukim.finki.wp.homework2das.repository.TickerRepository;
import mk.ukim.finki.wp.homework2das.service.TickerService;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class TickerServiceImpl implements TickerService {

    private final TickerRepository tickerRepository;

    public TickerServiceImpl(TickerRepository tickerRepository) {
        this.tickerRepository = tickerRepository;
    }

    // Fetch all tickers
    public List<Ticker> findAll() {
        return tickerRepository.findAll();
    }
    // Custom logic (e.g., find by symbol)
    public Optional<Ticker> findBySymbol(String symbol) {
        return tickerRepository.findAll().stream()
                .filter(ticker -> symbol.equalsIgnoreCase(ticker.getTickerCode()))
                .findFirst();
    }
    public Optional <Ticker> findByCompanyName(String company_name){
        return tickerRepository.findAll().stream().
                filter(ticker -> company_name.equalsIgnoreCase(ticker.getCompanyName())).
                findFirst();
    }
}

