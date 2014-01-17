wjbbwebserver
=============

using django


RESTful API:

1. 注册
POST
domain:8000/user/register/
必选参数：
username  base64编码过的用户名
password  base64编码过的密码
可选参数：
name  用户宝贝的名字
babyheight  宝贝的体重
babyweight  宝贝的身高
birthday  宝贝的生日 （格式：2014-01-01）
babysex   宝贝的性别 （'boy' or 'girl'）
返回：
True  注册成功
False 注册失败
DuplicateName 用户名已被注册


2. 身份验证 （无状态登录）
POST
domain:8000/user/informationcheck/
必选参数：
username  base64编码过的用户名
password  base64编码过的密码
返回：
True  身份验证成功
False 身份验证失败



3. 更新用户信息
POST
domain:8000/user/update/
必选参数：
username  base64编码过的用户名
password  base64编码过的密码
可选参数：
name  用户宝贝的名字
babyheight  宝贝的体重
babyweight  宝贝的身高
birthday  宝贝的生日 （格式：2014-01-01）
babysex   宝贝的性别 （'boy' or 'girl'）
返回：
AUTH_FAILED 身份认证失败
True  更新成功
False 更新失败



4. 获取若干条知识的详细内容
POST
domain:8000/knowledge/getknowl
必选参数：
username  base64编码过的用户名
password  base64编码过的密码
可选参数：
number  要返回知识的条数
返回数据：
AUTH_FAILED 认证失败
或者
json格式字符串（若干条知识详细内容的列表）：
[ {knowledgeId:知识id,  knowledgeTitle:知识标题, knowledgeContent:知识内容, knowledgePicLink:知识图片链接（已废弃）, tags:知识标签, commericals:[{"commericalId":0, "commericalTitle":"fake_title", "commericalLink":"www.fakecommercial.com"}], pic:知识图片链接, icon:知识图标链接} , ......]



5. 获取若干条知识的简易信息
POST
domain:8000/knowledge/getknowllist
必选参数：
username  base64编码过的用户名
password  base64编码过的密码
可选参数：
number  要返回知识的条数
返回数据：
AUTH_FAILED 认证失败
或者
json格式字符串（若干条知识简易内容的列表）：
[ {knowledgeId:知识id, knowledgeTitle:知识标题, pic:知识图片链接, icon:知识图标链接}, ..... ]


6. 根据id获取一条知识的详细内容
POST
domain:8000/knowledge/getknowlbyid
必选参数：
knowledgeid 知识的id
返回数据：
NOT_FOUND 未找到对应id的知识
或者
json格式字符串（一条知识的详细内容）：
{knowledgeId:知识id,  knowledgeTitle:知识标题, knowledgeContent:知识内容, knowledgePicLink:知识图片链接（已废弃）, tags:知识标签, commericals:[{"commericalId":0, "commericalTitle":"fake_title", "commericalLink":"www.fakecommercial.com"}], knowledgePicLink:知识图片链接}


7. 收藏一条知识
POST
domain:8000/knowledge/collectknowl
必选参数：
username  base64编码过的用户名
password  base64编码过的密码
id  知识id
返回：
AUTH_FAILED 身份认证失败
True  收藏成功
False 收藏失败


8. 根据经纬度获取周边商户信息（基本信息）
POST
domain:8000/knowledge/collectknowl
必选参数：
username  base64编码过的用户名
password  base64编码过的密码
latitude  纬度
longitude 经度
返回数据：
AUTH_FAILED 身份认证失败
PARAM_ERROR 参数错误
或者商户信息列表：
[ {business_id:商户id, name:商户名称, address:地址, telephone:电话}, ..... ]




9. 根据商户id获取商户详细信息
POST
domain:8000/knowledge/collectknowl
必选参数：
username  base64编码过的用户名
password  base64编码过的密码
latitude  纬度
longitude 经度
id  商户id
返回数据：
AUTH_FAILED 身份认证失败
PARAM_ERROR 参数错误
或者商户信息列表：
 {business_id:商户id, name:商户名称, branch_name:分店名称, address:地址, telephone:电话, city:城市, business_url:商户url, s_photo_url:商户图片链接, description:商户描述, regions:商户所属商业区, categories:商户类别}




