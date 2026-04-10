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

backend/web/views/friend/message/chat/graph.py 聊天模块的计算流程图

friend_id可以唯一地确定用户与某个虚拟角色之间的好友关系

xxx.strip()可以删除前后空格、回车

### 使用langgraph对接大模型

封装ChatGraph代码，

langgraph就是用一个图定义所有的计算关系，

在langgraph中需要维护一个数据，称为状态，维护图计算的状态

**class AgentState**看着复杂，本质上就是一个字典，只不过类型更加严格一些。

TypedDict说明是一个字典，字典里有一个messages，对应的是一个列表，

add_messages说明其合并方式：传入[a, b, c]，大模型输出为[x]，自动合并为[a, b, c, x]，一般传给大模型的就是一个消息列表，大模型的回复自动追加到消息列表尾部，这是一个很常见的操作；



```python
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        // {
        //     'messages': []
        // }
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

app.invoke是非流式输出，app.stream是流式输出，app.astream是异步流式输出。

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

full_usage是干啥的？表示消耗量，看着是msg中的固有属性

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

## 实现消息持久化

### 后端

每次打开聊天界面，可以把历史聊天记录自动拉取下来。

后端实现动态加载消息接口：get_history

前端正在显示回复消息的时候，后端还没将消息写入到数据库中，因此不传items_count了，改为传msg_id，

当前端初始加载、还没有消息的时候last_message_id传0；否则传最上边一条消息的id；后端从数据库查询小于该last_message_id的消息并返回；

返回给前端用户消息、AI消息；

### 前端

整个ChatField.vue是聊天界面，把history聊天信息放这里，因为多个子组件会用到；

在InputField.vue中点击发送时要将聊天信息放到history的最后；
同时ChatHistory.vue也要显示history；

将history传给这2个子组件，注意不要直接在子组件中修改父组件的内容，而是在父组件中定义一些函数，把这些函数传给子组件，子组件调用这些函数去修改父组件的变量；

定义handlePushBackMessage、handleAddToLastMessage并传给InputField.vue;
在InputField.vue中使用`const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])`接收这两个事件；

使用emit('', 'xx')即可调用父组件传过来的事件；

每一条消息都是用的现成的daisyUI中的组件，左侧：class="chat chat-start"，右侧：class="chat chat-end"

用户信息保存在全局变量**useUserStore**里；

聊天泡泡要保留回车、空格，使用whitespace-pre-wrap属性

**实现聊天记录自动滚动到下边**

定义滚动区的引用：ref="scroll-ref"

scroll height、client height是固有不变的，通过改变scroll top可以改变展示区域

一般令scrollRef.value.scrollTop = scrollRef.value.scrollHeight即可

<img src="D:\Courses\学习笔记\视窗默认显示最下边的消息.png" style="zoom:80%;" />

由于是在每一次改表history消息的时候滚动，所以需要在handlePushBackMessage、handleAddToLastMessage中触发，因此将滚动的函数从ChatHistory.vue暴露给其父组件ChatField.vue

**往上滚动鼠标时，实现流式加载消息**

通过哨兵实现

每次加载到消息后，需要修改视窗的scrollTop，这样才能保证聊天消息不会自动向上翻滚。

判断哨兵是否在可视区域内：

```
  const sentinelRect = sentinelRef.value.getBoundingClientRect()
  const scrollRect = scrollRef.value.getBoundingClientRect()
