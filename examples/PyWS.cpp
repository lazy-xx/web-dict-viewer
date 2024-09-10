#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "imgui/imgui.h"
#include "imgui/imgui_internal.h"
#include "imgui-ws/imgui-ws.h"
#include "imgui-ws/imgui-draw-data-compressor.h"
#include "../include/pybind11/attr.h"

#include "common.h"

#include <map>
namespace py = pybind11;

//按键映射
// ImGuiKey toImGuiKey(int32_t keyCode) {
//     switch (keyCode) {
//         case 8: return ImGuiKey_Backspace;
//         case 9: return ImGuiKey_Tab;
//         case 13: return ImGuiKey_Enter;
//         case 16: return ImGuiKey_ModShift;
//         case 17: return ImGuiKey_ModCtrl;
//         case 18: return ImGuiKey_ModAlt;
//         case 19: return ImGuiKey_Pause;
//         case 20: return ImGuiKey_CapsLock;
//         case 27: return ImGuiKey_Escape;
//         case 32: return ImGuiKey_Space;
//         case 33: return ImGuiKey_PageUp;
//         case 34: return ImGuiKey_PageDown;
//         case 35: return ImGuiKey_End;
//         case 36: return ImGuiKey_Home;
//         case 37: return ImGuiKey_LeftArrow;
//         case 38: return ImGuiKey_UpArrow;
//         case 39: return ImGuiKey_RightArrow;
//         case 40: return ImGuiKey_DownArrow;
//         case 45: return ImGuiKey_Insert;
//         case 46: return ImGuiKey_Delete;
//         case 48: return ImGuiKey_0;
//         case 49: return ImGuiKey_1;
//         case 50: return ImGuiKey_2;
//         case 51: return ImGuiKey_3;
//         case 52: return ImGuiKey_4;
//         case 53: return ImGuiKey_5;
//         case 54: return ImGuiKey_6;
//         case 55: return ImGuiKey_7;
//         case 56: return ImGuiKey_8;
//         case 57: return ImGuiKey_9;
//         case 65: return ImGuiKey_A;
//         case 66: return ImGuiKey_B;
//         case 67: return ImGuiKey_C;
//         case 68: return ImGuiKey_D;
//         case 69: return ImGuiKey_E;
//         case 70: return ImGuiKey_F;
//         case 71: return ImGuiKey_G;
//         case 72: return ImGuiKey_H;
//         case 73: return ImGuiKey_I;
//         case 74: return ImGuiKey_J;
//         case 75: return ImGuiKey_K;
//         case 76: return ImGuiKey_L;
//         case 77: return ImGuiKey_M;
//         case 78: return ImGuiKey_N;
//         case 79: return ImGuiKey_O;
//         case 80: return ImGuiKey_P;
//         case 81: return ImGuiKey_Q;
//         case 82: return ImGuiKey_R;
//         case 83: return ImGuiKey_S;
//         case 84: return ImGuiKey_T;
//         case 85: return ImGuiKey_U;
//         case 86: return ImGuiKey_V;
//         case 87: return ImGuiKey_W;
//         case 88: return ImGuiKey_X;
//         case 89: return ImGuiKey_Y;
//         case 90: return ImGuiKey_Z;
//         //case 91: return ImGuiKey_LWin;
//         //case 92: return ImGuiKey_RWin;
//         //case 93: return ImGuiKey_Apps;
//         case 91: return ImGuiKey_ModSuper;
//         case 92: return ImGuiKey_ModSuper;
//         case 93: return ImGuiKey_ModSuper;
//         case 96: return ImGuiKey_Keypad0;
//         case 97: return ImGuiKey_Keypad1;
//         case 98: return ImGuiKey_Keypad2;
//         case 99: return ImGuiKey_Keypad3;
//         case 100: return ImGuiKey_Keypad4;
//         case 101: return ImGuiKey_Keypad5;
//         case 102: return ImGuiKey_Keypad6;
//         case 103: return ImGuiKey_Keypad7;
//         case 104: return ImGuiKey_Keypad8;
//         case 105: return ImGuiKey_Keypad9;
//         case 106: return ImGuiKey_KeypadMultiply;
//         case 107: return ImGuiKey_KeypadAdd;
//         case 108: return ImGuiKey_KeypadEnter;
//         case 109: return ImGuiKey_KeypadSubtract;
//         case 110: return ImGuiKey_KeypadDecimal;
//         case 111: return ImGuiKey_KeypadDivide;
//         case 112: return ImGuiKey_F1;
//         case 113: return ImGuiKey_F2;
//         case 114: return ImGuiKey_F3;
//         case 115: return ImGuiKey_F4;
//         case 116: return ImGuiKey_F5;
//         case 117: return ImGuiKey_F6;
//         case 118: return ImGuiKey_F7;
//         case 119: return ImGuiKey_F8;
//         case 120: return ImGuiKey_F9;
//         case 121: return ImGuiKey_F10;
//         case 122: return ImGuiKey_F11;
//         case 123: return ImGuiKey_F12;
//         case 144: return ImGuiKey_NumLock;
//         case 145: return ImGuiKey_ScrollLock;
//         case 186: return ImGuiKey_Semicolon;
//         case 187: return ImGuiKey_Equal;
//         case 188: return ImGuiKey_Comma;
//         case 189: return ImGuiKey_Minus;
//         case 190: return ImGuiKey_Period;
//         case 191: return ImGuiKey_Slash;
//         case 219: return ImGuiKey_LeftBracket;
//         case 220: return ImGuiKey_Backslash;
//         case 221: return ImGuiKey_RightBracket;
//         case 222: return ImGuiKey_Apostrophe;
//         default: return ImGuiKey_COUNT;
//     }
//     return ImGuiKey_COUNT;
// }


