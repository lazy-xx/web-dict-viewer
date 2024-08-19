#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import multiprocessing
import time
import traceback
import imgui

import websockets
import PyWS as pw
from drawwindows import DisplayDict, show_test_window

dataini = {
    'uid': 10001,
    'name': "test",
    'time': 0,
    'fps': 60,
    'hp_list': [1,2,3,4,5],
    'dir_list':[{'hp':100}, {'nihao':200}],
    'hp': 100,
    'other_attr': {
        'other_attr1':100,
        'other_attr2':200,
        'other_inform': {
            'other_inform1': 100,
            'other_inform2': 200,
            'other_inform3': 300,
        },
    },
    'other_att': {
        'other_attr1':40,
        'other_attr2':30,
        'other_inform': {
            'other_inform1': 100,
            'other_inform2': 200,
            'other_inform3': 300,
        },
        'other_inform': {
            'other_hp': {
                'other_hp1': 100,
                'other_hp2': 100
            },
            'other_inform1': 100,
            'other_inform2': 200,
            'other_inform3': 400,
        },
    }
}

use_test_sample = False
def main(window_width, window_height):
    global dataini
    global use_test_sample

    #imgui的一些配置
    imgui.create_context()
    io = imgui.get_io()
    #io.mouse_draw_cursor = True
    imgui.style_colors_dark()
    imgui.get_style().anti_aliased_fill = False
    imgui.get_style().anti_aliased_lines = False
    imgui.get_style().window_rounding = 0.0
    imgui.get_style().scrollbar_rounding = 0.0
    new_font = io.fonts.add_font_from_file_ttf("examples/Final/Sources/Fonts/Roboto-Regular.ttf", 20)
    io.display_size = 1920, 1080

    #imgui-ws的初始化，参数为端口号、html文件所在文件夹、imgui上下文指针
    a = pw.PyDraw(5000, "/home/lazybox/imgui-ws/examples/Final", imgui.get_current_context().ptr)
    width, height, pixels = io.fonts.get_tex_data_as_alpha8()
    a.PrepareFontTexture(width, height, pixels)

    #读取data文件或者使用dataini变量
    import os
    with open("examples/Final/Sources/Texts/data.txt", "r") as f:
        my_dict = eval(f.read())
    if use_test_sample:
        displayDict = DisplayDict(dataini)
    else:
        displayDict = DisplayDict(my_dict)

    timer = 0
    start_time = time.time()  # 获取当前时间
    end_time = start_time

    
    while True:
        #imgui-ws的事件处理
        a.EventHandling(imgui.get_time())
        io.delta_time = a.GetDeltaTime()

        #绘制逻辑
        imgui.new_frame() 

        with imgui.font(new_font):
            imgui.set_next_window_size(window_width.value, window_height.value)
            imgui.set_next_window_position(0,0)
            displayDict.show_window()

            end_time = time.time()
            timer += end_time - start_time
            start_time = end_time
            displayDict.data['mvp_uid'] = timer
            

        imgui.render()

        #发送drawdata至imgui-ws
        a.SetDrawData(imgui.get_draw_data().ptr)

        #当没有客户端访问网页时节省cpu
        a.Wait()
    
    imgui.destroy_context()
    sock.close()

#异步接收网页端的宽高数据，用来设置窗口的大小
async def get_size(websocket, path, window_width, window_height):
    async for message in websocket:
        try:
            data = json.loads(message)
            # 处理收到的大小信息 
            window_width.value = data['width']
            window_height.value = data['height']
            print("rec: " + str(window_width.value) + ' ' + str(window_height.value))
            ## 发送响应
            #await websocket.send('Received size: {} x {}'.format(width, height))
        except Exception as e:
            print('Exception:', e)
            print('Traceback:', traceback.format_exc())

# 启动 WebSocket 服务器，不断执行函数get_size，端口默认8000
def start_servers(window_width, window_height):
    #端口改为服务器ip地址
    #server1 = websockets.serve(lambda websocket, path: get_size(websocket, path, window_width, window_height), '192.168.56.101', 8000)
    server1 = websockets.serve(lambda websocket, path: get_size(websocket, path, window_width, window_height), 'localhost', 8000)
    asyncio.get_event_loop().run_until_complete(server1)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    #多线程共享数据
    window_width = multiprocessing.Value('i', 1200)
    window_height = multiprocessing.Value('i', 800)
    
    #p1进程接收网页的宽高并设置对应数据，p2进程负责绘制窗口
    p1 = multiprocessing.Process(target=start_servers, args=(window_width,window_height))
    p2 = multiprocessing.Process(target=main, args=(window_width,window_height))
    
    p1.start()
    p2.start()
