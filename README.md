Redis admin by tornado
============

学习redis的最好方法，就是动手做一个有关redis的项目，考虑了下，决定做一个redis的web manager，定名redis-admin，UI就直接拿官网主页的。

进度日志:
-----------
    2012-4-3: 完成菜单与基本功能
    2012-4-9: 完成values获取
    2012-4-12: 完成编辑与keys结果集显示
    2012-4-16: 完善不同keys的不同操作，例如list，应用lpush, rpush, rpop, lpop功能
    2012-4-19: 完成db切换


已完成的功能：
-------

    1. keys树形菜单
    2. keys搜索，比如session:*
    3. 根据key获取value(所有类型的key)
    4. 当点击keys菜单(比如session:*)，需要合并出所有“session:”子键的data，作出类似select * from table的效果. 并加入分页处理.
    5. 全局功能: flushall, flushdb,info
    6. keys功能: edit, expire, move, delete
    7. 切换db功能 (connect db)
    8. list的pop和push功能
    9. 添加新的key-value功能 


待完成功能：
--------
    1. 备份功能 (backup)
    2. 加入管理员用户权限
    3. 加入远程连接功能

