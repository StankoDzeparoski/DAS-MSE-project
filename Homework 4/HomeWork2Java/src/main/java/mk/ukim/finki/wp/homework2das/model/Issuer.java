package mk.ukim.finki.wp.homework2das.model;

import jakarta.persistence.*;
import lombok.Data;

import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.time.LocalDate;
import java.util.Locale;

@Data
@Entity
@Table(name = "mse_data", uniqueConstraints = {
        @UniqueConstraint(columnNames = {"ticker_code", "date"})
})

public class Issuer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(name = "ticker_code", nullable = false)
    private String tickerCode;
    @Column(name = "date", nullable = false)
    private LocalDate date;
    @Column(name = "last_price")
    private Float lastPrice;
    @Column(name = "max_price")
    private Float maxPrice;
    @Column(name = "min_price")
    private Float minPrice;
    @Column(name = "volume")
    private Float volume;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTickerCode() {
        return tickerCode;
    }

    public void setTickerCode(String tickerCode) {
        this.tickerCode = tickerCode;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public Float getLastPrice() {
        return lastPrice;
    }

    public void setLastPrice(Float lastPrice) {
        this.lastPrice = lastPrice;
    }

    public Float getMaxPrice() {
        return maxPrice;
    }

    public void setMaxPrice(Float maxPrice) {
        this.maxPrice = maxPrice;
    }

    public Float getMinPrice() {
        return minPrice;
    }

    public void setMinPrice(Float minPrice) {
        this.minPrice = minPrice;
    }

    public Float getVolume() {
        return volume;
    }

    public void setVolume(Float volume) {
        this.volume = volume;
    }

    public Issuer() {}

    public Float getVolumeInMoney(){
        return (this.volume * this.getAveragePrice());
    }

    public Double getChangeInPercent(){
        return (double) Math.round((((lastPrice - minPrice)/minPrice)*(float)100) * 100d) / 100d;
    }

    public Float getAveragePrice(){
        return (maxPrice + minPrice)/2;
    }

    public static String formatNumber(double number) {
        // Create a DecimalFormatSymbols object to change the grouping separator
        DecimalFormatSymbols symbols = new DecimalFormatSymbols(Locale.getDefault());
        symbols.setGroupingSeparator('.');  // Set the thousands separator to a period
        symbols.setDecimalSeparator(',');  // Set the decimal separator to a comma

        // Create a DecimalFormat with the custom symbols and two decimal places
        DecimalFormat decimalFormat = new DecimalFormat("#,###.00", symbols);

        // Format the number
        String formattedNumber = decimalFormat.format(number);

        // Handle edge case where the number is less than 1 and has no digits before the decimal
        if (formattedNumber.startsWith(",")) {
            formattedNumber = "0" + formattedNumber;
        }

        return formattedNumber;
    }

    public String getStringLastPrice() {
        return formatNumber(lastPrice);
    }
    public String getStringMaxPrice() {
        return formatNumber(maxPrice);
    }
    public String getStringMinPrice() {
        return formatNumber(minPrice);
    }
    public String getStringVolume() {
        return formatNumber(volume);
    }
    public String getStringVolumeInMoney() {
        return formatNumber(this.getVolumeInMoney());
    }
    public String getStringAveragePrice() {
        return formatNumber(this.getAveragePrice());
    }

}
