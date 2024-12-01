package mk.ukim.finki.wp.homework2das.bootstrap;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.hibernate.dialect.Dialect;
import org.hibernate.community.dialect.SQLiteDialect;

@Configuration
public class HibernateConfig {

    @Bean
    public Dialect hibernateDialect() {
        return new SQLiteDialect();
    }
}
