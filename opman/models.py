from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


# Create your models here.

# 用户相关
class PermissonList(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'权限名称')
    url = models.CharField(max_length=255, verbose_name=u'URL地址')

    def __str__(self):
        return '%s(%s)' % (self.name, self.url)


class RoleList(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'部门名称')
    permission = models.ManyToManyField(PermissonList, blank=True, verbose_name=u'权限')

    def __str__(self):
        return self.name


class MyUser(AbstractUser):
    fullname = models.CharField(max_length=64, null=True, unique=True, default=None, verbose_name=u'姓名')
    birthday = models.DateField(null=True, blank=True, default=None, verbose_name=u'生日')
    sex = models.CharField(max_length=2, null=True, verbose_name=u'性别')
    role = models.ForeignKey(RoleList, null=True, blank=True, verbose_name=u'部门')
    permission = models.ManyToManyField(PermissonList, blank=True, verbose_name=u'权限')


#资产相关
ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
    )

ASSET_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器"),
    (str(4), u"网络设备"),
    (str(5), u"其他")
    )


class Idc(models.Model):
    name = models.CharField(u"机房名称", max_length=30, null=True)
    address = models.CharField(u"机房地址", max_length=100, null=True)
    tel = models.CharField(u"机房电话", max_length=30, null=True)
    contact = models.CharField(u"客户经理", max_length=30, null=True)
    contact_phone = models.CharField(u"移动电话", max_length=30, null=True)
    jigui = models.CharField(u"机柜信息", max_length=30, null=True)
    ip_range = models.CharField(u"IP范围", max_length=30, null=True)
    bandwidth = models.CharField(u"接入带宽", max_length=30, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'数据中心'
        verbose_name_plural = verbose_name


class HostGroup(models.Model):
    name = models.CharField(u"组名", max_length=30, unique=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
    ip = models.GenericIPAddressField(u"管理IP", max_length=15)
    other_ip = models.CharField(u"其它IP", max_length=100, null=True, blank=True)
    group = models.ForeignKey(HostGroup, verbose_name=u"设备组", on_delete=models.SET_NULL, null=True, blank=True)
    asset_no = models.CharField(u"资产编号", max_length=50, null=True, blank=True)
    asset_type = models.CharField(u"设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField(u"操作系统", max_length=100, null=True, blank=True)
    vendor = models.CharField(u"设备厂商", max_length=50, null=True, blank=True)
    cpu_model = models.CharField(u"CPU型号", max_length=100, null=True, blank=True)
    cpu_num = models.CharField(u"CPU数量", max_length=100, null=True, blank=True)
    memory = models.CharField(u"内存大小", max_length=30, null=True, blank=True)
    disk = models.CharField(u"硬盘信息", max_length=255, null=True, blank=True)
    sn = models.CharField(u"SN号 码", max_length=60, blank=True)
    idc = models.ForeignKey(Idc, verbose_name=u"所在机房", on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(u"所在位置", max_length=100, null=True, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, null=True, blank=True)

    def __str__(self):
        return self.hostname


class Assets(models.Model):
    assets_type_choices = (
                          ('server',u'服务器'),
                          ('switch',u'交换机'),
                          ('route',u'路由器'),
                          ('printer',u'打印机'),
                          ('scanner',u'扫描仪'),
                          ('firewall',u'防火墙'),
                          ('storage',u'存储设备'),
                          ('wifi',u'无线设备'),
                          )
    assets_type = models.CharField(choices=assets_type_choices, max_length=100, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=100, verbose_name='资产编号', unique=True)
    sn = models.CharField(max_length=100, verbose_name='设备序列号')
    buy_time = models.DateField(blank=True, null=True, verbose_name='购买时间')
    expire_date = models.DateField(u'过保修期', null=True, blank=True)
    buy_user = models.CharField(max_length=100, blank=True, null=True, verbose_name='购买人')
    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name='制造商')
    provider = models.CharField(max_length=100, blank=True, null=True, verbose_name='供货商')
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name='资产型号')
    status = models.SmallIntegerField(blank=True, null=True, verbose_name='状态')
    put_zone = models.SmallIntegerField(blank=True, null=True, verbose_name='放置区域')
    group = models.SmallIntegerField(blank=True, null=True, verbose_name='使用组')
    business = models.SmallIntegerField(blank=True, null=True, verbose_name='业务类型')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)


class Log_Assets(models.Model):
    assets_id = models.IntegerField(verbose_name='资产类型id', blank=True, null=True, default=None)
    assets_user = models.CharField(max_length=50, verbose_name='操作用户', default=None)
    assets_content = models.CharField(max_length=100, verbose_name='名称', default=None)
    assets_type = models.CharField(max_length=50, default=None)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')


class Service_Assets(models.Model):
    '''业务分组表'''
    service_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'opsmanage_service_assets'
        permissions = (
            ("can_read_service_assets", "读取业务资产权限"),
            ("can_change_service_assets", "更改业务资产权限"),
            ("can_add_service_assets", "添加业务资产权限"),
            ("can_delete_service_assets", "删除业务资产权限"),
        )
        verbose_name = '业务分组表'
        verbose_name_plural = '业务分组表'


class Server_Assets(models.Model):
    assets = models.OneToOneField('Assets')
    ip = models.CharField(max_length=100, unique=True, blank=True, null=True)
    hostname = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    passwd = models.CharField(max_length=100, blank=True, null=True)
    keyfile = models.SmallIntegerField(blank=True,null=True)  # FileField(upload_to = './upload/key/',blank=True,null=True,verbose_name='密钥文件')
    port = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    line = models.CharField(max_length=100, blank=True, null=True)
    cpu = models.CharField(max_length=100, blank=True, null=True)
    cpu_number = models.SmallIntegerField(blank=True, null=True)
    vcpu_number = models.SmallIntegerField(blank=True, null=True)
    cpu_core = models.SmallIntegerField(blank=True, null=True)
    disk_total = models.CharField(max_length=100, blank=True, null=True)
    ram_total = models.CharField(max_length=100, blank=True, null=True)
    kernel = models.CharField(max_length=100, blank=True, null=True)
    selinux = models.CharField(max_length=100, blank=True, null=True)
    swap = models.CharField(max_length=100, blank=True, null=True)
    raid = models.SmallIntegerField(blank=True, null=True)
    system = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)


