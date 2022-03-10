import sqlalchemy

metadata = sqlalchemy.MetaData()


staff = sqlalchemy.Table(
    "staff",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=64)),
    sqlalchemy.Column("cardnum", sqlalchemy.String(length=64)),
    sqlalchemy.Column("nation", sqlalchemy.String(length=12)),
    sqlalchemy.Column("mobile", sqlalchemy.String(length=12)),
    sqlalchemy.Column("email", sqlalchemy.String(length=64)),
    sqlalchemy.Column("sex", sqlalchemy.Integer),
    sqlalchemy.Column("birth", sqlalchemy.DATETIME),
    sqlalchemy.Column("marriage", sqlalchemy.Integer),
    sqlalchemy.Column("province", sqlalchemy.String(length=24)),
    sqlalchemy.Column("city", sqlalchemy.String(length=24)),
    sqlalchemy.Column("area", sqlalchemy.String(length=24)),
    sqlalchemy.Column("department", sqlalchemy.String(length=64)),
    sqlalchemy.Column("job", sqlalchemy.String(length=64)),
)

certificate = sqlalchemy.Table(
    "certificate",
    metadata,
    sqlalchemy.Column("c_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("c_name", sqlalchemy.String(length=64)),
    sqlalchemy.Column("c_img", sqlalchemy.String(length=64)),
    sqlalchemy.Column("s_id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('staff.id')),
)
