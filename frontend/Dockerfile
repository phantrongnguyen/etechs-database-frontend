FROM maven:3.9.9-eclipse-temurin-23 AS build

WORKDIR /app
COPY pom.xml .
COPY src ./src
COPY .mvn ./.mvn

RUN mvn clean package -DskipTests

FROM eclipse-temurin:23-jre-alpine

WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "--enable-native-access=ALL-UNNAMED", "-jar", "app.jar"]
