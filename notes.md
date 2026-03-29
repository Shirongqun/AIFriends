工程课

# 1. 配置环境、创建导航栏

后端是Django，前端是Vue

安装pycharm、git，注册github账号

Vue3需要配置Node环境

跨域：从前端5173端口调用后端8000端口

django的静态文件一般是放在static或者media文件夹里，static一般是开发者放的文件，比如说js文件、css文件、logo，media一般放用户上传的图片，比如头像、用户文章里上传的图片；这些可以让django找到文件。

前端的内容是需要放到后端的，那么前端的内容是怎么放到后端里的呢？
vite.config.js中配置的。

django里写一个页面需要定义3个东西：url、views、html
比如http://127.0.0.1:8000/api/token/，这里的/api/token就是url；放在urls.py文件
views定义上边的url让哪个函数来处理；放在views文件夹下
html是views返回的页面；放在template文件夹下

点击 http://127.0.0.1:8000/ 
	-> path('', index)【web.views.index】 
	-> return render(request, 'index.html')【web/templates/index.html】

所以说，开发的时候，是通过两个不同的端口开发的；在部署的时候，只访问django的8000端口

安装Tailwind CSS、daisyUI

什么叫padding？就是一个元素内部的阴影，外部的叫margin

whitespace-nowrap 禁止换行

执行npm run build会将前端文件夹frontend复制到backend/static/frontend
这是已经配置过的，讲义中有写。

```shell
# 启动django
(.venv) PS D:\Courses\AIFriends\backend> python manage.py runserver
# 启动前端测试代码
(.venv) PS D:\Courses\AIFriends\frontend> npm run dev
# 将前端代码打包到后端
(.venv) PS D:\Courses\AIFriends\frontend> npm run build
```

LangChain - 大模型应用开发框架
DeepSeek - 大模型提供商

-----

详细细节实现

创建项目

1、使用Pycharm创建项目，创建的是一个Python虚拟环境，这样能保证不同项目之间不会出现环境混乱；注意路径中不能出现中文，

2、创建后端项目

首先，安装django相关

`pip install django djangorestframework djangorestframework-simplejwt django-cors-headers`

jwt可以实现多端登录

cors:支持跨域

创建django项目

在AIFriends/目录下执行：

```shell
cd backend
django-admin startproject backend # 创建backend项目，只在项目开始时用一次
django-admin startapp web # 创建web应用，项目中需要新功能模块时就创建
python manage.py migrate # 由于上边创建了新应用，需要将数据库从当前状态更新到最新设计状态
python manage.py createsuperuser # 创建超级管理员
python manage.py runserver # 运行django服务器
```

3、创建前端项目



对于前端，所有的模块是分块划分好的。

django里写一个页面，需要写3个东西：

-------

我的疑问

1. 路由的流程是什么样子的？
   当输入`http://127.0.0.1:8000`时，先进入到`backend/urls.py`，根据`path('', include('web.urls'))`再去`web/urls.py`中根据`path('', index)`进入到`web/views/index.py`，然后根据`render(request, 'index.html')`进入`web/templates/index.html`中，这就是返回给前端的html文件。
2. django是怎么使用frontend中的文件的？
   以web应用为例，其`web/templates/index.html`中已经引入了`static/frontend/index.html`
   整个前端文件会打包成一些静态文件，变成一堆js文件、css文件、图片，
   django中将静态文件放到static（开发者的）、media文件夹中，希望直接将前端frontend打包的文件放到static中，然后将整个项目文件放到服务器上运行。
3. 开发阶段时，点击前端按钮会访问后端代码，这里涉及到了跨域，这部分是怎么实现跨域的？

# 2. 登录模块

创建前端的各个页面

引入<RouterView />，就会根据路由url去index.js里找这个url对应的组件是哪个，然后把对应的组件渲染到<RouterView />这个位置。

**怎么把http://localhost:5173/usr/space/123中的123给拿出来呢？**

通过`const route = useRoute()`来取当前 url的信息，注意与`useRouter`区分

**如何实现通过点击按钮`好友`就可以跳转到好友页面呢？**

只需要将按钮从button变成`<RouteLink />`即可。

![](D:\Courses\RouterLink.png)

![image-20260128225553835](C:\Users\HI\AppData\Roaming\Typora\typora-user-images\image-20260128225553835.png)

