# k8s搭建rabbitmq3.8.2集群rabbitmq-cluster-k8s-Imageversion
### 一、创建nfs-statfullset存储
1. 在nfs共享目录中创建对应的数据写入目录并赋予777权限

```
# cd /opt/nfs-data/stroageclass
# mkdir -p rabbitmq
# chmod 777 -R rabbimq
```
2. 创建rbac
   kubectl apply -f rbac.yml（注意以下截图中红框部分要做出对应的修改，name请定义一个唯一值，namespace是对应的命名空间）
   
3. 创建deployment
   kubectl apply -f deployment.yml（注意以下截图中红框部分要做出对应的修改，name请和rbac中的name保持一致，namespace是对应的命名空间，数据目录请确保修改正确）

4. 创建class

   kubectl apply -f class.yml（注意以下截图中红框部分要做出对应的修改，name请和rbac中的name保持一致，namespace是对应的命名空间）


