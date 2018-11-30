#### redis相关
##### 1.redis数据结构
```
常用数据结构
	字符串String
	字典Hash
	列表list
	集合set
	有序集合SortedSet
中高级
	HyperLogLog
	Geo
	Pub/Sub
Redis Module
	BloomFilter
	RedisSearch
	Redis-ML
```
##### 2.redis分布式锁
```
先拿setnx来争到锁，抢到之后在用expire给锁加一个过期时间防止锁忘记了释放
若在setnx争到锁之后，进程意外crash或者意外重启
此时这个锁就永远不会释放
解决办法：
		用set将setnx和expire合成一个指令
```
##### 3.redis里有1亿个key,其中有10W个key是以某个固定的已知的前缀开始的，如何将它们全部找出来
```
使用keys可以扫描出指定模式的key列表
若是redis正在给线上的业务提供服务，则此时使用keys命令会导致的问题
因为redis是单线程的，在使用keys命令的时候，线程会阻塞一段时间，线上服务会停顿，直到keys命令执行完毕，服务才能恢复。
此时可以使用scan命令，scan命令可以无阻塞的取出指定模式的key列表，但会有一定几率的重复，需要在客户端做去重操作，整体花费的时间比keys命令长
```
##### 4.redis做异步队列
```
使用list作为消息队列，rpush生产消息，lpop消费消息，当lpop没有消息的时候要适当的sleep一会再重试，也可以使用blpop，在没有消息的时候会阻塞等待消息的到来

使用pub/sub的主题订阅者模式，可以实现1：N的消息队列
```
##### 5.有大量的key需要设置同一时间过期，一般需要注意什么
```
大量的key在同一时间过期时，会出现短暂的卡顿现象。一般需要在时间上添加随机值，使得过期时间分散一些
```
##### 6.redis持久化
```
bgsave做镜像全量持久化，aof做增量持久化。因为bgsave会比较耗时，不够实时，在停机的时候会丢失大量的数据，所以需要aof来配合。在redis实例重启的时候，会使用bgsave持久化文件重新构建内存，再使用aof重放近期操作的数据恢复到重启之前的状态。

突然机器掉电会怎么样？

取决于aof日志sunc的配置，如果不要求性能，每一条指令都sync，就不会丢失数据。
在高性能要求下，一般使用1ssync一次，取决于配置

bgsave的原理：

fork和cow，redis通过fork子进程来进行bgsave操作，cow指的是copy on write，子进程创建之后，父子进程共享数据段，父进程继续提供读写服务，写脏的数据会逐渐和子进程分离开来

```
##### 7.redis同步机制
```
redis可以使用主从同步，从从同步。第一次同步时，主节点做一次bgsave，并同时将后续操作记录到buffer中，待完成后将rdb文件全量同步到复制节点，复制节点接受完rdb文件之后加载到内存。加载完成之后再通知主节点将期间修改的记录同步到复制节点进行重放就完成了同步过程
```
##### 8.redis集群
```
Redis Sentinal着眼于高可用，在master宕机时会自动将slave提升为master，继续提供服务。

Redis Cluster着眼于扩展性，在单个redis内存不足时，使用Cluster进行分片存储。
```