package mk.ukim.finki.wp.homework2das.model;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDate;

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

    public Issuer() {}

}