```

getBoundingClientRect()返回元素相对于浏览器视口（viewport）的位置和大小信息。

与scrollRef标签是否有交集，如果有就从后端加载消息；

一切都是相对于浏览器视口而言，

注意无论我怎么滑动，scrollRect的位置、大小相对于浏览器视口是不变的；

当我滑动、加载到更多<Message />时，sentinelRect的相对位置是会变化，可能就看不见了；

所以才可以判断2个标签相对于浏览器视口的位置是否相交。

<img src="D:\Courses\学习笔记\判断哨兵与聊天窗口是否相交.png" style="zoom:55%;" />

为什么已经监听了哨兵的可见性还要加一个判断是否相交的逻辑呢？

这是因为监听器只能在哨兵的可见性发生变化时触发，存在一种场景：监测到哨兵可见然后触发加载后端消息，但是加载过后没有填充满视窗口，此时哨兵仍然是可见的、监听器却不会触发（因为哨兵的状态没有改变），就需要判断哨兵与可视窗口是否存在交集才能触发再次从后端加载消息。





# 5.2 文字聊天（下）

`npm install`安装一下有安全隐患的包。

## 添加系统提示词和短期记忆

系统提示词：写情景规则

扩展给大模型输入的信息

一般给大模型的输入是一个列表 messages: [xx, xx, xx, ... ]

消息是按照friend_id来绑定对话的

<img src="D:\Courses\学习笔记\实现系统提示词.png" style="zoom:70%;" />

创建数据库**SystemPrompt**存储提示词

提示词类型有很多：回复、记忆，使用title区分；

一种提示词可能有很多段，使用order_number分块，使用时将相同类型的所有提示词按照order_number顺序拼接；

更新角色介绍。

后端实现函数：add_system_prompt，需要添加角色性格，所以传入friend

将回复系统提示词、角色性格、长期记忆拼接成SystemMessage(prompt)，添加到inputs中；

将最近的10轮对话，按照HumanMessage、AIMessage格式添加到系统提示词和用户消息中间；

pprint()在输出字典的时候会自动缩进；

## 添加function call

大模型不是万能的，

给大模型传工具函数，由其自己决定是否要调用这些函数。

给大模型传递一个工具列表（函数列表），会告诉大模型每个函数是干嘛的，输入、输出是什么，大模型每次决定要不要调用工具、调用工具中的哪些，我们在收到大模型的回复之后看一下是否要调用工具，如果需要就调用有关工具，然后将工具的执行结果包装成一个ToolMessage再发给大模型、重新调用一次大模型

计算流程图

**condition条件边**会判断最后一个AI回复中是不是要调用tool，如果是的话就会走到相应的**工具节点ToolNode**，然后工具节点将工具的执行结果包装成一个工具信息添加到messages的最后，执行完工具后会再回到大模型，把messages发给大模型，大模型会再回复我们一个AI信息，condition条件边会再判断AI信息里要不要调用tool，...，就变成了一个循环，只要需要调用工具就会一直调用工具，直到不需要调用工具为止；





<img src="D:\Courses\学习笔记\带工具调用的流程图.png" style="zoom:70%;" />

### 把工具节点添加到流程图

定义获取时间的工具函数，添加函数文档

`@tool` 让 AI 知道有一个获取精确时间的工具可用，当用户询问时间相关问题时，AI 会自动调用这个函数来获取真实时间，而不是自己猜测。

将定义好的工具（get_time）添加到工具列表里，`tools = [get_time, search_knowledge_base]`

将工具列表绑定到大模型上，

```python
tools = [get_time, search_knowledge_base]
llm = ChatOpenAI(xxx).bind_tools(tools)
```

定义工具节点：ToolNode()，lang_graph自己实现的，会根据AI的信息调用对应的函数；

tool_calls是lang_graph自己定义的，如果有工具需要调用就会将其放到这个tool_calls对象上；

LangGraph 将智能体工作流建模为一张“图”。这张图有三个关键组成部分：

- **节点 (Nodes)**：代表具体的工作单元，比如“调用大模型”、“执行一个工具”或“发送一封邮件”。
- **边 (Edges)**：定义节点之间的连接，决定了工作流的执行路径。
- **状态 (State)**：一个在所有节点间共享的数据结构，用于传递和存储信息。

![](D:\Courses\学习笔记\现在几点了演示.png)

<img src="D:\Courses\学习笔记\现在几点了前端效果.png" style="zoom:50%;" />

第一次：把系统提示词+用户消息发送给llm，llm返回tool_calls中值为get_time，

于是，进入工具节点tool_node：ToolNode，工具节点将执行结果ToolMessage添加到状态中；

第二次：把State再次传递给llm，llm组织好数据后，返回给前端；

什么叫function call？

class Message保存每一轮对话的内容。

<img src="D:\Courses\学习笔记\长期记忆agent流程图.png" style="zoom:80%;" />

## 添加长期记忆

将总结长期记忆的系统提示词保存到到SystemPrompt，title="记忆"；

长期记忆保存在好友关系（Friend.Memory）中；

创建新的软件包memory，即新的流程图

backend/web/views/friend/message/memory/graph.py 长期记忆的计算流程图

backend/web/views/friend/message/memory/update.py 调用长期记忆的计算流程图

长期记忆模块不需要返回给用户，因此不需要采用流式，

让大模型总结长期记忆时，也需要一个总结的系统提示词，然后再加上原始记忆、最近对话，一起发给llm。

每次在MessageChatView中创建完消息后，调用更新记忆模块；

同时注意，在组织**聊天**的系统提示词时，需要加上这个长期记忆

```python
# backend/web/views/friend/message/chat/chat.py
# 添加系统提示词
def add_system_prompt(state, friend):
    prompt += f'【长期记忆】\n{friend.memory}\n'
