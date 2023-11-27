# ./target/spring-boot-docker-0.1.0.jar 是通过maven打包的jar包，参考自：https://github.com/bingohuang/spring-boot-docker
# 生成./target/spring-boot-docker-0.1.0.jar，只需要在project中执行：mvn package

FROM hub.c.163.com/xbingo/jdk8:latest

COPY ./target/spring-boot-docker-0.1.0.jar /app.jar

ENTRYPOINT ["java","-jar","/app.jar"]
