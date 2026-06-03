from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///decodelabs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Project(db.Model):
    """Project model - stores intern project submissions"""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='In Progress')
    priority = db.Column(db.String(20), default='Medium')
    github_url = db.Column(db.String(500))
    tech_stack = db.Column(db.String(300))
    progress = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with tasks
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'status': self.status,
            'priority': self.priority,
            'github_url': self.github_url,
            'tech_stack': self.tech_stack,
            'progress': self.progress,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else '',
            'task_count': len(list(self.tasks)) if self.tasks else 0
        }


class Task(db.Model):
    """Task model - stores tasks associated with projects"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')
    priority = db.Column(db.String(20), default='Medium')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'project_id': self.project_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M') if self.completed_at else None
        }


class Intern(db.Model):
    """Intern model - stores intern profiles"""
    __tablename__ = 'interns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    batch = db.Column(db.String(20), default='2026')
    role = db.Column(db.String(100))
    skills = db.Column(db.String(500))
    bio = db.Column(db.Text)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'batch': self.batch,
            'role': self.role,
            'skills': self.skills,
            'bio': self.bio,
            'joined_at': self.joined_at.strftime('%Y-%m-%d') if self.joined_at else '',
            'is_active': self.is_active
        }



@app.context_processor
def inject_stats():
    """Inject global statistics into all templates"""
    return {
        'total_projects': Project.query.count(),
        'total_tasks': Task.query.count(),
        'total_interns': Intern.query.count(),
        'completed_projects': Project.query.filter_by(status='Completed').count(),
        'pending_tasks': Task.query.filter_by(status='Pending').count()
    }


@app.route('/')
def index():
    """Homepage - Dashboard view"""
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()

    # Stats for charts
    status_counts = db.session.query(Project.status, db.func.count(Project.id)).group_by(Project.status).all()
    category_counts = db.session.query(Project.category, db.func.count(Project.id)).group_by(Project.category).all()

    return render_template('index.html', 
                         recent_projects=recent_projects,
                         recent_tasks=recent_tasks,
                         status_counts=status_counts,
                         category_counts=category_counts)


@app.route('/dashboard')
def dashboard():
    """Full dashboard with analytics"""
    projects = Project.query.all()
    tasks = Task.query.all()
    interns = Intern.query.all()

    # Calculate completion rate
    total = len(projects)
    completed = len([p for p in projects if p.status == 'Completed'])
    completion_rate = round((completed / total * 100), 1) if total > 0 else 0

    return render_template('dashboard.html',
                         projects=projects,
                         tasks=tasks,
                         interns=interns,
                         completion_rate=completion_rate)


@app.route('/projects')
def projects_list():
    """List all projects"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')

    query = Project.query

    if status_filter:
        query = query.filter_by(status=status_filter)
    if category_filter:
        query = query.filter_by(category=category_filter)

    projects = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False
    )

    categories = db.session.query(Project.category).distinct().all()
    statuses = ['In Progress', 'Completed', 'On Hold', 'Review']

    return render_template('projects.html', 
                         projects=projects,
                         categories=[c[0] for c in categories],
                         statuses=statuses,
                         current_status=status_filter,
                         current_category=category_filter)


@app.route('/projects/create', methods=['GET', 'POST'])
def project_create():
    """Create a new project"""
    if request.method == 'POST':
        project = Project()
        project.title = request.form['title']
        project.description = request.form['description']
        project.category = request.form['category']
        project.status = request.form.get('status', 'In Progress')
        project.priority = request.form.get('priority', 'Medium')
        project.github_url = request.form.get('github_url', '')
        project.tech_stack = request.form.get('tech_stack', '')
        project.progress = int(request.form.get('progress', 0))

        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects_list'))

    return render_template('project_form.html', project=None)


@app.route('/projects/<int:id>')
def project_detail(id):
    """View project details"""
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)


@app.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def project_edit(id):
    """Edit an existing project"""
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.category = request.form['category']
        project.status = request.form.get('status', 'In Progress')
        project.priority = request.form.get('priority', 'Medium')
        project.github_url = request.form.get('github_url', '')
        project.tech_stack = request.form.get('tech_stack', '')
        project.progress = int(request.form.get('progress', 0))
        project.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project_detail', id=id))

    return render_template('project_form.html', project=project)


@app.route('/projects/<int:id>/delete', methods=['POST'])
def project_delete(id):
    """Delete a project"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects_list'))

@app.route('/tasks')
def tasks_list():
    """List all tasks"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')

    query = Task.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    tasks = query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=8, error_out=False
    )

    projects = Project.query.all()
    statuses = ['Pending', 'In Progress', 'Completed', 'Blocked']

    return render_template('tasks.html',
                         tasks=tasks,
                         projects=projects,
                         statuses=statuses,
                         current_status=status_filter)


@app.route('/tasks/create', methods=['POST'])
def task_create():
    """Create a new task"""
    task = Task()
    task.title = request.form['title']
    task.description = request.form.get('description', '')
    task.status = request.form.get('status', 'Pending')
    task.priority = request.form.get('priority', 'Medium')
    task.project_id = int(request.form['project_id'])

    db.session.add(task)
    db.session.commit()
    flash('Task created successfully!', 'success')
    return redirect(url_for('tasks_list'))


@app.route('/tasks/<int:id>/update', methods=['POST'])
def task_update(id):
    """Update task status"""
    task = Task.query.get_or_404(id)
    task.status = request.form.get('status', task.status)
    task.title = request.form.get('title', task.title)
    task.description = request.form.get('description', task.description)
    task.priority = request.form.get('priority', task.priority)

    if task.status == 'Completed' and not task.completed_at:
        task.completed_at = datetime.utcnow()
    elif task.status != 'Completed':
        task.completed_at = None

    db.session.commit()
    flash('Task updated!', 'success')
    return redirect(url_for('tasks_list'))