```



 **LangGraph 的节点定义非常灵活**，只要是一个**可调用对象（callable）**，都可以作为节点。

`add_node()` 接受任何**可调用对象**，包括：

- 普通函数（如 `model_call`）
- 类实例（如果实现了 `__call__` 方法）
- 任何实现了 `__call__` 的对象（如 `ToolNode` 实例）

长期记忆和短期记忆什么区别？

短期记忆就是最近10轮对话；长期记忆是记忆模块计算流程图总结得到的；

每次在组织传给llm的消息`inputs`时，采用系统提示词（SystemPrompt）+角色性格（friend.character.profile）+长期记忆（friend.memory）+最近十轮对话（Message）+用户消息（request.data['message']）的格式

langchain_openai这个python软件包是在什么章节install的？

总结：所谓长期记忆就是新建一个流程图，让大模型按照指定的规则总结最近的消息。

## 知识库

知识库是干嘛的呢？
大模型不是万能的，不能知道最新的消息、不能知道某个垂直领域的知识，当我们问他某些垂直领域的知识时，可以给他外挂一个知识库（硬盘），这就是知识库。
大模型从知识库里检索信息之后，再去回答，这个过程称为RAG(**Retrieval-Augmented Generation 检索增强生成**)。有一个很重要的问题就是如何存知识库？现在比较常用的是用向量数据库来存知识库，

知识库可能很大，几十M、几十G，使用向量数据库可以很快帮助我们找到语义相关的文档。

如何把段落转换成向量，可以使用embedding模型实现。

向量数据库可以很方便地去存这些向量，然后很方便地去查找距离某个向量最近的向量，

向量的夹角可以反应语义的相关性，



安装pip install ipython便于交互，安装速度很慢，可以换源。

```shell
pip install ipython
```

### 创建、查询向量数据库

本地LanceDB数据库调用阿里云text-embedding-v4模型将文本转换为 1024 维向量；

embed_documents、embed_query为重载基类Embeddings的函数；

创建

```
原始文档 (data.txt)
      ↓
[1. 加载文档]
      ↓
Document 对象
      ↓
[2. 文本切分] chunk_size=500, overlap=50
      ↓
文本片段列表 (chunks)
      ↓
[3. 向量化] 调用阿里云 API
      ↓
向量列表 (每个 chunk → 1024维向量)
      ↓
[4. 存储到 LanceDB]
      ↓
向量数据库表 (本地文件)
```

查询

```
用户问题: "什么是深度学习？"
      ↓
[1. 查询向量化] 调用阿里云 API
      ↓
查询向量 (1024维)
      ↓
[2. 相似度计算] LanceDB 本地执行
   (余弦相似度/欧几里得距离)
      ↓
[3. 找出最相似的 k 个向量]
      ↓
[4. 返回对应的原始文本]
      ↓
