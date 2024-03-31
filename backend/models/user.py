from models.common import Table, fields


class UserModel(Table):
    """
    用户模型类 > user table
    """

    username = fields.CharField(max_length=16, description="账号", unique=True)
    nickname = fields.CharField(max_length=20, description="姓名", null=True)
    password = fields.CharField(max_length=128, description="密码")
    limit_start = fields.IntField(description="限制登陆开始时间", null=True)
    limit_end = fields.IntField(description="限制登陆结束时间", null=True)

    class Meta:
        table = "sys_user"
        table_description = "用户表"
        # 索引
        unique_together = ("username",)
