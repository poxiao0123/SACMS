CREATE TABLE `certificate` (
    `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `c_id` int(11) UNSIGNED NOT NULL COMMENT '证件号',
    `c_name` varchar(64) NOT NULL DEFAULT '_' COMMENT '证件名',
    `c_stime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '拿证时间',
    `c_etime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '过期时间',
    `c_img` MediumBlob NOT NULL COMMENT '证件图片',
    `s_id` int(11) UNSIGNED NOT NULL COMMENT '职工号',
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_name_id` (`c_id`,`c_name`,`s_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证件表';