最相似的文档片段列表
```

**创建向量数据库** = 调用 API 将文档转为向量后存入本地；
**查询向量数据库** = 调用 API 将问题转为向量后在本地找最相似的文档。
两次都需要调用 Embedding API，因为向量数据库只懂向量，不懂文本。

### 添加新的工具节点

实现search_knowledge_base，并将其添加到工具列表：tools = [get_time, search_knowledge_base]

所谓的检索增减生成也是一个tool函数，由lang_graph识别到然后去调用。



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

automatic speech recognition (ASR) 语音识别；

Text-to-Speech (TTS) 语音合成；

文本生成大模型：文字**非流式**输入、文字流式输出；使用sse

语音识别大模型：语音流式输入、文字流式输出；websocket

语音合成大模型：文字流式输入，语音流式输出；websocket

<img src="D:\Courses\学习笔记\语音模块架构图.png" style="zoom:80%;" />

2个简化

1）浏览器到服务器的流式改为非流式

client给server发消息由流式改为非流式后，可以不用在django中实现websocket，

2）把后端语音识别的结果先发给前端，前端再重新调用一遍后端

这样，语音回复、文字回复都可以复用语音识别后这段代码逻辑了。前端语音也是调用handleSend函数

由于网络请求的时间远远小于大模型生成结果的时间，所以加这一段（2个网络延迟）区别不是很明显。

## 语音识别

### 前端浏览器实现语音输入

**实现当我们说话时，打断ai的回复**
增加processId标识对话的版本号，比如在第7轮对话，全局变量processId=7，回复了一半时，我又输入一段文字，开启了第8轮对话，此时processId=8，但是第7轮对话里curId的仍为7，在onmessage中，curId !== processId就直接退出了，不会再向下执行了。

只要更新版本号processId，就不再接受新消息了。

InputField.vue包括文本输入模块（<form />）和语音输入模块（<Microphone />）

引用语音监测模块，AI实现

<Microphone />组件挂载时即调用startRecording()，当监测到说话时调用onSpeechStart上的匿名函数；当监测到说话结束了，就会调用onSpeechEnd上的匿名函数：把数据发送给后端（sendToBackend）调用语音识别接口。

将pcm格式的语音发送给后端/api/friend/message/asr/asr/；

语音识别成功返回后调用handleSend将文字再发送给后端；因此需要将handleSend以事件的形式传给子组件；

### 实现后端语音识别

语音相关的大模型一般都是用websocket来调用，后端安装websocket包：`pip install websockets`

语音识别、语音合成的url都是`WSS_URL`

后端实现ASRView

websocket协议可以传字节，也可以传文本；sse只能传文本；



<img src="D:\Courses\学习笔记\后端与大模型语音识别交互逻辑.png" style="zoom:80%;" />

可以发现，在与大模型语音识别的交互过程中，一个线程是无法实现发送消息的同时接收消息，在python使用协程实现即可，一个协程负责发送，另一个协程负责接受。

后端大部分时间都是在等待网络请求上，比如给大模型发送完消息后，大模型产生消息其实是比较慢的，大模型给我们回复消息就是IO，协程就是一旦我们遇到IO语句的时候就会把当前任务挂起，然后去执行其他的请求，其实是在一个线程里，

语音识别：ASR

阿里云ASR文档：https://bailian.console.aliyun.com/cn-beijing/?spm=5176.12818093_47.console-base_product-drawer-right.dproducts-and-services-sfm.258b16d0dZyCzu&tab=api#/api/?type=model&url=2869339

由于django主要支持异步，而websocket是异步调用，所以使用asyncio.run()做了一个桥接。**简单说**：这是**同步世界和异步世界之间的桥接模式**。虽然效果上都是等待，但它让你能：

1. 保持 Django 视图的同步 simplicity
2. 复用已有的异步代码
3. 利用异步库的功能

阿里云建议每次发送100ms的音频，我们采用的是pcm16音频格式，用16位（2字节）来表示一次采样，采样频率是16000hz，1s16000次，所以1s是采样16000✖️2=32000字节，那么100ms就是3200字节。

asr_receiver时，只有语音识别结果有值且`output['transcription']['sentence_end']`为true时才使用这个文本，其实比如微信翻译，会传过来很多识别结果而且后边的会修改前边的识别结果，我们只需要使用最终的翻译结果（'sentence_end'）即可。

异步生成的结果不能同步给生成器，

添加后端url: 'api/friend/message/asr/asr/'

协程的核心机制：事件循环

```python
import asyncio
import time

