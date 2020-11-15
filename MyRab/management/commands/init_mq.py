from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from MyRab.management.untils.Rabbitmqserver import RabbitmqClient
        # logger = Logger("init_mq")
        # logger.infolog("init_mq", "开始初始化Rabbitmq队列")
        print("init_mq", "开始初始化Rabbitmq队列")
        try:
            RabbitmqClient.connent()
            RabbitmqClient.channel.queue_declare(queue='send_result', durable=True)
            RabbitmqClient.channel.queue_declare(queue='backend', durable=True)
            RabbitmqClient.channel.queue_declare(queue='intelligent', durable=True)
            RabbitmqClient.channel.queue_declare(queue='resume', durable=True)
            # logger.infolog("init_mq", "初始化Rabbitmq队列成功")
            print("init_mq", "初始化Rabbitmq队列成功")
        except Exception as e:
            print("init_mq",e,"队列初始化失败")
            # logger.errlog("init_mq",e,"队列初始化失败")