//Initialize the key mapping
void ImGui_WS_Init()
{
    ImGuiIO& io = ImGui::GetIO();
    io.BackendFlags |= ImGuiBackendFlags_HasMouseCursors;       // We can honor GetMouseCursor() values (optional)
    io.BackendFlags |= ImGuiBackendFlags_HasSetMousePos;        // We can honor io.WantSetMousePos requests (optional, rarely used)
    io.BackendPlatformName = "imgui_impl_web";

    // Keyboard mapping. Dear ImGui will use those indices to peek into the io.KeysDown[] array.
    io.KeyMap[ImGuiKey_Tab] = 9;
    io.KeyMap[ImGuiKey_LeftArrow] = 37;
    io.KeyMap[ImGuiKey_RightArrow] = 39;
    io.KeyMap[ImGuiKey_UpArrow] = 38;
    io.KeyMap[ImGuiKey_DownArrow] = 40;
    io.KeyMap[ImGuiKey_PageUp] = 33;
    io.KeyMap[ImGuiKey_PageDown] = 34;
    io.KeyMap[ImGuiKey_Home] = 36;
    io.KeyMap[ImGuiKey_End] = 35;
    io.KeyMap[ImGuiKey_Insert] = 45;
    io.KeyMap[ImGuiKey_Delete] = 46;
    io.KeyMap[ImGuiKey_Backspace] = 8;
    io.KeyMap[ImGuiKey_Space] = 32;
    io.KeyMap[ImGuiKey_Enter] = 13;
    io.KeyMap[ImGuiKey_Escape] = 27;
    io.KeyMap[ImGuiKey_KeyPadEnter] = 108;
    //下面实现不对，1.82版本的ImGuiKey_A表示按下ctrl+a；
    //而incppect返回的67表示按下a，这与1.88版本的ImGuiKey_A一致
    //其他同理
    // io.KeyMap[ImGuiKey_A] = 65;
    // io.KeyMap[ImGuiKey_C] = 67;
    // io.KeyMap[ImGuiKey_V] = 86;
    // io.KeyMap[ImGuiKey_X] = 88;
    // io.KeyMap[ImGuiKey_Y] = 89;
    // io.KeyMap[ImGuiKey_Z] = 90;
}

struct State {
    State() {}

    bool showDemoWindow = true;

    // client control management
    struct ClientData {
        bool hasControl = false;

