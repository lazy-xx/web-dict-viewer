#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui
import sys

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

class DisplayDict:
    def __init__(self, data:dict):
        #初始化data，即输入的dict
        self.data = data
        #搜索窗口默认打开dict的深度和标志位
        self.default_opened_depth = 0
        self.default_opened_depth_changed = False
        #搜索是否会展开whole窗口的tree_node
        self.is_search_open_tree_node = False
        #各窗口字体大小
        self.whole_window_font_scale = 1
        self.search_window_font_scale = 1
        self.watch_window_font_scale = 1
        #折叠、展开所有whole窗口树节点的标志位
        self.collapse_all_node_in_whole_window = False
        self.expand_all_node_in_whole_window =False
        #折叠、展开watch窗口树节点的标志位
        self.collapse_all_node_in_watch_window = False
        self.expand_all_node_in_watch_window = False
        #是否按下了定位以及需要定位的路径
        self.is_located = False
        self.need_locate_path = "" 
        #用来打开定位时折叠的tree_node节点，是定位路径拆分后的数组
        self.need_locate_path_split = []
        #保存需要高亮的数据的路径
        self.is_hl = {}
        #保存展开的tree_node节点的路径，设置TREE_NODE_FRAMED标志位       
        self.is_framed = {}
        #定位路径的缓存，下一次定位刷新
        self.located_hl_path_cache = ""
        #保留search窗口搜索记录的相关参数
        self.checkbox_enabled_last_state = []
        self.checkbox_enabled = []
        #颜色列表,绿蓝黄红
        self.color_list = [[0.18, 0.84, 0.451, 1.0],[0.118, 0.565, 1.0, 1.0],[0.976, 0.8, 0.141, 1.0],[1.0, 0.278, 0.34, 1.0]]
        #按下搜索后标志位设为True
        self.search_flag = False
        #当前查找的字符
        self.search_str = ""
        #whole_window的窗口数量、默认宽度、宽度数组
        self.whole_window_default_width = 500
        self.whole_window_width = self.whole_window_default_width
        #search窗口的信息，包含搜索到的数据。二维数组，每一个数组存储搜索到的数据的路径
        self.search_window_display_path_array = []
        #包含所有search窗口保留的字符串
        self.search_str_array = []
        #搜索的缓存字符串，如果没打勾再次进行搜索就删除search_str_array中的该字符串
        self.search_str_cache = ""
        #whole窗口的信息，包含了self.data内所有dict的打开情况。key值为路径，value值为是否展开
        self.whole_window_dict_open_status = {}
        self.set_whole_window_dict_open_status(data, False, "")
        #watch窗口的信息，包含使用者特别关注的数据。存储所有加入到watch窗口数据的路径
        self.watch_window_display_path_array = []
        #主窗口信息
        self.main_window_size = (0,0)
        self.main_window_pos = (0,0)
        self.main_scroll_y = 0
        #上一个子窗口的信息。用来动态计算下一个窗口的渲染位置
        self.last_child_window_size = (0,0)
        self.last_child_window_pos = (0,0)

    def show_window(self):
        is_expand, _ = imgui.begin("Dict Viewer", False)

        if is_expand:
            #获取主窗口的大小和位置
            self.main_window_size = imgui.get_window_size()
            self.main_window_pos = imgui.get_window_position() 
            self.main_scroll_y = imgui.get_scroll_y()
            #存储上一个子窗口的大小和位置，用来确定下一个窗口的渲染位置
            self.last_child_window_size = (0,0)
            self.last_child_window_pos = (0,0) 

            #第一排部件的显示
            self.button_collapse_all()
            imgui.same_line()
            self.button_expand_all()
            imgui.same_line()
            self.button_clear_all_hl()
            imgui.same_line()
            self.button_adjust_font_scale()
            imgui.same_line()
            self.checkbox_search_expand_dict()
            imgui.same_line()
            self.slider_default_open_depth()
             
            #一些样式调整
            var_num = 0
            color_num = 0
            imgui.push_style_var(imgui.STYLE_SCROLLBAR_SIZE, 10)
            var_num += 1
            imgui.push_style_color(imgui.COLOR_HEADER, 0.3, 0.3, 0.3, 1)
            color_num += 1
            imgui.push_style_color(imgui.COLOR_HEADER_HOVERED, 0.5, 0.5, 0.5, 1)
            color_num += 1
            #三个窗口的显示
            self.display_whole_window()
            imgui.set_next_window_position(self.last_child_window_pos[0] + self.last_child_window_size[0] + 5, self.last_child_window_pos[1])        
            #绘制search、watch窗口
            imgui.same_line(spacing = 0)
            #search\whole窗口的大小
            search_and_watch_window_size = (self.main_window_size[0] - imgui.get_cursor_position()[0] - 15, (self.last_child_window_size[1] - 5)/2)
            self.display_search_window(search_and_watch_window_size)
            self.display_watch_window(search_and_watch_window_size)
            imgui.pop_style_var(var_num)
            imgui.pop_style_color(color_num)
        imgui.end()
    
    def button_collapse_all(self):
        #按钮按下折叠whole窗口所有tree_node
        if imgui.button("CollapseAll"):
            self.collapse_all_tree_node(self.data)
            self.collapse_all_node_in_whole_window = True
        if imgui.is_item_hovered():
            imgui.set_tooltip("Close all nodes in the whole window")

    def button_expand_all(self):
        #按钮按下展开whole窗口所有tree_node
        if imgui.button("ExpandAll"):
            self.expand_all_tree_node(self.data)
            self.expand_all_node_in_whole_window = True
        if imgui.is_item_hovered():
            imgui.set_tooltip("Open all nodes in the whole window")

    def button_clear_all_hl(self):
        #按钮按下清空所有高亮
        if imgui.button("TurnOffAllHL"):
            self.is_hl.clear()
        if imgui.is_item_hovered():
            imgui.set_tooltip("Turn off all highlighting")

    def button_adjust_font_scale(self):
        #按下按钮弹出字体调节的窗口
        if imgui.button("AdjustFontSize"):
            imgui.open_popup('FontSize')
        if imgui.begin_popup_context_item('FontSize'):
            if imgui.button("Reset"):
                self.whole_window_font_scale = 1
                self.search_window_font_scale = 1
                self.watch_window_font_scale = 1
            #调节字体大小
            clicked, self.whole_window_font_scale = imgui.slider_float(
                label="WholeWindowFontSize",
                value=self.whole_window_font_scale,
                min_value=0.9,
                max_value=2.0,
                format="%3.2f",
            )
            #调节字体大小
            clicked, self.search_window_font_scale = imgui.slider_float(
                label="SearchWindowFontSize",
                value=self.search_window_font_scale,
                min_value=0.9,
                max_value=2.0,
                format="%3.2f",
            )
            #调节字体大小
            clicked, self.watch_window_font_scale = imgui.slider_float(
                label="WatchWindowFontSize",
                value=self.watch_window_font_scale,
                min_value=0.9,
                max_value=2.0,
                format="%3.2f",
            )
            imgui.end_popup() 

    def checkbox_search_expand_dict(self): 
        #是否打开搜索展开所有搜索到的tree_node节点功能
        _, self.is_search_open_tree_node = imgui.checkbox(
            "SearchOpen", self.is_search_open_tree_node,
        )
        if imgui.is_item_hovered():
            imgui.set_tooltip("Search Expands all the searched tree nodes in the whole window")

    def slider_default_open_depth(self):
        #调整search窗搜索默认展开几层dict
        imgui.set_next_item_width(3 * imgui.get_frame_height())
        self.default_opened_depth_changed, self.default_opened_depth = imgui.slider_int(
            "Depth", self.default_opened_depth,
            min_value=0, max_value=2,
            format="%d"
        )
        if imgui.is_item_hovered():
            imgui.set_tooltip("Adjust how many dict layers are expanded by default in the search window")

    def display_whole_window(self):
        #绘制whole窗口            
        #外层窗口，使得窗口宽度控件始终位于窗口顶部
        with imgui.begin_child("whole", self.whole_window_width, self.main_window_size[1] + self.main_scroll_y - 25 - imgui.get_cursor_position().y, border=True):
            self.last_child_window_size = imgui.get_window_size()
            self.last_child_window_pos = imgui.get_window_position()
            imgui.push_item_width(200)
            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (4, 0))
            clicked, self.whole_window_width = imgui.slider_float(
                label="Width##whole",
                value=self.whole_window_width,
                min_value=50,
                max_value=800,
                format="%.0f",
            )
            imgui.separator()
            imgui.pop_item_width()
            imgui.pop_style_var(1)
            #子窗口，渲染dict树结构
            with imgui.begin_child("dict", width = self.whole_window_width - 10, border=False, flags = imgui.WINDOW_ALWAYS_HORIZONTAL_SCROLLBAR):
                imgui.set_window_font_scale(self.whole_window_font_scale)
                if True:
                    self.display_whole_content(self.data, "", 0) 
                    self.search_flag = False   
                    self.expand_all_node_in_whole_window = False
                    self.collapse_all_node_in_whole_window = False
    
    def display_search_window(self, size):
        #外层窗口使得搜索栏始终在窗口顶部
        with imgui.begin_child("SearchWindow", size[0], size[1], border=True):
            self.last_child_window_size = imgui.get_window_size()
            self.last_child_window_pos = imgui.get_window_position()
            #输入框
            changed, self.search_str = imgui.input_text(
                label="", value=self.search_str, buffer_length=400
            )
            imgui.same_line()
            #搜索按钮
            self.button_search()
            imgui.separator()
            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (4, 0))
            #子窗口渲染搜索到的结果
            with imgui.begin_child("search_context", width = size[0] - 12, border=False, flags = imgui.WINDOW_ALWAYS_HORIZONTAL_SCROLLBAR):
                imgui.set_window_font_scale(self.search_window_font_scale)
                #所有搜索的字符串列表，每个搜索记录放在一个collapsing_header中
                self.header_all_search_item()
            imgui.pop_style_var(1)
            imgui.set_next_window_position(self.last_child_window_pos[0], self.last_child_window_pos[1] + self.last_child_window_size[1] + 5) 

    def button_search(self):
        #按钮按下 or 按下回车查询
        if imgui.small_button("Search") or imgui.is_key_pressed(imgui.get_key_index(imgui.KEY_ENTER)):
            imgui.core.set_keyboard_focus_here(-1)
            if self.search_str == "":
                pass
            else:
                self.search_flag = True
                if self.is_search_open_tree_node == True:
                    self.update_whole_window_dict_open_status(self.data, self.search_str, "")
                #移除缓存
                if self.search_str_cache != "":
                    del self.checkbox_enabled[-1]
                    del self.checkbox_enabled_last_state[-1]
                    del self.search_window_display_path_array[-1]
                    del self.search_str_array[-1] 
                    self.search_str_cache = ""
                if not self.search_str in self.search_str_array:
                    #设置缓存
                    self.search_str_cache = self.search_str
                    self.checkbox_enabled.append(False)
                    self.checkbox_enabled_last_state.append(False)
                    self.search_str_array.append(self.search_str)
                    self.search_window_display_path_array.append([])
                    self.update_search_window_display_path_array(self.data, self.search_str,"")
                    pass

    def header_all_search_item(self):
        #所有搜索的字符串列表，每个搜索记录放在一个collapsing_header中
        i, length = 0, len(self.search_str_array)
        while i < length:
            self.checkbox_enabled_last_state[i] = self.checkbox_enabled[i]
            _, self.checkbox_enabled[i] = imgui.checkbox("##search_header" + str(i), self.checkbox_enabled[i])
            imgui.same_line()
            #绘制header控件
            color = self.color_list[i%3][:3]
            imgui.push_style_color(imgui.COLOR_HEADER, *color, 0.6)
            imgui.push_style_color(imgui.COLOR_HEADER_HOVERED, *color, 0.8)   
            imgui.push_style_color(imgui.COLOR_HEADER_ACTIVE, *color, 1)                     
            show, _ = imgui.collapsing_header(self.search_str_array[i], flags = imgui. TREE_NODE_DEFAULT_OPEN)
            imgui.pop_style_color(3)
            if show:
                self.display_search_content(self.search_window_display_path_array[i], self.search_str)  
            #如果玩家打勾checkbox，则清除搜索缓存，下一次搜索时不清除搜索记录；如果玩家取消勾checkbox，则删除该条搜索记录
            if self.checkbox_enabled_last_state[i] == True and self.checkbox_enabled[i] == False:
                del self.checkbox_enabled[i]
                del self.checkbox_enabled_last_state[i]
                del self.search_window_display_path_array[i]
                del self.search_str_array[i] 
                length -= 1
                self.search_str_cache = ""
                continue
            elif self.checkbox_enabled_last_state[i] == False and self.checkbox_enabled [i] == True:
                self.search_str_cache = ""
            i += 1

    def display_watch_window(self, size):
        #绘制watch窗口
        with imgui.begin_child("watch", size[0], size[1], border=True):
            #按钮按下折叠所有tree_node
            if imgui.button("CollapseAll"):
                self.search_flag = True
                self.collapse_all_node_in_watch_window = True
            if imgui.is_item_hovered():
                imgui.set_tooltip("Close all nodes in the watch window")
            imgui.same_line()
            #按钮按下展开所有tree_node
            if imgui.button("ExpandAll"):
                self.expand_all_node_in_watch_window = True
            if imgui.is_item_hovered():
                imgui.set_tooltip("Open all nodes in the watch window")
            imgui.same_line()
            #绘制居中文本
            self.text_centered_text("Watch Window")
            #子窗口绘制watch窗口里面的内容
            with imgui.begin_child("watch", width = size[0] - 10, border=False, flags = imgui.WINDOW_ALWAYS_HORIZONTAL_SCROLLBAR):
                imgui.set_window_font_scale(self.watch_window_font_scale)
                self.display_watch_content(self.watch_window_display_path_array) 
    
    def text_centered_text(self, text_str):
        #绘制“Watch Window"文本
        imgui.set_window_font_scale(1.2)
        text = text_str
        text_width, text_height = imgui.calc_text_size(text)
            # 计算文本的位置
        text_x = (self.last_child_window_size[0] - text_width) / 2
        text_y = imgui.get_cursor_pos()[1]
            # 在窗口中居中显示文本
        imgui.set_cursor_pos((text_x, text_y))
        imgui.text(text)
        imgui.separator()
        imgui.set_window_font_scale(1)

    #设置whole_window_dict_open_status
    def set_whole_window_dict_open_status(self, data : dict, true_or_false : bool, parent_key : str):
        for i in data.keys():
            path = parent_key + str(i)
            if(type(data[i]) == dict):
                self.whole_window_dict_open_status[path] = true_or_false
                self.set_whole_window_dict_open_status(data[i], true_or_false, path + '.')
            elif(type(data[i]) == list):
                self.whole_window_dict_open_status[path] = true_or_false
                for j, value in enumerate(data[i]):
                    self.set_whole_window_dict_open_status({str(j) : value}, False, path + '.')
            
    
    #更新whole树的展开情况，使搜索到的结果展开
    def update_whole_window_dict_open_status(self, data : dict, search_str : str, parent_key):
        if(self.search_str == ""):
            return
        child_opened_situation = False
        for i in data.keys():
            path = parent_key + str(i)
            if(type(data[i]) == dict):
                self.whole_window_dict_open_status[path] = False
                self.update_whole_window_dict_open_status(data[i], search_str, path + '.')
                child_opened_situation |= self.whole_window_dict_open_status[path]
            elif(type(data[i]) == list):
                self.whole_window_dict_open_status[path] = False
                for j, value in enumerate(data[i]):
                    self.update_whole_window_dict_open_status({str(j) : value}, search_str, path + '.')
                    child_opened_situation |= self.whole_window_dict_open_status[path]
            else:
                if search_str in str(data[i]):
                    child_opened_situation = True
                    continue
            if(search_str in str(i)):
                child_opened_situation = True
        if parent_key != "" and parent_key != None:
            self.whole_window_dict_open_status[parent_key[:-1]] |= child_opened_situation

    #search窗口搜索结果存储在search_window_display_path_array中
    def update_search_window_display_path_array(self, data : dict, search_str : str, parent_key):
        if(search_str == "" or search_str == None):
            return
        
        for i in data.keys(): 
            path = parent_key + str(i)
            if(type(data[i]) == dict):       
                self.update_search_window_display_path_array(data[i], search_str, path + '.')  
            elif(type(data[i]) == list):
                for j, value in enumerate(data[i]):
                    self.update_search_window_display_path_array({str(j) : value}, search_str, path + '.')  
            else:
                if self.search_str in str(data[i]) and path not in self.search_window_display_path_array[-1]:
                    self.search_window_display_path_array[-1].append(path)
                    continue
            if search_str in str(i) and path not in self.search_window_display_path_array[-1]:
                self.search_window_display_path_array[-1].append(path)

    #whole窗口内容的展示
    def display_whole_content(self, data : dict, parent_key, depth = 0):
        #遍历字典，遍历字典的键值对。
        for i in data.keys():
            path = parent_key + str(i)
            #如果字典的键值对是字典类型，则递归遍历该字典的键值对。
            if(type(data[i]) == dict or type(data[i]) == list):
                #判断tree_node节点是否需要展开
                if (self.search_flag == True and self.is_search_open_tree_node == True) or self.collapse_all_node_in_whole_window or self.expand_all_node_in_whole_window:
                        imgui.set_next_item_open(self.whole_window_dict_open_status[path] )
                if self.is_located == True:
                    if depth < len(self.need_locate_path_split) and str(i) == self.need_locate_path_split[depth]:
                        imgui.set_next_item_open(True)
                #绘制tree_node节点。定位变红，展开高亮
                imgui.unindent(7)
                imgui.push_style_color(imgui.COLOR_TEXT, *self.color_list[depth % 3])
                    #如果is_hl为True，则绘制tree_node节点的背景为红色；否则看是否展开，如果展开，绘制tree_node节点的背景为半透明白色。
                if self.is_hl.get(path, False) == True:
                    imgui.push_style_color(imgui.COLOR_HEADER, *self.color_list[3])
                    opened = self.is_framed[path] = imgui.tree_node(str(i), flags = imgui.TREE_NODE_FRAMED | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH)
                    imgui.pop_style_color(1)
                else:
                    opened = self.is_framed[path] = imgui.tree_node(str(i), flags = (imgui.TREE_NODE_FRAMED if self.is_framed.get(path, False) else 0) | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH)
                imgui.pop_style_color(1)
                imgui.indent(7)
                #右键事件，加入到watch窗口
                self.whole_window_right_click_event(path)
                #被定位后执行
                self.execute_if_located(path)
                #递归内部内容，同时tree_node弹栈
                if opened:
                    if type(data[i]) == dict:
                        self.display_whole_content(data[i], path + '.', depth + 1)    
                    elif type(data[i]) == list:
                        for j, value in enumerate(data[i]):
                            self.display_whole_content({str(j) : value}, path + '.', depth + 1)
                    imgui.tree_pop()
            else:  
                #绘制键值对文本
                self.draw_text_by_depth(str(i), str(data[i]), depth)
                #右键按下事件，加入到watch窗口
                self.whole_window_right_click_event(path)
                #被定位后执行
                self.execute_if_located(path)
                #鼠标悬浮或者需要绘制高亮后执行
                self.whole_execute_if_hoverd_or_hl(path, str(i), str(data[i]), depth)

    
    def whole_window_right_click_event(self, path):
        #右键按下事件，加入到watch窗口
        if imgui.begin_popup_context_item(path):
            changed_add, _ = imgui.selectable("Adds to the watch window")
            if changed_add and path not in self.watch_window_display_path_array:
                self.watch_window_display_path_array.append(path)
            imgui.end_popup()
    
    def execute_if_located(self, path):
        #当前路径的数据被定位后执行如下操作
        if self.is_located == True and self.need_locate_path == path:
            imgui.set_scroll_here_y()
            #将高亮缓存定位的路径关闭高亮
            if self.located_hl_path_cache != "":
                self.is_hl[self.located_hl_path_cache] = False
                self.located_hl_path_cache = ""
            #当前定位路径加入缓存
            self.located_hl_path_cache = path
            self.is_hl[path] = True
            self.is_located = False

    def draw_text_by_depth(self, key_text, data_text, depth):
        with imgui.begin_group():
            imgui.push_style_color(imgui.COLOR_TEXT, *self.color_list[depth % 3])
            imgui.text(key_text)
            imgui.pop_style_color(1)
            imgui.same_line(spacing = 0)
            imgui.text(" : " + data_text)

    def whole_execute_if_hoverd_or_hl(self, path, key_text, data_text, depth):
        #确定高亮颜色
        hl_color = (0.5,0.5,0.5,1)
        if self.located_hl_path_cache == path:
            hl_color = self.color_list[3]
        if imgui.is_item_hovered() or self.is_hl.get(path, False):
            hlpos = imgui.core.get_item_rect_min()
            hlsize = [imgui.core.get_item_rect_max()[0] - hlpos[0], imgui.core.get_item_rect_max()[1] - hlpos[1]]
            imgui.set_next_window_position(*hlpos)
            #绘制高亮以及重绘文本
            imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, *hl_color)
            with imgui.begin_child(path, width = hlsize[0], height = hlsize[1], flags = imgui.WINDOW_NO_MOUSE_INPUTS) :
                self.draw_text_by_depth(key_text, data_text, depth)
            imgui.pop_style_color(1)

    #search窗口内容的展示
    def display_search_content(self, path_array, search_str):
        #遍历路径数组，绘制获取到的路径下的dict
        for path in path_array[:]:
            path_value = self.get_value_form_path(path)
            if path_value == None:
                path_array.remove(path)
                continue
            self.display_search_or_watch_dict(1, {path : path_value}, "", 0, search_str)


    #watch窗口内容的展示
    def display_watch_content(self, path_array):
        #倒序，新添加的在最前面
        for path in reversed(path_array[:]):
            path_value = self.get_value_form_path(path)
            if path_value == None:
                path_array.remove(path)
                continue
            self.display_search_or_watch_dict(2, {path : path_value}, "", 0)
        self.expand_all_node_in_watch_window = False
        self.collapse_all_node_in_watch_window = False


    #绘制search窗口和watch窗口下的dict
    def display_search_or_watch_dict(self, search_or_watch_mode, path_data, parent_key : str, depth, search_str = None):
        for i in path_data.keys():
            path = parent_key + str(i)
            path_value = path_data[i]
            if(type(path_value) == dict or type(path_value) == list):
                imgui.unindent(7)
                #搜索或者调整self.default_opened_depth时会影响search_window的dict展开层数
                if search_or_watch_mode == 1 and (self.search_flag == True or self.default_opened_depth_changed == True):
                    if depth < self.default_opened_depth:
                        imgui.set_next_item_open(True)
                    else:
                        imgui.set_next_item_open(False)
                #search_or_watch_mode==2表示watch窗口，两个按钮会影响是否展开
                if search_or_watch_mode == 2:
                    if self.expand_all_node_in_watch_window == True:
                        imgui.set_next_item_open(True)
                    if self.collapse_all_node_in_watch_window == True:
                        imgui.set_next_item_open(False)
                #绘制tree_node节点
                changed, opened = self.path_tree_node_display(path, str(i), search_or_watch_mode, depth)
                imgui.indent(7)
                if changed and opened and search_or_watch_mode == 2:
                    imgui.tree_pop()   
                    continue
                if opened and type(path_value) == dict:
                    self.display_search_or_watch_dict(search_or_watch_mode, path_value, path + '.', depth + 1, search_str)
                    imgui.tree_pop()   
                elif opened and type(path_value) == list:
                    for j, value in enumerate(path_value):
                        self.display_search_or_watch_dict(search_or_watch_mode, {str(j) : value}, path + '.', depth + 1, search_str)
                    imgui.tree_pop()       
            else:
                #绘制带颜色、搜索红色的路径字符串
                hl_pos, hl_width, hl_height = self.path_text_display(str(i), str(path_value), search_str)
                #右键事件
                if search_or_watch_mode == 2 and depth == 0:
                    self.watch_window_right_click_event(path)
                else:
                    self.search_window_right_click_event(path)
                #悬浮时高光背景
                if imgui.is_item_hovered():
                    imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5, 1)
                    imgui.set_next_window_position(*hl_pos)
                    with imgui.begin_child(path, width = hl_width, height = hl_height, flags = imgui.WINDOW_NO_MOUSE_INPUTS) :
                        #绘制字符串
                        self.path_text_display(str(i), str(path_value), search_str)
                    imgui.pop_style_color(1)

    #路径树节点的显示
    def path_tree_node_display(self, path, text, window_flag, depth, flags = 0):
        nodes = text.split('.')
        opened = imgui.tree_node('##' + str(path), flags = flags | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH)
        changed = False
        if window_flag == 2 and depth == 0:
            changed = self.watch_window_right_click_event(path)
        else:
            self.search_window_right_click_event(path)
        imgui.same_line()
        for i, node in enumerate(nodes):
            imgui.push_style_color(imgui.COLOR_TEXT, *self.color_list[i % 3])
            imgui.text(node)
            if i < len(nodes) - 1:
                imgui.same_line(spacing = 0)
                imgui.text(".")
                imgui.same_line(spacing = 0)
            imgui.pop_style_color(1)
        
        return changed, opened

    def search_window_right_click_event(self, path : str):
        #右键按下事件，加入到watch窗口、定位
        if imgui.begin_popup_context_item(path):
            #添加到watch窗口
            changed_add, _ = imgui.selectable("Adds to the watch window")
            if changed_add and path not in self.watch_window_display_path_array:
                self.watch_window_display_path_array.append(path)
            #定位
            changed_locate, _ = imgui.selectable("Locate in the dict tree")
            if changed_locate:
                self.is_located = True
                self.need_locate_path = path
                self.need_locate_path_split = path.split('.')
                pass
            imgui.end_popup()

    def watch_window_right_click_event(self, path : str):
        #右键移除
        if imgui.begin_popup_context_item(path):
            #移除
            changed, _ = imgui.selectable("Remove")
            if changed:
                self.watch_window_display_path_array = [x for x in self.watch_window_display_path_array if x != path]
            #定位
            changed_locate, _ = imgui.selectable("Locate in the dict tree")
            if changed_locate:
                self.is_located = True
                self.need_locate_path = path
                self.need_locate_path_split = path.split('.')
                pass
            imgui.end_popup()
            return changed

    def get_value_form_path(self, path : str):
        data = self.data
        nodes = path.split('.')
        for node in nodes:
            if type(data) == dict:
                if(data.get(str(node)) != None):
                    data = data[node]
                else:
                    try:
                        node_int = int(node)
                        if data.get(int(node))!= None:
                            data = data[node_int]
                            continue
                        node_float = float(node)
                        if data.get(float(node)) != None:
                            data = data[node_float]
                            continue
                        return None
                    except:
                        return None
            elif type(data) == list:
                if(int(node) < len(data)):
                    data = data[int(node)]
                else:
                    return None
        return data
        
    #路径文本的显示，返回该文本的位置、宽高
    def path_text_display(self, key : str, value : str, search_str = None) -> float:
        with imgui.begin_group():
            imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (1, 4))
            str_list = key.split(".")
            for i, s in enumerate(str_list):
                color_index = i%3
                if(i == len(str_list) - 1):
                    if search_str != None and search_str in s:
                        color_index = 3
                    imgui.push_style_color(imgui.COLOR_TEXT, *self.color_list[color_index])
                    imgui.text(s)
                else:
                    imgui.push_style_color(imgui.COLOR_TEXT, *self.color_list[color_index])
                    imgui.text(s + '.')
                imgui.same_line()
                imgui.pop_style_color(1)
            imgui.pop_style_var(1)

            imgui.same_line(spacing = 1)
            imgui.text(' : ')
            imgui.same_line(spacing = 1)
            if search_str != None and search_str in str(value):
                imgui.push_style_color(imgui.COLOR_TEXT, *self.color_list[3])
                imgui.text(str(value))
                imgui.pop_style_color(1)
            else:
                imgui.text(str(value))
        origin_pos = [0,0]
        text_width = 0
        text_height = 0
        origin_pos[0] = imgui.get_item_rect_min().x
        origin_pos[1] = imgui.get_item_rect_min().y
        text_width = imgui.get_item_rect_size().x
        text_height = imgui.get_item_rect_size().y
        return origin_pos, text_width, text_height

            
    #折叠所有字典节点
    def collapse_all_tree_node(self, data : dict):       
        self.set_whole_window_dict_open_status(data, False, "")
    
    #设置self.whole_window_dict_open_status，设置全为True。
    def expand_all_tree_node(self, data):
        self.set_whole_window_dict_open_status(data, True, "")
    


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window