# 定义协程函数
async def task(name, duration):
    print(f"{name} 开始: {time.strftime('%X')}")
    await asyncio.sleep(duration)  # 模拟I/O
    print(f"{name} 结束: {time.strftime('%X')}")
    return name

# 执行
async def main():
    # 事件循环开始工作，并发执行多个协程
    tasks = [
        task("A", 2),
        task("B", 1),
        task("C", 3)
    ]
    
    # 事件循环调度这三个任务
    results = await asyncio.gather(*tasks)
    
asyncio.run(main())

# 执行结果如下
A 开始: 22:59:52
B 开始: 22:59:52
C 开始: 22:59:52
B 结束: 22:59:53
A 结束: 22:59:54
C 结束: 22:59:55
```

## 语音合成

发送的文本，返回的是二进制音频；





<img src="D:\Courses\学习笔记\语音合成流程图.png" style="zoom:80%;" />





- **`async def`**：声明这个函数可以"异步执行"
- **`async for`**：声明这个循环的每次迭代都可能"等待数据"

使用 **`async` + `await`** 声明函数为异步，表明该函数内**遇到 `await` 阻塞**时可以将该函数挂起，转而执行函数外其他的代码

明确一下，当前端通过语音聊天时，语音读取完后是自动调用api/friend/message/asr/asr/语音识别api的，然后返回给前端后紧接着调用前端handelSend函数，再次调用api/friend/message/chat/进行聊天的，所以后端chat.py中仅涉及与文本大模型、语音合成大模型（cosyvoice-v3-flash）交互，并不会与语音识别大模型（gummy-realtime-v1）交互！！！

先与语音合成大模型建立websocket连接，然后使用2个协程同步发送文本、接收音频；

后端**动态判断并分发不同类型的数据**；**前端如何响应**：前端 JavaScript 代码会持续监听这个 SSE 流。每当收到一个 `data:` 行，它就会解析 JSON，然后检查其中是包含 `content` 字段还是 `audio` 字段，从而决定是渲染文字，还是播放音频。这种设计使前端可以根据数据类型做出不同的响应。

将音频使用base64编码成文本，因为SSE是基于文本，不认识二进制协议；

消息队列中既有文本也要音频，都发给前端，由前端识别处理。

对于同一个 WebSocket 连接，接收到的消息顺序与发送顺序**严格一致**。这是由 WebSocket 底层的 TCP 协议保证的

`async for` 是**严格的顺序迭代器**，必须等当前消息处理完（或遇到 `break`/`return`）才能处理下一个消息。消息的处理顺序就是它们的到达顺序。

`async for` 实现了"异步接收，同步处理"的模式——接收时可以等待（不阻塞），但处理时必须按顺序一个一个来。

前端播放音频，每次得到音频调用handleAudioChunk函数

音频缓冲区sourceBuffer在初始化的时候绑定了一个监听器mediaSource.addEventListener



上线的时候是用nginx部署的



# 7. 项目上线

模态框自动绑定了按esc键关闭。

## 1）租云服务器

租阿里云服务器，公网ip：8.130.157.21

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



**源码安装Python3.14解释器**：是指从 Python 官网下载 **源代码**，然后在你的操作系统上用编译器手动构建出 Python 解释器（`python` 命令）的过程。

```shell
# 将下载好的python软件包上传到服务器
scp .\Python-3.14.3.tar.xz llm:
# 解压
tar -xvf Python-3.14.3.tar.xz
```

源码安装，**Python 的标准实现（CPython）是用 C 语言编写的**

```shell
# 统计耗时
time ./configure --enable-optimizations
sudo make altinstall # 不会覆盖系统路径下原有的，而是创建一个指定版本的
```

**在云端重新安装本地Python环境**

把本地的python包在云端重新安装一遍

在本地导出python安装过的所有包及其版本号：

```shell
# 在AIFriends目录下执行：
pip freeze > requirements.txt
```

然后将`requirements.txt`上传到云服务器上。把这个文件中所有的包都安装一遍。

然后在云服务上执行：`pip3.14 install -r requirements.txt --user`。安装到用户目录





## 2）将本地项目部署到云端

### 本地修改

将前端网站的vue图标logo修改为自己的图片：修改frontend/public/favicon.ico为自己的图片

**把公网IP地址关联一个域名**

```python
# backend/backend/settings.py
# 告诉 Django：只接受来自本机 (127.0.0.1) 和你线上域名 (app1565.acapp.acwing.com.cn) 的请求，其他来源的请求都会被安全地拒绝。
ALLOWED_HOSTS = ['127.0.0.1', 'app1565.acapp.acwing.com.cn']
```

- **静态文件**：属于代码的一部分，由开发者提供（如 `style.css`、`logo.png`）
- **媒体文件**：属于用户数据，由用户上传（如头像、帖子图片）

配置前端：frontend/src/js/config/config.js

访问域名是怎么访问到具体端口号的呢？https就是443端口，hppt就是80端口；

在服务器上配置一个 **Nginx** 或 **Apache**，让它“守卫”在 80/443 端口，并设置规则：**“凡是访问域名 app1565.acapp.acwing.com.cn 的请求，都转发给本地 8000 端口上的 Django 程序处理。”**


打包完前端后，前端的所有的包就都放到backend/static/frontend/assets/index-BI_WbIZS.js了，所以不需要在云服务器上安装vue环境。

记得重置数据库密码

假如在 Django 中忘记管理员密码，最直接和安全的方法是通过命令行来修改

```bash
python manage.py shell
```

```
# 1. 导入 User 模型
from django.contrib.auth.models import User

