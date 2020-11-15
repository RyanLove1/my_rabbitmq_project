import json

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from MyRab.management.untils.Rabbitmqserver import RabbitmqClient
from MyRab.models import Student, MyClass
from MyRab.serializers import TestRabbitmqSer, MyClassSer
import logging

logger = logging.getLogger('django')


class TestRabbitmq(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = TestRabbitmqSer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print(type(data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 将数据发送到rabbitmq消息队列
        student_mq(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# 班级消息队列
def sendtoparse_one(data):
    data = json.dumps(data)
    # rabbitmq
    # logger.info("AduitOneParseView", "开始发送消息到算法端:data:{}".format(str(data)))
    RabbitmqClient.connent()
    RabbitmqClient.productMessage("intelligent", data)
    # 发送消息通知算法端解析
    # logger.info("AduitOneParseView", "文件发送完成")
    print("AduitOneParseView", "文件发送完成")

# 学生消息队列
def student_mq(data):
    data = json.dumps(data)
    # rabbitmq
    # logger.info("AduitOneParseView", "开始发送消息到算法端")
    RabbitmqClient.connent()
    RabbitmqClient.productMessage("send_result", data)
    # 发送消息通知算法端解析
    # logger.info("AduitOneParseView", "文件发送完成")
    print("AduitOneParseView", "文件发送完成")


class ClassViewSet(viewsets.ModelViewSet):
    queryset = MyClass.objects.all()
    serializer_class = MyClassSer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print(type(data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 将数据发送到rabbitmq消息队列
        sendtoparse_one(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)