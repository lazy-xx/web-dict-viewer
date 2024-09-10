# Web：pyimgui文档

因为前面用pyimgui实现过一些可用工具，发现仅仅是可执行文件的灵活性还不是很好，所以有了将pyimui工具移植到网页端的需求，下面是这一段时间研究的一个可行解决方案：
关于项目

本项目fork自[imgui-ws](https://github.com/ggerganov/imgui-ws)项目，imgui-ws基于imgui和incppect实现了将Dear ImGui场景通过发送DrawData结构（Dear imgui内置数据结构）流式传输到多个WebSocket客户端，然后使用 WebGL 在浏览器中呈现该结构。
本项目基于linux通过pybind11将imgui-ws的web通信部分代码打包成动态链接库，开发者可在编写pyimgui的py代码中导入该包，并合适地调用包内的函数即可实现pyimgui工具移植到网页端

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%871.png?inline=false)

## 项目关键目录介绍

标红文件为关键文件，其中：

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%872.png?inline=false)

- PyWS.cpython-310-x86_64-linux-gnu.so：通过pybind11将PyWS.cpp导出成的动态链接库。生成位置为build\examples\路径下。py文件导包时需要和二者需要放到同一目录下
- PyWS.cpp：imgui与web互相传输信息的代码，同时使用pybind11进行类和函数的绑定。打包成动态链接库后，py导包后可以直接调用绑定了的函数
- draw.py：UI逻辑的编写代码。与常规的pyimgui代码不同的地方在于不需要考虑渲染后端的实现，只需要每帧将绘制数据通过PyWS内置的函数发送到web即可
- index.html：网页部分的代码，进行通信初始化和绘制一些网页元素。代码大部分基于imgui-ws的代码改写而来，可以查看examples\demo-null文件夹下的index.html文件进行对比。
- DLLs下的动态链接库：pyimgui的动态链接库。后续会介绍如何使用
- CMakeList包含了PyWS.cpp通过pybind11打包成动态链接库的代码

## 使用流程
### 构建和运行示例样例
1. git clone 仓库地址

2. 将DLLs下的两个pyimgui动态链接库替换掉原本的库（可以在python文件里通过ctrl + 鼠标左键点击import imgui代码跳转到imgui库的地方进行替换，通常位于/home/用户名/.local/lib/python3.10/site-packages/imgui）

3. 命令行构建和运行：

        (1) cd 项目文件夹 && mkdir build && cd build

        (2) cmake ..

        (3) make

        (4) 进入到项目文件夹下执行python3 ./examples/Final/draw.py可以运行示例样例

        (5) 默认端口为localhost:5000，进入网页进行查看

4. 或者可以基于vscode使用cmake进行项目管理，构建和运行均在ide中操作

5. build后产生的PyWS.cpython-310-x86_64-linux-gnu.so文件存储于build\examples\路径下

### 构建和运行自己的样例

最简单的方法是基于Final文件夹下的文件进行个人开发。如果想自己构建文件夹，见如下流程：

1. 构建项目和运行示例样例，跑通后执行后续开发

2. 个人项目文件夹（类似Final文件夹）最好置于examples文件夹下，要想迁移文件夹需要自行修改CMakeList和某些库的位置

3. 创建自己的文件夹，文件夹下需要有index.html文件（命名需要一样，或者可以修改PyWS.cpp中PyDraw类的构造函数并重新build），还需要有PyWS.cpython-310-x86_64-linux-gnu.so动态链接库

4. 编辑自己的pyimgui代码和index.html代码。PyWS模块的使用可以查看draw.py进行查看

## 项目详细介绍
### 实现方案
下图是一个draw.py代码运行的流程图：

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%873.png?inline=false)

**前提**：imgui-ws基于incppect实现了cpp端到web端的数据传输，同时额外实现了web端GUI 界面的创建和显示 。核心函数就是imguiWS.setDrawData(data)进行UI绘制。能够将py代码的drawdata传递给cpp,这个问题就解决大半

**方案**：

1. 修改pyimgui的部分代码并重新编译成动态链接库，替换原有py的imgui库。该操作可以在py中获取到DrawData的地址信息（无符号整形）

2. 将imgui-ws的与web通信部分封装成类，并修改io处理相关代码，使用pybind11绑定该类并打包成动态链接库，供py代码导入并调用imgui-ws内的函数（imgui中io信息是来自于第三方窗口库的，例如glfw。imgui为glfw、opengl、sdl2等第三方库编写对接代码，以便第三方库接收按键事件后修改imgui的io信息）

3. 基于1 2步可以将DrawData地址信息传参到cpp代码进行强转，并调用imgui-ws的setDrawData函数将绘制信息传递给web端进行绘制

**遇到的问题及解决方案**

因为pyimgui底层封装的imgui的版本和imgui-ws底层的imgui版本有差异，前者更低，导致ImGuiContext的格式有差异（主要集中于io方面），这导致了py传递的指针进行强转时出错。（ImGuiContext 是 ImGui 库中的一个结构体，每个 Dear ImGui 应用程序都需要一个上下文，用于存储 ImGui 库的状态和数据。例如ImGuiContext数据就存储当前帧的DrawData和io信息）

**解决方案有如下两种，选择了后者**：

1. 升级pyimgui的imgui版本（需要diff两个版本，使用cython全部包装一遍）

2. 降低imgui-ws的imgui版本，修改pyimgui中部分宏，同时降级PyWS中处理io逻辑的代码

## 详细代码实现

### 修改pyimgui使py可以获取指针参数

