CREATE TABLE `certificate` (
    `c_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '证件ID',
    `c_name` varchar(64) NOT NULL DEFAULT '_' COMMENT '证件名',
    `c_imgpath` varchar(64) NOT NULL DEFAULT '_' COMMENT '图片路径',
    `id` int(11) unsigned NOT NULL COMMENT '职工号',
    PRIMARY KEY (`c_id`),
    KEY `certificate_FK` (`s_id`),
    CONSTRAINT `certificate_FK` FOREIGN KEY (`s_id`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='证件表';