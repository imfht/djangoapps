这篇文章将简单地描述一下博客的搭建过程。博客源代码见[这里][blog]  
首先要感谢stevelosh, 博客的基本设计参考了他的博客，来源于[stevelosh.com][sl] 这篇文章。  
博客从2013.8开始搭建，暑假主要处于学习阶段，学期途中插空写了一点，2014寒假把基本框架完成了。  
对于想基于代码学习/搭建博客的行为，本人不能够更欢迎，但是请至少做到：  
**在运行之前修改`settings.py`**，再不济，请至少把这里的**email替换成你自己的email**
```python
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('laike9m', 'laike9m@gmail.com'),
)
```
否则，你的代码运行时的出错信息将被发送到我的邮箱，不利于你进行调试，也给我带来极大困扰。不胜感激！！

之前忘记提到，由于我一开始就使用 Py3，所以代码在很多地方都是 Py2 不兼容的，比如某位 fork 了代码的同学发现不能成功创建文章。排查了一下错误，发现是因为`My_Blog/css3two_blog/models.py`中有这么一段代码：
```python
if type(self.body) == bytes:  # sometimes body is str sometimes bytes...
     data = self.body
elif type(self.body) == str:
     data = self.body.encode('utf-8')
```
在 Py3里面，这么写就 cover 了`self.body`的所有可能情况， data 肯定会被赋值。但是那位同学发现`data`最后是未定义的，为什么呢？因为他用的是 Py2，所以`body`是`unicode`，自然不行。  
所以建议是，直接采用 Py3 来运行我的 blog，或者 fork 一份然后做一些 Py2 compatible 的修改（我也不知道哪些地方要改）。

设计
---
在博客搭建之初，我就决定要**尽可能少写前端代码**。最简单的方法自然是使用CMS。实际上有不少使用Django的CMS，比如最著名的[django CMS][django-cms]。不过调研一番之后发现一个问题：没有一个支持Python 3。考虑到博客里必然有一堆Unicode字符，我还是希望能用Python 3的，所以就放弃了CMS。  
（2014.6.25 EDIT: 目前发现django CMS已经能支持Python3.4了，至少3.0.2版本以及更新的都可以。参见[3.0.2 release][3.0.2]）  
好在马上找到了替代品：HTML模版。最后使用了[css3templates][templates] 里面的一个模板。模板基本只包含HTML/CSS/JS代码，这正是我需要的东西，因为后端本来就是想从零开始写的。  

文件路径结构
----------
用Django建网站，`static` 和 `media` 到底怎么放置？这个问题没有标准答案，反正我没有用 `STATICFILES_DIRS`，也就是把所有static files都放在了`appname/static/appname` 里面。这样的好处是文件结构比较清晰，坏处是如果app多了同样的文件可能要存很多份，会减慢网站加载速度。下面是我的文件夹结构，供参考，文件均未列出：

	my_blog
	├─media
	│  ├─content
	│  │  └─BlogPost
	│  │      ├─2009
	│  │      ├─2013
	│  │      ├─2014
	│  │      └─images
	│  └─files
	├─My_Blog
	│  ├─css3two_blog
	│  │  ├─migrations
	│  │  ├─static
	│  │  │  └─css3two_blog
	│  │  │      ├─documentation
	│  │  │      ├─fonts
	│  │  │      ├─images
	│  │  │      └─js
	│  │  └─templates
	│  │    └─css3two_blog
	│  ├─mytemplatetags
	│  │  └─templatetags
	│  ├─my_blog
	│  └─templates
	│      └─admin
	└─static
	    ├─admin
	    │  ├─css
	    │  ├─img
	    │  │  └─gis
	    │  └─js
	    │     └─admin
	    └─css3two_blog
	        ├─documentation
	        ├─fonts
	        ├─images
	        └─js

画这个东西的时候才知道Windows/Linux下有个命令叫 [`tree`][tree]，大好评！  
注意在开发的时候，`my_blog/static` 里面可以不放东西，只要 `DEBUG=True` 就行。如果要接受文件上传，那么在 `urlpatterns` 后面添加：   
```python
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```  
实际部署时该怎么来就怎么来。  
有一个 app 叫做 `mytemplatetags`，它是专门用来装 custom template tags/filters 的，参见 [官方文档：Custom template tags and filters][customtag].
[tree]:http://stackoverflow.com/questions/347551/what-tool-to-use-to-draw-file-tree-diagram
[customtag]:https://docs.djangoproject.com/en/1.6/howto/custom-template-tags/

