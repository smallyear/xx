###Dockerfile文件中的CMD和ENTRYPOINT指令差异对比
CMD指令和ENTRYPOINT指令的作用都是为镜像指定容器启动后的命令，那么它们两者之间有什么各自的优点呢？

为了更好地对比CMD指令和ENTRYPOINT指令的差异，我们这里再列一下这两个指令的说明，
```shell
>CMD 支持三种格式
    CMD ["executable","param1","param2"] 使用 exec 执行，推荐方式；
    CMD command param1 param2 在 /bin/sh 中执行，提供给需要交互的应用；
    CMD ["param1","param2"] 提供给 ENTRYPOINT 的默认参数；
	指定启动容器时执行的命令，每个 Dockerfile 只能有一条 CMD 命令。如果指定了多条命令，只有最后一条会被执行。
	如果用户启动容器时候指定了运行的命令，则会覆盖掉 CMD 指定的命令。
	
>ENTRYPOINT 两种格式：
    ENTRYPOINT ["executable", "param1", "param2"]
    ENTRYPOINT command param1 param2（shell中执行）。
	配置容器启动后执行的命令，并且不可被 docker run 提供的参数覆盖。
	每个 Dockerfile 中只能有一个 ENTRYPOINT，当指定多个时，只有最后一个起效。
```
从上面的说明，我们可以看到有两个共同点：
**1.都可以指定shell或exec函数调用的方式执行命令；**
**2.当存在多个CMD指令或ENTRYPOINT指令时，只有最后一个生效；**
而它们有如下差异：
```shell
	差异1：CMD指令指定的容器启动时命令可以被docker run指定的命令覆盖，而ENTRYPOINT指令指定的命令不能被覆盖，而是将docker run指定的参数当做ENTRYPOINT指定命令的参数。
 	差异2：CMD指令可以为ENTRYPOINT指令设置默认参数，而且可以被docker run指定的参数覆盖；
```

#### 差异1
	CMD指令指定的容器启动时命令可以被docker run指定的命令覆盖；而ENTRYPOINT指令指定的命令不能被覆盖，而是将docker run指定的参数当做ENTRYPOINT指定命令的参数。
下面有个命名为startup的可执行shell脚本，其功能就是输出命令行参数而已。内容如下所示，
```shell
#!/bin/bash
echo "in startup, args: $@"
```
**通过CMD指定容器启动时命令：**
现在我们新建一个Dockerfile文件，其将startup脚本拷贝到容器的/opt目录下，并通过CMD指令指定容器启动时运行该startup脚本。其内容如下:
```shell
FROM ubuntu:14.04
MAINTAINER wangyb@xxx.com

ADD startup /opt
RUN chmod a+x /opt/startup

CMD ["/opt/startup"]
```

然后我们通过运行docker build命令生成test:latest镜像

```shell
wangyb@test$ sudo docker build -t test .
Sending build context to Docker daemon 4.096 kB
Step 1 : FROM ubuntu:14.04
 ---> a5a467fddcb8
Step 2 : MAINTAINER wangyb@163.com
 ---> Using cache
 ---> 332259a92e74
Step 3 : ADD startup /opt
 ---> 3c26b6a8ef1b
Removing intermediate container 87022b0f30c5
Step 4 : RUN chmod a+x /opt/startup
 ---> Running in 4518ba223345
 ---> 04d9b53d6148
Removing intermediate container 4518ba223345
Step 5 : CMD /opt/startup
 ---> Running in 64a07c2f5e64
 ---> 18a2d5066346
Removing intermediate container 64a07c2f5e64
Successfully built 18a2d5066346
```

然后使用docker run启动两个test:latest镜像的容器，第一个docker run命令没有指定容器启动时命令，第二个docker run命令指定了容器启动时的命令为“/bin/bash -c 'echo Hello'”

```shell
wangyb@test$ sudo docker run -ti --rm=true test
in startup, args: 
wangyb@test$ sudo docker run -ti --rm=true test /bin/bash -c 'echo Hello'
Hello
```

从上面运行结果可以看到，docker run命令启动容器时指定的运行命令覆盖了Dockerfile文件中CMD指令指定的命令。

 **通过ENTRYPOINT指定容器启动时命令：**
将上面的Dockerfile中的CMD替换成ENTRYPOINT，内容如下所示
```shell
FROM ubuntu:14.04
MAINTAINER wangyb@xxx.com

ADD startup /opt
RUN chmod a+x /opt/startup

ENTRYPOINT [“/opt/startup”]
```

同样，通过运行docker build生成test:latest镜像

```shell
wangyb@test$ sudo docker build -t test .
Sending build context to Docker daemon 4.096 kB
Step 1 : FROM ubuntu:14.04
 ---> a5a467fddcb8
Step 2 : MAINTAINER wangyb@163.com
 ---> Using cache
 ---> 332259a92e74
Step 3 : ADD startup /opt
 ---> Using cache
 ---> 3c26b6a8ef1b
Step 4 : RUN chmod a+x /opt/startup
 ---> Using cache
 ---> 04d9b53d6148
Step 5 : ENTRYPOINT /opt/startup
 ---> Running in cdec60940ad7
 ---> 78f8aca2edc2
Removing intermediate container cdec60940ad7
Successfully built 78f8aca2edc2
```

然后使用docker run启动两个test:latest镜像的容器，第一个docker run命令没有指定容器启动时命令，第二个docker run命令指定了容器启动时的命令为“/bin/bash -c 'echo Hello'”

