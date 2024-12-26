package mk.ukim.finki.wp.homework2das.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "issuers", uniqueConstraints = {
        @UniqueConstraint(columnNames = {"ticker_code"})
})
public class Ticker {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(name = "ticker_code", nullable = false)
    private String tickerCode;

    public Ticker() {}

}

