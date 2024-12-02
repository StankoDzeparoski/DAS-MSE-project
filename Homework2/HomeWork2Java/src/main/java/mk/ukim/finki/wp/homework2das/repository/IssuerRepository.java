package mk.ukim.finki.wp.homework2das.repository;

import mk.ukim.finki.wp.homework2das.model.Issuer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

//The IssuerRepository extends JpaRepository<Issuer, Long>.
//This gives you access to common CRUD operations such as
//save(), findById(), findAll(), delete(), etc., without
//needing to implement them yourself.
@Repository
public interface IssuerRepository extends JpaRepository<Issuer, Long> {

    // Custom query methods (if needed)
    Optional<Issuer> findByTickerCodeAndDate(String tickerCode, LocalDate date);

    List<Issuer> findByTickerCode(String tickerCode);

//    @Query("SELECT i FROM Issuer i WHERE i.tickerCode = :tickerCode AND i.date = :date")
//    Optional<Issuer> findIssuerByTickerCodeAndDate(@Param("tickerCode") String tickerCode, @Param("date") LocalDate date);


}

