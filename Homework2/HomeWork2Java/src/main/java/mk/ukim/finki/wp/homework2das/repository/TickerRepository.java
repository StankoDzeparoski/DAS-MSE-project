package mk.ukim.finki.wp.homework2das.repository;

import mk.ukim.finki.wp.homework2das.model.Ticker;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TickerRepository extends JpaRepository<Ticker, Long> {
}

