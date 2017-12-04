/*=============================================*/
/*    西邮Linux兴趣小组官网 数据库设计            */
/*    version：0.1                             */
/*    mysql：  5.x above                       */
/*    author: zhoupan                          */
/*    time:   2017.10.30 19：45                */
/*=============================================*/
DROP DATABASE IF EXISTS DjangoWebSite;
DROP TABLE IF EXISTS anonymous;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS news;
DROP TABLE IF EXISTS pictures;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS enrolled;
DROP TABLE IF EXISTS devuser;

/*==============================================================*/
/* Table: anonymous      匿名用户                               */
/*==============================================================*/
CREATE TABLE anonymous
(
  aid      INT PRIMARY KEY AUTO_INCREMENT, # ID
  nickname VARCHAR(20), # 昵称
  email    VARCHAR(255) UNIQUE NOT NULL # 邮件
);

/*
{
"status":true,
"message":"error',
"data":
[{
"aid":1,
"nickname":"xiaoming",
"eamil":"A@qq.com"
}],
"all_count":1
}
*/

/*==============================================================*/
/* Table: events                       活动/沙龙                */
/*==============================================================*/
CREATE TEMPORARY TABLE events
(
  eid     INT PRIMARY KEY AUTO_INCREMENT, # ID
  title   VARCHAR(50) NOT NULL, # 活动标题
  content TEXT        NOT NULL, # 活动内容
  origin  TEXT        NOT NULL, # 活动源内容
  poster  VARCHAR(255), # 海报
  date    DATE        NOT NULL, # 日期
  time    TIME        NOT NULL, # 时间
  address VARCHAR(40) NOT NULL, # 活动地址
  labels  VARCHAR(30) NOT NULL, # 活动标签
  reader  INT             DEFAULT 0, # 阅读量
  upvote  INT             DEFAULT 0, # 点赞量
  enroll  INT             DEFAULT 0, # 报名人数
  status  INT(1)          DEFAULT 0 # 状态
);

/*
{
"status":true,
"message":"success",
"data":[{
  title:"第十四届软件自由日",
  content:"第十四届软件自由日",
  origin:"第十四届软件自由日"
  poster:"http://www.baidu.com",
  date:"2017-11-01",
  time:"21:30:01",
  address:"国际会议中心",
  labels:"SFD,开源",
  reader:0,
  upvote:0,
  enroll:0,
  status:0
  }
],
"all_count":1
}
 */
/*
  events status 说明：
          0 : 未发布
          1 :  已发布
   */

/*==============================================================*/
/* Table: feedback                       反馈                   */
/*==============================================================*/
CREATE TABLE feedback
(
  fid     INT PRIMARY KEY AUTO_INCREMENT, # ID
  email   VARCHAR(30) NOT NULL, # 邮箱
  content TEXT        NOT NULL, # 反馈内容
  date    DATE        NOT NULL, # 日期
  time    TIME        NOT NULL, # 时间
  status  INT(1)          DEFAULT 0 # 状态
);
/*
{
status:true,
message:"success",
data:[{
  fid:1,
  email:"root@xiyoulinux.org",
  content:"小组的位置在哪里？",
  date:"2017-11-02",
  time:"19:20:30",
  status:1
}],
all_count:1
}
 */
/*
  feedback status 说明：
          0 : 未回复
          1 :  已回复
   */


/*==============================================================*/
/* Table: news         新闻/动态                                */
/*==============================================================*/
CREATE TEMPORARY TABLE news
(
  nid     INT PRIMARY KEY AUTO_INCREMENT, # ID
  title   VARCHAR(50) NOT NULL, # 新闻标题
  content TEXT        NOT NULL, # 新闻内容
  origin  TEXT        NOT NULL, # 新闻源内容
  poster  VARCHAR(255), # 新闻图片
  date    DATE        NOT NULL, # 日期
  time    TIME        NOT NULL, # 时间
  labels  VARCHAR(30) NOT NULL, # 新闻标签
  reader  INT             DEFAULT 0, # 阅读量
  upvote  INT             DEFAULT 0, # 点赞量
  status  INT(1)          DEFAULT 0 # 新闻状态
);

/*
{
  "message":"success",
  "status":true,
  "data":[{
    "nid":1,
  title:"第十四届软件自由日（西邮站）圆满落下帷幕",
  content:"第十四届软件自由日（西邮站）圆满落下帷幕",
  origin:"第十四届软件自由日（西邮站）圆满落下帷幕",
  poster:"https://www.xiyoulinux.org/",
  date:"2017-11-1",
  time:"16:55:50",
  labels:"SFD,开源",
  reader:0,
  upvote:0,
  status:0
  }
  ],
  "total_count": 1
}
 */

/*
  news status 说明：
          0 : 未发布
          1 :  已发布
   */

