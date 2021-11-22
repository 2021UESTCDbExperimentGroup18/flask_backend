# Falsk后端

本repo为2021数据库实验18组的后端项目,主体使用flask编写,安装执行方式如下

## Installation

```bash
git clone https://github.com/2021UESTCDbExperimentGroup18/flask_backend flask_backend
cd flask_backend
make install
```

## Executing

This application has a CLI interface that extends the Flask CLI.

Just run:

```bash
flask_backend
```

or

```bash
python -m flask_backend
```

To see the help message and usage instructions.

## First run

由于实验要求,本次数据库使用MongoDB,因此此流程后续将会变更!后续将在流程变更后修改此工作流

```bash
flask_backend create-db   # 创建db
flask_backend populate-db  # 数据库填充
flask_backend add-user -u admin -p 1234  # 创建用户
flask_backend run # 运行项目
```

以下是一些地址和示例api,后续请修改对应代码:

- Website: <http://localhost:5000>
- Admin: <http://localhost:5000/admin/>
  - user: admin, senha: 1234
- API GET:
  - <http://localhost:5000/api/v1/product/>
  - <http://localhost:5000/api/v1/product/1>
  - <http://localhost:5000/api/v1/product/2>
  - <http://localhost:5000/api/v1/product/3>

> **Note**: You can also use `flask run` to run the application.
