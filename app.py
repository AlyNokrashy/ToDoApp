from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from sqlalchemy import case, desc
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.config["SECRET_KEY"] = "alyahmed2005"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_PERMANENT"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

egypt_tz = ZoneInfo("Africa/Cairo")
egypt_now = datetime.now(egypt_tz)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    todos = db.relationship("Todo", backref="owner", lazy=True)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(egypt_tz).astimezone(timezone.utc)
    )
    priority = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()

        if existing_user:
            raise ValidationError(
                "This username already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")


def convert_to_egyptian_time(dt_utc):
    if dt_utc is None:
        return None
    return dt_utc.astimezone(egypt_tz)


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("register"))


@app.route("/dashboard")
@login_required
def dashboard():
    query = request.args.get("query")
    if query:
        todos = (
            Todo.query.filter_by(user_id=current_user.id)
            .filter(Todo.title.like(f"%{query}%"))
            .order_by(Todo.complete, Todo.created_at)
            .all()
        )
        total = len(todos)
        completed_tasks = len([todo for todo in todos if todo.complete])
        pending_tasks = total - completed_tasks
    else:
        todos = (
            Todo.query.filter_by(user_id=current_user.id)
            .order_by(Todo.complete, Todo.created_at)
            .all()
        )
        total = len(todos)
        completed_tasks = len([todo for todo in todos if todo.complete])
        pending_tasks = total - completed_tasks

    for todo in todos:
        todo.created_at_display = convert_to_egyptian_time(todo.created_at)

    return render_template(
        "dashboard.html",
        todos=todos,
        total=total,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        form=LoginForm(),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()

    if form.validate_on_submit():
        print(f"Form submitted. Username: {form.username.data}")
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            return redirect(url_for("dashboard"))
        if not user:
            form.username.errors.append("Username does not exist.")
        if user and not bcrypt.check_password_hash(user.password, form.password.data):
            form.password.errors.append("Incorrect password.")
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            form.username.errors.append(
                "This username already exists. Please choose another one"
            )
        else:
            hashed_pass = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=False)

        return redirect(url_for("dashboard"))

    return render_template("register.html", form=form)


@app.route("/add", methods=["POST", "GET"])
@login_required
def add():
    if request.method == "POST":
        title = request.form.get("title")
        date = request.form.get("date")
        priority = request.form.get("priority")
        description = request.form.get("description")
        if title:
            new_todo = Todo(
                title=title,
                complete=False,
                priority=priority,
                date=datetime.strptime(date, "%Y-%m-%d") if date else None,
                description=description,
                user_id=current_user.id,
            )
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for("dashboard"))
    return render_template("add.html")


@app.route("/update/<int:todo_id>")
@login_required
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/delete/<int:todo_id>")
@login_required
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/status/<string:status>", methods=["GET"])
@login_required
def filter(status):
    query = Todo.query.filter_by(user_id=current_user.id)
    if status == "completed":
        todos = query.filter_by(complete=True).all()
    elif status == "not_completed":
        todos = query.filter_by(complete=False).all()
    else:
        todos = query.all()

    return render_template("dashboard.html", todos=todos)


@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
@login_required
def edit(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == "POST":
        todo.date = (
            datetime.strptime(request.form.get("date"), "%Y-%m-%d")
            if request.form.get("date")
            else None
        )
        todo.title = request.form.get("title")
        todo.priority = request.form.get("priority")
        todo.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("edit.html", todo=todo)


@app.route("/sort", methods=["GET"])
@login_required
def sort():
    criteria = request.args.get("criteria", "")
    Query = Todo.query.filter_by(user_id=current_user.id)
    if criteria == "date":
        todos = Query.order_by(Todo.date).all()
    elif criteria == "priority":
        priority_order = case(
            (Todo.priority == "High", 3),
            (Todo.priority == "Medium", 2),
            (Todo.priority == "Low", 1),
            else_=0,
        )
        todos = Query.order_by(desc(priority_order)).all()
    elif criteria == "title":
        todos = Query.order_by(Todo.title).all()
    else:
        todos = Query.all()

    return render_template("dashboard.html", todos=todos)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