pyimgui基于cython和imgui库实现，底层通过cython包装imgui库的函数和类成python中可以访问的形式来调取cpp代码中的函数和类。下面是代码的修改，位于third-party/pyimgui/imgui/core.pyx：

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%874.png?inline=false)

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%875.png?inline=false)

1. 将指针转化为无符号整形指针，暴露一个属性接口使得python代码中可以获取到该指针
2. 使用python setup.py build_ext --inplace重新将pyimgui项目编译成动态链接库，替换原有的库
3. py代码导包后可以直接获取对应实例的指针，然后将其传递给cpp函数进行强转

### PyDraw的实现

PyDraw这个类会`通过pybind11进行包装后供python使用`。该类的主要作用是`实现imgui与web端的数据传输`，包括io事件的处理、websocket的初始化、绘制数据的传输等等。
ImGuiContext 是 ImGui 库中的一个结构体，每个 Dear ImGui 应用程序都需要一个上下文，用于存储 ImGui 库的状态和数据。例如ImGuiContext数据就存储当前帧的DrawData和io信息

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%876.png?inline=false)

**构造函数**：需要传入打开的websocket端口号和index.html文件的相对路径还有当前imgui的上下文，进行初始化

**ImGui_WS_Init()**：从incppect传来的按键事件信息和imgui的按键事件的对接代码

**PrepareFontTexture**：准备字符集的贴图，供WebGL进行渲染，也是初始化的一环

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%877.png?inline=false)

**EventHandling**:处理按键事件，每一帧都需要调用。这里的takeEvents是来自web端接收的按键事件信息

**GetDeltaTime:获取异步等待的时间

**SetDrawData**:imgui-ws发送DrawData数据供WebGL进行绘制

**Wait**:每帧调用。imgui-ws实现的节省CPU性能的函数

### Pybind11的绑定和CMakeLists代码

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%878.png?inline=false)

位于examples/PyWS.cpp文件中，使用pybind11进行绑定，在python中导入该包可以使用PyDraw类

![](https://gitlab.nie.netease.com/liuzhaoxiang/mos-viewer/-/raw/master/pictures/%E5%9B%BE%E7%89%879.png?inline=false)

位于examples/CMakeLists中，用于生成动态链接库

### imgui-ws的降版本

1. 在该项目中，`修改third-party下的imgui/imgui库为1.82版本`，与pyimgui调用的imgui版本一致。imgui-ws第三方库基于1.88版本的imgui实现，pyimgui基于1.82版本的imgui实现，这导致了二者的ImContext类型数据有所差异，无法正确强转。

2. 同时为了保持pyimgui端和imgui-ws端ImContext一致，需要修改一些宏配置：

      (1) `注释掉third-party/pyimgui/config-cpp/py_imconfig.h文件下的宏“#define ImDrawIdx unsigned int”`。该宏中ImDrawIdx 是一个类型定义，用于表示绘制命令（ImDrawCmd）中的顶点索引（vertex index）。默认情况下，ImDrawIdx 的类型是 unsigned short，即 16 位无符号整数，可以表示最多 65535 个顶点。如果你的网格包含超过 65535 个顶点，那么你需要将 ImDrawIdx 的类型改为 unsigned int，即 32 位无符号整数，以支持更多的顶点。这里我们不需要该宏，取消掉。
      
      (2) `启用third-party/imgui/imguiconfig.h下的宏“#define IMGUI_USE_WCHAR32”或者注释掉third-party/pyimgui/config-cpp/py_imconfig.h下的宏“#define IMGUI_USE_WCHAR32”，确保一致即可`。该宏表示在 Unicode 中，字符被分为 17 个平面，其中平面 0 包含基本多文种平面（BMP）中的字符，平面 1-16 包含其他字符，如表情符号、古代文字、符号等。在默认情况下，Dear ImGui 库使用 16 位宽的字符类型（ImWchar）来表示字符，这意味着它只能表示 BMP 中的字符，无法表示平面 1-16 中的字符。如果你需要支持这些字符，你可以将 IMGUI_USE_WCHAR32 宏定义放在你的代码中，以便在编译时将 ImWchar 的类型定义为 32 位宽的字符类型，从而支持 Unicode 平面 1-16 中的字符。需要注意的是，如果你将 ImWchar 的类型定义为 32 位宽的字符类型，那么你需要使用支持 Unicode 的字体来渲染这些字符。另外，如果你的应用程序需要与其他使用 16 位宽字符类型的库或系统进行交互，你需要进行适当的转换。

3. `降低按键事件的处理代码`。1.88版本的imgui相对于1.82版本的imgui升级了按键事件处理系统。而imgui-ws的按键事件处理机制是：通过incppect第三方库于web端进行通信获取到web端传来的按键信息，然后再针对这些按键信息进行处理转化成imgui可以接收的按键事件信息，并在imgui.newframe中根据按键事件信息更新DrawData（或者说是更新组件位置、大小等等信息）。imgui-ws自带的按键事件信息处理代码可以见examples/demo-null/main.cpp文件，可以通过`diff等工具来对比查看examples/PyWS.cpp来具体查看修改了哪些按键事件绑定代码`

      (1) 1.88版本的imgui基于事件结构体和事件处理函数来处理按键事件，而1.82版本的imgui的按键事件就是一些标志位

      (2) 更详细的按键事件处理代码可以见1.82版本和1.88版本imgui中的类ImGuiIO以及内部的实现，以及imgui项目下的backends文件夹下的文件，该文件夹下的代码全是imgui层与后端渲染层的对接代码，其中就包括很多代码事件的处理

      (3) 该项目暂时只实现了一些基本的按键事件，比如字母的输入、退格、回车、鼠标左右键和滚轮等等。复制、粘贴、撤回等等其他功能暂未实现