主机
---
在哪里买主机是个需要好好思考的问题。使用VPS的话，可选择的范围很大。但是第一次建网站，没什么经验，怕配置不好。更重要的是用VPS不够短平快，而我希望博客能尽快投入使用。然后就查到了[WebFaction][wf]。虽然我并不想做广告，但真的向大家推荐这个主机服务，尤其是怕麻烦的人。Webfaction是个PaaS服务，支持许多语言/框架，而且服务很完善，不论是在它的 [Q&A Community][QA] 提问还是open a ticket，工作人员的解答都很迅速。虽然是美国的主机（也可以选东南亚的），但是国内访问速度不错。至于其它选择，外国人用 [heroku][h] 的比较多。国内主机不太了解，`SAE` 据说不错。
(**UPDATE**: 现在我已经用了两年多 [**DigitalOcean**](https://m.do.co/c/a582fa751343)，感觉还是非常不错的，参见[《决定转投 DigitalOcean》](https://laike9m.com/blog/jue-ding-zhuan-tou-digitalocean,73/))

[h]: https://www.heroku.com/

版本控制
-------
显然是Git+Github，没什么好说的。印象深刻的是有一次在主机上玩火敲了这个命令 `find . -not -name 'xxx' | xargs rm`，结果大家都懂。还好WebFaction重建一个Django app就是点击几下的事情，代码又在Github上，所以很容易就恢复了。  
还有，`settings.py` 这个文件最好ignore掉，因为部署和开发在设置上差异很大，所以这个文件在本地和服务器上需要保存不同的版本。顺便分享一下 `.gitignore` 吧：

    .pydevproject
    .project
    .settings/*
    db.sqlite3
    css3two_blog/migrations/*
    css3two_blog/static/css3two_blog/css/unused/*
    *.pyc

为什么`settings.py`没有包含在内呢？这个问题比较复杂，在我的另一篇文章 [Django Best Practice: How to deal with settings.py in Git][settings] 里面有详细讲述。
[settings]:http://www.laike9m.com/blog/django-best-practice-how-to-deal-with-settingspy-in-git,27/

使用Markdown
------------
这是跟stevelosh学的，而且似乎越来越多的个人博客都在这么做。我的每一篇文章都是用markdown写的，然后渲染成html。关于如何渲染有不同的做法，一开始尝试了`pygments` + `django markup`，虽然可以实现代码高亮不过样式比较难看。目前采用的方法是把markdown文本发送给Github API，得到 `gfm` 格式的html。需要注意的是得到的 html 是没有样式的，所以又在网上找了别人写的 gfm 的 css，添加到页面里，显示出来的页面就和 Github 的 README 差不多了。  
这部分的工作有一定难度，需要设计出一套 markdown 和 html 文件的保存机制，并且能正常应对 `admin` 界面中的修改/删除操作。具体可见
[`models.py`][models]，[`admin.py`][admin]

其它
---
1. 使用 [`south`][south] 来应对 `Model` 的变更
2. 尽量把逻辑放在 `models` 和 `views` 来完成，因为Django的 `templates` 实在很难用
3. 虽然用了 HTML 模版，但是在前端仍然花了很多时间
4. 博客完全可以用 [`Hyde`][hyde] 搭建，这样加载起来能快一些

<br>
> 初版：2014-2-5    
> EDIT：2014-2-20 加入**文件路径结构**小节，增补其它小节内容  
> EDIT：2014-6-25 django CMS 已经支持 Python3.4  
> EDIT：2014-8-29 强调了博客只支持 Py3  


[blog]: https://github.com/laike9m/My_Blog
[sl]: http://stevelosh.com/projects/stevelosh-com/
[django-cms]: https://www.django-cms.org/en/
[3.0.2]: https://www.django-cms.org/en/blog/2014/05/21/302-release/
[templates]: http://www.css3templates.co.uk/templates.html
[wf]: https://www.webfaction.com/?aid=49199
[QA]: https://community.webfaction.com/
[models]: https://github.com/laike9m/My_Blog/blob/master/css3two_blog/models.py
[admin]: https://github.com/laike9m/My_Blog/blob/master/css3two_blog/admin.py
[south]: http://south.aeracode.org/
[hyde]: http://hyde.github.io/