**如何实现点击后高亮呢？**

vue提供了一个方式，就是有一个属性叫，当前页面的url与`<RouterLink />里对应的url是相同的话，就自动激活这个"menu-focus"，自动将这个"menu-focus"加到class中。

![image-20260128230551434](C:\Users\HI\AppData\Roaming\Typora\typora-user-images\image-20260128230551434.png)

**怎么创建登录、注册前端界面？怎么布局该组件呢？**

使用daisyUI的Login form with fieldset组件，用一个`<div />` 包起来。设置属性为`class="flex justify-center mt-30"`，

**怎么添加注册按钮？**

直接复制登录界面，改一下就是注册前端。

需要创建一个数据库，用来存用户的简介、头像等信息。

用户上传的文件统一保存在media文件夹中。开发者相关的放在static中。

这样就在django里定义了一个数据库，数据库里的一条数据就类UserProfile的一个对象。类UserProfile就对应数据库里的一张表。

django自带的登录方式是利用sessioid，这种不能支持多端登录：网页、app。

现在常用的登录方式是jwt登录，token验证，json web token

![image-20260130000706701](C:\Users\HI\AppData\Roaming\Typora\typora-user-images\image-20260130000706701.png)

01:03:35

django写后端很快的，因为你不需要写任何sql语句。

在退出的时候必须得先判断是否为登录状态

refresh_token.py是用refresh去刷新access。

refresh = RefreshToken(refresh_token)判断是否在有效期内。

在user.js实现前端全局状态存储

定义响应式变量id，...

function setUserInfo(data)里的data就是login.py中返回的Response

怎么实现登录后头像变成图片、导航栏更新呢？

1、登录完之后多一个创作按钮

引入全局登录状态：`const user = useUserStore()`



icons：图标

退出登录上方的横线：加一个<li />

怎么点击下拉菜单后退出menu界面呢？

给每一项都绑定一个函数

在LoginIndex.vue中对接登录功能

如何让前端页面的输入信息跟前端代码中的变量绑定起来呢？

使用`v-model="username"`可以将输入框的用户名跟变量绑定

如何实现登录界面输入后点击回车能够去登录呢？

那就是将页面换成表单<form />，并阻止默认行为，同时登录按钮绑定登录功能。

route是获取当前页面的url信息，router是跳转。

此时，一刷新，页面的登录信息就会消息。

因为一刷新后，浏览器中所有的js就会消失，即useUserStore中的id、username、photo、profile、accessToken都会变成默认值。又恢复到了未登录状态。

下面实现在RegisterIndex.vue中对接注册功能

@就是绑定事件

主动退出后，应该有什么变化？

就是user.js中function logout()实现的内容

由于存在<slot></slot>，所以跳转页面会显示到这里。而导航栏则不会改变。

**给前端界面添加前置守卫：登录之后才可以看**

当打开一个需要授权的页面时，应该自动跳转到登录页面，

在frontend/src/router/index.js添加一个meta信息

**刷新页面会导致store中被初始化，如何去保留登录信息呢？**

在App.vue刚刚挂载的时候触发事件 onMounted() {}

router.push是可以后退的，而router.replace是不可以后退的。

前端页面的路由是通过frontend/src/router/index.js路由的；而**前端路由到后端**是通过调用post、get并传入'api/xxx'进入到后端backend/web/urls.py去进行后端路由的。

02:48:35

# 3.1 编辑资料、编辑角色模块

给{{ user.username }}添加break-all属性，就能使得字母也能将多余的字符用...显示。

当我在`http://127.0.0.1:8000/user/profile/`刷新的时候，先路由到后端路由，在`backend/web/urls.py`没有匹配路径，就返回默认的index，前端显示出index中的内容：index.html，然后前端又去路由`user/profile`，在`frontend/src/router/index.js`中找到应该是对应`ProfileIndex`组件，于是在前端把该组件给渲染出来了。

MTV 是 Django 特有的架构模式，本质上是 MVC 模式的变种：

| 模式              | 对应 MVC   | 功能描述                         |
| :---------------- | :--------- | :------------------------------- |
| **M（Model）**    | Model      | 数据层，处理数据和业务逻辑       |
| **T（Template）** | View       | 表现层，负责显示数据（HTML模板） |
| **V（View）**     | Controller | 控制层，处理业务逻辑和请求响应   |

