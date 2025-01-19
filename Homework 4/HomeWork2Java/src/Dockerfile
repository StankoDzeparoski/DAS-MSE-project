FROM openjdk:17-jdk-slim
WORKDIR /app

# Copy the JAR file into the container
COPY target/mvc-app.jar /app/mvc-app.jar

# Expose the port your Spring Boot app is running on (default is 8080)
EXPOSE 8080

# Run the Spring Boot application
CMD ["java", "HomeWork2DaSApplication.java"]

