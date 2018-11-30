#### 三次握手
- 客户端与服务端均处于closed状态
- 客户端发出请求  SYN=1 seq=x 之后客户端处于SYN-SENT状态
- 服务端收到请求之后处于LISTEN状态 返回 SYN=1 ACK=1 ack=x+1 seq=y 服务端处于SYN-REVD状态
- 客户端收到之后 发出 SYN=1 ACK=1 ack=y+1 seq=x+1 客户端处于ESTABLISHED状态
- 服务端收到后也处于ESTABLISHED状态

#### 四次挥手

- 客户端和服务端均处于ESTABLISHED状态
- 客户端停止发送数据 发送FIN=1 seq=u(u等于客户端发送的最后一个字节的序号加1)，之后客户端处于FIN-WAIT-1状态
- 服务端手收到之后回复 ACK=1 ack=u+1 seq=v(v等于服务端发送的最后一个字节的序号加1) 发送之后服务端进入CLOSE-WAIT状态 此时TCP连接处于半开半闭的状态服务端如果发送数据的话， 客户端会继续接收 客户端收到回复后进入FIN-WAIT-2状态
- 服务端在发送完数据之后发送FIN=1 ACK=1 ack=u+1 seq=w之后进入LAST-ACK状态
- 客户端收到之后回复 ACK=1 ack=w+1(w为半开半闭状态时服务端发送的最后一个字节的序号)
seq=u+1  进入TIME-WAIT状态
- 等待4分钟之后连接关闭