**简单记忆**：View = 处理"怎么做"，Template = 处理"怎么显示"，Model = 处理"数据是什么"。

**怎么实现替换头像呢？**

添加一个<input type='file' accept="image/*" />，同时给其绑定一个引用，然后在全局变量中拿到这个引用fileInputRef，最后给相机图标绑定一个点击事件：当点击相机图标时触发文件输入框。

**怎么在模态框汇总渲染图片裁剪功能？**

不会显示在前端就不用定义成响应式变量



**怎么上传更新后的信息到后端呢？**

将myPhoto给暴露出去：

```javascript
defineExpose({
  myPhoto,
})
```

前端判断用户名、密码、简介是否为空是为了及时响应，提高用户体验；后端判断是为了防止恶意用户；

**创建角色**

在后端models文件夹下创建角色数据库 

新创建的数据库一定加到管理员页面 backend/web/admin.py

记得同步数据库

```shell
python .\manage.py makemigrations
python .\manage.py migrate
```

CharField：不能回车；TextField：可以回车；

**创建角色相关的views**

创建Python软件包character

修改数据库中的character时得保证修改传入的id以及修改的是属于自己的角色。

写完角色相关的后端处理逻辑后，记得在web/urls.py添加其url。

# 3.2 编辑资料、编辑角色模块（下）

### Vue 的设计原则：**Props Down, Events Up**

1. **Props 是只读的**：子组件不能直接修改父组件的数据
2. **保持数据流清晰**：父 → 子通过 props，子 → 父通过 events
3. **避免副作用**：防止多个组件意外修改同一数据源

在js中调用响应式变量时一定得加value，如`modalRef.value.showModal()`
但是在template中是不需要的，`@click="modalRef.close()"`

在模态框中渲染croppie插件，

console.log，一部分没有删除。

一键激活pycharm pro

https://rcn1ac1swzm4.feishu.cn/wiki/PkxlwEK4CiMJuqk0YUkcMjJbnkd?from=from_copylink



# 4.1 流式布局（上）

往下翻的时候，动态加载内容，就叫作流式布局。

后端GetListCharacterView返回个人信息、角色列表。

不需要登录即可返回，因此不需要加permission

items_count：当前前端已经有多少个元素。

写完后端逻辑之后，添加一下后端路由，在backend/web/urls.py中添加。

接下来实现前端个人主页

UserInfoField实现存放用户信息区。

flex-col items-center一起作用，使得组件被设置为水平居中；

如何实现流式加载？

定义一个哨兵：sentinel-ref

如何利用哨兵实现动态加载呢？
只要哨兵在视窗内，就加载，直到红框被挤到屏幕外。

怎么判断哨兵是否出现在视窗内呢？
组件挂载时搞了一个监听new IntersectionObserver，监听哨兵是否跟视窗有交集

接下来实现前端样式

简介最多有四行：line-clamp-4 break-all

名字和头像之间的距离 gap-2

在<script />中使用props一定加上props，在<template />里使用就不用加了。

先实现后端class HomepageIndexView，然后实现该路由：

# 4.1 流式布局（下）

实现好友页面

**创建backend/web/models/friend.py数据库对象**，class Friend，存储每个用户和每一个虚拟角色的好友关系



**CASCADE** 意思是"级联删除"：

```python
# 举例：如果删除了"孙悟空"这个角色
Character表：
id | name
5  | "孙悟空"  <-- 删除这条记录

# 那么 Friend 表中所有 character_id=5 的记录会自动删除
Friend表：
id | me_id | character_id
1  | 1     | 5  <-- 自动删除
3  | 2     | 5  <-- 自动删除
# 2号记录 (character_id=6) 保留
```

**实现后端的views**

3个python文件

backend/web/views/friend/get_or_create.py

backend/web/views/friend/remove.py

backend/web/views/friend/get_list.py

**实现后端路由**

backend/web/urls.py

前端

输入框样式，输入框毛玻璃样式：backdrop-blur-sm；右边空出20像素位置：pr-20

父组件的@remove是怎么触发的？
在子组件中使用emit()触发。

如何保证仅子组件的click触发，而不再触发父组件的click？
使用.click.top

# 5.1 文字聊天（上）

