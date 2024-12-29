package mk.ukim.finki.wp.homework2das.service.impl;

import mk.ukim.finki.wp.homework2das.model.Issuer;
import mk.ukim.finki.wp.homework2das.repository.IssuerRepository;
import mk.ukim.finki.wp.homework2das.service.IssuerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import java.util.*;
import org.ta4j.core.*;
import org.ta4j.core.indicators.*;
import org.ta4j.core.indicators.helpers.ClosePriceIndicator;
import org.ta4j.core.indicators.helpers.HighPriceIndicator;
import org.ta4j.core.indicators.helpers.LowPriceIndicator;
import org.ta4j.core.BarSeries;
import org.ta4j.core.BaseBarSeries;

import java.time.Duration;
import java.time.ZoneId;
import java.math.BigDecimal;
import java.time.ZonedDateTime;
import java.util.stream.Collectors;

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

    @Override
    public Map<String, Map<String, Double>> calculateIndicators(List<Issuer> issuers) {
        // Convert Issuers to a BarSeries
        BarSeries series = createBarSeries(issuers);

        // Define indicators
        ClosePriceIndicator closePrice = new ClosePriceIndicator(series);
        HighPriceIndicator highPrice = new HighPriceIndicator(series);
        LowPriceIndicator lowPrice = new LowPriceIndicator(series);

        RSIIndicator rsi = new RSIIndicator(closePrice, 14);
        StochasticOscillatorKIndicator stochastic = new StochasticOscillatorKIndicator(series, 14);
        MACDIndicator macd = new MACDIndicator(closePrice, 12, 26);
        CCIIndicator cci = new CCIIndicator(series, 14);
        SMAIndicator sma = new SMAIndicator(closePrice, 14);
        EMAIndicator ema = new EMAIndicator(closePrice, 14);
        WMAIndicator wma = new WMAIndicator(closePrice, 14);
        ATRIndicator atr = new ATRIndicator(series, 14);
        TripleEMAIndicator tema = new TripleEMAIndicator(closePrice, 14); // Triple Exponential Moving Average
        KAMAIndicator kama = new KAMAIndicator(closePrice, 2, 30, 60); // Correct constructor usage

        // Prepare maps for results
        Map<String, Double> indicators1d = new HashMap<>();
        Map<String, Double> indicators7d = new HashMap<>();
        Map<String, Double> indicators30d = new HashMap<>();

        // Get indicator values for 1 day (most recent bar)
        int lastIndex = series.getEndIndex();
        indicators1d.put("RSI", rsi.getValue(lastIndex).doubleValue());
        indicators1d.put("Stochastic", stochastic.getValue(lastIndex).doubleValue());
        indicators1d.put("MACD", macd.getValue(lastIndex).doubleValue());
        indicators1d.put("CCI", cci.getValue(lastIndex).doubleValue());
        indicators1d.put("SMA", sma.getValue(lastIndex).doubleValue());
        indicators1d.put("EMA", ema.getValue(lastIndex).doubleValue());
        indicators1d.put("WMA", wma.getValue(lastIndex).doubleValue());
        indicators1d.put("ATR", atr.getValue(lastIndex).doubleValue());
        indicators1d.put("TEMA", tema.getValue(lastIndex).doubleValue());
        indicators1d.put("KAMA", kama.getValue(lastIndex).doubleValue());

        // Calculate averages for last 7 days and last 30 days
        calculateAverages(series, rsi, stochastic, macd, cci, sma, ema, wma, atr, tema, kama, lastIndex, 7, indicators7d);
        calculateAverages(series, rsi, stochastic, macd, cci, sma, ema, wma, atr, tema, kama, lastIndex, 30, indicators30d);

        // Combine results into a single map
        Map<String, Map<String, Double>> combinedResults = new HashMap<>();
        combinedResults.put("1d", indicators1d);
        combinedResults.put("7d", indicators7d);
        combinedResults.put("30d", indicators30d);

        return combinedResults;
    }

    private void calculateAverages(
            BarSeries series,
            RSIIndicator rsi,
            StochasticOscillatorKIndicator stochastic,
            MACDIndicator macd,
            CCIIndicator cci,
            SMAIndicator sma,
            EMAIndicator ema,
            WMAIndicator wma,
            ATRIndicator atr,
            TripleEMAIndicator tema,
            KAMAIndicator kama,
            int lastIndex,
            int period,
            Map<String, Double> resultMap
    ) {
        int startIndex = Math.max(0, lastIndex - period + 1);
        int count = lastIndex - startIndex + 1;

        double rsiSum = 0, stochasticSum = 0, macdSum = 0, cciSum = 0, smaSum = 0, emaSum = 0, wmaSum = 0, atrSum = 0;
        double temaSum = 0, kamaSum = 0;

        for (int i = startIndex; i <= lastIndex; i++) {
            rsiSum += rsi.getValue(i).doubleValue();
            stochasticSum += stochastic.getValue(i).doubleValue();
            macdSum += macd.getValue(i).doubleValue();
            cciSum += cci.getValue(i).doubleValue();
            smaSum += sma.getValue(i).doubleValue();
            emaSum += ema.getValue(i).doubleValue();
            wmaSum += wma.getValue(i).doubleValue();
            atrSum += atr.getValue(i).doubleValue();
            temaSum += tema.getValue(i).doubleValue();
            kamaSum += kama.getValue(i).doubleValue();
        }

        resultMap.put("RSI", rsiSum / count);
        resultMap.put("Stochastic", stochasticSum / count);
        resultMap.put("MACD", macdSum / count);
        resultMap.put("CCI", cciSum / count);
        resultMap.put("SMA", smaSum / count);
        resultMap.put("EMA", emaSum / count);
        resultMap.put("WMA", wmaSum / count);
        resultMap.put("ATR", atrSum / count);
        resultMap.put("TEMA", temaSum / count);
        resultMap.put("KAMA", kamaSum / count);
    }

    private BarSeries createBarSeries(List<Issuer> issuers) {
        BarSeries series = new BaseBarSeries("Issuer Time Series");

        issuers.sort(Comparator.comparing(Issuer::getDate));

        Set<LocalDate> uniqueSet = new HashSet<>();
        List<Issuer> uniqueIssuers = issuers.stream()
                .filter(event -> uniqueSet.add(event.getDate()))  // add returns false if the date is already in the set
                .collect(Collectors.toList());

        uniqueIssuers = uniqueIssuers.stream().filter(i -> uniqueSet.contains(i.getDate())).collect(Collectors.toList());

        for (Issuer issuer : uniqueIssuers) {
            // Create a Bar with the proper parameters (BigDecimal for price and volume)
            Bar bar = new BaseBar(
                    Duration.ofDays(1), // Bar duration (1 day)
                    ZonedDateTime.of(issuer.getDate().atStartOfDay(), ZoneId.systemDefault()), // Bar date (ZonedDateTime)
                    BigDecimal.valueOf(issuer.getMinPrice()), // Open price
                    BigDecimal.valueOf(issuer.getMaxPrice()), // High price
                    BigDecimal.valueOf(issuer.getMinPrice()), // Min price
                    BigDecimal.valueOf(issuer.getLastPrice()), // Close price
                    BigDecimal.valueOf(issuer.getVolume()) // Volume
            );
            series.addBar(bar); // Add the bar to the series
        }

        return series;
    }

}

