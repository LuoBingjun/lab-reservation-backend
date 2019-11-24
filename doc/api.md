# API测试说明

测试地址：http://www.lbjthu.tech:8080

不存在的请求会返回404，不满足要求的请求会返回400

## 数据库后台

```
http://xxx/admin
```

账号：admin
密码：admin

## 用户验证
凡是登录后进行的操作，应该在请求头Requst Header中加入

```
Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTY1MDY4Mzk0LCJlbWFpbCI6Imx1b2JpbmdqdW5AZ21haWwuY29tIiwib3JpZ19pYXQiOjE1NjQ5ODE5OTR9.jghv8bkOYlLa8jvxU9qjSoAVCbv630NJzOfAroSLbS4
```


# Account API

## register

### URL

```
POST http://xxx/accounts/register
```

### 请求参数

```json
{
    "username":"用户名", // 最大长度30
    "password":"密码", // 最大长度 50，最小长度6
    "email":"邮箱" // 最大长度50 会检测是不是清华邮箱
}
```

### 响应参数

```json
{
    "result":0 // number,0表示成功,非0表示失败 [1表示不满足以上要求(同时返回400),2表示用户名已被占用]
}
```

## login

### URL

```
POST http://xxx/accounts/login
```

### 请求参数

```json
{
    "username":"用户名",
    "password":"密码"
}
```

### 响应参数
成功返回以下内容
```json
{
    "token": "" // string,在成功时才会返回
}
```

失败返回400 Bad Request

## logout

### URL

```
POST http://xxx/accounts/logout
```

### 请求参数

无参数

### 响应参数
成功返回200

## setpwd
更改密码后原有token会立刻失效

### URL

```
POST http://xxx/accounts/setpwd
```

### 请求参数

```json
{
    "oldpwd":"123456",
    "newpwd":"123456"
}
```

### 响应参数
成功返回200

## setinfo
### URL

```
POST http://xxx/accounts/setinfo
```

### 请求参数

```json
{
    "email":"" // 需要更新的内容，仍然会检测邮箱是否为清华邮箱
}
```

### 响应参数
成功返回200

# Reserve API
## 
