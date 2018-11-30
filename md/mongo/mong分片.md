#### 分片和集群（双机方案，单机模拟）
##### 创建分片1副本集
###### 主节点
建立数据文件夹和日志文件目录命令如下：

	mkdir -p /data/mongodb/shard1-1/db/
	mkdir -p /data/mongodb/shard1-1/log/

建立配置文件目录命令如下：

	mkdir -p /data/mongodb/shard1-1/conf


修改配置文件

```
...
 pidFilePath: /home/test/shard1-1/config/mongomaster.pid
replication:
   oplogSizeMB: 200
   replSetName: shard1  

sharding:
##分片角色
   clusterRole: shardsvr #（分片角色名称都为shardsvr）
```
###### 从节点
建立分片1从节点数据文件夹和日志文件目录如下
	
	mkdir -p /data/mongodb/shard1-2/db/
	mkdir -p /data/mongodb/shard1-2/log/
立配置文件目录命令如下
	
	mkdir –p /data/mongodb/shard1-2/conf

配置参考主节点
###### 仲裁节点
建立分片1仲裁节点的数据文件和日志文件目录命令如下
	
	mkdir-p /data/mongodb/shard1-3/db/
	mkdir -p /data/mongodb/shard1-3/log/

建立分片1的仲裁节点的配置文件目录命令如下

	mkdir -p /data/mongodb/shard1-3/conf
配置参考主节点
##### 创建分片2副本集
注：分片2的配置与分片1的配置方法相同，需要注意以下几点：
1.在配置分片2的主、备、从节点时需要更改配置文件的数据文件和日志文件文件存放路径为自己所建立的实际路径。
2.	配置文件中端口号的配置不能和其他服务端口冲突，且主、备、从端口号不能一致。
3.	不同的分片，每个分片的的复制集名称不能相同，名称可由自己指定(如分片2的所有replSetName为shard2 ).
4.	主、备、从配置文件中其他配置不需要作更改。

###### 主节点
建立数据文件夹和日志文件目录命令

	mkdir -p /data/mongodb/shard2-1/db/
	mkdir -p /data/mongodb/shard2-1/log/

建立配置文件目录命令
	mkdir -p /data/mongodb/shard2-1/conf

修改配置文件
```
···
 pidFilePath: /home/chenguoa/shard2-1/config/mongomaster.pid
replication:
##oplog大小
   oplogSizeMB: 20480
##复制集名称
   replSetName: shard2  
sharding:
##分片角色
 clusterRole: shardsvr
```
###### 从节点
建立数据文件和日志文件目录命令
	mkdir -p /data/mongodb/shard2-2/db/
	mkdir -p /data/mongodb/shard2-2/log/

建立分片2的从节点的配置文件目录命令

	mkdir –p /data/mongodb/shard2-2/conf

配置参考主节点
###### 仲裁节点
建立分片2仲裁节点的数据文件和日志文件目录命令
	
	mkdir -p /data/mongodb/shard2-3/db/
	mkdir -p /data/mongodb/shard2-3/log/

建立分片2的仲裁节点的配置文件目录命令如下

	mkdir –p /data/mongodb/shard2-3/conf
配置参考主节点

##### 创建配置服务器
配置服务器简介
顾名思义为配置服务器，存储所有数据库元信息（路由、分片）的配置。mongos本身没有物理存储分片服务器和数据路由信息，只是缓存在内存里，配置服务器则实际存储这些数据。mongos第一次启动或者关掉重启就会从ConfigServer加载配置信息，以后如果配置服务器信息变化会通知到所有的 mongos 更新自己的状态，这样 mongos 就能继续准确路由。在生产环境通常有多个 config server 配置服务器，因为它存储了分片路由的元数据，这个可不能丢失！就算挂掉其中一台，只要还有存货， mongodb集群就不会挂掉。

###### 配置文件
创建配置服务器的数据存储和日志存储目录命令如下图
	
	mkdir -p /data/mongodb/ConfigServer/db/
	mkdir -p /data/mongodb/ConfigServer/log/
创建服务的配置文件目录命令如下图

	mkdir –p /data/mongodb/ConfigServer/conf

修改配置文件
```
···
##分片角色
 clusterRole: configsvr
```

##### Mongod 创建并配置mongos(路由器)
Mongos（路由器）简介：
数据库集群请求的入口，所有的请求都通过mongos进行协调，不需要在应用程序添加一个路由选择器，mongos自己就是一个请求分发中心，它负责把对应的数据请求请求转发到对应的shard服务器上。在生产环境通常有多mongos作为请求的入口，防止其中一个挂掉所有的mongodb请求都没有办法操作。
###### 配置文件
在使用Mongos（路由器）时，不需要建立数据存储目录，只需要建立日志存放路径和配置文件路径。
创建日志目录命令如下图：
mkdir -p /data/log/mongodb/mongos/logs
在日志目录下创建mongo.log文件

路由设置
   路由是能通过配置服务器(ConfigServer)来连接分片服务器，在启动路由进程时，先启动配置进程，路由配置文件过程如下：
 config.conf(在mongos配置文件夹conf目录下创建config.conf文件)
