这是一个初步的demo。

我暂时使用的框架是前端VUE后端Flask，语言的话前端是JavaScript，后端是python3. 如果到时候需要更改，我再调整。

重要！！！！！！需要下列package，必不可少，我是mac的，给的是unix shell的指令，windows我不太清楚：
npm - https://www.npmjs.com/get-npm 这个是nodejs的集成安装包，需要下载安装配置，如果不行可以使用yarn代替
vue -  	npm install -g @vue/cli
		yarn global add vue-cli
Flask - pip install flask
Flask_cors - pip install flask_cors

我把前后端初步的框架写好了，在root（demo文件夹）下分了frontend 和 backend
运行方法：
先跑server：
$cd backend
$python3 backend_test.py
出现 Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) 即为成功
然后跑client:
$cd frontend
$cd projectlabdemo
$npm install
$npm run dev
忽视所有的eslint的warning，光标闪烁没有且只有eslint的error即为成功
然后打开browser，输入localhost：8080，能看到Welcome to Your Vue.js App 即为成功

前后端链接的demo在localhost:8080/#/flaskTovue，能看见Waiting for server response 和一个按钮
摁一下，会弹出alert，出现Success 200, [object Object], Hello, This is a simple demo!即为成功
如果出现Error，尝试清空cookie再试一次，或者换个浏览器。
点击确定后，按钮前的文字会变成后端发来的文字demo。