```shell
wangyb@test$ sudo docker run -ti --rm=true test
in startup, args: 
wangyb@test$ sudo docker run -ti --rm=true test /bin/bash -c 'echo Hello'
in startup, args: /bin/bash -c echo Hello
```

**通过上面的运行结果可以看出，docker run命令指定的容器运行命令不能覆盖Dockerfile文件中ENTRYPOINT指令指定的命令，反而被当做参数传递给ENTRYPOINT指令指定的命令。**

####差异2
	CMD指令可以为ENTRYPOINT指令设置默认参数，而且可以被docker run指定的参数覆盖；
同样使用上面的startup脚本。编写Dockerfile，内容如下所示
```shell
FROM ubuntu:14.04
MAINTAINER wangyb@xxx.com
 
ADD startup /opt
RUN chmod a+x /opt/startup

ENTRYPOINT ["/opt/startup", "arg1"]
CMD ["arg2"]
```
运行docker build命令生成test:latest镜像

```shell
wangyb@test$ sudo docker build -t test .
Sending build context to Docker daemon 4.096 kB
Step 1 : FROM ubuntu:14.04
 ---> a5a467fddcb8
Step 2 : MAINTAINER wangyb@163.com
 ---> Using cache
 ---> 332259a92e74
Step 3 : ADD startup /opt
 ---> Using cache
 ---> 3c26b6a8ef1b
Step 4 : RUN chmod a+x /opt/startup
 ---> Using cache
 ---> 04d9b53d6148
Step 5 : ENTRYPOINT /opt/startup arg1
 ---> Running in 54947233dc3d
 ---> 15a485253b4e
Removing intermediate container 54947233dc3d
Step 6 : CMD arg2
 ---> Running in 18c43d2d90fd
 ---> 4684ba457cc2
Removing intermediate container 18c43d2d90fd
Successfully built 4684ba457cc2
```
下面运行docker run启动两个test:latest镜像的容器，第一条docker run命令没有指定参数，第二条docker run命令指定了参数arg3，其运行结果如下
```shell
wangyb@test$ sudo docker run -ti --rm=true test
in startup, args: arg1 arg2
wangyb@test$ sudo docker run -ti --rm=true test arg3
in startup, args: arg1 arg3
```
**从上面第一个容器的运行结果可以看出CMD指令为ENTRYPOINT指令设置了默认参数；从第二个容器的运行结果看出，docker run命令指定的参数覆盖了CMD指令指定的参数。**
####注意点
**CMD指令为ENTRYPOINT指令提供默认参数是基于镜像层次结构生效的，而不是基于是否在同个Dockerfile文件中。意思就是说，如果Dockerfile指定基础镜像中是ENTRYPOINT指定的启动命令，则该Dockerfile中的CMD依然是为基础镜像中的ENTRYPOINT设置默认参数。**
例如，我们有如下一个Dockerfile文件
```shell
FROM ubuntu:14.04
MAINTAINER wangyb@xxx.com
 
ADD startup /opt
RUN chmod a+x /opt/startup

ENTRYPOINT ["/opt/startup", "arg1"]
```
通过运行docker build命令生成test:0.0.1镜像，然后创建该镜像的一个容器，查看运行结果，
```shell
wangyb@test$ sudo docker build -t test:0.0.1 .
Sending build context to Docker daemon 6.144 kB
Step 1 : FROM ubuntu:14.04
 ---> a5a467fddcb8
Step 2 : MAINTAINER wangyb@163.com
 ---> Running in 57a96522061a
 ---> c3bbf1bd8068
Removing intermediate container 57a96522061a
Step 3 : ADD startup /opt
 ---> f9884fbc7607
Removing intermediate container 591a82b2f382
Step 4 : RUN chmod a+x /opt/startup
 ---> Running in 7a19f10b5513
 ---> 16c03869a764
Removing intermediate container 7a19f10b5513
Step 5 : ENTRYPOINT /opt/startup arg1
 ---> Running in b581c32b25c3
 ---> c6b1365afe03
Removing intermediate container b581c32b25c3
Successfully built c6b1365afe03
wangyb@test$ sudo docker run -ti --rm=true test:0.0.1
in startup, args: arg1
```
下面新建一个Dockerfile文件，基础镜像是刚生成的test:0.0.1，通过CMD指定要通过echo打印字符串“in test:0.0.2”。文件内容如下所示:
```shell
FROM test:0.0.1
MAINTAINER wangyb@xxx.com

CMD ["/bin/bash", "-c", "echo in test:0.0.2"]
```
运行docker build命令生成test:0.0.2镜像，然后通过运行docker run启动一个test:0.0.2镜像的容器来查看结果
```shell
wangyb@test$ sudo docker build -t test:0.0.2 .
Sending build context to Docker daemon 6.144 kB
Step 1 : FROM test:0.0.1
 ---> c6b1365afe03
Step 2 : MAINTAINER wangyb@163.com
 ---> Running in deca95cf4c15
 ---> 971b5a819b48
Removing intermediate container deca95cf4c15
Step 3 : CMD /bin/bash -c echo in test:0.0.2
 ---> Running in 4a31c4652e1e
 ---> 0ca06ba31405
Removing intermediate container 4a31c4652e1e
Successfully built 0ca06ba31405
wangyb@test$ sudo docker run -ti --rm=true test:0.0.2
in startup, args: arg1 /bin/bash -c echo in test:0.0.2
```
从上面结果可以看到，镜像test:0.0.2启动的容器运行时并不是打印字符串”in test:0.0.2”，而是将CMD指令指定的命令当做基础镜像test:0.0.1中ENTRYPOINT指定的运行脚本startup的参数




















































