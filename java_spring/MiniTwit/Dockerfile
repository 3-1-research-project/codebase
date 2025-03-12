FROM maven:3.8.4-openjdk-17 as maven-builder
COPY src /app/src
COPY pom.xml /app


RUN mvn -f /app/pom.xml clean package -DskipTests
FROM openjdk:17-oracle



COPY --from=maven-builder app/target/MiniTwit-1.0.3.war /app-service/MiniTwit-1.0.3.war
COPY minitwit.db /app-service/minitwit.db
WORKDIR /app-service


EXPOSE 5000
ENTRYPOINT ["java","-jar","MiniTwit-1.0.3.war"]