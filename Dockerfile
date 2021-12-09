FROM openjdk:11.0.10-jdk-slim-buster
EXPOSE 8080
COPY target/casestudy-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]