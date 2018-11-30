# 搭建docker私有镜像仓库步骤

1.为私有仓库建立两个文件夹

​	mkdir  /docker/docker_registry_certs

​	mkdir /docker/docker_registry_images

2.建立私钥

1.生成证书

```
-openssl genrsa -out registry.key 2048

	SRV_Country="CN"

	SRV_State="XiAn"

	SRV_Location="XiAn"

	SRV_Organization="DCITS"

	SRV_OrganizationUnit="DCITS"

	SRV_CommonName="192.168.10.133"

	openssl req -new -x509 -days 7300 -key registry.key -out registry.cert -subj \
"/C=SRV_Country/ST=SRV_State/L=SRV_Location/O=SRV_Organization/OU=SRV_OrganizationUnit/CN=SRV_CommonName" -config /etc/pki/tls/openssl.cnf
```

2.   启动容器

     ```
     docker run -d --name docker_registry -p 5000:5000 --restart=always -v /docker/docker_registry_images:/var/lib/registry/docker/registry/v2 -v /docker/docker_registry_certs:/certs -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.crt -e
     REGISTRY_HTTP_TLS_KEY=/certs/registry.key -u root registry:2
     ```

     说明一下参数的意义：

     -v

     /docker/docker_registry_images:/var/lib/registry/docker/registry/v2

     指定Docker镜像存储的路径，将容器宿主机的本地目录/docker/docker_registry_images映射进容器

     -v/docker/docker_registry_certs:/certs 将证书存放的目录映射进容器

     -eREGISTRY_HTTP_TLS_CERTIFICATE和 -e REGISTRY_HTTP_TLS_KEY 指定的是证书的路径，指的是容器内的路径，在/certs目录下

3.   测试仓库是否可以使用

           ​```
           docker images
           docker tag registry:2 localhost:5000/registry:2
           docker push localhost:5000/registry:2
           
           curl -X GET https://127.0.0.1:5000/v2/_catalog -k
           curl -X GET https://127.0.0.1:5000/v2/registry/tag/list -k
           ​```
           
           ​

4.客户端使用私有仓库

在客户端容器的宿主机上，创建一个以先前创建证书是CN所赋的值命名的目录

```
mkdir /etc/docker/certs.d/10.126.252.16:5000

```

将先前生成的证书文件registry.crt，拷贝到客户端容器宿主机上/etc/docker/certs.d/10.240.227.50目录下，并更名为ca.crt

**注意 ** 添加完证书之后，需要重启Docker服务： systemctl restart docker.service

之后就可以正常pull  push了

5.**搭建需证书加用户名密码认证的Docker私有仓库**

在1的基础上，在加上用户名和密码认证，首先需要创建一个包含用户和密码的文件

```
mkdir /dcoker/docker_registry_auth
docker run --entrypoint htpasswd registry:2 -Bbn testuser testpasswd > htpasswd

```

清除之前的docker registry容器，重新启动一个新的



```shell
docker run -d -p 5000:5000 --restart=always --name=docker_registry \
-v /docker/docker_registry_images:/var/lib/registry/docker/registry/v2 \
-v /docker/docker_registry_auth:/auth \
-v /docker/docker_registry_certs:/certs \
-e "REGISTRY_AUTH=htpasswd" \
-e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
-e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
-e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.crt \
-e REGISTRY_HTTP_TLS_KEY=/certs/registry.key \
-u root registry:2
```

此时在客户端，push镜像之前就需要先登录

```shell
docker login
docker pull
docker push
```

使用curl 获取镜像列表是需要添加用户名和密码

```shell
curl -u user:passwd  -X GET https://127.0.0.1:5000/v2/_catalog -k
```



```java
public void getStr(){
  return this.str;
}
```









































































