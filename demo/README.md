这是一个初步的demo。

我暂时使用的框架是前端VUE后端Flask，语言的话前端是JavaScript，后端是python3. 如果到时候需要更改，我再调整。

重要！！！！！！需要下列package，必不可少，我是mac的，给的是unix shell的指令，windows我不太清楚：
* npm - https://www.npmjs.com/get-npm 这个是nodejs的集成安装包，需要下载安装配置，如果不行可以使用yarn代替
* vue
    * npm install -g @vue/cli
    * yarn global add vue-cli
* Flask - pip install flask
* Flask_cors - pip install flask_cors

我把前后端初步的框架写好了，在root（demo文件夹）下分了frontend 和 backend
运行方法: (在demo路径下)
1. 运行server
    * 安装配置：python/python3 dashboard.py install (for Mac) / py -3 dashboard.py install (for Windows)
    * $export FLASK_APP=backend (for Mac) / set FLASK_APP=backend (for Windows)
    * $export FLASK_ENV=development (for Mac) / set FLASK_ENV=development (for Windows)
    * flask run
    * 出现 Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) 即为成功
2. 然后跑client:
    * $cd frontend
    * $cd projectlabdemp
    * $npm install
    * $npm install bootstrap@4.6.0 bootstrap-vue@2.21.2 (安装bootstrap for Vue）
    * $npm run dev
    * 忽视所有的eslint的warning，光标闪烁没有且只有eslint的error即为成功
    * 然后打开browser，输入localhost:8080，能看到Welcome to Your Vue.js App 即为成功

前后端链接的demo在localhost:8080/#/flaskTovue，能看见Waiting for server response 和一个按钮
摁一下，会弹出alert，出现Success 200, [object Object], Hello, This is a simple demo!即为成功
如果出现Error，尝试清空cookie再试一次，或者换个浏览器。
点击确定后，按钮前的文字会变成后端发来的文字demo。
