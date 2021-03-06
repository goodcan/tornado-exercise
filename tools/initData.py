#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/3/16 11:15
# @Author   : cancan
# @File     : initData.py
# @Function : 清理数据结构
from pymongo import MongoClient

from base.db.DBManger import DBManager

def get_connect_db(db_type=1):
    if db_type == 2:
        HOST = '122.152.192.158'
        PORT = 27017
    else:
        HOST = '127.0.0.1'
        PORT = 27017

    username = 'admin'
    password = 'szx0982'

    client = MongoClient(HOST, PORT)

    dbAuth = client.szx_admin
    dbAuth.authenticate(username, password)

    return client.szx_admin


def clearUserData():
    DBManager.init()

    db = DBManager.db

    total = db['users'].find()

    for each in total:
        del each['order']
        each.update({
            'orders': []
        })
        db['users'].update({'_id': each['_id']}, each)


def editUserPms():
    DBManager.init()

    db = DBManager.db

    total = db['users'].find()

    for each in total:
        pms = each['permissions']
        pms.update({
            'editOrderMorePara': 0
        })
        db['users'].update({'_id': each['_id']}, {'$set': {'permissions': pms}})


def removeUserOrders():
    DBManager.init()

    db = DBManager.db

    total = db['users'].find()

    for each in total:
        del each['orders']
        db['users'].update({'_id': each['_id']}, each)


def addOrderTitile():
    DBManager.init()

    db = DBManager.db

    orders = db['orders'].find()

    i = 1
    for order in orders:
        db['orders'].update(
            {'_id': order['_id']},
            {'$set': {'title': 'test' + str(i)}}
        )
        i += 1


def addOrderStamp():
    DBManager.init()

    db = DBManager.db

    orders = db['orders'].find()

    for order in orders:
        db['orders'].update(
            {'_id': order['_id']},
            {'$set': {
                'createTimeStamp': 0,
                'completeTimeStamp': 0,
                'paymentTimeStamp': 0,
            }}
        )

def addOrderPrice():
    DBManager.init()

    db = DBManager.db

    orders = db['orders'].find()

    for order in orders:
        db['orders'].update(
            {'_id': order['_id']},
            {'$set': {
                'expectNum': order['num'],
                'price': order['expectPrice'],
                'tax': 'preTax'
            }}
        )

def updateContacts():
    db = get_connect_db()

    contacts = db['options'].find_one({'_id': 2001}, {'contacts': 1})['contacts']

    for i, v in enumerate(contacts):
        v['realName'] = ''
        contacts[i] = v

    db['options'].update({'_id': 2001}, {'$set': {'contacts': contacts}})

def updateUsersAndOrders():
    updateData = {
        u'游戏': u'十字星信息服务',
        u'漫画': u'十字星文化创意'
    }
    db = get_connect_db()
    users = db['users'].find({})
    for user in users:
        if user.has_key('department'):
            user['company'] = updateData[user['department']]
            del user['department']
            db['users'].update({'_id': user['_id']}, user)

    orders = db['orders'].find({})
    for order in orders:
        if order.has_key('department'):
            order['company'] = updateData[order['department']]
            del order['department']
            db['orders'].update(
                {'_id': order['_id']}, order
            )

def updateUserPms():
    db = get_connect_db()
    users = db['users'].find({})
    for user in users:
        pms = user['permissions']
        pms['readCompanyOrder'] = pms['readDptOrder']
        pms['editCompanyOrder'] = pms['editDptOrder']
        del pms['readDptOrder']
        del pms['editDptOrder']
        db['users'].update({'_id': user['_id']}, {'$set': {'permissions': pms}})

if __name__ == "__main__":
    # updateUserPms()
    updateUsersAndOrders()