        std::string ip = "---";
    };

    // client control
    float tControl_s = 10.0f;
    float tControlNext_s = 0.0f;

    int controlIteration = 0;
    int curIdControl = -1;
    std::map<int, ClientData> clients;

    struct InputEvent {
        enum Type {
            EKey,
            EMousePos,
            EMouseButton,
            EMouseWheel,
        };

        Type type;

        bool isDown = false;

        int32_t key = ImGuiKey_COUNT;
        ImGuiMouseButton mouseButton = -1;
        ImVec2 mousePos;
        float mouseWheelX = 0.0f;
        float mouseWheelY = 0.0f;
    };

    // client input
    std::vector<InputEvent> inputEvents;
    std::string lastAddText = "";

    void handle(ImGuiWS::Event && event);
    void update(float time);
};

void State::handle(ImGuiWS::Event && event) {
    switch (event.type) {
        case ImGuiWS::Event::Connected:
            {
                clients[event.clientId].ip = event.ip;
            }
            break;
        case ImGuiWS::Event::Disconnected:
            {
                clients.erase(event.clientId);
            }
            break;
        case ImGuiWS::Event::MouseMove:
            {
                if (event.clientId == curIdControl) {
                    inputEvents.push_back(InputEvent { InputEvent::Type::EMousePos, false, ImGuiKey_COUNT, -1, { event.mouse_x, event.mouse_y }, 0.0f, 0.0f });
                }
            }
            break;
        case ImGuiWS::Event::MouseDown:
            {
                if (event.clientId == curIdControl) {
                    // map the JS button code to Dear ImGui's button code
                    ImGuiMouseButton butImGui = event.mouse_but;
                    switch (event.mouse_but) {
                        case 1: butImGui = ImGuiMouseButton_Middle; break;
                        case 2: butImGui = ImGuiMouseButton_Right; break;
                    }

                    inputEvents.push_back(InputEvent { InputEvent::Type::EMouseButton, true, ImGuiKey_COUNT, butImGui, { event.mouse_x, event.mouse_y }, 0.0f, 0.0f });
                }
            }
            break;
        case ImGuiWS::Event::MouseUp:
            {
                if (event.clientId == curIdControl) {
                    // map the JS button code to Dear ImGui's button code
                    ImGuiMouseButton butImGui = event.mouse_but;
                    switch (event.mouse_but) {
                        case 1: butImGui = ImGuiMouseButton_Middle; break;
                        case 2: butImGui = ImGuiMouseButton_Right; break;
                    }

                    inputEvents.push_back(InputEvent { InputEvent::Type::EMouseButton, false, ImGuiKey_COUNT, butImGui, { event.mouse_x, event.mouse_y }, 0.0f, 0.0f });
                }
            }
            break;
        case ImGuiWS::Event::MouseWheel:
            {
                if (event.clientId == curIdControl) {
                    inputEvents.push_back(InputEvent { InputEvent::Type::EMouseWheel, false, ImGuiKey_COUNT, -1, { }, event.wheel_x, event.wheel_y });
                }
            }
            break;
        case ImGuiWS::Event::KeyUp:
            {
                if (event.clientId == curIdControl) {
                    if (event.key > 0) {
                        inputEvents.push_back(InputEvent { InputEvent::Type::EKey, false, event.key, -1, { }, 0.0f, 0.0f });
                    }
                }
            }
            break;
        case ImGuiWS::Event::KeyDown:
            {
                if (event.clientId == curIdControl) {
                    if (event.key > 0) {
                        inputEvents.push_back(InputEvent { InputEvent::Type::EKey, true, event.key, -1, { }, 0.0f, 0.0f });
                    }
                }
            }
            break;
        case ImGuiWS::Event::KeyPress:
            {
                if (event.clientId == curIdControl) {
                    lastAddText.resize(1);
                    lastAddText[0] = event.key;
                }
            }
            break;
        default:
            {
                printf("Unknown input event\n");
            }
    }
}