class Zone_Assets(models.Model):
    zone_name = models.CharField(max_length=100, unique=True)
    '''自定义权限'''

    class Meta:
        db_table = 'opsmanage_zone_assets'
        permissions = (
            ("can_read_zone_assets", "读取机房资产权限"),
            ("can_change_zone_assets", "更改机房资产权限"),
            ("can_add_zone_assets", "添加机房资产权限"),
            ("can_delete_zone_assets", "删除机房资产权限"),
        )
        verbose_name = '机房资产表'
        verbose_name_plural = '机房资产表'


class Line_Assets(models.Model):
    line_name = models.CharField(max_length=100, unique=True)
    '''自定义权限'''

    class Meta:
        db_table = 'opsmanage_line_assets'
        permissions = (
            ("can_read_line_assets", "读取出口线路资产权限"),
            ("can_change_line_assetss", "更改出口线路资产权限"),
            ("can_add_line_assets", "添加出口线路资产权限"),
            ("can_delete_line_assets", "删除出口线路资产权限"),
        )
        verbose_name = '出口线路资产表'
        verbose_name_plural = '出口线路资产表'


class Raid_Assets(models.Model):
    raid_name = models.CharField(max_length=100, unique=True)
    '''自定义权限'''

    class Meta:
        db_table = 'opsmanage_raid_assets'
        permissions = (
            ("can_read_raid_assets", "读取Raid资产权限"),
            ("can_change_raid_assets", "更改Raid资产权限"),
            ("can_add_raid_assets", "添加Raid资产权限"),
            ("can_delete_raid_assets", "删除Raid资产权限"),
        )
        verbose_name = 'Raid资产表'
        verbose_name_plural = 'Raid资产表'

class Disk_Assets(models.Model):
    assets = models.ForeignKey('Assets')
    device_volume = models.CharField(max_length=100, blank=True, null=True, verbose_name='硬盘容量')
    device_status = models.CharField(max_length=100, blank=True, null=True, verbose_name='硬盘状态')
    device_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='硬盘型号')
    device_brand = models.CharField(max_length=100, blank=True, null=True, verbose_name='硬盘生产商')
    device_serial = models.CharField(max_length=100, blank=True, null=True, verbose_name='硬盘序列号')
    device_slot = models.SmallIntegerField(blank=True, null=True, verbose_name='硬盘插槽')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'opsmanage_disk_assets'
        permissions = (
            ("can_read_disk_assets", "读取磁盘资产权限"),
            ("can_change_disk_assets", "更改磁盘资产权限"),
            ("can_add_disk_assets", "添加磁盘资产权限"),
            ("can_delete_disk_assets", "删除磁盘资产权限"),
        )
        unique_together = (("assets", "device_slot"))
        verbose_name = '磁盘资产表'
        verbose_name_plural = '磁盘资产表'


