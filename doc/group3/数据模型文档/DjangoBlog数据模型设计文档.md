# 小组③：DjangoBlog数据模型设计文档
## 1 文档概述
本文档针对DjangoBlog博客系统`blog/models.py`源码进行分析，梳理系统全部数据模型、字段、继承关系、实体之间关联关系，用于第五周小组作业。
源码位置：`blog/models.py`。

## 2 总体模型架构说明
系统存在抽象基类`BaseModel`，**抽象模型不会生成数据库表**，只提供公共字段与公共方法；
`Article`、`Category`、`Tag` 继承`BaseModel`，自动获得主键id、创建时间、修改时间、获取绝对地址等通用能力。
`Links`、`SideBar`、`BlogSettings`直接继承Django原生`models.Model`，不继承BaseModel。

### 继承关系
1. BaseModel(abstract抽象类)
    - Article（文章）
    - Category（分类）
    - Tag（标签）
2. models.Model
    - Links（友情链接）
    - SideBar（侧边栏组件）
    - BlogSettings（网站全局配置）

## 3 各个模型字段详细说明
### 3.1 BaseModel 抽象基类
> 抽象类，不建表，供其他模型继承
|字段|字段类型|说明|
|---|---|---|
|id|AutoField|主键自增id|
|creation_time|DateTimeField|创建时间，默认当前时间|
|last_modify_time|DateTimeField|最后修改时间，默认当前时间|

**核心方法**
- `save()`：重写保存逻辑，自动生成slug别名；处理文章浏览计数更新
- `get_full_url()`：获取实体完整访问url
- `get_absolute_url()`：抽象方法，子类必须实现，获取相对访问地址

### 3.2 Article 文章模型
> 博客核心文章/页面数据表，继承BaseModel
|字段|字段类型|说明|
|---|---|---|
|title|CharField|文章标题，唯一，最大200字符|
|body|MDTextField|Markdown格式文章正文内容|
|pub_time|DateTimeField|文章发布时间|
|status|CharField|状态：d草稿 / p已发布|
|comment_status|CharField|评论状态：o开启 / c关闭|
|type|CharField|类型：a文章 / p页面|
|views|PositiveIntegerField|浏览量，默认0|
|author|ForeignKey|外键关联系统User用户，一对多，级联删除；**一个用户可以写多篇文章**|
|article_order|IntegerField|文章排序权重|
|show_toc|BooleanField|是否显示目录|
|category|ForeignKey|外键关联Category分类，一对多级联删除；**一个分类下有多篇文章**|
|tags|ManyToManyField|多对多关联Tag标签；**一篇文章多个标签，一个标签可以给多篇文章打标**|

**重要方法**
- `viewed()`：浏览数+1
- `comment_list()`：获取已开启的评论列表，带缓存
- `next_article()`、`prev_article()`：获取上一篇、下一篇文章
- `get_first_image_url()`：提取正文里第一张图片地址

### 3.3 Category 文章分类模型
> 文章分类，支持多级父子分类，继承BaseModel
|字段|字段类型|说明|
|---|---|---|
|name|CharField|分类名称，唯一，最大30字符|
|parent_category|ForeignKey|自关联外键，指向自己，可为null；实现父子分类结构|
|slug|SlugField|url访问别名|
|index|IntegerField|排序序号|

**核心方法**
- `get_category_tree()`：递归向上获取全部父级分类
- `get_sub_categorys()`：递归向下获取全部子分类

### 3.4 Tag 标签模型
> 文章标签，继承BaseModel
|字段|字段类型|说明|
|---|---|---|
|name|CharField|标签名称，唯一，最大30字符|
|slug|SlugField|url访问别名|

**核心方法**
- `get_article_count()`：统计该标签关联多少篇文章

### 3.5 Links 友情链接模型
> 不继承BaseModel，直接继承models.Model
|字段|字段类型|说明|
|---|---|---|
|name|CharField|链接名称，唯一|
|link|URLField|跳转url地址|
|sequence|IntegerField|排序序号，唯一|
|is_enable|BooleanField|是否启用展示|
|show_type|CharField|展示位置：首页/列表页/文章页/全部/轮播|
|creation_time|DateTimeField|创建时间|
|last_mod_time|DateTimeField|修改时间|

### 3.6 SideBar 侧边栏模型
> 自定义HTML侧边栏模块
|字段|字段类型|说明|
|---|---|---|
|name|CharField|侧边栏模块标题|
|content|TextField|侧边栏HTML内容|
|sequence|IntegerField|排序序号，唯一|
|is_enable|BooleanField|是否启用|
|creation_time|DateTimeField|创建时间|
|last_mod_time|DateTimeField|修改时间|

### 3.7 BlogSettings 网站配置模型
> 网站全局配置，**数据库只允许存在一条记录**
|字段|字段类型|说明|
|---|---|---|
|site_name|CharField|网站名称|
|site_description|TextField|网站描述|
|site_seo_description|TextField|SEO描述|
|site_keywords|TextField|SEO关键词|
|article_sub_length|IntegerField|文章摘要截取长度|
|sidebar_article_count|IntegerField|侧边栏文章展示条数|
|sidebar_comment_count|IntegerField|侧边栏评论展示条数|
|article_comment_count|IntegerField|文章页面评论条数|
|show_google_adsense|BooleanField|是否开启广告|
|google_adsense_codes|TextField|广告代码|
|open_site_comment|BooleanField|全局是否开启评论功能|
|global_header|TextField|全局头部自定义代码|
|global_footer|TextField|全局底部自定义代码|
|beian_code|CharField|网站备案号|
|analytics_code|TextField|统计代码|
|show_gongan_code|BooleanField|是否显示公安备案|
|gongan_beiancode|TextField|公安备案号|
|comment_need_review|BooleanField|评论是否需要审核|

> clean方法做校验，数据库只能保存一条网站配置记录。

## 4 模型实体关系分析
1. **User ↔ Article（一对多）**：一个用户可以有多篇文章；一篇文章只能属于一个作者。外键在Article表。
2. **Category ↔ Article（一对多）**：一个分类包含多篇文章；一篇文章归属一个分类。外键在Article表。
3. **Category ↔ Category（自关联一对多）**：分类支持父子级，一个父分类下有多个子分类。外键`parent_category`在Category表。
4. **Article ↔ Tag（多对多）**：一篇文章可以打多个标签，同一个标签可以作用多篇文章；Django自动生成中间关联表。

> Links、SideBar、BlogSettings和其他模型没有外键关联，属于独立配置表。

## 5 UML类图
![UML类图](./小组③：DjangoBlog数据模型UML类图.png)

> 将draw.io导出的UML类图png图片，和本md文档放在同一个文件夹，即可正常显示图片。

## 6 小结
1. BaseModel抽象类封装公共字段，减少重复代码，是Django模型抽象继承典型用法。
2. Article作为业务核心，通过外键、多对多完成与用户、分类、标签的关联。
3. Category自引用实现多级分类。
4. Links、SideBar、BlogSettings属于系统配置类模型，负责页面展示、网站全局参数。
