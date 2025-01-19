FROM maven:3.8.4-openjdk-17-slim AS build
WORKDIR /HomeWork2Java

# Copy the JAR file into the container
COPY pom.xml .
RUN mvn dependency:go-offline

COPY . .

RUN mvn clean package -DskipTests

FROM openjdk:17-jdk-slim
WORKDIR /HomeWork2Java

COPY --from=build /HomeWork2Java/target/HomeWork2Java-0.0.1-SNAPSHOT.jar /HomeWork2Java/HomeWork2Java-0.0.1-SNAPSHOT.jar



EXPOSE 8080

# Run the Spring Boot application
CMD ["java", "-jar", "HomeWork2Java-0.0.1-SNAPSHOT.jar"]

