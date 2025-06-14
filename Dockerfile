# Multi-stage build for smaller image size
FROM eclipse-temurin:21-jdk-jammy AS builder

# 작업 디렉토리 설정
WORKDIR /app

# Gradle wrapper와 설정 파일 복사
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .

# 의존성 다운로드 (캐시 최적화)
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon

# 소스 코드 복사
COPY src src

# 애플리케이션 빌드
RUN ./gradlew build -x test --no-daemon

# Runtime stage
FROM eclipse-temurin:21-jre-jammy

# 메타데이터 라벨
LABEL maintainer="hyeongju6"
LABEL description="Portfolio Spring Boot Application"
LABEL version="1.0.0"

# 애플리케이션 사용자 생성 (보안)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 작업 디렉토리 설정
WORKDIR /app

# JAR 파일 복사
COPY --from=builder /app/build/libs/*.jar app.jar

# 정적 파일들 복사
COPY --from=builder /app/build/resources/main/static ./static

# 파일 소유권 변경
RUN chown -R appuser:appuser /app

# 사용자 변경
USER appuser

# 포트 노출
EXPOSE 8080

# JVM 옵션 설정
ENV JAVA_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"

# 애플리케이션 실행
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]