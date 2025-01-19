FROM openjdk:17-jdk-slim
WORKDIR /HomeWork2Java

# Copy the JAR file into the container
COPY target/mvc-app.jar /app/mvc-app.jar
EXPOSE 8080

# Run the Spring Boot application
CMD ["java", "HomeWork2DaSApplication.java"]

