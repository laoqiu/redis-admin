Redis admin by tornado
============

学习redis的最好方法，就是动手做一个有关redis的项目，考虑了下，决定做一个redis的web manager，定名redis-admin，UI就直接拿官网主页的。

需要完成的功能：
-------

    1. keys树形菜单
    2. keys搜索，比如session:*
    3. 根据key获取value(所有类型的key)
    4. 当点击keys菜单(比如session:*)，需要合并出所有“session:”子键的data，作出类似select * from table的效果. 并加入分页处理.
    5. 全局功能: flushall, flushdb,info
    6. keys功能: edit, expire, move, delete


待完成功能：
--------

    1. 切换db功能 (connect db)
    2. 备份功能 (backup)
    3. list不具备指定value的删除, 需要添加pop功能（new)