# 2. 查找你的用户对象（根据用户名）
user = User.objects.get(username='your_username')

# 3. 检查用户是否找到（可选）
print(user.username, user.email)

# 4. 设置新密码（Django 会自动处理加密）
user.set_password('your_new_strong_password')

# 5. 保存到数据库
user.save()

# 6. 退出 Shell
exit()
```

### 上传项目到云端

在AIFriends目录下上传后端代码：

`scp -r backend llm:`比如数据库、知识库、静态文件都要从本地上传到云端。

我的域名：https://app1565.acapp.acwing.com.cn

```bash
django-admin --version
6.0.1
python3.14 --version
Python 3.14.3

# 修改backend/settings.py文件：
DEBUG = False

# 收集静态文件：
python3.14 manage.py collectstatic
```

**部署项目**

让项目运行起来

### 配置gunicorn

运行`gunicorn`，在`/home/acs/backend/`目录下执行：

```
gunicorn --workers 3 --graceful-timeout 3 --bind unix:/home/acs/backend/gunicorn.sock backend.wsgi:application
```

nginx已经运行，这时就可以访问域名了。

### 配置nginx

安装nginx：

```shell
sudo apt update
sudo apt install nginx
# 列出 nginx 包安装的所有文件
dpkg -L nginx
# 查看 nginx 命令位置
which nginx
# 或使用 whereis
whereis nginx
# 查看 nginx 包的详细信息
apt show nginx
# 如果想知道卸载时会删除哪些文件
sudo apt remove nginx --dry-run
# 彻底删除（包括配置文件）
sudo apt purge nginx
# 删除依赖和配置文件
sudo apt autoremove --purge nginx
```

**配置nginx反向代理**

将https证书复制到自己的服务器上，每年11月份左右要手动更新：

/etc/nginx/cert/acapp.key
/etc/nginx/cert/acapp.pem

/etc/nginx/nginx.conf会用到上述2文件。

配置/etc/nginx/nginx.conf：

```
xxx
http {
    server {
        listen 443 ssl;
        server_name app1565.acapp.acwing.com.cn;  # 替换成自己的域名

        ssl_certificate     /etc/nginx/cert/acapp.pem;
        ssl_certificate_key /etc/nginx/cert/acapp.key;
    }
}
```

这是一个符合生产环境标准的 Nginx 配置，它安全、高效地将 HTTP 流量升级为 HTTPS，并分工明确地处理了静态文件和 Django 动态请求。

所有 HTTPS 请求确实都发往 443 端口，Nginx 根据请求头中的 `Host` 字段（即域名）来区分它们，然后转发给不同的后端服务。这就是你可以在同一台服务器上运行多个网站的核心原理。

当业务大到需要多台 Nginx 时，引入 F5/LVS 来监听 443，然后把流量分发给多台 Nginx，如下：

```
用户 → [443] → LVS 负载均衡器 (1台)
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
    Nginx 1     Nginx 2     Nginx 3
    (内部端口)   (内部端口)   (内部端口)
        ↓           ↓           ↓
      Django      Django      Django