class Ram_Assets(models.Model):
    assets = models.ForeignKey('Assets')
    device_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存型号')
    device_volume = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存容量')
    device_brand = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存生产商')
    device_slot = models.SmallIntegerField(blank=True, null=True, verbose_name='内存插槽')
    device_status = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存状态')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'opsmanage_ram_assets'
        permissions = (
            ("can_read_ram_assets", "读取内存资产权限"),
            ("can_change_ram_assets", "更改内存资产权限"),
            ("can_add_ram_assets", "添加内存资产权限"),
            ("can_delete_ram_assets", "删除内存资产权限"),
        )
        unique_together = (("assets", "device_slot"))
        verbose_name = '内存资产表'
        verbose_name_plural = '内存资产表'


class Network_Assets(models.Model):
    assets = models.OneToOneField('Assets')
    bandwidth = models.CharField(max_length=100, blank=True, null=True, verbose_name='背板带宽')
    ip = models.CharField(max_length=100, blank=True, null=True, verbose_name='管理ip')
    port_number = models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')
    firmware = models.CharField(max_length=100, blank=True, null=True, verbose_name='固件版本')
    cpu = models.CharField(max_length=100, blank=True, null=True, verbose_name='cpu型号')
    stone = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存大小')
    configure_detail = models.TextField(max_length=100, blank=True, null=True, verbose_name='配置说明')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'opsmanage_network_assets'
        permissions = (
            ("can_read_network_assets", "读取网络资产权限"),
            ("can_change_network_assets", "更改网络资产权限"),
            ("can_add_network_assets", "添加网络资产权限"),
            ("can_delete_network_assets", "删除网络资产权限"),
        )
        verbose_name = '网络资产表'
        verbose_name_plural = '网络资产表'


class Cron_Config(models.Model):
    cron_server = models.ForeignKey('Server_Assets')
    cron_minute = models.CharField(max_length=10, verbose_name='分', default=None)
    cron_hour = models.CharField(max_length=10, verbose_name='时', default=None)
    cron_day = models.CharField(max_length=10, verbose_name='天', default=None)
    cron_week = models.CharField(max_length=10, verbose_name='周', default=None)
    cron_month = models.CharField(max_length=10, verbose_name='月', default=None)
    cron_user = models.CharField(max_length=50, verbose_name='任务用户', default=None)
    cron_name = models.CharField(max_length=100, verbose_name='任务名称', default=None)
    cron_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='任务描述', default=None)
    cron_command = models.CharField(max_length=200, verbose_name='任务参数', default=None)
    cron_script = models.FileField(upload_to='./upload/cron/', blank=True, null=True, verbose_name='脚本路径', default=None)
    cron_script_path = models.CharField(max_length=100, blank=True, null=True, verbose_name='脚本路径', default=None)
    cron_status = models.SmallIntegerField(verbose_name='任务状态', default=None)


class ProjectConfig(models.Model):
    repertory_choices = (
        ('Git', 'git'),
        ('SVN', 'svn')
    )
    deploy_model_choices = (
        ('Branch', 'branch'),
        ('Tag', 'tag')
    )
    project_env = models.CharField(max_length=50, verbose_name='项目环境', default=None)
    project_name = models.CharField(max_length=100, verbose_name='项目名称', default=None)
    project_local_command = models.TextField(blank=True, null=True, verbose_name='部署服务器要执行的命令', default=None)
    project_repo_dir = models.CharField(max_length=100, verbose_name='本地仓库目录', default=None)
    project_dir = models.CharField(max_length=100, verbose_name='代码目录', default=None)
    project_exclude = models.TextField(blank=True, null=True, verbose_name='排除文件', default=None)
    project_address = models.CharField(max_length=100, verbose_name='版本仓库地址', default=None)
    project_uuid = models.CharField(max_length=50, verbose_name='唯一id')
    project_repo_user = models.CharField(max_length=50, verbose_name='仓库用户名', blank=True, null=True)
    project_repo_passwd = models.CharField(max_length=50, verbose_name='仓库密码', blank=True, null=True)
    project_repertory = models.CharField(choices=repertory_choices, max_length=10, verbose_name='仓库类型', default=None)
    project_status = models.SmallIntegerField(verbose_name='是否激活', blank=True, null=True, default=None)
    project_remote_command = models.TextField(blank=True, null=True, verbose_name='部署之后执行的命令', default=None)
    project_user = models.CharField(max_length=50, verbose_name='项目文件宿主', default=None)
    project_model = models.CharField(choices=deploy_model_choices, max_length=10, verbose_name='上线类型', default=None)
    project_audit_group = models.SmallIntegerField(verbose_name='项目授权组', blank=True, null=True, default=None)

    class Meta:
        db_table = 'opsmanage_project_config'
        permissions = (
            ("can_read_project_config", "读取项目权限"),
            ("can_change_project_config", "更改项目权限"),
            ("can_add_project_config", "添加项目权限"),
            ("can_delete_project_config", "删除项目权限"),
        )
        unique_together = (("project_env", "project_name"))
        verbose_name = '项目管理表'
        verbose_name_plural = '项目管理表'