对接大模型，其实就是**用框架给大模型发一个http请求**。

借助`langgraph`对接大模型

遇到了python软件包版本不一致的问题。

```shell
pip install --upgrade langchain langchain-core langchain-community
```

敏感信息保存在环境变量中，安装python-dotenv：pip install python-dotenv，负责加载环境变量

与大模型聊天是回合制，将每一轮对话存下来，在backend/web/models/friend.py定义`class Message`。

记得migrate

```
python ./manage.py makemigrations
python ./manage.py migrate
```

每一轮对话中，用户发送的消息保存在user_message中，但是实际上发送给大模型的信息会加上提示词、最近的对话等等很多信息，所以将给大模型的输入保存到input变量，方便调试。

输入输出token的价格不一样，一般输出会贵一些。

注册阿里云账号，获得api-key、发送请求的url。

在`AIFriends/backend/backend/settings.py`开头添加：

```python
from dotenv import load_dotenv

load_dotenv()
```

然后重启Django服务，这样django就能自动将.env里的环境变量加载到内存中。



## 实现chat.py

实现AIFriends/backend/web/views/friend/message/chat/chat.py，接收前端发送来的聊天消息

friend_id可以唯一地确定用户与某个虚拟角色之间的好友关系

xxx.strip()可以删除前后空格、回车

### 使用langgraph对接大模型

封装ChatGraph代码，

langgraph就是用一个图定义所有的计算关系，

在langgraph中需要维护一个数据，称为状态，维护图计算的状态

**class AgentState**看着复杂，本质上就是一个字典，只不过类型更加严格一些。

TypedDict说明是一个字典，字典里有一个messages，对应的是一个列表，

add_messages说明其合并方式：传入[a, b, c]，大模型输出为[x]，自动合并为[a, b, c, x]，一般传给大模型的就是一个消息列表，大模型的回复自动追加到消息列表尾部，这是一个很常见的操作；



```
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        {
            'messages': []
        }
```

**定义agent的逻辑**，就是对大模型的调用：model_call，名字自定义

**定义状态图**，图里维护的消息类型是AgentState

```python
graph = StateGraph(AgentState)
```

给状态图添加一个自定义节点agent，节点的函数是model_call

```python
graph.add_node('agent', model_call)
```

添加2条边

```
graph.add_edge(START, 'agent')
graph.add_edge('agent', 'END')
```

将传入的用户消息封装成HumanMessage

```python
        inputs = {
            'messages': [HumanMessage(message)],
        }
```

**实现打开聊天窗口自动聚焦到聊天信息窗口的功能**

要求打开模态框的时候自动聚焦到输入聊天信息的地方。需要在父组件中调用子组件，因此，把组件的接口暴露出去

```vue
// 将接口暴漏给父组件
defineExpose({
  focus,
  close,
})
```

### 在InputField.vue中对接后端的api

实现async function handleSend(event, audio_msg) 

点击发送按钮可以触发提交，因此添加@click="handleSend"

回车也可以触发提交、切不能刷新，因此将输入框修改为表单<form @submit.prevent="handleSend"/>，监听表单的提交事件，并阻止默认行为，然后执行 handleSend 方法

使用v-model="message"可以把这个**输入框的值**和脚本里的 `message` 变量**绑定在一起**

### 实现流式回复

前端发送消息时不需要流式，后端回消息时需要流水，因此使用SSE（Server-Sent Events）

SSE 只是 HTTP 响应的一种特殊格式，它仍然使用 HTTP/HTTPS 协议。



定义生成器函数event_stream，内部使用`yield`生成数据

将大模型输出修改为流水输出：`streaming=True,`

app.invoke是非流水输出，app.stream是流式输出，app.astream是异步流式输出。

判断返回的消息是否为BaseMessageChunk类型

```python
if isinstance(msg, BaseMessageChunk):
```

判断是否有属性

```
if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
```

遍历生成器里的内容

```python
for date in event_stream(): # 会自动用next遍历生成器里的内容
```

必须使用 yield f'data: [DONE]\n\n'这种格式，是SSE定义的。

#### 改造前端请求

新建frontend/src/js/http/streamApi.js，流式接收数据

为了防止用户重复发消息，定义了isProcessing变量。后边咋又删除了呢。

55:30



full_usage是干啥的？

