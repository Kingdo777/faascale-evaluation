# 使用 OpenJDK 8 作为基础镜像
FROM openjdk:8-jdk-alpine

# 设置工作目录
WORKDIR /app

# 复制源代码
COPY ./* /app/

# 编译 Java 代码
RUN javac /app/SimpleHttpServer.java


# 暴露容器端口
EXPOSE 8080

# 启动应用程序
CMD ["java", "SimpleHttpServer"]