class Project_Config(models.Model):
    project_repertory_choices = (
        ('git', u'git'),
        ('svn', u'svn'),
    )
    deploy_model_choices = (
        ('branch', u'branch'),
        ('tag', u'tag'),
    )
    project_env = models.CharField(max_length=50, verbose_name='项目环境', default=None)
    project_name = models.CharField(max_length=100, verbose_name='项目名称', default=None)
    project_local_command = models.TextField(blank=True, null=True, verbose_name='部署服务器要执行的命令', default=None)
    project_repo_dir = models.CharField(max_length=100, verbose_name='本地仓库目录', default=None)
    project_dir = models.CharField(max_length=100, verbose_name='代码目录', default=None)
    project_exclude = models.TextField(blank=True, null=True, verbose_name='排除文件', default=None)
    project_address = models.CharField(max_length=100, verbose_name='版本仓库地址', default=None)
    project_uuid = models.CharField(max_length=50, verbose_name='唯一id')
    project_repo_user = models.CharField(max_length=50, verbose_name='仓库用户名', blank=True, null=True)
    project_repo_passwd = models.CharField(max_length=50, verbose_name='仓库密码', blank=True, null=True)
    project_repertory = models.CharField(choices=project_repertory_choices, max_length=10, verbose_name='仓库类型',
                                         default=None)
    project_status = models.SmallIntegerField(verbose_name='是否激活', blank=True, null=True, default=None)
    project_remote_command = models.TextField(blank=True, null=True, verbose_name='部署之后执行的命令', default=None)
    project_user = models.CharField(max_length=50, verbose_name='项目文件宿主', default=None)
    project_model = models.CharField(choices=deploy_model_choices, max_length=10, verbose_name='上线类型', default=None)
    project_audit_group = models.SmallIntegerField(verbose_name='项目授权组', blank=True, null=True, default=None)


class Project_Number(models.Model):
    project = models.ForeignKey('Project_Config', related_name='project_number', on_delete=models.CASCADE)
    server = models.CharField(max_length=100, verbose_name='服务器IP', default=None)
    dir = models.CharField(max_length=100, verbose_name='项目目录', default=None)

    class Meta:
        db_table = 'opsmanage_project_number'
        permissions = (
            ("can_read_project_number", "读取项目成员权限"),
            ("can_change_project_number", "更改项目成员权限"),
            ("can_add_project_number", "添加项目成员权限"),
            ("can_delete_project_number", "删除项目成员权限"),
        )
        unique_together = (("project", "server"))
        verbose_name = '项目成员表'
        verbose_name_plural = '项目成员表'

    def __unicode__(self):
        return '%s' % (self.server)

class ProjectOrder(models.Model):
    STATUS = (
        (0, '已经通过'),
        (1, '已经拒绝'),
        (2, '审核中'),
        (3, '已经部署')
    )
    LEVEL = (
        (0, '非紧急'),
        (1, '紧急')
    )

    order_user = models.CharField(max_length=30, verbose_name='工单申请人')
    order_project = models.ForeignKey('ProjectConfig', verbose_name='项目id')
    order_subject = models.CharField(max_length=200, verbose_name='工单申请主题')
    order_content = models.TextField(verbose_name='工单申请内容')
    order_branch = models.CharField(max_length=50, blank=True, null=True, verbose_name='分支版本')
    order_comid = models.CharField(max_length=100, blank=True, null=True, verbose_name='版本id')
    order_tag = models.CharField(max_length=50, blank=True, null=True, verbose_name='标签')
    order_audit = models.CharField(max_length=30, verbose_name='部署指派人')
    order_status = models.IntegerField(choices=STATUS, default='审核中', verbose_name='工单状态')
    order_level = models.IntegerField(choices=LEVEL, default='非紧急', verbose_name='工单紧急程度')
    order_cancel = models.TextField(blank=True, null=True, verbose_name='取消原因')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='工单发布时间')
    modify_time = models.DateTimeField(auto_now=True, blank=True, verbose_name='工单最后修改时间')


