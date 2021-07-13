# k8s搭建rabbitmq3.8.2集群rabbitmq-cluster-k8s-Imageversion
### 一、创建nfs-statfullset存储
1. 在nfs共享目录中创建对应的数据写入目录并赋予777权限

```
# cd /opt/nfs-data/stroageclass
# mkdir -p rabbitmq
# chmod 777 -R rabbimq
```
2. 创建rbac
```
   kubectl apply -f rbac.yml（注意以下截图中红框部分要做出对应的修改，name请定义一个唯一值，namespace是对应的命名空间）
```
![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/servicaccounte.png)  

![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/rolebind.png)

3. 创建deployment
   kubectl apply -f deployment.yml（注意以下截图中红框部分要做出对应的修改，name请和rbac中的name保持一致，namespace是对应的命名空间，数据目录请确保修改正确）

![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/deployment.png)

4. 创建class

   kubectl apply -f class.yml（注意以下截图中红框部分要做出对应的修改，name请和rbac中的name保持一致，namespace是对应的命名空间）

![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/class.png)

### 二、部署rabbitmq集群
1. 创建configmap

```
   kubectl appy -f configmap.yml（注意以下截图中红框部分要做出对应的修改，name请定义一个唯一值，namespace是对应的命名空间）
```
![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/configmap.png)

2. 执行生成cookie的脚本
```
   sh erlang.cookie.sh 
```
3. 创建rabbitm集群
```
   kubectl apply -f rabbitmq_cluster.yml（注意以下截图中红框部分要做出对应的修改，name请定义一个唯一值，namespace是对应的命名空间）
```
![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/rabbitmq_cluster.png)

![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/rabbitmq_cluster-management.png)

![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/rabbitmq_cluster-statefulset01.png)

![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/rabbitmq_cluster-statefulset02.png)

4. 在控制台将对应的service访问方式修改为loadblace（注意：对应的端口也可以进行修改）

5. 使用http://loadblace_ip:manger_port登录（默认用户名、密码均是：guest）

### 三、使用shovel插件进行数据同步
1. 登录旧的rabbitmq下载rabbitmq元数据

![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/rabbitmq.png)

2. 导出旧rabbitmq所有队列名称
```
   kubectl exec rabbitmq容器名称 -n 命名空间 rabbitmqctl list_queues|grep -v Listing|awk '{print $1}' > log.txt
```
3. 将下载的rabbitmq元数据文件重命名成rabbit.json，将rabbit.json、log.txt放在rabbitmq.py同级目录下，修改rabbitmq.py并执行

```
   pip install requests

   python rabbitmq.py
```
![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/rabbitmq-py.png)

4. 将生成的log.json导入到新的rabbitm集群中（新的rabbitmq集群configmap中我默认配置的是：开启shovel插件，不使用时可以进行禁用）

![avatar](https://github.com/TomMorant/rabbitmq-cluster-k8s-Imageversion/blob/master/screenshot/new-rabbitmq.png)

5. 观察新旧rabbitmq是否同步数据完成，当同步数据完成时，旧的queued messages数据为0

### 四、注意事项

1. 内存大小设置、插件配置均在configmap中，直接在腾讯云控制台进行修改即可。

2. 当configmap有修改时，可以通过控制台进行重启，但是由于有健康检查的存在，所以再重启的时候要逐一进行重启，即一个启动成功后再重启下一个，直至最后一个重启成功。











