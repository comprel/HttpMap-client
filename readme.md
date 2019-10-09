# NetMapClient

```
NetMap 客户端
提供http访问请求监听， 并将分析数据上报
```

部署：
1. 安装httpry
```
备注： 安装包参考doc/httpry.zip

yum install gcc make git libpcap-devel -y
下载源码包：
https://github.com/jbittel/httpry

make
make install

验证 httry -h
```

2. 初始化：
```
mkdir -p /usr/local/netmap
将源代码复制到/usr/local/netmap/
chmod +x /usr/local/netmap/manager
```

3. 启动sniffer
```
sh sniffer
或：
chmod +x  sniffer
./sniffer
```

4. 注册节点
/usr/local/netmap/manager register

5. 注册systemd service 服务
```
cp doc/netmap-client.service /usr/lib/systemd/system

chmod +x /usr/lib/systemd/system/netmap-client.service

systemctl daemon-reload
systemctl enable netmap-client.service
systemctl start netmap-client.service
```

其他：
1.节点下线， 取消注册：
```
/usr/local/netmap/manager unregister
```

备注：
```
由于sniffer会写入请求数据， 可能造成空间不足
建议设置定时任务将服务重启
```

