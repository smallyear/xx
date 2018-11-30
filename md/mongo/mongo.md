##### 配置文件
```shell
dbpath = /usr/local/mongodb/esbdb/data  #数据库路径
logpath = /usr/local/mongodb/esbdb/log/mongodb.log #日志输出文件路径 
logappend=true  #错误日志采用追加模式，配置这个选项后mongodb的日志会追加到现有的日志文件，而不是从新创建一个新文件
journal=true #启用日志文件，默认启用
quite=true #这个选项可以过滤掉一些无用的日志信息，若需要调试使用请设置为false
port = 27017 #端口号 默认为27017
fork =true # 指定以守护进程的方式来启动MongoDB

```
注意：mongodb集群必须非root用户安装否则会导致集群不生效

##### 启动命令
```
./mongod -f <confpath>

```

##### 用户创建
1、	切换需要创建数据库

	use esbdb

2、	创建用户

	db.createUser({user:"sys",pwd:"esb",roles:[{role:"readWrite",db:"esbdb"}]});
	db.createUser({user:"esb",pwd:"esb",roles:[{role:"readWrite",db:"esbdb"}]});


#### 副本集
```
副本集就是有自动故障恢复功能的主从集群，副本集没有固定的"主节点"，集群会通过投票选举一个"主节点"。当主节点岩机时，会变更到其他节点。副本集布在不同机器上时，至少要启动三个（单数）数据库服务器进程，否则启动时投票不成功会一直初始化不了
   默认设置下，主节点提供所有增删查改服务，备节点不提供任何服务。但是可以通过设置使备节点提供查询服务，这样就可以减少主节点的压力，当客户端进行数据查询时，请求自动转到备节点上。这个设置叫做Read Preference Modes       
仲裁节点是一种特殊的节点，它本身并不存储数据，主要的作用是决定哪一个备节点在主节点挂掉之后提升为主节点，所以客户端不需要连接此节点。这里虽然只有一个备节点，但是仍然需要一个仲裁节点来提升备节点级别。没仲裁节点的话，主节点挂了备节点还是备节点，所以必须配置

```
##### 安装
一台机器上安装三个mongod实例 

在一台服务器上安装端口分别为
```
192.168.128.31:27020  主
192.168.128.31:27021  从
192.168.128.31:27022 仲裁
```

1.创建目录

	mkdir -p /home/test/mongodb/{master,slave,arbiter}
	mkdir -p /home/test/log/{master,slave,arbiter}
2.创建配置文件

	mkdir -p /home/test/conf/{master,slave,arbiter}

配置文件以主为例
主,备,仲裁部署方式一致。主、备、仲裁配置文件路径为各自创建的数据文件，日志文件路径和进程文件路径，如果主、备、仲裁在一台机器上配置端口号需不同，其他配置均相同
```
systemLog:
 destination: file
###日志存储位置
 path: /home/test/log/master/master.log
 logAppend: true  
storage:
##journal配置
 journal:
  enabled: true  
##数据文件存储位置
 dbPath: /home/test/mongodb/master/
##是否一个库一个文件夹
 directoryPerDB: true
##数据引擎
 engine: wiredTiger  
##WT引擎配置
 wiredTiger:
  engineConfig:
##WT最大使用cache
   cacheSizeGB: 10
##是否将索引也按数据库名单独存储
   directoryForIndexes: true
##表压缩配置
  collectionConfig:
   blockCompressor: zlib
##索引配置
  indexConfig:
   prefixCompression: true
##端口配置
net:
 port: 27020   
 maxIncomingConnections: 12000 
processManagement:
 fork: true  
replication:
 replSetName: grape
 oplogSizeMB: 10240

```
3.启动三个mongod实例
```
  ./mongod -f /home/test/conf/master/master.conf
  ./mongod -f /home/test/conf/slave/slave.conf
  ./mongod -f /home/test/conf/arbiter/arbiter.conf
```

##### 初始化副本集（只能启动一次）
1.在mongodb的bin目录下通过如下命令连接一个mongo实例：

	./mongo --port 27020(主，备，仲裁任意一个端口都可以)

2.连接上mongo实例后，进入管理员权限下操作，命令如下
```
> use admin
switched to db admin
> config={ _id:"blort", members:[ {_id:0,host:'192.168.128.31:27020',priority:2}, {_id:1,host:'192.168.128.31:27021',priority:1},{_id:2,host:'192.168.128.31:27022',arbiterOnly:true}] };
```
config是可以任意的名字，当然最好不要是mongodb的关键字如启动命令之类的关键字，conf，cfg都可以。最外层的_id表示replica set（副本集）的名字，是主、备、仲裁的配置文件中设置的副本集的名称，members里包含的是所有节点的地址以及优先级priority。优先级最高的即成为主节点，即这里的192.168.128.31:27020。特别注意的是，对于仲裁节点，需要有个特别的配置——arbiterOnly:true。这个不能少了，不然主备模式就不能生效。host为配置主、备、从的ip和端口号。

3.初始化副本集指令如下图

	rs.initiate(config)   #初始化副本集

Ok:1表示命令执行成功，ok:0表示命令执行失败。

4.查看集群状态指令如下

	rs.status()   #查看集群状态



