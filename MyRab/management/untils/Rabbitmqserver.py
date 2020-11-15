import pika
import sys
import time

if __name__ != '__main__':  # 测试服务是否能启动时使用
    from django.conf import settings


class RabbitmqServer(object):
    def __init__(self, username, password, serverip, port):
        self.username = username
        self.password = password
        self.serverip = serverip
        self.port = port

    def connent(self):
        user_pwd = pika.PlainCredentials(self.username, self.password)
        s_conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.serverip, port=self.port, credentials=user_pwd))  # 创建连接
        self.channel = s_conn.channel()

    def productMessage(self, queuename, message):
        self.channel.queue_declare(queue=queuename, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=queuename,  # 写明将消息发送给队列queuename
                                   body=message,  # 要发送的消息
                                   properties=pika.BasicProperties(delivery_mode=2, )
                                   # 设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
                                   )

    def expense(self, queuename, func):
        """
        :param queuename: 消息队列名称
        :param func: 要回调的方法名
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(auto_ack=False,  # 设置为应答（也就是必须处理完了，才将数据从队列里面删除）
                                   on_message_callback=func,
                                   queue=queuename,
                                   )
        self.channel.start_consuming()


def callback(ch, method, properties, body):
    print(" [消费者] Received %r" % body)
    time.sleep(1)
    print(" [消费者] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 接收到消息后会给rabbitmq发送一个确认


if __name__ != '__main__':
    username = settings.RABBITMQCONFIG.get("username")
    password = settings.RABBITMQCONFIG.get("password")
    severip = settings.RABBITMQCONFIG.get("host")
    port = settings.RABBITMQCONFIG.get("port")
    RabbitmqClient = RabbitmqServer(username, password, severip, port)

if __name__ == '__main__':
    import json

    RabbitmqClient = RabbitmqServer("admin", "admin", "39.106.1.89", 5672)
    RabbitmqClient.connent()
    data = {"code": 3}
    RabbitmqClient.productMessage("test3", json.dumps(data))
    RabbitmqClient.expense("test3", callback)
