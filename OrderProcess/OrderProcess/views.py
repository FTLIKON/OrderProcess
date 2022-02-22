# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.views.decorators import csrf
from dbModel.models import orders
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# 接收POST请求数据


@csrf_exempt
def add(request):

    try:

        data = eval(bytes.decode(request.body))
        print(data["orderId"])
        orderId = data["orderId"]
        orderTime = data["orderTime"]
        skuId = data["skuId"]
        userId = data["userId"]
        status = data["status"]
        price = data["price"]
        pay = data["pay"]
        if orders.objects.filter(orderId=orderId):
            orders.objects.filter(orderId=orderId).update(orderTime=orderTime, skuId=skuId, userId=userId, status=status, price=price, pay=pay)
            message = {"data": {}, "succeed": True, "msg": "已存在orderId={}的订单，订单数据修改成功！，当前订单数：{}".format(orderId, len(orders.objects.all()))}
        else:
            neworder = orders(orderId=orderId, orderTime=orderTime, skuId=skuId, userId=userId, status=status, price=price, pay=pay)
            neworder.save()
            message = {"data": {}, "succeed": True, "msg": "新增订单数据成功，当前订单数：{}".format(len(orders.objects.all()))}
    except Exception as e:
        message = {"data": {}, "succeed": False, "msg": "您的请求提交不正确或提交格式错误，请检查！"}

    return HttpResponse(json.dumps(message, ensure_ascii=False))


def user_orders(request):

    try:
        userId = request.GET['userId']
        orderlist = orders.objects.filter(userId=userId)
        user_order = []
        for data in orderlist:
            user_order.append({"orderId": data.orderId,
                               "orderTime": data.orderTime,
                               "skuId": data.skuId,
                               "userId": data.userId,
                               "status": data.status,
                               "price": data.price,
                               "pay": data.pay})

        message = {"data": {"user_orders":user_order}, "succeed": True, "msg": "已成功查询到用户订单数量：{}".format(len(user_order))}
    except Exception as e:
        message = {"data": {}, "succeed": False, "msg": "您的请求提交不正确或提交格式错误，请检查！"}

    return HttpResponse(json.dumps(message, ensure_ascii=False))

def pay_rate(request):

    try:
        skuId = request.GET['skuId']
        orderlist = orders.objects.filter(skuId=skuId)
        order_num = len(orderlist)
        pay_num = 0
        for data in orderlist:
            if data.status == 1:
                pay_num += 1
        if order_num == 0:
            message = {"data": {}, "succeed": False, "msg": "未查询到该skuId"}    
        else:
            payrate = float(pay_num)/float(order_num)
            message = {"data": {"skuId":skuId,"order_num":order_num,"pay_num":pay_num,"pay_rate":payrate}, "succeed": True, "msg": "已成功查询到skuId={}的订单共有{}个，其中已付款{}个，实际付款率为{}（付款数/订单总数）".format(skuId,order_num,pay_num,payrate)}
    except Exception as e:
        message = {"data": {}, "succeed": False, "msg": "您的请求提交不正确或提交格式错误，请检查！"}

    return HttpResponse(json.dumps(message, ensure_ascii=False))

def get_top(request):

    try:
        starttime = int(request.GET['starttime'])
        endtime = int(request.GET['endtime'])
        print(starttime,endtime)
        orderlist = []
        for data in orders.objects.all():
            if data.orderTime >= starttime and data.orderTime <= endtime:
                orderlist.append(data)
        
        sku_done = {}
        for order in orderlist:
            if order.status == 1:
                try:
                    sku_done[str(order.skuId)] += 1
                except Exception as e:
                    sku_done[str(order.skuId)] = 1

        print(sku_done)

        topsku = []

        for obj in sorted(sku_done.items(), key = lambda kv:(kv[1], kv[0])):
            topsku.append(obj[0])
        print(topsku)


        message = {"data": {"top10_skuId":topsku[:10]}, "succeed": True, "msg": "已成功获取并分析从{}到{}的共{}个订单，共{}个成交的skuId，已按正序已列出成交额top10的skuId.".format(starttime,endtime,len(orderlist),len(topsku))}
        
    except Exception as e:
        message = {"data": {}, "succeed": False, "msg": "您的请求提交不正确或提交格式错误，请检查！"}

    return HttpResponse(json.dumps(message, ensure_ascii=False))

def test(request):
    # return HttpResponse("good")
    print("len", len(orders.objects.all()))
    list = orders.objects.all()
    for obj in list:
        print(str(obj.orderId)+"\t"+str(obj.orderTime)+"\t"+str(obj.skuId)+"\t"+str(obj.userId)+"\t"+str(obj.status)+"\t"+str(obj.price)+"\t"+str(obj.pay))
    return HttpResponse("test")


def deltest(request):
    orders.objects.all().delete()
    print("len", len(orders.objects.all()))
    return HttpResponse(str("删除完成"))