/*==============================================================*/
/* Table: pictures   照片墙                                     */
/*==============================================================*/
CREATE TEMPORARY TABLE pictures
(
  pid     INT PRIMARY KEY       AUTO_INCREMENT, # ID
  content VARCHAR(255) NOT NULL, # 照片简介
  link    VARCHAR(255) NOT NULL, # 照片链接
  date    DATE         NOT NULL, # 日期
  time    TIME         NOT NULL, # 时间
  upvote  INT          NOT NULL, # 点赞量
  status  INT(1)                DEFAULT 0 # 照片状态
);

/*
{
status:true,
message:"success",
data:[{
 pid:1,
  content:"小组四届合照",
  link:"http://www.baidu.com",
  date:"2017-11-01",
  time:"12:23:20",
  upvote:1,
  status:0
}],
all_count:1
}
 */

/*
  pictures status 说明：
          0 : 未发布
          1 :  已发布
   */



/*==============================================================*/
/* Table: project     项目展示                                  */
/*==============================================================*/
CREATE TEMPORARY TABLE projects
(
  pid     INT PRIMARY KEY AUTO_INCREMENT, # ID
  title   VARCHAR(50)    NOT NULL, # 项目标题
  content TEXT           NOT NULL, # 项目内容描述
  origin  TEXT           NOT NULL, # 项目源内容
  poster  VARCHAR(255)   NOT NULL, # 项目标志
  link    VARBINARY(255) NOT NULL, # 项目链接
  date    DATE           NOT NULL, # 日期
  time    TIME           NOT NULL, # 时间
  reader  INT             DEFAULT 0, # 阅读量
  upvote  INT             DEFAULT 0, # 点赞量
  status  INT(1)          DEFAULT 0 # 项目状态
);
/*
{
"status":true,
"message":"success",
"data":[
{
  pid:1,
  gid:1,
  title:"小组官网",
  content:"小组官网",
  origin:"小组官网",
  poster:"http://www,baidu.com",
  link: "https://github.com"
  date:"2017-11-01",
  time:"19:30:20",
  reader:0,
  upvote:0,
  status:0
}
],
all_count:1
}
 */
/*
  project status 说明：
          0 : 未发布
          1 :  已发布
   */


/*==============================================================*/
/* Table: commnet         评论                                  */
/*==============================================================*/
CREATE TABLE comments
(
  cid     INT PRIMARY KEY AUTO_INCREMENT, # ID
  user    INT    NOT NULL, # 评论者
  o_type  INT(2) NOT NULL, # 评论的对象类型
  obj     INT    NOT NULL, # 评论的对象
  content TEXT   NOT NULL, # 评论的内容
  date    DATE   NOT NULL, # 日期
  time    TIME   NOT NULL, # 时间
  upvote  INT             DEFAULT 0, # 点赞量
  deal    INT(1)          DEFAULT 0, # 是否处理
  status  INT(1)          DEFAULT 0 # 状态

);
/*
{
status:true,
message:"success",
data:[
{
  rid:1,
  user:1.
  o_type:1
  object:1,
  content:"大家早上好",
  upvote:1,
  date:"2017-11-01",
  time:"12:23:20",
  deal:1,
  status:1
}
],
all_count:1
}
 */
/*
  comment status 说明：
          0 : 不允许显示
          1 :  允许显示
  comment o_type 说明：
          0 : 对 news 的评论
          1 ：对 events 的评论
          2 ：对 pictures 的评论
          3 : 对 project 的评论
          4 : 对 comment 的评论
  comment deal 说明：
          0 : 未处理
          1 ：已处理

   */

/*==============================================================*/
/* Table: enrolled         报名记录                              */
/*==============================================================*/

CREATE TABLE enrolled
(
  eid    INT PRIMARY KEY AUTO_INCREMENT,
  obj    INT  NOT NULL, # 报名对象
  uid    INT  NOT NULL, # 报名者id
  status INT             DEFAULT 0, # 状态
  date   DATE NOT NULL, # 日期
  time   TIME NOT NULL # 时间
);

/*
{
status:true,
message:"success",
data:[
{
  eid:1,
  obj:1,
  uid:1,
  status:0,
  date:"2017-10-10",
  time:"12:00:00"
}
],
all_count:1
}
 */
/*
  comment status 说明：
          0 : 已回复
          1 :  未回复
   */


/*==============================================================*/
/* Table: devuser         项目对应的开发者列表                     */
/*==============================================================*/


CREATE TABLE devuser  #
(
  did INT PRIMARY KEY AUTO_INCREMENT, #ID
  uid INT NOT NULL, # 用户ID
  pid INT NOT NULL   # 项目ID
);

/*
{
status:true,
message:"success",
data:[
{
  did:1,
  uid:1,
  pid:1
}
],
all_count:1
}
 */