当把yield f'data: [DONE]\n\n'返回后，怎么还会执行到下边的逻辑呢？

前端向后端传消息id，后端知道回传哪些消息

子组件尽量不要修改父组件里的变量，可以在父组件里定义一些函数来修改。将函数传给子组件。

实现向上滚动的效果
定义一个哨兵，

调试Python代码，

```python
import traceback
print(traceback.format_exc())
```



# 5.2 文字聊天（下）

`npm install`安装一下有安全隐患的包。



<img src="D:\Courses\学习笔记\实现系统提示词.png" style="zoom:70%;" />





流程图是什么？

什么叫function call？

<img src="D:\Courses\学习笔记\带工具调用的流程图.png" style="zoom:70%;" />

class Message保存每一轮对话的内容。

<img src="D:\Courses\学习笔记\长期记忆agent流程图.png" style="zoom:80%;" />

长期记忆和短期记忆什么区别？

每次在组织传给llm的消息`inputs`时，采用系统提示词（SystemPrompt）+角色性格（friend.character.profile）+长期记忆（friend.memory）+最近十轮对话（Message）+用户消息（request.data['message']）的格式

langchain_openai这个python软件包是在什么章节install的？

长期记忆模块不需要返回给用户，因此不需要采用流式，

长期基于保存在系统提示词（SystemPrompt）中，title='记忆'

## 知识库

知识库是干嘛的呢？
大模型不是万能的，不能知道最新的消息、不能知道某个垂直领域的知识，当我们问他某些垂直领域的知识时，可以给他外挂一个知识库（硬盘），这就是知识库。
大模型从知识库里检索信息之后，再去回答，这个过程称为RAG(**Retrieval-Augmented Generation 检索增强生成**)。有一个很重要的问题就是如何存知识库？现在比较常用的是用向量数据库来存知识库，

知识库可能很大，几十M、几十G，使用向量数据库可以很快帮助我们找到语义相关的文档。

如何把段落转换成向量，可以使用embedding模型实现。

向量数据库可以很方便地去存这些向量，然后很方便地去查找距离某个向量最近的向量，



安装pip install ipython便于交互，安装速度很慢，可以换源。

```shell
pip install ipython
```



流程举例演示如下：

**用户提问**：现在精确时间是多少？帮我查询一下阿里云百炼平台新人有没有新人额度？

首先组装系统提示词+用户输入信息，第一次调用大模型

![](D:\Courses\学习笔记\调用tool步骤1.png)

然后得到大模型的返回结果，langgraph的StateGraph根据大模型第一次返回的信息判断是否需要调用tools，发现需要调用tools，于是组装工具的调用结果，组装好后第二次调用大模型，

![](D:\Courses\学习笔记\调用tool步骤2.png)

大模型返回结果，langchain觉得可以返回了，就返回大模型的结果。

<img src="D:\Courses\学习笔记\前端显示调用tool的返回结果.png" style="zoom:60%;" />

<img src="D:\Courses\学习笔记\使用tool2次调用ai流程图.png" style="zoom:60%;" />

# 6. 语音模块

上传一段语音，可以把语音复刻出来。模仿人说话。

<img src="D:\Courses\学习笔记\语音模块架构图.png" style="zoom:80%;" />

2个简化

1）浏览器到服务器的流式改为非流式

client给server发消息由流式改为非流式后，可以不用在django中实现websocket，

2）把后端语音识别的结果发给前端，前端再重新调用一遍

这样，前端、后端只需实现一套逻辑即可

网络请求的时间远远小于大模型生成结果的时间，所以加这一段（2个网络延迟）区别不是很明显。



websocket协议可以传字节，也可以传文本；sse只能传文本；



<img src="D:\Courses\学习笔记\后端与大模型语音识别交互逻辑.png" style="zoom:80%;" />

可以发现，在与大模型语音识别的交互过程中，一个线程是无法实现发送消息的同时接收消息，在python使用协程实现即可

语音识别：ASR

阿里云ASR文档：https://bailian.console.aliyun.com/cn-beijing/?spm=5176.12818093_47.console-base_product-drawer-right.dproducts-and-services-sfm.258b16d0dZyCzu&tab=api#/api/?type=model&url=2869339