#参数1为传入字典，随机化该字典；参数2为随机化字典的深度，深度高于5则不再产生子字典
#计数器
count = 0
def init_random_dict(data, depth):
    global count
    #字典元素个数
    item_num = 0
    match depth:
        case 0:
            item_num = random.randint(100, 300)
        case 1:
            item_num = random.randint(10, 20)
        case 2:
            item_num = random.randint(10, 20)
        case 3:
            item_num = random.randint(10, 20)
        case 4:
            item_num = random.randint(5, 10)
    for i in range(item_num):
        match random.randint(0,2):
            case 0:
                data.update({"val" + str(count) :random.randint(0,1000)})
                count = count + 1
            case 1:
                data.update({"str" + str(count) :"string"})   
                count = count + 1
            case 2:
                if depth < 5:
                    dict = {}
                    data.update({"dict" + str(count) : init_random_dict(dict, depth + 1)})
                    count = count + 1
    print(count)
    return data

#基于glfw展示dict查看器
use_test_sample = False
opened = True
def display(data : dict):
    global use_test_sample, opened
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    show_custom_window = True
    io = imgui.get_io()

    new_font = io.fonts.add_font_from_file_ttf("examples/Final/Sources/Fonts/Roboto-Regular.ttf", 20)
    impl.refresh_font_texture()

    displayDict = DisplayDict(data)
    start_time = time.time()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()
        #dict查看器
        if show_custom_window:
            with imgui.font(new_font):
                displayDict.show_window()
            if opened:
                is_expand, opened = imgui.begin("Whether to use test sample", True)
                if is_expand:
                    _, use_test_sample = imgui.checkbox("use test sample", use_test_sample)
                    imgui.end()
            else:
                use_test_sample = False
            if use_test_sample:
                displayDict.data = dataini
            else:
                displayDict.data = data
            

        gl.glClearColor(1.0, 1.0, 1.0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

        end_time = time.time()
        if use_test_sample:
            test_sample(end_time - start_time)
        start_time = end_time


    impl.shutdown()
    glfw.terminate()

#用来测试数据随时间变化的函数
timer = 0
minitimer = 0
big_timer = 0
def test_sample(delay):
    global timer, minitimer, big_timer
    timer += delay
    minitimer += delay
    big_timer += delay
    dataini['time'] = round(timer,2)
    if minitimer > 0.5:
        minitimer = 0
        dataini["fps"] += random.randint(-10, +10) + random.randint(0,100)/100
        dataini["fps"] = round(dataini["fps"], 2)
    if big_timer > 2:
        big_timer = 0
        dataini['other_attr']['other_attr1'] = big_timer
        dataini["hp_list"] = [round(x + 1 + random.randint(0,100)/100,2) for x in dataini["hp_list"]] 

#debug的函数，无实际作用
def debugger():
    imgui.set_next_item_open(True)
    imgui.set_next_item_open(True)
    opened1 = imgui.tree_node('1')
    if opened1:
        imgui.text_ansi('\033[31m' + '1' + '\033[0m ')
        imgui.tree_pop()
    opened2 = imgui.tree_node('2')
    if opened2:
        imgui.text_ansi('\033[31m' + '2' + '\033[0m ')
        imgui.tree_pop()

if __name__ == "__main__":
    import os
    print(os.getcwd())
    with open("examples/Final/Sources/Texts/data.txt", "r") as f:
        my_dict = eval(f.read())
    if use_test_sample:
        display(dataini)
    else:
        display(my_dict)