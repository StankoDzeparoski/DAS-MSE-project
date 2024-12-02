package mk.ukim.finki.wp.homework2das.model;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

@Converter(autoApply = true) // autoApply ensures it's applied to all LocalDate fields
public class DateFormatConverter implements AttributeConverter<LocalDate, String> {

    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("d.M.yyyy");

    @Override
    public String convertToDatabaseColumn(LocalDate attribute) {
        if (attribute == null) {
            return null;
        }
        return attribute.format(FORMATTER); // Format the LocalDate to DD.MM.YYYY
    }

    @Override
    public LocalDate convertToEntityAttribute(String dbData) {
        if (dbData == null) {
            return null;
        }
        try {
            return LocalDate.parse(dbData, FORMATTER); // Parse the string to LocalDate
        } catch (Exception e) {
            throw new IllegalArgumentException("Invalid date format: " + dbData, e);
        }
    }
}