void State::update(float time) {
    auto & io = ImGui::GetIO();
    if (clients.size() > 0 && (clients.find(curIdControl) == clients.end() || time > tControlNext_s)) {
        if (clients.find(curIdControl) != clients.end()) {
            clients[curIdControl].hasControl = false;
        }
        int k = ++controlIteration % clients.size();
        auto client = clients.begin();
        std::advance(client, k);
        client->second.hasControl = true;
        curIdControl = client->first;
        tControlNext_s = time + tControl_s;
        //ImGui::GetIO().ClearInputKeys();
        memset(io.KeysDown, 0, sizeof(io.KeysDown));
    }

    if (clients.size() == 0) {
        curIdControl = -1;
    }

    if (curIdControl > 0) {
        {

            if (lastAddText.size() > 0) {
                io.AddInputCharactersUTF8(lastAddText.c_str());
            }

            for (const auto & event : inputEvents) {
                switch (event.type) {
                    case InputEvent::Type::EKey:
                        {
                            //io.AddKeyEvent(event.key, event.isDown);
                            int key = event.key;
                            IM_ASSERT(key >= 0 && key < IM_ARRAYSIZE(io.KeysDown));
                            io.KeysDown[key] = event.isDown;

                            if (key == 17) { io.KeyCtrl = event.isDown; }
                            if (key == 16) { io.KeyShift = event.isDown; }
                            if (key == 18) { io.KeyAlt = event.isDown; }
                            if (key >= 91 && key <= 93) { io.KeySuper = event.isDown; }
                            //io.KeyMods = ImGui::GetMergedKeyModFlags();
                        } break;
                    case InputEvent::Type::EMousePos:
                        {
                            io.MousePos = ImVec2(event.mousePos.x, event.mousePos.y);
                        } break;
                    case InputEvent::Type::EMouseButton:
                        {
                            if (event.mouseButton == 0) io.MouseDown[0] = event.isDown;
                            if (event.mouseButton == 1) io.MouseDown[1] = event.isDown;
                            if (event.mouseButton == 2) io.MouseDown[2] = event.isDown;
                        } break;
                    case InputEvent::Type::EMouseWheel:
                        {
                            io.MouseWheelH += event.mouseWheelX;
                            io.MouseWheel += event.mouseWheelY;
                        } break;
                };
            }
        }
        //memset(KeysDown, 0, sizeof(KeysDown));
        inputEvents.clear();
        lastAddText = "";
    }
}

//关键类，供py端进行调用
struct PyDraw {
    // setup imgui-ws
    private:
    ImGuiWS imguiWS;
    VSync vsync;
    State state;
    ImGuiContext* imGuiContext;
    ImGuiIO* imGuiIO;
    public:
    //初始化函数，建立imgui-ws的通信，以及统一两侧的上下文
    PyDraw(int port, const std::string &httpRoot, Py_uintptr_t imGuiContext){
        this->imGuiContext = reinterpret_cast<ImGuiContext* >(imGuiContext);
        ImGui::SetCurrentContext(this->imGuiContext);
        this->imGuiIO = &ImGui::GetIO();
        ImGui_WS_Init();
        this->imguiWS.init(port, httpRoot, { "", "index.html" });
    }
    void PrepareFontTexture(int width, int height, const char* pixels)
    {   
        //const char* pixels_data = PyByteArray_AsString(reinterpret_cast<PyObject*>(&pixels));
        imguiWS.setTexture(0, ImGuiWS::Texture::Type::Alpha8, width, height, pixels);
    }   
    void EventHandling(float time) {
        // websocket event handling
        auto events = imguiWS.takeEvents();
        for (auto & event : events) {
            this->state.handle(std::move(event));
        }
        this->state.update(time);
    }
    float GetDeltaTime(){
        return this->vsync.delta_s();
    }
    //关键函数，发送绘制数据
    void SetDrawData(Py_uintptr_t imDrawData) {
        ImDrawData* data = reinterpret_cast<ImDrawData*>(imDrawData);
        this->imguiWS.setDrawData(data);
    }
    // if not clients are connected, just sleep to save CPU
    void Wait(){
        do {
            this->vsync.wait();
        } while (this->imguiWS.nConnected() == 0);
    }
};