class Ansible_Playbook(models.Model):
    playbook_name = models.CharField(max_length=50, verbose_name='剧本名称', unique=True)
    playbook_desc = models.CharField(max_length=200, verbose_name='功能描述', blank=True, null=True)
    playbook_vars = models.TextField(verbose_name='模块参数', blank=True, null=True)
    playbook_uuid = models.CharField(max_length=50, verbose_name='唯一id')
    playbook_file = models.FileField(upload_to='./upload/playbook/', verbose_name='剧本路径')
    playbook_auth_group = models.SmallIntegerField(verbose_name='授权组', blank=True, null=True)
    playbook_auth_user = models.SmallIntegerField(verbose_name='授权用户', blank=True, null=True, )


class Log_Ansible_Playbook(models.Model):
    ans_id = models.IntegerField(verbose_name='id', blank=True, null=True, default=None)
    ans_user = models.CharField(max_length=50, verbose_name='使用用户', default=None)
    ans_name = models.CharField(max_length=100, verbose_name='模块名称', default=None)
    ans_content = models.CharField(max_length=100, default=None)
    ans_server = models.TextField(verbose_name='服务器', default=None)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')


class Log_Ansible_Model(models.Model):
    ans_user = models.CharField(max_length=50, verbose_name='使用用户', default=None)
    ans_model = models.CharField(max_length=100, verbose_name='模块名称', default=None)
    ans_args = models.CharField(max_length=500, blank=True, null=True, verbose_name='模块参数', default=None)
    ans_server = models.TextField(verbose_name='服务器', default=None)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')


class Ansible_Playbook_Number(models.Model):
    playbook = models.ForeignKey('Ansible_Playbook', related_name='server_number', on_delete=models.CASCADE)
    playbook_server = models.CharField(max_length=100, verbose_name='目标服务器', blank=True, null=True)

    class Meta:
        db_table = 'opsmanage_ansible_playbook_number'
        permissions = (
            ("can_read_ansible_playbook_number", "读取Ansible剧本成员权限"),
            ("can_change_ansible_playbook_number", "更改Ansible剧本成员权限"),
            ("can_add_ansible_playbook_number", "添加Ansible剧本成员权限"),
            ("can_delete_ansible_playbook_number", "删除Ansible剧本成员权限"),
        )
        verbose_name = 'Ansible剧本成员表'
        verbose_name_plural = 'Ansible剧本成员表'

    def __unicode__(self):
        return '%s' % (self.playbook_server)

class Log_Project_Config(models.Model):
    project_id = models.IntegerField(verbose_name='资产类型id', blank=True, null=True, default=None)
    project_user = models.CharField(max_length=50, verbose_name='操作用户', default=None)
    project_name = models.CharField(max_length=100, verbose_name='名称', default=None)
    project_content = models.CharField(max_length=100, default=None)
    project_branch = models.CharField(max_length=100, default=None, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')


class Global_Config(models.Model):
    ansible_model = models.SmallIntegerField(verbose_name='是否开启ansible模块操作记录', blank=True, null=True)
    ansible_playbook = models.SmallIntegerField(verbose_name='是否开启ansible剧本操作记录', blank=True, null=True)
    cron = models.SmallIntegerField(verbose_name='是否开启计划任务操作记录', blank=True, null=True)
    project = models.SmallIntegerField(verbose_name='是否开启项目操作记录', blank=True, null=True)
    assets = models.SmallIntegerField(verbose_name='是否开启资产操作记录', blank=True, null=True)
    server = models.SmallIntegerField(verbose_name='是否开启服务器命令记录', blank=True, null=True)
    email = models.SmallIntegerField(verbose_name='是否开启邮件通知', blank=True, null=True)


class Email_Config(models.Model):
    site = models.CharField(max_length=100, verbose_name='部署站点')
    host = models.CharField(max_length=100, verbose_name='邮件发送服务器')
    port = models.SmallIntegerField(verbose_name='邮件发送服务器端口')
    user = models.CharField(max_length=100, verbose_name='发送用户账户')
    passwd = models.CharField(max_length=100, verbose_name='发送用户密码')
    subject = models.CharField(max_length=100, verbose_name='发送邮件主题标识', default=u'[OPS]')
    cc_user = models.TextField(verbose_name='抄送用户列表', blank=True, null=True)


class Log_Cron_Config(models.Model):
    cron_id = models.IntegerField(verbose_name='id', blank=True, null=True, default=None)
    cron_user = models.CharField(max_length=50, verbose_name='操作用户', default=None)
    cron_name = models.CharField(max_length=100, verbose_name='名称', default=None)
    cron_content = models.CharField(max_length=100, default=None)
    cron_server = models.CharField(max_length=100, default=None)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')