```

加载nginx配置：

`sudo nginx -s reload`

## 3）语音复刻

定义class Voice数据库，存所有的音色列表；主要就是维护一个voice_id属性；

音色列表：https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list?spm=a2c4g.11186623.0.0.3e867741hUe7K7

在前端的await中，当执行到 await 时，程序并不会“卡死”等待，而是会“让出控制权”，让浏览器继续处理其他任务，等网络请求完成后再回来继续执行。

所谓让角色按照某个音色讲话，就是在语音合成的时候传递一个**voice_id**，语音合成模型利用这个voice_id生成带音色的音频。

在前端使用的是自定义当的id，在对接大模型时使用的是voice_id。

前端更新角色信息、创建角色信息时都要传voice.id，后端使用这个id从数据库表Voice中查询

Friend有character成员，在过滤的时候可以直接使用character_id

```
Friend.objects.filter(character_id=character_id, me=user_profile)
```

这种方式过滤

这个cosyvoice-v3-flash是语音合成大模型。

语音复刻的url：`VOICE_URL="https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"`



**语音复刻**

```shell
In [2]: from web.views.create.character.voice.custom.create_voice import create_voice
vs = [1, 2, 4, 6, 7, 8]
for v in vs:
	print(create_voice(f'https://app1565.acapp.acwing.com.cn/media/tmp/{v}.mp3', v))

```

**复刻自己的声音**

录音，然后上传到服务器，在本地调用create_voice()会生成一个voice_id，把这个voice_id保存到数据库表Voice中。

查看自己所有的voice，调用list_voice，底层也是向VOICE_URL发送一个请求，请求头中携带自己API_KEY、action动作。

**把项目上传到云端**

修改config.js为`cloud`

然后打包 `npm run build`

删除云端backend，这会导致云端已有的数据被删除 `rm -r backend/`

重新上传项目 `scp -r backend llm:`

修改云端的settings.py中的 `DEBUG = False`

收集静态文件

```
xx@xxx:~/backend$ python3.14 manage.py collectstatic
```

`collectstatic` 就像**把所有散落在各地的静态文件"打包"到一个文件夹**，方便 Nginx 一次性找到并高效提供访问。

以后维护项目，尽量只把代码上传，数据库不要删除。

启动gunicorn

```
xx@xxx:~/backend$ gunicorn --workers 3 --graceful-timeout 3 --bind unix:/home/acs/backend/gunicorn.sock backend.wsgi:application
```

统计代码量：

```
# 前端
# src目录下统计js
$ find ./ -name '*.js' | wc -l
$ find ./ -name '*.js' | xargs cat | wc -l
379
# 统计vue
$ find ./ -name '*.vue' | xargs cat | wc -l
2491
# 后端
$ find ./ -name '*.py' | xargs cat | wc -l
1700
# 总共约4500行代码
```



