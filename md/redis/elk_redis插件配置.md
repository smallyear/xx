elk_redis插件

最小化配置
```shell
    input {

        redis {

                    data_type => "list" #logstash redis插件工作方式
                    
                    key => "logstash-test-list" #监听的键值
                    
                    host => "127.0.0.1" #redis地址
                    
                    port => 6379 #redis端口号

                }

              }

output {

         stdout{}
        
        }

```
详细配置
```
input {

    redis {
    
        batch_count => 1 #EVAL命令返回的事件数目
        
        data_type => "list" #logstash redis插件工作方式
        
        key => "logstash-test-list" #监听的键值
        
        host => "127.0.0.1" #redis地址
        
        port => 6379 #redis端口号
        
        password => "123qwe" #如果有安全认证，此项为密码
        
        db => 0 #redis数据库的编号
        
        threads => 1 #启用线程数量
    
    }

}

    output {
    
        stdout{}
    
    }
```

#### 关于其他的参数

##### db
Redis里面有数据库的概念，一般是16个，默认登录后是0，可以通过命令选择。如果应用系统选择使用了不同的数据库，那么可以通过配置这个参数从指定的数据库中读取信息。

##### key
Redis中的数据都是通过键值来索引的，不管是字符串还是列表，所以这个key相当于数据库中的表。
如果是list或者channel模式，key都是指定的键值；而如果是pattern_channel，那么key可以通过glob通配的方式来指定。

##### password
有的Redis为了安全，是需要进行验证的。只有设置了password，才能正确的读取信息。相反，如果redis没有设置密码，而logstash中配置了密码，也会报错！

##### batch_count
这个属性设置了服务器端返回的事件数目，比如设置了5条，那么每次请求最多会直接获取5条日志返回。

#### data_type logstash工作的类型

logstash中的redis插件，指定了三种方式来读取redis队列中的信息。

list=>BLPOP

channel=>SUBSCRIBE

pattern_channel=>PSUBSCRIBE

其中list，相当于队列；

channel相当于发布订阅的某个特定的频道；


pattern_channel相当于发布订阅某组频道。