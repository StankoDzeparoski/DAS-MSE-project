package mk.ukim.finki.wp.homework2das.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "issuers", uniqueConstraints = {
        @UniqueConstraint(columnNames = {"ticker_code", "company_name"})
})



public class Ticker {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(name = "ticker_code", nullable = false)
    private String tickerCode;
    @Column(name="company_name", nullable = false)
    private String companyName;

    public Ticker() {}

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

    public String getCompanyName() {
        return companyName;
    }

    public void setCompanyName(String companyName) {
        this.companyName = companyName;
    }
}

