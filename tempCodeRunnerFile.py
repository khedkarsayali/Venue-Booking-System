
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    contactNo = db.Column(db.String(20), nullable=True)
    clubname = db.Column(db.String(100), nulla