```
systemLog:
 destination: file
##日志位置
 path: /data/log/mongodb/mongos/conf/mongos2.log
 logAppend: true
##网路配置
net:
##端口配置
 port: 50002
##分片配置
sharding:
##指定config server
configDB: 10.126.252.31:40001（配置指定的configServer的ip地址多个可用逗号分开）
#configDB: 10.126.252.31:40001, 10.126.252.33:40002
processManagement:	
```
##### 启动分片
###### 分片1副本集启动
首选通过配置文件启动分片一上配置的3个主，从，仲裁的mongodb实例
通过在mongodb的bin目录下执行mongod命令，命令如下

	./mongod -f /data/mongodb/shard1-1/config.conf
	./mongod -f /data/mongodb/shard1-2/config.conf
	./mongod -f /data/mongodb/shard1-3/config.conf

通过在bin目录下执行mongo命令连接分片一副本集的主节点mongo实例初始化分片一的副本集

	./mongo --port 27020（端口号可以是主、从、备的端口，这里为主节点端口）

连接mongodb实例后选则管理员权限

	 use admin

初始化副本集

	db.runCommand({"replSetInitiate":{"_id":"shard1","members":[{"_id":0,"host":"10.126.252.31:27020",priority:2},{"_id":1,"host":"10.126.252.31:27021","arbiterOnly":true},{"_id":2,"host":"10.126.252.31:27022", priority:1}]}})

replSetInitiate为初始化副本集指令。最外层的_id表示分片一replica set（副本集）的名字，members里包含的是所有节点的地址以及优先级priority。优先级最高的即成为主节点，即这里的10.126.252.31:27020。特别注意的是，对于仲裁节点，需要有个特别的配置——arbiterOnly:true。这个千万不能少了，不然主备模式就不能生效。host为配置主、备、从的ip和端口号



###### 分片2副本集启动
首选通过配置文件启动分片2上配置的3个主，从，仲裁的mongodb实例
在mongodb 的bin目录下执行mongod命令，命令如下
	
	 ./mongod -f /data/mongodb/shard2-1/config.conf
	 ./mongod -f /data/mongodb/shard2-2/config.conf
	 ./mongod -f /data/mongodb/shard2-3/config.conf

通过在bin目录下执行mongo命令连接连接分片2主节点的mongo实例初始化分片2的副本集

	  ./mongo --port 32001 
连接mongodb实例后选则管理员权限

	use admin
初始化副本集

	db.runCommand({"replSetInitiate":{"_id":"shard2","members":[{"_id":0,"host":"10.126.252.31:32001",priority:2},{"_id":1,"host":"10.126.252.31:32002","arbiterOnly":true},{"_id":2,"host":"10.126.252.31:32003", priority:1}]}})


###### 配置服务器启动
通过ConfigServer配置文件在mongodb 的bin目录下启动Server实例

	./mongod -f /data/mongodb/ConfigServer/conf /config.conf

######  mongos路由器启动 
通过mongos的配置文件在mongodb的bin目录下进行启动
命令如下：
	
	./mongos  --config=/data/mongodb/mongos/conf /mongos.conf
	(注意启动路由时执行的是mongos命令而不是mongo命令)

##### 配置分片
在mongodb的bin目录下进行启动


	./mongo 10.126.252.31:50002 (这里必须连接mongos(路由器)ip和端口)

连接成功后通过show dbs 指令如果出现数据库名表示连接成功。
###### 添加分片指令
添加分片指令：这里添加分片时只需要添加各个副本集主节点的的ip和端口mongoDB会自动查找当前节点的副本集。shard1和 shard2为副本集的名称。

	sh.addShard("shard1/10.126.252.31:27020")
	sh.addShard("shard2/10.126.252.31:32001")

###### 激活分片的配置
激活分片指令，成功后如下所示： 

	sh.enableSharding("数据库名")
 
Try为数据库名：ok:1表示分片成功，ok:0表示分片失败。
这里只是标识这个数据库可以启用分片，但实际上并没有进行分片。

###### 设定集合片键命令
设定集合片键命令成功如下图所示

	sh.shardCollection("数据库名.集合名", {key : value})
Key为设置的片键（一般为数据库表中的字段名），value为设置的片（为-1或者1，表示按照升序或降序进行分片，具体片键值需要根据库中的数据进行合理设置）

###### 检查分片添加
命令检查分片添加情况，如出现以下结果则表示配置成功：
分配管理员权限进行操作
	
	mongos>use admin
检查分片情况命令如下图所示：
	
	db.runCommand( {listshards : 1 } )

查看分片状态指令
	
	db.printShardingStatus() #查看分片状态

Shards下表示分片的名称以及各个片的副本集的情况。
Databases:
“_id”,。表示数据库名。
“partioned”,布尔型。如果为true则表示开启了分片功能。
“primary”，字符串，这个值与“_id”对应表示这个数据库的“大本营“在哪里，不论分片与否，数据库总是会有个“大本营”，创建数据库时会随机选择一个片，也就是说大本营是开始创建数据库文件的位置。虽然分片的时候数据库也会用到很多别的服务器，但是分片从这开始。
test.short下shard key表示分的片键情况。
Chunks块表示name:minkey和maxkey表示当前分片的起始和结束。