CREATE TABLE `certificate` (
    `c_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '证件ID',
    `c_name` varchar(64) NOT NULL DEFAULT '_' COMMENT '证件名',
    `c_imgpath` varchar(64) NOT NULL DEFAULT '_' COMMENT '图片路径',
    `s_id` int(11) unsigned NOT NULL COMMENT '职工号',
    PRIMARY KEY (`c_id`),
    UNIQUE KEY (`c_name`, `s_id`),
    INDEX (`s_id`),
    FOREIGN KEY (`s_id`) REFERENCES `staff` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='证件表';