由于django主要支持异步，而websocket是异步调用，所以使用asyncio.run()做了一个桥接。**简单说**：这是**同步世界和异步世界之间的桥接模式**。虽然效果上都是等待，但它让你能：

1. 保持 Django 视图的同步 simplicity
2. 复用已有的异步代码
3. 利用异步库的功能

阿里云建议每次发送100ms的音频，我们采用的是pcm16音频格式，用16位（2字节）来表示一次采样，采样频率是16000hz，1s16000次，所以1s是采样16000✖️2=32000字节，那么100ms就是3200字节。



异步生成的结果不能同步给生成器，



协程的核心机制：事件循环

```python
import asyncio
import time

async def task(name, duration):
    print(f"{name} 开始: {time.strftime('%X')}")
    await asyncio.sleep(duration)  # 模拟I/O
    print(f"{name} 结束: {time.strftime('%X')}")
    return name

async def main():
    # 事件循环开始工作
    tasks = [
        task("A", 2),
        task("B", 1),
        task("C", 3)
    ]
    
    # 事件循环调度这三个任务
    results = await asyncio.gather(*tasks)
    
asyncio.run(main())
```



<img src="D:\Courses\学习笔记\语音合成流程图.png" style="zoom:80%;" />





- **`async def`**：声明这个函数可以"异步执行"
- **`async for`**：声明这个循环的每次迭代都可能"等待数据"



使用 **`async` + `await`** 声明函数为异步，表明该函数内**遇到 `await` 阻塞**时可以将该函数挂起，转而执行函数外其他的代码



上线的时候是用nginx部署的



# 7. 项目上线

模态框自动绑定了按esc键关闭。

公网ip：8.130.157.21

登录

```shell
ssh root@8.130.157.21
```

创建新用户

```shell
adduser acs # 创建账户acs
usermod -aG sudo acs # 给acs添加sudo权限
ssh acs@8.130.157.21
```

**给服务器配置别名**

在 `~/.ssh/config`中添加配置

```shell
Host llm
    HostName 8.130.157.21
    user acs
```

**配置免密登录**

```shell
 ssh-copy-id llm
```

**安装tmux**

```
sudo apt-get update  # 更新软件包列表
sudo apt-get install tmux
```

使用tmux

```
tmux
# 左右分割
# ctrl + a %
# 上下分割
# ctrl + a "
# 删除窗口
# ctrl + d
# 全屏
# ctrl + a ctrl + z
```



安装Python3.14

```
# 统计耗时
time ./configure --enable-optimizations
sudo make altinstall # 不会覆盖系统路径下原有的，而是创建一个指定版本的
```



将前端网站的vue图标logo修改为自己的图片：修改frontend/public/favicon.ico为自己的图片

**把IP地址关联一个域名**



访问域名是怎么访问到具体端口号的呢？


打包完前端后，前端的所有的包就都放到backend/static/frontend/assets/index-BI_WbIZS.js了，所以不需要在云服务器上安装vue环境。

但是在本地安装的所有的python的包都需要在云端重新安装一遍，而且要确保每一个包的版本号是一致的。

在本地导出python安装过的所有包及其版本号：

在AIFriends目录下执行：

```
pip freeze > requirements.txt
```

然后将requirements.txt上传到云服务器上。

然后在云服务上执行：pip3.14 install -r requirements.txt --user。

记得重置数据库密码

我的域名：https://app1565.acapp.acwing.com.cn

让项目运行起来

运行`gunicorn`，在`/home/acs/backend/`目录下执行：

```
gunicorn --workers 3 --graceful-timeout 3 --bind unix:/home/acs/backend/gunicorn.sock backend.wsgi:application
```

nginx已经运行，这时就可以访问域名了。

### 语音复刻

定义Voice数据库，

在前端的await中，当执行到 await 时，程序并不会“卡死”等待，而是会“让出控制权”，让浏览器继续处理其他任务，等网络请求完成后再回来继续执行。



这个cosyvoice-v3-flash是什么东西？



把项目上传到云端

修改config.js为cloud

然后打包 

删除云端backend，这会导致云端已有的数据被删除 rm -r backend/

重新上传项目

修改云端的settings.py中的DEBUG = False

python3.14 manage.py collectstatic:`collectstatic` 就像**把所有散落在各地的静态文件"打包"到一个文件夹**，方便 Nginx 一次性找到并高效提供访问。





