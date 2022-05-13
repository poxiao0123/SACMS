CREATE TABLE `staff` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
    `s_id` int(11) unsigned NOT NULL UNIQUE DEFAULT 0 COMMENT '工号',
    `name` varchar(64) NOT NULL DEFAULT '_' COMMENT '姓名',
    `cardnum` varchar(64) NOT NULL UNIQUE DEFAULT '_' COMMENT '身份证号',
    `mobile` varchar(16) NOT NULL UNIQUE DEFAULT '_' COMMENT '手机号',
    `email` varchar(32) NOT NULL UNIQUE DEFAULT '_' COMMENT '邮箱',
    `sex` varchar(4) NOT NULL DEFAULT '_' COMMENT '女 男',
    `province` varchar(24) NOT NULL DEFAULT '_' COMMENT '省',
    `city` varchar(24) NOT NULL DEFAULT '_' COMMENT '市',
    `area` varchar(24) NOT NULL DEFAULT '_' COMMENT '区',
    `nation` varchar(12) NOT NULL DEFAULT '_' COMMENT '民族',
    `birth` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生日',
    `marriage` varchar(8) NOT NULL  DEFAULT '_' COMMENT '未婚 已婚 离异',
    `department` varchar(64) NOT NULL DEFAULT '_' COMMENT '部门',
    `job` varchar(64) NOT NULL DEFAULT '_' COMMENT '职位',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='职工表';