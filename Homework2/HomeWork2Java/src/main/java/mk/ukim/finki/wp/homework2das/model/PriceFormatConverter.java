//package mk.ukim.finki.wp.homework2das.model;
//
//import jakarta.persistence.AttributeConverter;
//import jakarta.persistence.Converter;
//
//@Converter(autoApply = true)
//public class PriceFormatConverter implements AttributeConverter<Float, String> {
//
//    @Override
//    public String convertToDatabaseColumn(Float attribute) {
//        if (attribute == null) {
//            return null;
//        }
//        // Return the float as a string with a comma separator for thousands (optional)
//        return String.format("%,.2f", attribute); // Format it as "24,550.00"
//    }
//
//    @Override
//    public Float convertToEntityAttribute(String dbData) {
//        if (dbData == null) {
//            return null;
//        }
//        try {
//            // Remove the comma and convert to a float
//            String cleanedData = dbData.replace(",", "");
//            return Float.parseFloat(cleanedData); // Convert to Float
//        } catch (NumberFormatException e) {
//            throw new IllegalArgumentException("Invalid price format: " + dbData, e);
//        }
//    }
//}
//