void test(){
    int port = 5000;
    std::string httpRoot = "/home/lazybox/Tools/imgui-ws/examples";

    // if (argc > 1) port = atoi(argv[1]);
    // if (argc > 2) httpRoot = argv[2];

    IMGUI_CHECKVERSION();
    int a = 100;
    int b = 90;
    ImGuiContext* imguiContext = ImGui::CreateContext();
    ImGui::SetCurrentContext(imguiContext);
    ImGui::GetIO().MouseDrawCursor = true;

    //ImGui::StyleColorsDark(); //bug
    ImGui::GetStyle().AntiAliasedFill = false;
    ImGui::GetStyle().AntiAliasedLines = false;
    ImGui::GetStyle().WindowRounding = 0.0f;
    ImGui::GetStyle().ScrollbarRounding = 0.0f;

    // setup imgui-ws
    ImGuiWS imguiWS;
    imguiWS.init(port, httpRoot + "/demo-null", { "", "index.html" });

    // prepare font texture
    {
        unsigned char * pixels;
        int width, height;
        //bug
        ImGui::GetIO().Fonts->GetTexDataAsAlpha8(&pixels, &width, &height);
        imguiWS.setTexture(0, ImGuiWS::Texture::Type::Alpha8, width, height, (const char *) pixels);
    }

    VSync vsync;
    State state;

    while (true) {
        // websocket event handling
        auto events = imguiWS.takeEvents();
        for (auto & event : events) {
            state.handle(std::move(event));
        }
        state.update(ImGui::GetTime());

        {
            auto & io = ImGui::GetIO();
            io.DisplaySize = ImVec2(1200, 800);
            io.DeltaTime = vsync.delta_s();
        }
        //会初始化主窗口，跳转到imgui_widgets.cpp，有查询不到GImGui的bug
        ImGui::NewFrame();

        // render stuff
        if (state.showDemoWindow) {
            ImGui::ShowDemoWindow(&state.showDemoWindow);
        }

        // debug window
        {
            ImGui::Begin("Hello, world!");
            ImGui::Checkbox("Demo Window", &state.showDemoWindow);
            ImGui::Text("Application average %.3f ms/frame (%.1f FPS)", 1000.0f / ImGui::GetIO().Framerate, ImGui::GetIO().Framerate);
            ImGui::End();
        }

        // show connected clients
        ImGui::SetNextWindowPos({ 10, 10 } , ImGuiCond_Always);
        ImGui::SetNextWindowSize({ 400, 300 } , ImGuiCond_Always);
        ImGui::Begin((std::string("WebSocket clients (") + std::to_string(state.clients.size()) + ")").c_str(), nullptr, ImGuiWindowFlags_NoCollapse);
        ImGui::Text(" Id   Ip addr");
        for (auto & [ cid, client ] : state.clients) {
            ImGui::Text("%3d : %s", cid, client.ip.c_str());
            if (client.hasControl) {
                ImGui::SameLine();
                ImGui::TextDisabled(" [has control for %4.2f seconds]", state.tControlNext_s - ImGui::GetTime());
            }
        }
        ImGui::End();

        // generate ImDrawData
        ImGui::Render();

        // store ImDrawData for asynchronous dispatching to WS clients
        imguiWS.setDrawData(ImGui::GetDrawData());

        // if not clients are connected, just sleep to save CPU
        do {
            vsync.wait();
        } while (imguiWS.nConnected() == 0);
    }

    //ImGui::DestroyContext();
}


//进行绑定
PYBIND11_MODULE(PyWS, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    m.def("test", &test, py::return_value_policy::copy);

    py::class_<PyDraw>(m, "PyDraw")
        .def(py::init<int, const std::string &, Py_uintptr_t>())
        .def("PrepareFontTexture", &PyDraw::PrepareFontTexture)
        .def("EventHandling", &PyDraw::EventHandling)
        .def("GetDeltaTime", &PyDraw::GetDeltaTime)
        .def("SetDrawData", &PyDraw::SetDrawData)
        .def("Wait", &PyDraw::Wait);
}