@app.route('/tasks/<int:id>/delete', methods=['POST'])
def task_delete(id):
    """Delete a task"""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('tasks_list'))


@app.route('/interns')
def interns_list():
    """List all interns"""
    interns = Intern.query.order_by(Intern.joined_at.desc()).all()
    return render_template('interns.html', interns=interns)


@app.route('/interns/create', methods=['POST'])
def intern_create():
    """Create a new intern profile"""
    intern = Intern()
    intern.name = request.form['name']
    intern.email = request.form['email']
    intern.role = request.form.get('role', 'Intern')
    intern.skills = request.form.get('skills', '')
    intern.bio = request.form.get('bio', '')

    db.session.add(intern)
    db.session.commit()
    flash('Intern profile created!', 'success')
    return redirect(url_for('interns_list'))


@app.route('/interns/<int:id>/update', methods=['POST'])
def intern_update(id):
    """Update intern profile"""
    intern = Intern.query.get_or_404(id)
    intern.name = request.form.get('name', intern.name)
    intern.email = request.form.get('email', intern.email)
    intern.role = request.form.get('role', intern.role)
    intern.skills = request.form.get('skills', intern.skills)
    intern.bio = request.form.get('bio', intern.bio)
    intern.is_active = request.form.get('is_active') == 'on'

    db.session.commit()
    flash('Profile updated!', 'success')
    return redirect(url_for('interns_list'))


@app.route('/interns/<int:id>/delete', methods=['POST'])
def intern_delete(id):
    """Delete intern profile"""
    intern = Intern.query.get_or_404(id)
    db.session.delete(intern)
    db.session.commit()
    flash('Profile removed!', 'success')
    return redirect(url_for('interns_list'))


@app.route('/api/projects')
def api_projects():
    """Get all projects as JSON"""
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])


@app.route('/api/projects/<int:id>')
def api_project_detail(id):
    """Get single project as JSON"""
    project = Project.query.get_or_404(id)
    data = project.to_dict()
    data['tasks'] = [t.to_dict() for t in project.tasks]
    return jsonify(data)


@app.route('/api/stats')
def api_stats():
    """Get dashboard statistics"""
    return jsonify({
        'total_projects': Project.query.count(),
        'total_tasks': Task.query.count(),
        'total_interns': Intern.query.count(),
        'completed_projects': Project.query.filter_by(status='Completed').count(),
        'pending_tasks': Task.query.filter_by(status='Pending').count(),
        'in_progress_tasks': Task.query.filter_by(status='In Progress').count()
    })


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.cli.command('init-db')
def init_db():
    """Initialize database with sample data"""
    db.create_all()

    # Add sample interns
    if Intern.query.count() == 0:
        sample_interns = [
            Intern(name='Aarav Sharma', email='aarav@decodelabs.tech', role='Full Stack Developer', 
                   skills='Python, Flask, React, SQL', bio='Passionate about building scalable web applications.'),
            Intern(name='Priya Patel', email='priya@decodelabs.tech', role='Backend Developer',
                   skills='Python, Django, PostgreSQL, Docker', bio='Database architecture enthusiast.'),
            Intern(name='Rohan Gupta', email='rohan@decodelabs.tech', role='Frontend Developer',
                   skills='React, Vue, CSS, JavaScript', bio='Creating beautiful user interfaces.'),
        ]
        db.session.add_all(sample_interns)

    # Add sample projects
    if Project.query.count() == 0:
        sample_projects = [
            Project(title='E-Commerce Platform', description='Full-stack e-commerce application with payment integration and inventory management.', 
                   category='Web Application', status='In Progress', priority='High', 
                   tech_stack='Python, Flask, React, PostgreSQL', progress=65),
            Project(title='Task Management System', description='Collaborative task management tool with real-time updates and team analytics.',
                   category='Productivity', status='Completed', priority='Medium',
                   tech_stack='Python, Flask, JavaScript, SQLite', progress=100),
            Project(title='AI Chatbot Interface', description='Intelligent chatbot with natural language processing capabilities.',
                   category='AI/ML', status='In Progress', priority='High',
                   tech_stack='Python, Flask, OpenAI API, React', progress=40),
            Project(title='Portfolio Website', description='Personal portfolio website with dynamic content management.',
                   category='Web Application', status='Completed', priority='Low',
                   tech_stack='HTML, CSS, JavaScript, Flask', progress=100),
            Project(title='Data Analytics Dashboard', description='Real-time data visualization dashboard for business metrics.',
                   category='Analytics', status='On Hold', priority='Medium',
                   tech_stack='Python, Flask, D3.js, MongoDB', progress=30),
        ]
        db.session.add_all(sample_projects)
        db.session.commit()

        # Add sample tasks
        sample_tasks = [
            Task(title='Design Database Schema', description='Create ER diagram and define table relationships', 
                status='Completed', priority='High', project_id=1),
            Task(title='Implement User Authentication', description='Add login/register with JWT tokens',
                status='In Progress', priority='High', project_id=1),
            Task(title='Build API Endpoints', description='Create RESTful API for all CRUD operations',
                status='Pending', priority='High', project_id=1),
            Task(title='Frontend Integration', description='Connect React frontend with Flask backend',
                status='Pending', priority='Medium', project_id=1),
            Task(title='Write Unit Tests', description='Achieve 80% test coverage',
                status='Completed', priority='Medium', project_id=2),
            Task(title='Deploy to Production', description='Set up CI/CD pipeline and deploy',
                status='Completed', priority='High', project_id=2),
        ]
        db.session.add_all(sample_tasks)

    db.session.commit()
    print('Database initialized with sample data!')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
